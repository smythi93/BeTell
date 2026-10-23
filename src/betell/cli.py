"""Command line interface.

``betell run`` checks out base and head into temporary worktrees (or switches
the repository in place), records the test suite on each revision, and writes
the report. ``betell record`` and ``betell compare`` expose the two halves on
their own, for environments such as containers where the test run and the
comparison happen in different places.
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from betell.compare import Run, compare
from betell.report import markdown, to_json

PACKAGE_PARENT = str(Path(__file__).resolve().parent.parent)


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=check, capture_output=True, text=True
    ).stdout.strip()


def record(workdir, out, pytest_args, python, root=None, values=True, env_extra=None, timeout=None,
           backend="auto"):
    """Run pytest under the recorder in ``workdir`` and return the wall time."""
    env = dict(os.environ)
    paths = [PACKAGE_PARENT, str(workdir)]
    if (Path(workdir) / "src").is_dir():
        paths.append(str(Path(workdir) / "src"))
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(paths)
    env.setdefault("PYTHONHASHSEED", "0")  # stable set and dict orders across runs
    env.update(env_extra or {})
    command = [python, "-m", "pytest", "-p", "betell.pytest_plugin", "--betell-out", str(out),
               "--betell-root", str(root or workdir), "-q", "-p", "no:cacheprovider"]
    if not values:
        command.append("--betell-no-values")
    if backend != "auto":
        command += ["--betell-backend", backend]
    command += pytest_args
    started = time.time()
    result = subprocess.run(command, cwd=workdir, env=env, capture_output=True, text=True, timeout=timeout)
    if not Path(out).exists():
        sys.stderr.write(result.stdout[-4000:] + result.stderr[-4000:])
        raise RuntimeError(f"recording failed in {workdir} (exit {result.returncode})")
    return time.time() - started


def changed_sources(repo, base, head):
    """Both versions of every Python file the textual diff touches."""
    names = git(repo, "diff", "--name-only", base, head, "--", "*.py").splitlines()
    before, after = {}, {}
    for name in names:
        before[name] = _show(repo, base, name)
        after[name] = _show(repo, head, name)
    return before, after


def _show(repo, rev, name):
    result = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{name}"], capture_output=True)
    return result.stdout.decode("utf-8", "replace") if result.returncode == 0 else None


def inject(runs, sources):
    for run in runs:
        run.sources.update(sources)


def resolve_python(python):
    """Return an absolute interpreter path, since recordings run in other directories."""
    if os.sep in python:
        return os.path.abspath(python)
    return shutil.which(python) or python


def command_run(args):
    args.python = resolve_python(args.python)
    repo = Path(args.repo).resolve()
    base = git(repo, "rev-parse", args.base)
    head = git(repo, "rev-parse", args.head)
    pytest_args = shlex.split(args.pytest_args)
    work = Path(tempfile.mkdtemp(prefix="betell-"))
    base_runs, head_runs = [], []
    try:
        if args.mode == "worktree":
            for name, rev in (("base", base), ("head", head)):
                git(repo, "worktree", "add", "--detach", str(work / name), rev)
            for i in range(args.runs_base):
                out = work / f"base-{i}.json.gz"
                record(work / "base", out, pytest_args, args.python, values=not args.no_values, backend=args.backend)
                base_runs.append(Run.load(out))
            for i in range(args.runs_head):
                out = work / f"head-{i}.json.gz"
                record(work / "head", out, pytest_args, args.python, values=not args.no_values, backend=args.backend)
                head_runs.append(Run.load(out))
        else:
            original = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
            if original == "HEAD":
                original = git(repo, "rev-parse", "HEAD")
            if git(repo, "status", "--porcelain", "--untracked-files=no"):
                raise SystemExit("in-place mode needs a clean working tree")
            try:
                for name, rev, runs, count in (("base", base, base_runs, args.runs_base),
                                               ("head", head, head_runs, args.runs_head)):
                    git(repo, "checkout", "--quiet", rev)
                    for i in range(count):
                        out = work / f"{name}-{i}.json.gz"
                        record(repo, out, pytest_args, args.python, values=not args.no_values, backend=args.backend)
                        runs.append(Run.load(out))
            finally:
                git(repo, "checkout", "--quiet", original)
        before, after = changed_sources(repo, base, head)
        inject(base_runs, before)
        inject(head_runs, after)
        comparison = compare(base_runs, head_runs, args.base, args.head)
        write_outputs(comparison, args)
    finally:
        if args.mode == "worktree":
            for name in ("base", "head"):
                git(repo, "worktree", "remove", "--force", str(work / name), check=False)
        if args.keep:
            print(f"recordings kept in {work}", file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)


def write_outputs(comparison, args):
    text = markdown(comparison)
    if args.out:
        Path(args.out).write_text(text)
    else:
        sys.stdout.write(text)
    if args.json:
        Path(args.json).write_text(to_json(comparison))


def command_record(args):
    args.python = resolve_python(args.python)
    seconds = record(Path(args.workdir).resolve(), Path(args.out).resolve(), shlex.split(args.pytest_args),
                     args.python, root=args.root, values=not args.no_values, backend=args.backend)
    print(f"recorded in {seconds:.1f}s")


def command_compare(args):
    base_runs = [Run.load(p) for p in args.base]
    head_runs = [Run.load(p) for p in args.head]
    if args.repo:
        before, after = changed_sources(Path(args.repo), args.base_rev, args.head_rev)
        inject(base_runs, before)
        inject(head_runs, after)
    comparison = compare(base_runs, head_runs, args.base_rev, args.head_rev)
    write_outputs(comparison, args)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="betell", description="Behavioral diff for pull requests")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="record base and head and report behavioral changes")
    run.add_argument("--repo", default=".")
    run.add_argument("--base", required=True)
    run.add_argument("--head", default="HEAD")
    run.add_argument("--pytest-args", default="", help="arguments passed to pytest, e.g. a test directory")
    run.add_argument("--python", default=sys.executable)
    run.add_argument("--runs-base", type=int, default=2, help="repeated base runs to filter nondeterminism")
    run.add_argument("--runs-head", type=int, default=2, help="repeated head runs to filter nondeterminism")
    run.add_argument("--mode", choices=("worktree", "inplace"), default="worktree")
    run.add_argument("--no-values", action="store_true", help="skip argument and return values")
    run.add_argument("--backend", choices=("auto", "settrace", "monitoring"), default="auto",
                     help="recorder backend (auto picks sys.monitoring on Python 3.12 and later)")
    run.add_argument("--out", help="Markdown report (default: stdout)")
    run.add_argument("--json", help="also write the comparison as JSON")
    run.add_argument("--keep", action="store_true", help="keep the recordings")
    run.set_defaults(func=command_run)

    rec = sub.add_parser("record", help="record one revision")
    rec.add_argument("--workdir", default=".")
    rec.add_argument("--root", default=None)
    rec.add_argument("--out", required=True)
    rec.add_argument("--pytest-args", default="")
    rec.add_argument("--python", default=sys.executable)
    rec.add_argument("--no-values", action="store_true")
    rec.add_argument("--backend", choices=("auto", "settrace", "monitoring"), default="auto")
    rec.set_defaults(func=command_record)

    cmp_ = sub.add_parser("compare", help="compare existing recordings")
    cmp_.add_argument("--base", nargs="+", required=True)
    cmp_.add_argument("--head", nargs="+", required=True)
    cmp_.add_argument("--repo", help="git repository to read the edited sources from")
    cmp_.add_argument("--base-rev", default="base")
    cmp_.add_argument("--head-rev", default="head")
    cmp_.add_argument("--out")
    cmp_.add_argument("--json")
    cmp_.set_defaults(func=command_compare)

    demo = sub.add_parser("demo", help="run betell on a bundled toy repository")
    demo.add_argument("scenario", nargs="?", default="helper",
                      choices=("helper", "threshold", "exception", "outcome", "refactor", "shift"))
    demo.add_argument("--dir", default=None)
    demo.set_defaults(func=lambda a: __import__("betell.demo").demo.main(a.scenario, a.dir))

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
