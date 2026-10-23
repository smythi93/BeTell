# Usage

BeTell compares the behavior of two revisions of a Python project under the project's own pytest tests.
This page covers the command line interface, the demo, and the pytest plugin.
For continuous integration, see [github-action.md](github-action.md).

## Installation

BeTell is not on PyPI yet. Install it from GitHub into the environment that runs your tests.

```bash
pip install git+https://github.com/smythi93/BeTell
```

The `betell` command needs Python 3.9 or later and git.
If your tests run on an older interpreter, see [Test environments with another interpreter](#test-environments-with-another-interpreter).

## Comparing two revisions

```bash
betell run --base main --head HEAD --pytest-args tests --out report.md
```

`betell run` performs the whole workflow.

1. It checks out the base and the head revision in temporary git worktrees.
2. It runs the selected tests twice on each revision and records their behavior.
3. It compares the recordings and writes the report.
4. It removes the worktrees again.

Your own working tree is never modified in the default mode.
Without `--out`, the report goes to standard output.

### Options of `betell run`

| Option | Default | Meaning |
|---|---|---|
| `--repo PATH` | `.` | git repository to analyze |
| `--base REV` | required | base revision, such as the target branch of a pull request |
| `--head REV` | `HEAD` | head revision |
| `--pytest-args ARGS` | empty | arguments for pytest, such as a test directory or `-k` filters, as one string |
| `--python PATH` | the current interpreter | interpreter that runs the tests |
| `--runs-base N` | `2` | runs of the base revision, used to filter nondeterminism |
| `--runs-head N` | `2` | runs of the head revision, used to filter nondeterminism |
| `--mode worktree\|inplace` | `worktree` | where the revisions are checked out (see below) |
| `--no-values` | off | skip arguments and return values to reduce the overhead |
| `--backend auto\|monitoring\|settrace` | `auto` | recorder backend; `auto` uses `sys.monitoring` on Python 3.12 and later |
| `--out FILE` | stdout | Markdown report |
| `--json FILE` | none | the comparison as JSON (see [report.md](report.md#json-output)) |
| `--keep` | off | keep the raw recordings and print their directory |

### Choosing the number of runs

Two runs per revision are the default and remove most nondeterminism, such as time stamps, random numbers, and thread timing.
A test suite with much nondeterminism may need three runs.
A deterministic test suite can use one run per revision to halve the cost.

### Projects that must be installed or compiled

Worktrees work for projects that run from their source tree.
Projects with compiled extensions, or projects that are installed into the environment, need the revisions checked out where the environment expects them.

```bash
betell run --mode inplace --base main --head HEAD --pytest-args tests
```

In-place mode checks out each revision in the repository itself, records it, and returns to the original branch at the end.
It requires a clean working tree.
If a compiled extension changes between the revisions, rebuild it between the runs, for example, with `betell record` (see below).

### Test environments with another interpreter

The recorder runs inside the test environment and supports Python 3.6 and later.
The `betell` command itself can run on a newer interpreter and drive the old one.

```bash
betell run --python /path/to/old-venv/bin/python --base main --pytest-args tests
```

The test environment needs pytest, but it does not need BeTell installed, because BeTell puts its recorder on the `PYTHONPATH` of the test run.

## Recording and comparing separately

`betell record` and `betell compare` expose the two halves of the workflow.
This helps when the revisions are built in separate jobs or containers.

```bash
git checkout main
betell record --out base-0.json.gz --pytest-args tests
betell record --out base-1.json.gz --pytest-args tests
git checkout feature
betell record --out head-0.json.gz --pytest-args tests
betell record --out head-1.json.gz --pytest-args tests
betell compare --base base-0.json.gz base-1.json.gz --head head-0.json.gz head-1.json.gz \
    --repo . --base-rev main --head-rev feature --out report.md
```

`betell record` accepts `--workdir`, `--root` (the project root to trace, by default the working directory), `--python`, `--no-values`, and `--backend`.
`betell compare` reads the edited sources from `--repo` to align lines between the revisions, so pass the repository and both revision names.

## Using the pytest plugin directly

The recorder is a pytest plugin, so any pytest invocation can record a run.

```bash
python -m pytest -p betell.pytest_plugin --betell-out run.json.gz tests
```

| Option | Meaning |
|---|---|
| `--betell-out FILE` | write the recording to this file; without it, the plugin stays inactive |
| `--betell-root PATH` | project root to trace (default: the pytest root directory) |
| `--betell-include-tests` | also trace test files, which are skipped by default |
| `--betell-no-values` | skip arguments and return values |
| `--betell-backend auto\|monitoring\|settrace` | recorder backend |

Set `PYTHONHASHSEED=0` for recordings that you want to compare, as `betell run` does.
Otherwise the iteration order of sets changes between runs.

## Demo

`betell demo SCENARIO` builds a toy repository with the tags `base` and `head`, prints the textual diff, and prints BeTell's report.
The same command works in the Docker image.

```bash
betell demo threshold
docker run --rm ghcr.io/smythi93/betell demo threshold
```

| Scenario | Edit | Report of BeTell |
|---|---|---|
| `refactor` | rewrites `discount` without changing its results | no change |
| `shift` | adds comments and an unused function | no change |
| `helper` | `normalize` also lowercases names | unedited `describe` takes another branch, with the same result |
| `threshold` | raises the threshold of the bulk discount | unedited `checkout` returns other totals |
| `exception` | `parse` returns `None` instead of raising | unedited `safe_parse` no longer handles a `ValueError` |
| `outcome` | halves bulk prices | a test now fails, and `checkout` returns other totals |

Pass `--dir DIR` to keep the toy repository, for example, to open it in an editor or push it to GitHub and try the action.
