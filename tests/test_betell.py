"""End-to-end checks of betell on toy repositories with known ground truth."""
import json
import sys
import tempfile

import pytest

from betell.cli import main
from betell.demo import BASE, NONDETERMINISTIC, SCENARIOS, build


BACKENDS = ["settrace"] + (["monitoring"] if sys.version_info >= (3, 12) else [])


@pytest.fixture(params=BACKENDS, autouse=True)
def backend(request):
    return request.param


@pytest.fixture
def run(backend):
    def run(tmp_path, name, base, head, *extra):
        repo = build(tmp_path / name, base, head)
        out = tmp_path / f"{name}.json"
        main(["run", "--repo", str(repo), "--base", "base", "--head", "head", "--backend", backend,
              "--out", str(tmp_path / f"{name}.md"), "--json", str(out), *extra])
        return json.loads(out.read_text())["changes"]
    return run


def kinds(changes, outside=None):
    return {(c["kind"], c["location"], c["detail"]) for c in changes
            if outside is None or c["outside_diff"] == outside}


@pytest.mark.parametrize("name", ["refactor", "shift"])
def test_no_false_alarms(run, tmp_path, name):
    assert run(tmp_path, name, BASE, SCENARIOS[name]) == []


def test_helper_change_reaches_untouched_caller(run, tmp_path):
    changes = run(tmp_path, "helper", BASE, SCENARIOS["helper"])
    outside = kinds(changes, outside=True)
    assert ("branch", "shop/api.py::describe", "newly taken") in outside
    assert ("return", "shop/util.py::normalize", "values changed") in kinds(changes, outside=False)


def test_threshold_changes_untouched_return(run, tmp_path):
    changes = run(tmp_path, "threshold", BASE, SCENARIOS["threshold"])
    assert ("return", "shop/api.py::checkout", "values changed") in kinds(changes, outside=True)


def test_symlinked_temporary_directory(run, tmp_path, monkeypatch):
    # On macOS, temporary directories live under the symlink /var -> /private/var.
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    monkeypatch.setattr(tempfile, "tempdir", str(link))
    changes = run(tmp_path, "threshold", BASE, SCENARIOS["threshold"])
    assert ("return", "shop/api.py::checkout", "values changed") in kinds(changes, outside=True)


def test_exception_no_longer_handled(run, tmp_path):
    changes = run(tmp_path, "exception", BASE, SCENARIOS["exception"])
    assert ("exception", "shop/api.py::safe_parse", "no longer handled: ValueError") in kinds(changes, outside=True)
    assert ("exception", "shop/util.py::parse", "no longer raised: ValueError") in kinds(changes, outside=False)


def test_outcome_flip(run, tmp_path):
    changes = run(tmp_path, "outcome", BASE, SCENARIOS["outcome"])
    flips = [c for c in changes if c["kind"] == "outcome"]
    assert [c["detail"] for c in flips] == ["passed -> failed"]


def test_repeated_base_runs_filter_nondeterminism(run, tmp_path):
    tree = dict(BASE, **NONDETERMINISTIC)
    noisy = run(tmp_path, "noisy", tree, tree, "--runs-base", "1", "--runs-head", "1")
    assert any(c["location"] == "shop/clock.py::stamp" for c in noisy)
    filtered = run(tmp_path, "filtered", tree, tree, "--runs-base", "2", "--runs-head", "2")
    assert filtered == []
