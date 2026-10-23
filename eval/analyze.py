"""Summarize the SWE-bench runs.

For every instance this computes the default comparison (two runs of each
revision), an A/A comparison of the two unfiltered base runs to measure the
nondeterminism the filter removes, outcome-flip agreement with the
FAIL_TO_PASS and PASS_TO_PASS ground truth, and the recording overhead.
"""
import json
import os
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# LaTeX macros with the numbers reported in the paper.
NUMBERS = Path(os.environ.get("BETELL_NUMBERS", HERE / "numbers"))
sys.path.insert(0, str(HERE.parent / "src"))

from betell.compare import Run, compare  # noqa: E402
from betell.report import markdown, to_json  # noqa: E402


def load(directory, tag):
    path = directory / f"{tag}.json.gz"
    return Run.load(path) if path.exists() else None


def analyze(directory, row):
    info = json.loads((directory / "done.json").read_text())
    if not info.get("ok"):
        return {"instance_id": row["instance_id"], "ok": False, "error": info.get("error") or "recording failed"}
    sources = json.loads((directory / "sources.json").read_text())
    runs = {tag: load(directory, tag) for tag in ("base-0", "base-1", "head-0", "head-1")}
    for tag, run in runs.items():
        run.sources.update(sources["base" if tag.startswith("base") else "head"])

    default = compare([runs["base-0"], runs["base-1"]], [runs["head-0"], runs["head-1"]], "base", "gold")
    unfiltered = compare([runs["base-0"]], [runs["head-0"]], "base", "gold")
    aa = compare([runs["base-0"]], [runs["base-1"]], "base", "base")
    (directory / "report.md").write_text(markdown(default))
    (directory / "report.json").write_text(to_json(default))

    f2p = set(json.loads(row["FAIL_TO_PASS"]))
    p2p = set(json.loads(row["PASS_TO_PASS"]))
    flips = {c.location: c.detail for c in default.changes if c.kind == "outcome"}
    compared = set(runs["base-0"].tests) & set(runs["head-0"].tests)
    f2p_seen = f2p & compared
    behavior = [c for c in default.changes if c.kind != "outcome"]
    outside = [c for c in behavior if c.outside]
    functions = {c.location for c in behavior}
    functions_outside = {c.location for c in outside}
    silent_outside = {c.location for c in outside if c.silent}
    silent_inside = {c.location for c in behavior if c.silent and not c.outside}

    def ratio(key):
        rec = info.get(f"recorded_base-1_{key}")
        plain = info.get(f"plain_base-1_{key}")
        return rec / plain if rec and plain else None

    return {
        "instance_id": row["instance_id"],
        "ok": True,
        "tests": default.compared_tests,
        "f2p": len(f2p),
        "f2p_compared": len(f2p_seen),
        "f2p_flip_detected": sum(1 for t in f2p_seen if flips.get(t) == "failed -> passed"),
        "p2p_compared": len(p2p & compared),
        "p2p_false_flips": sum(1 for t in p2p & compared if t in flips),
        "other_flips": sorted(set(flips) - f2p),
        "changes": len(behavior),
        "outside": len(outside),
        "outside_kinds": sorted({c.kind for c in outside}),
        "touched_functions": len(default.touched_functions),
        "functions": len(functions),
        "functions_outside": len(functions_outside),
        "silent_outside": len(silent_outside),
        "silent_inside": len(silent_inside),
        "silent_outside_examples": sorted(silent_outside)[:10],
        "overhead_novalues": (info.get("recorded_novalues_pytest") / info["plain_base-1_pytest"]
                              if info.get("recorded_novalues_pytest") and info.get("plain_base-1_pytest") else None),
        "dropped": default.unstable_dropped,
        "unfiltered_changes": len([c for c in unfiltered.changes if c.kind != "outcome"]),
        "aa_changes": len([c for c in aa.changes if c.kind != "outcome"]),
        "aa_functions": len({c.location for c in aa.changes if c.kind != "outcome"}),
        "overhead_pytest": ratio("pytest"),
        "overhead_wall": ratio("seconds"),
        "plain_pytest": info.get("plain_base-1_pytest"),
        "recorded_pytest": info.get("recorded_base-1_pytest"),
        "recording_kb": (directory / "base-0.json.gz").stat().st_size / 1024,
    }


