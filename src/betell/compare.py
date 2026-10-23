"""Compare recorded execution features of a base and a head revision.

The comparison works on the files written by :mod:`betell.recorder`. Each run
carries the source of every traced file, so the comparison needs neither
checkout. Base lines are mapped to head lines with a line alignment per
file. A function counts as *touched* when the textual diff changes a line
inside it, and every behavioral change is classified by whether it occurs in
a touched function or in code the pull request leaves textually unchanged.
"""
from __future__ import annotations

import ast
import difflib
import gzip
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field

KIND_ORDER = ("outcome", "exception", "return", "argument", "call", "branch")

# Values that encode the revision itself differ between any two commits.
# setuptools-scm style versions such as 3.7.0.dev1365+g3c8c98d28a are the common case.
# Sphinx style versions such as 3.5.0+/4a6641072 embed the hash as well.
REVISION = re.compile(r"(\.dev\d+)?\+/?g?(?=[0-9]*[a-f])[0-9a-f]{7,40}\b(\.d\d{8})?")


# Raised when the garbage collector closes a suspended generator, so its timing
# depends on memory pressure rather than on the program's logic.
IGNORED_EXCEPTIONS = {"GeneratorExit"}


def normalize(value: str) -> str:
    return REVISION.sub("+<rev>", value)


@dataclass
class Run:
    files: list[str]
    sources: dict[str, str | None]
    functions: list[tuple[str, int, str]]
    tests: dict[str, dict]
    meta: dict

    @classmethod
    def load(cls, path):
        with gzip.open(path, "rt") as handle:
            data = json.load(handle)
        files = data["files"]
        functions = [(files[f], line, name) for f, line, name in data["functions"]]
        return cls(files, data["sources"], functions, data["tests"], data.get("meta", {}))


@dataclass
class Features:
    """Comparable features of one test in one run, in the run's own coordinates."""
    outcome: str | None
    arcs: set = field(default_factory=set)
    calls: set = field(default_factory=set)
    returns: dict = field(default_factory=dict)
    args: dict = field(default_factory=dict)
    exceptions: set = field(default_factory=set)
    saturated: set = field(default_factory=set)


def features(run: Run, test: dict) -> Features:
    """Features of one test. Code from non-Python files, such as compiled templates, is ignored."""
    files, fns = run.files, run.functions
    python = {i for i, rel in enumerate(files) if rel.endswith(".py")}
    test = dict(test)
    test["arcs"] = [a for a in test["arcs"] if a[0] in python]
    ok = {i for i, f in enumerate(run.functions) if f[0].endswith(".py")}
    test["calls"] = [c for c in test["calls"] if c[1] in ok and (c[0] < 0 or c[0] in ok)]
    test["returns"] = {k: v for k, v in test["returns"].items() if int(k) in ok}
    test["args"] = {k: v for k, v in test["args"].items() if int(k) in ok}
    test["exceptions"] = [e for e in test["exceptions"] if e[0] in ok and e[1] not in IGNORED_EXCEPTIONS]
    return Features(
        outcome=test["outcome"],
        arcs={(files[f], a, b) for f, a, b in test["arcs"]},
        calls={(fns[c] if c >= 0 else None, fns[d]) for c, d in test["calls"]},
        returns={fns[int(k)]: frozenset(map(normalize, v)) for k, v in test["returns"].items()},
        args={fns[int(k)]: frozenset(map(normalize, v)) for k, v in test["args"].items()},
        exceptions={(fns[f], exc, mode) for f, exc, mode in test["exceptions"]},
        saturated={(s[0], fns[int(s[1:])]) for s in test.get("saturated", [])},
    )


