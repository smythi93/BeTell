"""Summarize the worktree-mode runs on real commits (see real_run.py)."""
import json
import os
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
# LaTeX macros with the numbers reported in the paper.
NUMBERS = Path(os.environ.get("BETELL_NUMBERS", HERE / "numbers"))
# Commits whose message announces a behavior-preserving change.
PRESERVING = {"0cfb9f5", "ca0586d", "ed1bd2d"}


def main():
    summary = json.loads((HERE / "real" / "summary.json").read_text())
    rows = []
    for entry in summary:
        if not entry["ok"]:
            print("FAILED", entry["project"], entry["commit"], entry["stderr"][-300:])
            continue
        data = json.loads((HERE / "real" / f"{entry['project']}-{entry['commit']}.json").read_text())
        behavior = [c for c in data["changes"] if c["kind"] != "outcome"]
        functions = {c["location"] for c in behavior}
        outside = {c["location"] for c in behavior if c["outside_diff"]}
        silent_outside = {c["location"] for c in behavior if c["outside_diff"] and c["silent"]}
        recordings = [s for s in data["seconds"]["base"] + data["seconds"]["head"] if s]
        overhead = statistics.mean(recordings) / entry["plain_seconds"] if recordings else None
        rows.append({
            "project": entry["project"], "commit": entry["commit"], "subject": entry["subject"],
            "preserving": entry["commit"] in PRESERVING,
            "tests": data["compared_tests"], "added_tests": len(data["added_tests"]),
            "flips": len([c for c in data["changes"] if c["kind"] == "outcome"]),
            "functions": len(functions), "outside": len(outside), "silent_outside": len(silent_outside),
            "silent_outside_list": sorted(silent_outside), "dropped": data["unstable_dropped"],
            "overhead": overhead, "plain": entry["plain_seconds"], "betell": entry["betell_seconds"],
        })
    for r in rows:
        print(f"{r['project']:15} {r['commit']} pres={r['preserving']!s:5} tests={r['tests']:5} new={r['added_tests']:3} "
              f"flips={r['flips']} fun={r['functions']:3} out={r['outside']:3} silOut={r['silent_outside']:3} "
              f"drop={r['dropped']:4} ovh={r['overhead']:.2f} plain={r['plain']:.0f}s betell={r['betell']:.0f}s  {r['subject'][:50]}")
    (HERE / "real-results.json").write_text(json.dumps(rows, indent=2))
    overheads = [r["overhead"] for r in rows if r["overhead"]]
    numbers = {
        "nRealCommits": len(rows),
        "nPreserving": len([r for r in rows if r["preserving"]]),
        "nPreservingEmpty": len([r for r in rows if r["preserving"] and r["functions"] == 0]),
        "nPreservingUnedited": len([r for r in rows if r["preserving"] and r["outside"] == 0]),
        "nRealNoOutside": len([r for r in rows if r["outside"] == 0]),
        "nRealWithChanges": len([r for r in rows if r["functions"] > 0]),
        "nRealSilentOutside": len([r for r in rows if r["silent_outside"]]),
        "medRealOverhead": f"{statistics.median(overheads):.1f}$\\times$" if overheads else "n/a",
        "maxRealOverhead": f"{max(overheads):.1f}$\\times$" if overheads else "n/a",
    }
    lines = [f"\\newcommand{{\\{k}}}{{{v}\\xspace}}" for k, v in numbers.items()]
    target = NUMBERS / "numbers-real.tex"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
