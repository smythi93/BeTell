"""Run betell in worktree mode on real commits of two pure-Python libraries.

Each commit is compared against its parent, the way the GitHub Action compares
a pull request against its base. Plain pytest on the head revision is timed
in a separate worktree for the overhead estimate.

Usage:
    python eval/real_run.py WORKDIR
where WORKDIR holds clones ``click`` and ``more-itertools`` and virtual
environments ``click-venv`` and ``more-itertools-venv`` with the project, pytest
and betell installed.
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMMITS = {
    "more-itertools": ["0cfb9f5", "67fcf64", "f89d7a3", "ca0586d", "ed1bd2d", "def2dab", "d032cab"],
    "click": ["f67c2bb", "05f6fd0", "f58ca3e", "047adef"],
}


def plain_seconds(repo, commit, python):
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "head"
        subprocess.run(["git", "-C", repo, "worktree", "add", "--detach", str(tree), commit],
                       check=True, capture_output=True)
        try:
            env = {"PYTHONPATH": f"{tree}:{tree / 'src'}", "PYTHONHASHSEED": "0", "PATH": "/usr/bin:/bin"}
            started = time.time()
            subprocess.run([python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                           cwd=tree, env=env, capture_output=True)
            return time.time() - started
        finally:
            subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", str(tree)], capture_output=True)


def main():
    work = Path(sys.argv[1]).resolve()
    out = HERE / "real"
    out.mkdir(exist_ok=True)
    existing = out / "summary.json"
    summary = json.loads(existing.read_text()) if existing.exists() else []
    done = {(e["project"], e["commit"]) for e in summary if e["ok"]}
    summary = [e for e in summary if e["ok"]]
    for project, commits in COMMITS.items():
        repo = str(work / project)
        python = str(work / f"{project}-venv" / "bin" / "python")
        betell = str(work / f"{project}-venv" / "bin" / "betell")
        for commit in commits:
            if (project, commit) in done:
                continue
            subject = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%s", commit],
                                     capture_output=True, text=True).stdout.strip()
            started = time.time()
            result = subprocess.run([betell, "run", "--repo", repo, "--base", f"{commit}^", "--head", commit,
                                     "--python", python, "--pytest-args", "tests",
                                     "--out", str(out / f"{project}-{commit}.md"),
                                     "--json", str(out / f"{project}-{commit}.json")],
                                    capture_output=True, text=True)
            seconds = time.time() - started
            entry = {"project": project, "commit": commit, "subject": subject, "betell_seconds": seconds,
                     "ok": result.returncode == 0, "stderr": result.stderr[-800:]}
            entry["plain_seconds"] = plain_seconds(repo, commit, python)
            summary.append(entry)
            print(json.dumps({k: v for k, v in entry.items() if k != "stderr"}), flush=True)
            (out / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