def stable(runs: list[Features]) -> tuple[Features, Features, int]:
    """Split repeated runs into what all runs agree on and what any run saw.

    The first result keeps only observations every run made. The second keeps
    every observation of any run. Set features are compared asymmetrically
    with them, so an observation that comes and goes between runs of one
    revision never counts as a change. Values that differ between runs are
    dropped from both results.
    """
    first = runs[0]
    dropped = 0

    def sets(attr):
        nonlocal dropped
        all_sets = [getattr(r, attr) for r in runs]
        common = set.intersection(*all_sets)
        union = set.union(*all_sets)
        dropped += len(union) - len(common)
        return common, union

    def meet_values(attr):
        nonlocal dropped
        maps = [getattr(r, attr) for r in runs]
        keys = set.union(*(set(m) for m in maps))
        kept = {}
        for key in keys:
            values = [m.get(key) for m in maps]
            if all(v == values[0] for v in values):
                kept[key] = values[0]
            else:
                dropped += 1
        return kept

    outcomes = {r.outcome for r in runs}
    outcome = first.outcome if len(outcomes) == 1 else "unstable"
    arcs, all_arcs = sets("arcs")
    calls, all_calls = sets("calls")
    exceptions, all_exceptions = sets("exceptions")
    returns, args = meet_values("returns"), meet_values("args")
    saturated = set.union(*(r.saturated for r in runs))
    common = Features(outcome, arcs, calls, returns, args, exceptions, saturated)
    union = Features(outcome, all_arcs, all_calls, returns, args, all_exceptions, saturated)
    return common, union, dropped


# -- source alignment ---------------------------------------------------------

@dataclass
class FunctionExtent:
    name: str
    qualname: str
    start: int
    end: int


def function_extents(source: str | None) -> list[FunctionExtent]:
    if not source:
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    extents = []

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qual = f"{prefix}{child.name}"
                if not isinstance(child, ast.ClassDef):
                    start = min([child.lineno] + [d.lineno for d in child.decorator_list])
                    extents.append(FunctionExtent(child.name, qual, start, child.end_lineno))
                visit(child, qual + ".")
            else:
                visit(child, prefix)

    visit(tree, "")
    return extents


class FileAlignment:
    """Line mapping from one version of a file to another."""

    def __init__(self, old: str | None, new: str | None):
        old_lines = (old or "").splitlines()
        new_lines = (new or "").splitlines()
        self.forward: dict[int, int] = {}
        self.changed_new: set[int] = set()
        self.changed_old: set[int] = set()
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    self.forward[i1 + k + 1] = j1 + k + 1
            else:
                self.changed_old.update(range(i1 + 1, i2 + 1))
                self.changed_new.update(range(j1 + 1, j2 + 1))
                if tag == "delete":
                    # A pure deletion touches the lines around it in the new file.
                    self.changed_new.update({j1, j1 + 1})

    def map(self, line: int) -> int | None:
        if line < 0:
            mapped = self.forward.get(-line)
            return -mapped if mapped is not None else None
        return self.forward.get(line)


class Alignment:
    """Maps base coordinates into head coordinates and knows what the diff touched."""

    def __init__(self, base: Run, head: Run):
        self.files: dict[str, FileAlignment] = {}
        self.head_extents: dict[str, list[FunctionExtent]] = {}
        self.base_extents: dict[str, list[FunctionExtent]] = {}
        missing = object()
        for rel in set(base.sources) | set(head.sources):
            old = base.sources.get(rel, missing)
            new = head.sources.get(rel, missing)
            # A file recorded on one side only did not run on the other side.
            # Without evidence of an edit, both sides share the same source.
            if old is missing:
                old = new
            if new is missing:
                new = old
            self.files[rel] = FileAlignment(old, new)
            self.head_extents[rel] = function_extents(new)
            self.base_extents[rel] = function_extents(old)
        self.head_names = defaultdict(list)
        for rel, extents in self.head_extents.items():
            for extent in extents:
                self.head_names[(rel, extent.name)].append(extent)

    def map_line(self, rel, line):
        alignment = self.files.get(rel)
        return alignment.map(line) if alignment else line

    def map_function(self, function):
        if function is None:
            return None
        rel, line, name = function
        mapped = self.map_line(rel, line)
        if mapped is not None:
            return (rel, mapped, name)
        candidates = self.head_names.get((rel, name), [])
        if len(candidates) == 1:
            return (rel, candidates[0].start, name)
        return (rel, None, name)

    def enclosing(self, rel, line, head=True):
        extents = (self.head_extents if head else self.base_extents).get(rel, [])
        best = None
        for extent in extents:
            if extent.start <= abs(line) <= extent.end:
                if best is None or extent.start >= best.start:
                    best = extent
        return best

    def touched(self, rel, line, head=True):
        """True if the function around ``line`` (or the module level) contains a changed line."""
        alignment = self.files.get(rel)
        if alignment is None:
            return False
        changed = alignment.changed_new if head else alignment.changed_old
        if not changed:
            return False
        extent = self.enclosing(rel, line, head)
        if extent is None:
            return abs(line) in changed
        return any(extent.start <= c <= extent.end for c in changed)

    def describe(self, rel, line, head=True):
        extent = self.enclosing(rel, line, head)
        name = extent.qualname if extent else "<module>"
        return f"{rel}::{name}"


