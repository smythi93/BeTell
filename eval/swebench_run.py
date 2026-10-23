"""Run betell on SWE-bench gold patches inside the instance containers.

For each instance the driver commits the test patch as ``base`` and the gold
patch on top of it as ``head``, so both revisions share the same tests. It
then times one plain pytest run on base, records base and head twice each,
and copies the recordings and both versions of the edited files to the host.

Usage (on a host with the SWE-bench images):
    python3 eval/swebench_run.py --instances eval/candidates.json --out eval/runs --jobs 6
"""
import argparse
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent / "src" / "betell"
ACTIVATE = "source /opt/miniconda3/bin/activate testbed 2>/dev/null || true; cd /testbed"


def sh(*args, check=True, timeout=None, input=None):
    return subprocess.run(list(args), check=check, capture_output=True, text=True, timeout=timeout, input=input)


def dexec(name, script, timeout=None, check=True):
    return sh("docker", "exec", name, "bash", "-c", f"{ACTIVATE}; {script}", timeout=timeout, check=check)


def image_for(instance_id):
    repo, number = instance_id.rsplit("-", 1)
    return f"swebench/sweb.eval.x86_64.{repo.replace('__', '_1776_')}-{number}:latest"


def test_files(test_patch):
    files = re.findall(r"^\+\+\+ b/(\S+\.py)$", test_patch, re.M)
    return [f for f in files if re.search(r"(^|/)test_[^/]*\.py$|_test\.py$", f)]


def pytest_seconds(stdout):
    found = re.findall(r" in ([0-9.]+)s", stdout)
    return float(found[-1]) if found else None


def timed(name, script, timeout):
    started = time.time()
    result = dexec(name, script, timeout=timeout, check=False)
    return time.time() - started, result


def run_instance(row, out_root, timeout):
    iid = row["instance_id"]
    out = out_root / iid
    if (out / "done.json").exists():
        return json.loads((out / "done.json").read_text())
    out.mkdir(parents=True, exist_ok=True)
    name = "betell_" + iid.replace("__", "_")
    sh("docker", "rm", "-f", name, check=False)
    sh("docker", "run", "-d", "--name", name, image_for(iid), "sleep", "infinity")
    info = {"instance_id": iid}
    try:
        dexec(name, "mkdir -p /tmp/bdpkg/betell")
        for module in ("__init__.py", "recorder.py", "pytest_plugin.py"):
            sh("docker", "cp", str(PKG / module), f"{name}:/tmp/bdpkg/betell/{module}")
        for label, patch in (("test", row["test_patch"]), ("gold", row["patch"])):
            sh("docker", "exec", "-i", name, "bash", "-c", f"cat > /tmp/{label}.patch", input=patch)
        dexec(name, "git config user.email e@x.org; git config user.name eval; "
                    "git apply /tmp/test.patch && git add -A && git commit -qm base --no-verify && git tag bd_base && "
                    "git apply /tmp/gold.patch && git add -A && git commit -qm head --no-verify && git tag bd_head")
        files = test_files(row["test_patch"])
        info["test_files"] = files
        args = " ".join(files)
        plain = "PYTHONHASHSEED=0 python -m pytest -q -p no:cacheprovider " + args
        recorded = ("PYTHONHASHSEED=0 PYTHONPATH=/tmp/bdpkg:$PYTHONPATH python -m pytest -q -p no:cacheprovider "
                    "-p betell.pytest_plugin --betell-root /testbed --betell-out /tmp/{tag}.json.gz " + args)
        dexec(name, "git checkout -q bd_base")
        for i in range(2):  # the first run also warms caches and bytecode
            seconds, result = timed(name, plain, timeout)
            info[f"plain_base-{i}_seconds"] = seconds
            info[f"plain_base-{i}_pytest"] = pytest_seconds(result.stdout)
        info["plain_base_tail"] = result.stdout[-300:]
        seconds, result = timed(name, recorded.format(tag="novalues") + " --betell-no-values", timeout)
        info["recorded_novalues_seconds"] = seconds
        info["recorded_novalues_pytest"] = pytest_seconds(result.stdout)
        for rev in ("base", "head"):
            dexec(name, f"git checkout -q bd_{rev}")
            for i in range(2):
                tag = f"{rev}-{i}"
                seconds, result = timed(name, recorded.format(tag=tag), timeout)
                info[f"recorded_{tag}_seconds"] = seconds
                info[f"recorded_{tag}_pytest"] = pytest_seconds(result.stdout)
                got = sh("docker", "cp", f"{name}:/tmp/{tag}.json.gz", str(out / f"{tag}.json.gz"), check=False)
                if got.returncode != 0:
                    info[f"error_{tag}"] = (result.stdout + result.stderr)[-1500:]
        changed = dexec(name, "git diff --name-only bd_base bd_head -- '*.py'").stdout.split()
        sources = {"base": {}, "head": {}}
        for rel in changed:
            for rev in ("base", "head"):
                shown = dexec(name, f"git show bd_{rev}:{rel}", check=False)
                sources[rev][rel] = shown.stdout if shown.returncode == 0 else None
        (out / "sources.json").write_text(json.dumps(sources))
        info["changed_files"] = changed
        info["ok"] = all((out / f"{r}-{i}.json.gz").exists() for r in ("base", "head") for i in range(2))
    except Exception as error:  # keep going with the other instances
        info["ok"] = False
        info["error"] = repr(error)[-1500:]
    finally:
        sh("docker", "rm", "-f", name, check=False)
    (out / "done.json").write_text(json.dumps(info, indent=2))
    return info


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instances", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    rows = json.loads(Path(args.instances).read_text())
    if args.only:
        rows = [r for r in rows if r["instance_id"] in args.only]
    out_root = Path(args.out)
    with ThreadPoolExecutor(args.jobs) as pool:
        for info in pool.map(lambda r: run_instance(r, out_root, args.timeout), rows):
            print(info["instance_id"], info.get("ok"), info.get("error", "")[:200], flush=True)


if __name__ == "__main__":
    main()
