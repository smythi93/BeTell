"""Lightweight execution-feature recorder.

This module runs inside the environment of the project under test, so it must
stay compatible with old interpreters (Python 3.6 and later) and must not
import anything outside the standard library.

The recorder installs a ``sys.settrace`` hook that only follows frames whose
code lives in the project root, and records, per test:

* arcs: consecutive line pairs inside a function, including entry and exit;
* calls: edges between project functions;
* arguments and return values, abstracted to a type and a bounded repr;
* exceptions raised out of or handled inside project functions.
"""
import gzip
import json
import os
import re
import reprlib
import sys
import threading

ADDRESS = re.compile(r" at 0x[0-9a-fA-F]+")
TEST_FILE = re.compile(r"(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_tests?\.py$|(^|/)conftest\.py$")
IGNORED_ARGS = ("self", "cls")

WHITESPACE = re.compile(r"\s+")
# Version strings that embed the commit, such as 3.7.0.dev1365+g3c8c98d28a or
# 3.5.0+/4a6641072, differ between any two revisions. They are normalized
# before truncation, which could otherwise cut the hash in half.
REVISION = re.compile(r"(\.dev\d+)?\+/?g?(?=[0-9]*[a-f])[0-9a-f]{7,40}\b(\.d\d{8})?")


# pytest numbers its temporary directories per session, e.g. pytest-of-alice/pytest-17.
PYTEST_TMP = re.compile(r"pytest-of-[^/\\'\"]+[/\\]pytest-\d+")
# Paths into the checkout differ between base and head worktrees. The recorder
# registers the project root here, and values show it as <root>.
ROOTS = []


def normalize_text(text):
    for root in ROOTS:
        text = text.replace(root, "<root>")
    return PYTEST_TMP.sub("<pytest-tmp>", REVISION.sub("+<rev>", text))


def clean(text):
    return WHITESPACE.sub(" ", normalize_text(ADDRESS.sub(" at 0x?", text)))