# -- change detection ---------------------------------------------------------

@dataclass
class Change:
    kind: str
    location: str
    detail: str
    outside: bool
    tests: set = field(default_factory=set)
    silent: bool = False  # seen in at least one test whose outcome did not change
    before: set = field(default_factory=set)
    after: set = field(default_factory=set)


@dataclass
class Comparison:
    base_rev: str
    head_rev: str
    changes: list[Change]
    compared_tests: int
    added_tests: list[str]
    removed_tests: list[str]
    unstable_dropped: int
    saturated_skipped: int
    touched_functions: list[str]
    seconds: dict


def _function_label(alignment, function, head):
    rel, line, name = function
    if line is None:
        return f"{rel}::{name}"
    return alignment.describe(rel, line, head)


def _function_touched(alignment, function, head):
    rel, line, name = function
    if line is None:
        return True
    return alignment.touched(rel, line, head)


def compare(base_runs: list[Run], head_runs: list[Run], base_rev="base", head_rev="head") -> Comparison:
    base, head = base_runs[0], head_runs[0]
    alignment = Alignment(base, head)
    common = sorted(set.intersection(*(set(r.tests) for r in base_runs + head_runs)))
    added = sorted(set(head.tests) - set(base.tests))
    removed = sorted(set(base.tests) - set(head.tests))
    changes: dict[tuple, Change] = {}
    dropped = 0
    saturated_skipped = 0

    def note(kind, function_or_arc, detail, test, before=None, after=None, head_side=True):
        if kind in ("branch",):
            rel, line = function_or_arc
            location = alignment.describe(rel, line, head_side)
            outside = not alignment.touched(rel, line, head_side)
        else:
            location = _function_label(alignment, function_or_arc, head_side)
            outside = not _function_touched(alignment, function_or_arc, head_side)
        key = (kind, location, detail)
        change = changes.get(key)
        if change is None:
            change = changes[key] = Change(kind, location, detail, outside)
        change.tests.add(test)
        if before:
            change.before.update(before)
        if after:
            change.after.update(after)

    for test in common:
        b, b_any, d1 = stable([features(r, r.tests[test]) for r in base_runs])
        h, h_any, d2 = stable([features(r, r.tests[test]) for r in head_runs])
        dropped += d1 + d2

        if b.outcome != h.outcome and "unstable" not in (b.outcome, h.outcome):
            changes.setdefault(("outcome", test, ""), Change("outcome", test, f"{b.outcome} -> {h.outcome}", True))
            changes[("outcome", test, "")].tests.add(test)

        # Branches: arcs mapped into head coordinates. A transition is new if no
        # base run took it, and gone if no head run takes it.
        def mapped(arcs):
            result = set()
            for rel, a, c in arcs:
                ma, mc = alignment.map_line(rel, a), alignment.map_line(rel, c)
                if ma is not None and mc is not None:  # else it runs through edited lines
                    result.add((rel, ma, mc))
            return result

        def fresh(arcs):
            return {arc for arc in arcs if not _arc_in_new_code(alignment, arc)}

        base_arcs, base_any_arcs = mapped(b.arcs), mapped(b_any.arcs)
        head_arcs, head_any_arcs = fresh(h.arcs), fresh(h_any.arcs)
        for rel, a, c in head_arcs - base_any_arcs:
            note("branch", (rel, a if a > 0 else c), "newly taken", test, after={_arc_text(a, c)})
        for rel, a, c in base_arcs - head_any_arcs:
            note("branch", (rel, a if a > 0 else c), "no longer taken", test, before={_arc_text(a, c)})

        # Calls.
        def mapped_calls(calls):
            return {(alignment.map_function(x), alignment.map_function(y)) for x, y in calls}

        base_calls, base_any_calls = mapped_calls(b.calls), mapped_calls(b_any.calls)
        for caller, callee in h.calls - base_any_calls:
            note("call", callee, f"newly called from {_short(caller, alignment)}", test)
        for caller, callee in base_calls - h_any.calls:
            if callee[1] is None:
                continue  # the function disappeared from the head version
            note("call", callee, f"no longer called from {_short(caller, alignment)}", test)

        # Values.
        for attr, kind in (("returns", "return"), ("args", "argument")):
            letter = "r" if attr == "returns" else "a"
            base_values = {alignment.map_function(f): v for f, v in getattr(b, attr).items()}
            base_saturated = {alignment.map_function(f) for k, f in b.saturated if k == letter}
            head_saturated = {f for k, f in h.saturated if k == letter}
            for function, after in getattr(h, attr).items():
                before = base_values.get(function)
                if before is None or before == after:
                    continue
                if function in base_saturated or function in head_saturated:
                    saturated_skipped += 1
                    continue
                note(kind, function, "values changed", test, before=before - after, after=after - before)

        # Exceptions.
        def mapped_exceptions(exceptions):
            return {(alignment.map_function(f), e, m) for f, e, m in exceptions}

        base_exc, base_any_exc = mapped_exceptions(b.exceptions), mapped_exceptions(b_any.exceptions)
        for function, exc, mode in h.exceptions - base_any_exc:
            note("exception", function, f"now {mode}: {exc}", test)
        for function, exc, mode in base_exc - h_any.exceptions:
            if function[1] is None:
                continue
            note("exception", function, f"no longer {mode}: {exc}", test)

    flipped = {c.location for c in changes.values() if c.kind == "outcome"}
    for change in changes.values():
        change.silent = change.kind != "outcome" and bool(change.tests - flipped)

    touched = set()
    for rel, fa in alignment.files.items():
        for line in fa.changed_new:
            extent = alignment.enclosing(rel, line)
            touched.add(f"{rel}::{extent.qualname if extent else '<module>'}")

    ordered = sorted(
        changes.values(),
        key=lambda c: (KIND_ORDER.index(c.kind), not c.silent, not c.outside, -len(c.tests), c.location, c.detail),
    )
    return Comparison(
        base_rev, head_rev, ordered, len(common), added, removed, dropped, saturated_skipped,
        sorted(touched),
        {"base": [r.meta.get("seconds") for r in base_runs], "head": [r.meta.get("seconds") for r in head_runs]},
    )


def _arc_in_new_code(alignment, arc):
    rel, a, c = arc
    fa = alignment.files.get(rel)
    if fa is None:
        return False
    return abs(a) in fa.changed_new or abs(c) in fa.changed_new


def _arc_text(a, c):
    if a == c:
        return f"L{a}"
    left = "entry" if a < 0 else f"L{a}"
    right = "exit" if c < 0 else f"L{c}"
    return f"{left}->{right}"


def _short(function, alignment):
    if function is None:
        return "a test"
    return _function_label(alignment, function, True).split("::", 1)[-1]
