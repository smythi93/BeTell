# How BeTell works

BeTell follows four steps.
It records the behavior of both revisions under the existing tests, removes noise, separates edited from unedited code, and reports what changed.

```
pull request ──► run tests on base, twice ──┐
             └─► run tests on head, twice ──┴─► filter, align, classify ──► report and comment
```

## Recording behavior

BeTell runs pytest with its plugin on each revision.
The plugin follows only the code of the project, which lies under the project root and outside of test files.
For every test, it records five kinds of behavior.

- **Control flow** covers the executed lines and the transitions between consecutive lines in a function, including function entry and exit.
- **Calls** are the edges between functions of the project.
- **Values** are the arguments and return values of these functions. BeTell stores each value as its type and a short representation from `reprlib`, and keeps at most 24 calls per function and test.
- **Exceptions** record whether a function lets an exception escape or catches it.
- **Outcome** is whether the test passes, fails, errors, or is skipped.

Representations are normalized before BeTell stores them.
Memory addresses, the paths of temporary pytest directories, and paths into the checkout are replaced by placeholders.
Version strings that embed a commit hash, such as `3.7.0.dev1365+g3c8c98d28a`, are normalized as well, since they differ between any two revisions.

### Two recorder backends

On Python 3.12 and later, BeTell uses `sys.monitoring` ([PEP 669](https://peps.python.org/pep-0669/)).
It reports each line and each branch direction once per test and then disables the event, so loops cost almost nothing after their first iterations.
Branch events that Python 3.12 cannot disable per direction, and calls, are sampled for the first 64 hits per location and test.

Older interpreters use a `sys.settrace` hook that records every line transition.
It is slower but needs nothing beyond the standard library of Python 3.6.

## Removing noise

Some observations change between runs of the same code, such as time stamps, random numbers, thread timing, and the iteration order of sets.
Reporting them would bury the real changes, so BeTell records each revision twice by default.

- A value counts only if both runs of its revision agree on it.
- A line transition, call, or exception counts as new only if no base run made it, and as gone only if no head run made it.
- BeTell fixes `PYTHONHASHSEED`, which otherwise changes the iteration order of sets and dictionaries with string keys from run to run.

In our evaluation on SWE-bench Verified, two runs of the same base revision already differed in a median of 9 functions.

## Separating edited from unedited code

Edits shift line numbers.
BeTell therefore aligns the lines of each edited file between the revisions with a sequence alignment (`difflib`), and maps every base observation into head coordinates before the comparison.
Code that only moves thus does not appear as a change.

Lines that the diff edits are visible to the reviewer already, so BeTell does not report transitions through them.
Every other difference is attributed to the function in which it occurs.
A function counts as *edited* if the diff changes one of its lines, and as *unedited* otherwise.

A change is *silent* if it occurs in at least one test whose outcome stays the same.
Changes that occur only in tests whose outcome changed usually explain that outcome, so the report folds them away.

## Reporting

The report groups the changes by function and orders them by how hard they are to notice otherwise.
Changed test outcomes come first, then silent changes in unedited functions, then silent changes in edited functions, and finally the folded changes behind changed outcomes.
See [report.md](report.md) for details.

## Limitations

- BeTell sees only what the tests execute. A change on a path that no test runs stays invisible.
- State shared between tests, such as a cache, can attribute an effect to a later test. A test that now passes may fill a cache, so that a later test skips the cached computation.
- Values that embed line numbers of edited files, such as some error messages, appear as changes.
- The cap of 24 recorded calls per function and test, and the sampling on Python 3.12, can hide changes that appear only after many repetitions within one test.
- BeTell supports Python projects that use pytest.