class _Repr(reprlib.Repr):
    def repr_str(self, value, level):
        return reprlib.Repr.repr_str(self, normalize_text(value), level)

    def repr_instance(self, value, level):
        try:
            text = repr(value)
        except Exception:
            return "<" + type(value).__name__ + ">"
        text = clean(text)
        if len(text) > self.maxother:
            half = max(0, (self.maxother - 3) // 2)
            text = text[:half] + "..." + text[len(text) - half:]
        return text


_REPR = _Repr()
_REPR.maxstring = 60
_REPR.maxother = 60
_REPR.maxlist = 6
_REPR.maxtuple = 6
_REPR.maxdict = 6
_REPR.maxset = 6
_REPR.maxlevel = 3

SIMPLE = (bool, int, float, complex, str, bytes, type(None))
# Values whose representation names a location or an identity rather than data.
OPAQUE = ("frame", "traceback", "code", "function", "builtin_function_or_method", "method",
          "module", "type", "generator", "coroutine", "cell", "weakref", "Thread")


def abstract(value):
    """Map a runtime value to a short, address-free string."""
    kind = type(value)
    name = kind.__name__
    try:
        if kind is str:
            text = repr(normalize_text(value))
        elif kind in SIMPLE:
            text = repr(value)
        elif name in OPAQUE or isinstance(value, type):
            text = "<" + str(getattr(value, "__qualname__", None) or getattr(value, "__name__", name)) + ">"
        elif kind.__repr__ is object.__repr__:
            text = "<" + name + ">"
        else:
            text = _REPR.repr(value)
    except Exception:
        text = "<unrepresentable>"
    text = clean(text)
    if len(text) > 100:
        text = text[:97] + "..."
    return name + ":" + text


class TestRecord(object):
    __slots__ = ("arcs", "calls", "returns", "args", "exceptions", "return_counts", "arg_counts",
                 "saturated", "outcome", "branches", "hits")

    def __init__(self):
        self.arcs = {}  # function id -> set of (previous line << 20 | line), 0 marks entry and exit
        self.calls = set()
        self.returns = {}
        self.args = {}
        self.exceptions = set()
        self.return_counts = {}
        self.arg_counts = {}
        self.saturated = set()
        self.outcome = None
        self.branches = {}
        self.hits = {}


_MISSING = object()
LINE_BITS = 20
LINE_MASK = (1 << LINE_BITS) - 1
NO_ARGUMENTS = 0x20 | 0x80 | 0x200  # generators, coroutines, and async generators


class Recorder(object):
    """Recorder based on ``sys.settrace``. It records line-to-line transitions."""

    backend = "settrace"

    def __init__(self, root, include_tests=False, values=True, max_values=24):
        self.root = os.path.realpath(root) + os.sep
        for variant in sorted({os.path.realpath(root), os.path.abspath(root)}, key=len, reverse=True):
            if variant not in ROOTS:
                ROOTS.append(variant)
        ROOTS.sort(key=len, reverse=True)
        self.include_tests = include_tests
        self.values = values
        self.max_values = max_values
        self.files = {}
        self.file_ids = {}
        self.functions = {}
        self.codes = {}
        self.tests = {}
        self.current = None
        self.own = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.local_code = self.local_tracer(TestRecord(), set(), -1).__code__

    # -- file and function interning -------------------------------------
    def relative(self, filename):
        try:
            return self.files[filename]
        except KeyError:
            pass
        rel = None
        if filename and not filename.startswith("<"):
            path = os.path.realpath(filename)
            if path.startswith(self.root) and not path.startswith(self.own):
                candidate = path[len(self.root):].replace(os.sep, "/")
                if (
                    candidate.endswith(".py")
                    and "site-packages/" not in candidate
                    and not candidate.startswith(".")
                    and (self.include_tests or not TEST_FILE.search(candidate))
                ):
                    rel = candidate
                    if rel not in self.file_ids:
                        self.file_ids[rel] = len(self.file_ids)
        self.files[filename] = rel
        return rel

    def register(self, code):
        """Intern ``code`` and return (function id, argument names), or None for foreign code."""
        rel = self.relative(code.co_filename)
        info = None
        if rel is not None:
            key = (self.file_ids[rel], code.co_firstlineno, code.co_name)
            fid = self.functions.get(key)
            if fid is None:
                fid = len(self.functions)
                self.functions[key] = fid
            names = ()
            if not code.co_flags & NO_ARGUMENTS:
                count = code.co_argcount + getattr(code, "co_kwonlyargcount", 0)
                names = tuple(n for n in code.co_varnames[:count] if n not in IGNORED_ARGS)
            info = (fid, names)
        self.codes[code] = info
        return info

    # -- test lifecycle ---------------------------------------------------
    def begin(self, test_id):
        record = self.tests.get(test_id)
        if record is None:
            record = TestRecord()
            self.tests[test_id] = record
        self.current = record

    def end(self):
        self.current = None

    def outcome(self, test_id, outcome):
        record = self.tests.get(test_id)
        if record is None:
            record = TestRecord()
            self.tests[test_id] = record
        if record.outcome in (None, "passed") or outcome == "failed":
            record.outcome = outcome

    def start(self):
        sys.settrace(self.trace)
        threading.settrace(self.trace)

    def stop(self):
        sys.settrace(None)
        threading.settrace(None)

    # -- tracing ------------------------------------------------------------
    def trace(self, frame, event, arg):
        """Global trace function. Python calls it on every function call."""
        record = self.current
        if record is None:
            return None
        existing = frame.f_trace
        if existing is not None and getattr(existing, "__code__", None) is self.local_code:
            return existing  # a resumed generator keeps its local tracer and state
        codes = self.codes
        info = codes.get(frame.f_code, _MISSING)
        if info is _MISSING:
            info = self.register(frame.f_code)
        if info is None:
            return None
        fid, names = info

        caller = frame.f_back
        caller_id = -1
        depth = 0
        while caller is not None and depth < 8:
            caller_info = codes.get(caller.f_code, _MISSING)
            if caller_info is _MISSING:
                caller_info = self.register(caller.f_code)
            if caller_info is not None:
                caller_id = caller_info[0]
                break
            caller = caller.f_back
            depth += 1
        record.calls.add((caller_id, fid))

        if names and self.values:
            count = record.arg_counts.get(fid, 0)
            if count < self.max_values:
                record.arg_counts[fid] = count + 1
                local = frame.f_locals
                text = "(" + ", ".join(n + "=" + abstract(local.get(n)) for n in names) + ")"
                bucket = record.args.get(fid)
                if bucket is None:
                    bucket = record.args[fid] = set()
                bucket.add(text)
            elif count == self.max_values:
                record.arg_counts[fid] = count + 1
                record.saturated.add(("a", fid))

        arcs = record.arcs.get(fid)
        if arcs is None:
            arcs = record.arcs[fid] = set()
        return self.local_tracer(record, arcs, fid)

    def local_tracer(self, record, arcs, fid):
        previous = 0  # previous line, 0 at entry
        pending = None  # name of an exception that has not been handled yet
        values = self.values
        cap = self.max_values
        counts = record.return_counts
        returns = record.returns
        exceptions = record.exceptions
        add = arcs.add

        def local(frame, event, arg):
            nonlocal previous, pending
            if event == "line":
                line = frame.f_lineno
                add(previous << 20 | line)
                previous = line
                if pending is not None:
                    exceptions.add((fid, pending, "handled"))
                    pending = None
            elif event == "return":
                add(previous << 20)
                if pending is not None:
                    exceptions.add((fid, pending, "raised"))
                    pending = None
                elif values:
                    count = counts.get(fid, 0)
                    if count < cap:
                        counts[fid] = count + 1
                        bucket = returns.get(fid)
                        if bucket is None:
                            bucket = returns[fid] = set()
                        bucket.add(abstract(arg))
                    elif count == cap:
                        counts[fid] = count + 1
                        record.saturated.add(("r", fid))
            elif event == "exception":
                pending = getattr(arg[0], "__name__", str(arg[0]))
            return local

        return local

    # -- output ---------------------------------------------------------------
    def dump(self, path, meta=None):
        files = sorted(self.file_ids, key=self.file_ids.get)
        sources = {}
        for rel in files:
            try:
                with open(os.path.join(self.root, rel), "rb") as handle:
                    sources[rel] = handle.read().decode("utf-8", "replace")
            except (IOError, OSError):
                sources[rel] = None
        functions = [None] * len(self.functions)
        for (file_id, line, name), fid in self.functions.items():
            functions[fid] = [file_id, line, name]
        tests = {}
        for test_id, record in self.tests.items():
            arcs = set()
            for fid, keys in record.arcs.items():
                file_id, first = functions[fid][0], -functions[fid][1]
                for key in keys:
                    arcs.add((file_id, (key >> LINE_BITS) or first, (key & LINE_MASK) or first))
            tests[test_id] = {
                "outcome": record.outcome,
                "arcs": sorted(arcs),
                "calls": sorted(record.calls),
                "returns": dict((str(k), sorted(v)) for k, v in record.returns.items()),
                "args": dict((str(k), sorted(v)) for k, v in record.args.items()),
                "exceptions": sorted(record.exceptions),
                "saturated": sorted(k[0] + str(k[1]) for k in record.saturated),
            }
        payload = {
            "format": 1,
            "backend": self.backend,
            "meta": meta or {},
            "files": files,
            "sources": sources,
            "functions": functions,
            "tests": tests,
        }
        directory = os.path.dirname(os.path.abspath(path))
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with gzip.open(path, "wt") as handle:
            json.dump(payload, handle)


class MonitoringRecorder(Recorder):
    """Recorder based on ``sys.monitoring`` (Python 3.12 and later).

    It records executed lines and branch outcomes instead of every line
    transition. Each line and each branch direction is reported once per test
    and then disabled, so loops cost almost nothing after their first
    iterations. Events are re-enabled at the start of every test.
    """

    backend = "monitoring"
    # Events that cannot be disabled per direction or per caller are sampled.
    # After this many hits of one location within one test, the location is
    # disabled until the next test starts.
    sample = 64

    def __init__(self, *args, **kwargs):
        Recorder.__init__(self, *args, **kwargs)
        self.monitoring = sys.monitoring
        self.tool = None
        self.lines = {}

    def begin(self, test_id):
        Recorder.begin(self, test_id)
        if self.tool is not None:
            self.monitoring.restart_events()

    def start(self):
        m = self.monitoring
        for tool in (3, 4):
            if m.get_tool(tool) is None:
                m.use_tool_id(tool, "betell")
                self.tool = tool
                break
        if self.tool is None:
            raise RuntimeError("no free sys.monitoring tool id")
        e = m.events
        callbacks = [
            (e.PY_START, self.on_start),
            (e.PY_RETURN, self.on_return),
            (e.LINE, self.on_line),
            (e.PY_UNWIND, self.on_unwind),
            (e.EXCEPTION_HANDLED, self.on_handled),
        ]
        if hasattr(e, "BRANCH_LEFT"):
            callbacks += [(e.BRANCH_LEFT, self.on_branch_side), (e.BRANCH_RIGHT, self.on_branch_side)]
        else:
            callbacks.append((e.BRANCH, self.on_branch))
        mask = 0
        for event, callback in callbacks:
            m.register_callback(self.tool, event, callback)
            mask |= event
        m.set_events(self.tool, mask)

    def stop(self):
        if self.tool is not None:
            self.monitoring.set_events(self.tool, 0)
            self.monitoring.free_tool_id(self.tool)
            self.tool = None

    def info(self, code):
        info = self.codes.get(code, _MISSING)
        if info is _MISSING:
            info = self.register(code)
        return info

    def line_of(self, code, offset):
        table = self.lines.get(code)
        if table is None:
            table = {}
            for start, end, line in code.co_lines():
                if line is not None:
                    for position in range(start, end, 2):
                        table[position] = line
            self.lines[code] = table
        return table.get(offset, 0)

    def on_start(self, code, offset):
        record = self.current
        if record is None:
            return None
        info = self.info(code)
        if info is None:
            return self.monitoring.DISABLE
        fid, names = info
        frame = sys._getframe(1)
        caller = frame.f_back
        caller_id = -1
        depth = 0
        while caller is not None and depth < 8:
            caller_info = self.info(caller.f_code)
            if caller_info is not None:
                caller_id = caller_info[0]
                break
            caller = caller.f_back
            depth += 1
        record.calls.add((caller_id, fid))
        if names and self.values:
            count = record.arg_counts.get(fid, 0)
            if count < self.max_values:
                record.arg_counts[fid] = count + 1
                local = frame.f_locals
                text = "(" + ", ".join(n + "=" + abstract(local.get(n)) for n in names) + ")"
                record.args.setdefault(fid, set()).add(text)
            elif count == self.max_values:
                record.arg_counts[fid] = count + 1
                record.saturated.add(("a", fid))
        hits = record.hits.get(code, 0) + 1
        record.hits[code] = hits
        return self.monitoring.DISABLE if hits >= self.sample else None

    def on_return(self, code, offset, value):
        record = self.current
        if record is None or not self.values:
            return self.monitoring.DISABLE
        info = self.info(code)
        if info is None:
            return self.monitoring.DISABLE
        fid = info[0]
        count = record.return_counts.get(fid, 0)
        if count < self.max_values:
            record.return_counts[fid] = count + 1
            record.returns.setdefault(fid, set()).add(abstract(value))
            return None
        record.saturated.add(("r", fid))
        return self.monitoring.DISABLE

    def on_line(self, code, line):
        record = self.current
        if record is not None:
            info = self.info(code)
            if info is not None:
                arcs = record.arcs.get(info[0])
                if arcs is None:
                    arcs = record.arcs[info[0]] = set()
                arcs.add(line << LINE_BITS | line)
        return self.monitoring.DISABLE

    def _branch(self, code, source, destination):
        record = self.current
        if record is None:
            return None
        info = self.info(code)
        if info is None:
            return None
        arcs = record.arcs.get(info[0])
        if arcs is None:
            arcs = record.arcs[info[0]] = set()
        arcs.add(self.line_of(code, source) << LINE_BITS | self.line_of(code, destination))
        return record

    def on_branch_side(self, code, source, destination):
        self._branch(code, source, destination)
        return self.monitoring.DISABLE

    def on_branch(self, code, source, destination):
        record = self._branch(code, source, destination)
        if record is None:
            return self.monitoring.DISABLE
        key = (code, source)
        seen = record.branches.setdefault(key, set())
        seen.add(destination)
        hits = record.hits.get(key, 0) + 1
        record.hits[key] = hits
        return self.monitoring.DISABLE if len(seen) > 1 or hits >= self.sample else None

    def on_unwind(self, code, offset, exception):
        record = self.current
        if record is not None:
            info = self.info(code)
            if info is not None:
                record.exceptions.add((info[0], type(exception).__name__, "raised"))

    def on_handled(self, code, offset, exception):
        record = self.current
        if record is not None:
            info = self.info(code)
            if info is not None:
                record.exceptions.add((info[0], type(exception).__name__, "handled"))


def create(root, backend="auto", **options):
    """Create the fastest recorder the running interpreter supports."""
    if backend == "auto":
        backend = "monitoring" if hasattr(sys, "monitoring") else "settrace"
    if backend == "monitoring":
        return MonitoringRecorder(root, **options)
    return Recorder(root, **options)
