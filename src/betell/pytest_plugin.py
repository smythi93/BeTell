"""pytest plugin that records execution features per test.

Load it with ``-p betell.pytest_plugin --betell-out run.json.gz``. Like the
recorder, this module must stay compatible with Python 3.6.
"""
import os
import time

import pytest

from betell.recorder import create

_ACTIVE = []


def pytest_addoption(parser):
    group = parser.getgroup("betell")
    group.addoption("--betell-out", default=None, help="write recorded features to this file")
    group.addoption("--betell-root", default=None, help="project root to trace (default: rootdir)")
    group.addoption("--betell-include-tests", action="store_true", default=False)
    group.addoption("--betell-no-values", action="store_true", default=False)
    group.addoption("--betell-backend", default="auto", choices=("auto", "settrace", "monitoring"))


def pytest_configure(config):
    out = config.getoption("--betell-out")
    if not out:
        return
    root = config.getoption("--betell-root") or str(config.rootdir)
    recorder = create(
        root,
        backend=config.getoption("--betell-backend"),
        include_tests=config.getoption("--betell-include-tests"),
        values=not config.getoption("--betell-no-values"),
    )
    config._betell = (recorder, out, time.time())
    _ACTIVE.append(recorder)
    recorder.start()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item, nextitem):
    state = getattr(item.config, "_betell", None)
    if state is not None:
        state[0].begin(item.nodeid)
    yield
    if state is not None:
        state[0].end()


def pytest_runtest_logreport(report):
    if not _ACTIVE:
        return
    state = _ACTIVE[-1]
    if report.when == "call" or report.outcome != "passed":
        outcome = report.outcome
        if report.when != "call" and outcome == "failed":
            outcome = "error"
        state.outcome(report.nodeid, outcome)


def pytest_unconfigure(config):
    state = getattr(config, "_betell", None)
    if state is None:
        return
    recorder, out, started = state
    recorder.stop()
    if recorder in _ACTIVE:
        _ACTIVE.remove(recorder)
    recorder.dump(out, meta={"seconds": time.time() - started, "cwd": os.getcwd()})
