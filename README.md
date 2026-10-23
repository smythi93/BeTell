# BeTell

**Behavioral evidence for human and AI code review.**

[![Tests](https://github.com/smythi93/BeTell/actions/workflows/tests.yml/badge.svg)](https://github.com/smythi93/BeTell/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/smythi93/BeTell/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

A textual diff shows which lines a pull request edits.
It does not show what the edit does when the program runs.
BeTell runs your existing tests on the base and the head revision of a pull request, records how your project's code executes, and reports the behavior that changed.
It leads with *silent* changes in code that the pull request does not edit, because neither the diff nor the test results point a reviewer at them.

BeTell needs no specification, no new tests, and no changes to your project.
It runs as a command line tool, as a pytest plugin, in a Docker image, and as a GitHub Action that comments on pull requests.

## An example

This pull request raises the threshold of a bulk discount.

```diff
 # shop/util.py
 def discount(total):
-    if total > 100:
+    if total > 150:
         return total * 0.9
     return total
```

The diff does not show that the unedited function `checkout` in `shop/api.py` now charges 120 instead of 108 for twelve items at a price of 10.
The tests do not show it either, because the test for bulk orders only asserts a total of at least 100.
BeTell does:

> ## Behavioral diff `base` → `head`
>
> **2 functions behave differently.** Not edited by this pull request: 1. Different in tests whose outcome stays the same: 2. Test outcomes that changed: 0.
>
> ### Silent changes in code this pull request does not edit
>
> - `shop/api.py::checkout` in 1 test(s), e.g. `tests/test_shop.py::test_checkout_bulk`: return values changed (new `int:120`, gone `float:108.0`).
>
> ### Silent changes in edited code
>
> - `shop/util.py::discount` in 1 test(s), e.g. `tests/test_shop.py::test_checkout_bulk`: return values changed (new `int:120`, gone `float:108.0`); control flow changed (1 newly taken, 1 no longer taken line transitions).

Whether the new total is intended is exactly the question a reviewer should ask.

## Try it in one command

The Docker image contains six toy pull requests with known effects.

```bash
docker run --rm ghcr.io/smythi93/betell demo threshold
```

The demo builds a small repository, prints the textual diff of the pull request, and then prints BeTell's report.
The other scenarios are `refactor`, `shift`, `helper`, `exception`, and `outcome` (see [docs/usage.md](https://github.com/smythi93/BeTell/blob/main/docs/usage.md#demo)).

## Use it on your project

Install BeTell into the environment that runs your tests and compare two revisions.

```bash
pip install betell
betell run --base main --head HEAD --pytest-args tests --out report.md
```

BeTell checks out both revisions in temporary worktrees, so your working tree stays untouched.
See [docs/usage.md](https://github.com/smythi93/BeTell/blob/main/docs/usage.md) for all options, for projects that must be installed or compiled, and for test environments with older Python versions.

## Use it on every pull request

Add this workflow as `.github/workflows/betell.yml`.

```yaml
name: betell
on: pull_request
permissions:
  contents: read
  pull-requests: write
jobs:
  behavior:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # BeTell checks out the base revision as well
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e . pytest
      - uses: smythi93/BeTell@v0.1.1
        with:
          pytest-args: tests
```

On every pull request, the action records both revisions, writes the report to the job summary, and posts it as a comment.
When the author pushes new commits, it updates its comment.
See [docs/github-action.md](https://github.com/smythi93/BeTell/blob/main/docs/github-action.md) for inputs, outputs, and pull requests from forks.

## What BeTell records

For every test, BeTell records five kinds of behavior of your project's own code.

| Feature | What it captures |
|---|---|
| Control flow | executed lines and the transitions between them |
| Calls | which project function calls which |
| Values | arguments and return values, as type and short representation |
| Exceptions | exceptions that a function raises or handles |
| Outcome | whether the test passes, fails, errors, or is skipped |

Each revision runs twice, and BeTell ignores everything that differs between runs of the same code, such as time stamps and random numbers.
It aligns the lines of edited files, so code that only moves does not show up as a change.
Every change is attributed to a function, which is either *edited* by the pull request or not, and the change is *silent* if it occurs in a test whose outcome stays the same.
[docs/how-it-works.md](https://github.com/smythi93/BeTell/blob/main/docs/how-it-works.md) explains the details, and [docs/report.md](https://github.com/smythi93/BeTell/blob/main/docs/report.md) explains how to read the report.

## Requirements

- The `betell` command needs Python 3.9 or later and git.
- The recorder runs inside your test environment, supports Python 3.6 and later with pytest 6 or later, and uses only the standard library.
- On Python 3.12 and later, BeTell records through `sys.monitoring`, which keeps the overhead low. A median recording of real commits took 1.3 times as long as a plain test run.
- Older interpreters fall back to `sys.settrace`, which is slower. In our evaluation, the median overhead was 7.2 times a plain test run, or 4 times with `--no-values`.

## Documentation

- [Usage](https://github.com/smythi93/BeTell/blob/main/docs/usage.md): commands, options, the demo, and the pytest plugin
- [GitHub Action](https://github.com/smythi93/BeTell/blob/main/docs/github-action.md): workflow setup, inputs, and outputs
- [Reading the report](https://github.com/smythi93/BeTell/blob/main/docs/report.md): sections, change kinds, and the JSON format
- [How it works](https://github.com/smythi93/BeTell/blob/main/docs/how-it-works.md): recording, noise filtering, alignment, and limitations
- [Evaluation](https://github.com/smythi93/BeTell/blob/main/docs/evaluation.md): reproducing the results on SWE-bench Verified and real commits

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e . pytest
python -m pytest tests
```

The tests run every demo scenario and the nondeterminism filter with both recorder backends, and check that BeTell reports exactly the expected changes.

## License

BeTell is licensed under the [Apache License 2.0](https://github.com/smythi93/BeTell/blob/main/LICENSE).
