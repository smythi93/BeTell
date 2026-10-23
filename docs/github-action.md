# GitHub Action

The BeTell action runs on pull requests.
It records the base and the head revision, writes the report to the job summary, and posts it as a comment on the pull request.

## Setup

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

Three parts matter.

- `fetch-depth: 0` fetches the full history, so that BeTell can check out the base revision.
- The step before the action installs your project and pytest, just as for your normal test job. BeTell installs itself into the same environment.
- `pull-requests: write` allows the action to comment. Without it, set `comment: false` and read the report in the job summary.

Python 3.12 or later gives the lowest overhead, because BeTell then records through `sys.monitoring`.

## Inputs

| Input | Default | Meaning |
|---|---|---|
| `pytest-args` | empty | arguments for pytest, such as a test directory |
| `runs-base` | `2` | runs of the base revision, used to filter nondeterminism |
| `runs-head` | `2` | runs of the head revision, used to filter nondeterminism |
| `python` | `python` | interpreter that has your project and its test dependencies installed |
| `comment` | `true` | post the report as a comment on the pull request |

## Outputs

| Output | Meaning |
|---|---|
| `report` | path of the Markdown report, `betell-report.md` |

The action also writes the comparison as JSON to `betell-report.json` in the workspace.
To keep both files, upload them as an artifact.

```yaml
      - uses: smythi93/BeTell@v0.1.1
        id: betell
        with:
          pytest-args: tests
      - uses: actions/upload-artifact@v4
        with:
          name: betell-report
          path: |
            betell-report.md
            betell-report.json
```

## Comments

The action posts one comment per pull request.
When the author pushes new commits, it edits its most recent comment instead of adding another one.
The edit goes to the latest comment of the workflow's account, so another workflow that comments with the same token can have its comment replaced.
Set `comment: false` in such a setup and rely on the job summary.

GitHub limits comments to 65,536 characters.
BeTell truncates reports after 60,000 characters and notes the truncation.

## Pull requests from forks

For pull requests from forks, GitHub gives the workflow a read-only token, so the comment cannot be posted.
Restrict comments to pull requests from the same repository, and read the report of forks in the job summary.

```yaml
      - uses: smythi93/BeTell@v0.1.1
        with:
          pytest-args: tests
          comment: ${{ github.event.pull_request.head.repo.full_name == github.repository }}
```

## Cost

BeTell runs the selected tests four times, twice per revision.
With `sys.monitoring`, a recording took a median of 1.3 times as long as a plain test run in our evaluation.
For long test suites, select a subset with `pytest-args`, or set `runs-base` and `runs-head` to `1` if the suite is deterministic.
