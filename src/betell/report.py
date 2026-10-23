"""Render a comparison as a reviewer-facing Markdown report or as JSON.

The Markdown report groups changes by function and orders them by how much a
reviewer is likely to care. Changes in tests whose outcome did not change come
first, because no test result points at them. Within those, changes in
functions the pull request does not edit come first, because the textual diff
does not point at them either.
"""
from __future__ import annotations

import json
from collections import defaultdict

from betell.compare import Comparison

GITHUB_LIMIT = 60000
WEIGHT = {"exception": 0, "return": 1, "argument": 2, "call": 3, "branch": 4}


def _rev(rev):
    return rev[:10] if len(rev) == 40 and all(c in "0123456789abcdef" for c in rev) else rev


def _count(n, noun):
    return f"{n} {noun}" + ("" if n == 1 else "s")


def _code(text):
    return "`" + text.replace("`", "'") + "`"


def _values(values, limit=2):
    items = sorted(values)
    shown = ", ".join(_code(v) for v in items[:limit])
    if len(items) > limit:
        shown += f" (+{len(items) - limit} more)"
    return shown


def _tests(tests, limit=1):
    items = sorted(tests)
    shown = ", ".join(_code(t) for t in items[:limit])
    if len(items) > limit:
        shown += f" and {len(items) - limit} more"
    return shown


def _describe(changes):
    """One line of text for all changes recorded in one function."""
    parts = []
    by_kind = defaultdict(list)
    for change in changes:
        by_kind[change.kind].append(change)
    for change in by_kind["exception"]:
        parts.append(change.detail)
    for kind, label in (("return", "return values"), ("argument", "arguments")):
        for change in by_kind[kind]:
            text = f"{label} changed"
            details = []
            if change.after:
                details.append(f"new {_values(change.after)}")
            if change.before:
                details.append(f"gone {_values(change.before)}")
            if details:
                text += " (" + ", ".join(details) + ")"
            parts.append(text)
    new_callers = sorted(c.detail.split(" from ", 1)[1] for c in by_kind["call"] if c.detail.startswith("newly"))
    old_callers = sorted(c.detail.split(" from ", 1)[1] for c in by_kind["call"] if c.detail.startswith("no longer"))
    if new_callers:
        parts.append("newly called from " + ", ".join(_code(c) for c in new_callers[:3])
                     + (f" (+{len(new_callers) - 3} more)" if len(new_callers) > 3 else ""))
    if old_callers:
        parts.append("no longer called from " + ", ".join(_code(c) for c in old_callers[:3])
                     + (f" (+{len(old_callers) - 3} more)" if len(old_callers) > 3 else ""))
    taken = sum(len(c.after) for c in by_kind["branch"])
    dropped = sum(len(c.before) for c in by_kind["branch"])
    if taken or dropped:
        flow = []
        if taken:
            flow.append(f"{taken} newly taken")
        if dropped:
            flow.append(f"{dropped} no longer taken")
        parts.append("control flow changed (" + ", ".join(flow) + " line transitions)")
    return "; ".join(parts)


def group(changes):
    """Group changes by function and order the groups by priority."""
    groups = defaultdict(list)
    for change in changes:
        groups[change.location].append(change)
    ordered = []
    for location, items in groups.items():
        tests = set().union(*(c.tests for c in items))
        weight = min(WEIGHT[c.kind] for c in items)
        ordered.append((weight, -len(tests), location, items, tests))
    ordered.sort(key=lambda g: g[:3])
    return [(location, items, tests) for _, _, location, items, tests in ordered]


def _section(groups, max_items):
    lines = []
    for location, items, tests in groups[:max_items]:
        lines.append(f"- {_code(location)} in {len(tests)} test(s), e.g. {_tests(tests)}: {_describe(items)}.")
    if len(groups) > max_items:
        lines.append(f"- ... and {len(groups) - max_items} more function(s)")
    return lines


def markdown(comparison: Comparison, max_items=25) -> str:
    outcomes = [c for c in comparison.changes if c.kind == "outcome"]
    behavior = [c for c in comparison.changes if c.kind != "outcome"]
    silent_outside = group([c for c in behavior if c.silent and c.outside])
    silent_inside = group([c for c in behavior if c.silent and not c.outside])
    flipped_only = group([c for c in behavior if not c.silent])
    functions = {c.location for c in behavior}
    outside = {c.location for c in behavior if c.outside}
    silent = {c.location for c in behavior if c.silent}

    lines = [
        f"## Behavioral diff `{_rev(comparison.base_rev)}` → `{_rev(comparison.head_rev)}`",
        "",
        f"Compared {comparison.compared_tests} test(s) on both revisions. "
        f"{len(comparison.added_tests)} test(s) exist only in head and "
        f"{len(comparison.removed_tests)} only in base. "
        f"{comparison.unstable_dropped} unstable observation(s) were dropped after repeated runs.",
        "",
    ]
    if not comparison.changes:
        lines.append("No behavioral change observed in the compared tests.")
        return "\n".join(lines) + "\n"
    lines += [
        f"**{_count(len(functions), 'function')} behave differently.** "
        f"Not edited by this pull request: {len(outside)}. "
        f"Different in tests whose outcome stays the same: {len(silent)}. "
        f"Test outcomes that changed: {len(outcomes)}.",
        "",
    ]
    if outcomes:
        lines += ["### Test outcomes that changed", ""]
        lines += [f"- {_code(c.location)} {c.detail.replace('->', '→')}" for c in outcomes[:max_items]]
        if len(outcomes) > max_items:
            lines.append(f"- ... and {len(outcomes) - max_items} more")
        lines.append("")
    if silent_outside:
        lines += ["### Silent changes in code this pull request does not edit", "",
                  "These functions are textually unchanged and the tests keep their outcome, "
                  "yet the functions behave differently.", ""]
        lines += _section(silent_outside, max_items) + [""]
    if silent_inside:
        lines += ["### Silent changes in edited code", ""]
        lines += _section(silent_inside, max_items) + [""]
    if flipped_only:
        lines += [f"<details><summary>Behavior behind the changed test outcomes ({len(flipped_only)} function(s))"
                  "</summary>", ""]
        lines += _section(flipped_only, max_items) + ["", "</details>", ""]
    text = "\n".join(lines) + "\n"
    if len(text) > GITHUB_LIMIT:
        text = text[:GITHUB_LIMIT] + "\n\n(report truncated)\n"
    return text


def to_json(comparison: Comparison) -> str:
    return json.dumps(
        {
            "base": comparison.base_rev,
            "head": comparison.head_rev,
            "compared_tests": comparison.compared_tests,
            "added_tests": comparison.added_tests,
            "removed_tests": comparison.removed_tests,
            "unstable_dropped": comparison.unstable_dropped,
            "saturated_skipped": comparison.saturated_skipped,
            "touched_functions": comparison.touched_functions,
            "seconds": comparison.seconds,
            "changes": [
                {
                    "kind": c.kind,
                    "location": c.location,
                    "detail": c.detail,
                    "outside_diff": c.outside,
                    "silent": c.silent,
                    "tests": sorted(c.tests),
                    "before": sorted(c.before),
                    "after": sorted(c.after),
                }
                for c in comparison.changes
            ],
        },
        indent=2,
    )