def main():
    runs = Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "runs")
    rows = {r["instance_id"]: r for r in json.loads((HERE / "candidates.json").read_text())}
    results = []
    for directory in sorted(runs.iterdir()):
        if (directory / "done.json").exists() and directory.name in rows:
            results.append(analyze(directory, rows[directory.name]))
    (HERE / "results.json").write_text(json.dumps(results, indent=2))
    ok = [r for r in results if r["ok"]]
    print(f"{len(ok)}/{len(results)} instances recorded")
    header = ("instance", "tests", "f2p", "det", "p2pF", "fun", "out", "silO", "silI", "drop", "aaF", "ovh", "ovhNV")
    print("\t".join(header))
    for r in ok:
        print("\t".join(str(x) for x in (
            r["instance_id"], r["tests"], r["f2p_compared"], r["f2p_flip_detected"], r["p2p_false_flips"],
            r["functions"], r["functions_outside"], r["silent_outside"], r["silent_inside"], r["dropped"],
            r["aa_functions"], f"{r['overhead_pytest']:.2f}" if r["overhead_pytest"] else "-",
            f"{r['overhead_novalues']:.2f}" if r["overhead_novalues"] else "-")))
    for r in results:
        if not r["ok"]:
            print("FAILED", r["instance_id"], r["error"][:300])
    if ok:
        overheads = [r["overhead_pytest"] for r in ok if r["overhead_pytest"]]
        print("median overhead", statistics.median(overheads) if overheads else None)
        print("instances with outside-diff changes", sum(1 for r in ok if r["outside"]))
        print("total changes", sum(r["changes"] for r in ok), "outside", sum(r["outside"] for r in ok))
        print("f2p", sum(r["f2p_compared"] for r in ok), "detected", sum(r["f2p_flip_detected"] for r in ok))
        print("p2p false flips", sum(r["p2p_false_flips"] for r in ok))
        write_numbers(ok)


def write_numbers(ok):
    med = statistics.median

    def fmt(x):
        return f"{x:.1f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)

    overheads = [r["overhead_pytest"] for r in ok if r["overhead_pytest"]]
    novalues = [r["overhead_novalues"] for r in ok if r["overhead_novalues"]]
    numbers = {
        "nInstances": len(ok),
        "nRepos": len({r["instance_id"].split("__")[0] for r in ok}),
        "nTests": sum(r["tests"] for r in ok),
        "nFtp": sum(r["f2p_compared"] for r in ok),
        "nFtpDetected": sum(r["f2p_flip_detected"] for r in ok),
        "nFalseFlips": sum(r["p2p_false_flips"] for r in ok),
        "medFunctions": fmt(med([r["functions"] for r in ok])),
        "medOutside": fmt(med([r["functions_outside"] for r in ok])),
        "medSilentOutside": fmt(med([r["silent_outside"] for r in ok])),
        "nSilentOutsideInst": sum(1 for r in ok if r["silent_outside"]),
        "medDropped": fmt(med([r["dropped"] for r in ok])),
        "medAA": fmt(med([r["aa_functions"] for r in ok])),
        "medOverhead": fmt(med(overheads)) + r"$\times$" if overheads else "n/a",
        "medOverheadNoValues": fmt(med(novalues)) + r"$\times$" if novalues else "n/a",
    }
    lines = [f"\\newcommand{{\\{k}}}{{{v}\\xspace}}" for k, v in numbers.items()]
    target = NUMBERS / "numbers-swebench.tex"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.parent.exists():
        target.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
