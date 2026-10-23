# Evaluation

This page describes how to reproduce the evaluation of BeTell.
It covers three sets of changes, which answer three questions.

- Does BeTell report what changed, and only that?
- Does BeTell reveal effects that the diff and the tests hide?
- Is BeTell fast enough for continuous integration?

All scripts live in [`eval/`](../eval).
The analysis scripts write the numbers reported in the paper as LaTeX macros to `eval/numbers/`, or to the directory in the environment variable `BETELL_NUMBERS`.
The committed files in `eval/numbers/` are the numbers of the paper.

## Toy pull requests

The six demo scenarios have known effects and form the test suite of BeTell.

```bash
pip install -e . pytest
python -m pytest tests
```

The tests check every scenario with both recorder backends, and check that two runs per revision remove the noise of a test with time stamps, random numbers, and object identities.

## SWE-bench Verified fixes

[SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) pairs real GitHub issues with the fixes of the developers and with tests that check these fixes.
We used the 19 fixes from 5 projects whose tests use pytest and whose container images were available.
[`eval/candidates.json`](../eval/candidates.json) lists them with their patches.

For each fix, the revision with the new tests is the base, and the fixed revision is the head.
BeTell runs the test files that the new tests touch, twice per revision.

### Results without rerunning

The repository contains everything except the raw recordings.

| Path | Content |
|---|---|
| `eval/runs/<instance>/report.md` | BeTell's report for the fix |
| `eval/runs/<instance>/report.json` | the comparison as JSON |
| `eval/runs/<instance>/sources.json` | both versions of the edited files |
| `eval/results.json` | per-instance summary of `analyze.py` |
| `eval/silent_outside.tsv` | manual labels of every silent change in unedited code |

The raw recordings (`base-0.json.gz` to `head-1.json.gz` per instance, about 370 MB) are attached to the [v0.1.0 release](https://github.com/smythi93/BeTell/releases/tag/v0.1.0) as `betell-eval-recordings.tar`.
Extract the archive in the repository root to restore them into `eval/runs/`.

```bash
tar -xf betell-eval-recordings.tar
python eval/analyze.py
```

`analyze.py` recomputes every comparison from the recordings, the A/A comparison of two base runs, the agreement of changed outcomes with the ground truth of SWE-bench, and the overhead.
It writes `eval/results.json`, the reports in `eval/runs/`, and `eval/numbers/numbers-swebench.tex`.

### Manual classification

`silent_outside.py` lists every silent change in an unedited function and keeps the existing labels in `eval/silent_outside.tsv`.

```bash
python eval/silent_outside.py
```

Each row carries one label.

| Label | Meaning |
|---|---|
| `genuine` | an effect of the fix on code it does not edit |
| `state` | state shared between tests, such as caches |
| `revision` | values that embed the revision or line numbers of edited files |
| `timing` | values that depend on threads or timing |
| `unclear` | none of the above can be confirmed |

The script writes `eval/numbers/numbers-manual.tex`.

### Rerunning the recordings

Rerunning needs a Linux host with Docker and the SWE-bench evaluation images, such as `swebench/sweb.eval.x86_64.sphinx-doc_1776_sphinx-8721`.

```bash
python3 eval/swebench_run.py --instances eval/candidates.json --out eval/runs --jobs 6
python3 eval/analyze.py
```

For each instance, the driver starts the container, commits the test patch as base and the gold patch as head, copies the recorder into the container, times one plain pytest run, and records both revisions twice.
Pass `--only <instance>` to rerun selected instances.
The containers use older Python versions, so these recordings use the `sys.settrace` backend.

## Real commits

To check the worktree mode that the GitHub Action uses, BeTell ran on 11 recent commits of `click` and `more-itertools` against their parents, with the full test suites and Python 3.12.
[`eval/real_run.py`](../eval/real_run.py) lists the commits.

Prepare a working directory with clones of both projects and one virtual environment per project.

```bash
mkdir work && cd work
git clone https://github.com/pallets/click
git clone https://github.com/more-itertools/more-itertools
for p in click more-itertools; do
  python3.12 -m venv $p-venv
  $p-venv/bin/pip install -e ./$p pytest /path/to/BeTell
done
cd /path/to/BeTell
python eval/real_run.py /path/to/work
python eval/analyze_real.py
```

`real_run.py` writes one report per commit to `eval/real/` together with `summary.json`, and `analyze_real.py` writes `eval/real-results.json` and `eval/numbers/numbers-real.tex`.
Timings depend on the machine, so the overhead will differ slightly from the paper.

## Main results

- BeTell reported all 22 expected outcome changes of the SWE-bench fixes and no spurious outcome change.
- In 6 of 19 fixes, it revealed genuine silent changes in unedited functions, 39 in total.
- None of the 3 commits that announce a refactoring or an optimization changed the behavior of an unedited function.
- With `sys.monitoring`, recording took a median of 1.3 times as long as a plain test run, and at most 4.8 times.
- All evaluation runs took 2.7 hours in total on a shared server and a laptop.
