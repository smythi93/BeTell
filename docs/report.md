# Reading the report

BeTell writes a Markdown report that GitHub renders in pull request comments and job summaries.
This page explains its parts, the kinds of changes it lists, and the JSON output.

## Structure

```markdown
## Behavioral diff `base` → `head`

Compared 4 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base.
0 unstable observation(s) were dropped after repeated runs.

**2 functions behave differently.** Not edited by this pull request: 1.
Different in tests whose outcome stays the same: 2. Test outcomes that changed: 0.

### Test outcomes that changed
### Silent changes in code this pull request does not edit
### Silent changes in edited code
<details><summary>Behavior behind the changed test outcomes</summary> ... </details>
```

The header states which tests BeTell compared.
Only tests that exist on both revisions are compared, and the counts of added and removed tests show what the comparison leaves out.
The number of unstable observations shows how much nondeterminism the repeated runs removed.

The summary line counts the functions that behave differently.
A function counts once, however many of its features change.

When nothing changed, the report says so in one line.

## Sections

The sections are ordered by how hard their changes are to notice otherwise.

1. **Test outcomes that changed** lists every test that passes on one revision and fails, errors, or is skipped on the other. A failing test was the only signal a reviewer had before, so it comes first.
2. **Silent changes in code this pull request does not edit** lists functions that the diff does not touch, which behave differently in at least one test whose outcome stays the same. Neither the diff nor the test results point at these changes. Read this section first when you review.
3. **Silent changes in edited code** lists the same for functions that the diff edits. These changes are expected, but their effect can still surprise, such as a changed return value.
4. **Behavior behind the changed test outcomes** is folded. It lists changes that occur only in tests whose outcome changed. These changes usually explain the changed outcome, for example, the error path that a failing assertion triggers.

Within a section, functions with changed exceptions come first, then return values, arguments, calls, and control flow.
Functions that change in more tests come earlier.
Each section shows at most 25 functions.

## Entries

Each entry names one function, the tests in which it behaves differently, and the changes.

```markdown
- `shop/api.py::safe_parse` in 1 test(s), e.g. `tests/test_shop.py::test_parse`:
  no longer handled: ValueError; control flow changed (2 no longer taken line transitions).
```

Functions are named `path::qualified.name`, relative to the repository root.

| Text | Meaning |
|---|---|
| `now raised: E` / `no longer raised: E` | the function lets exception `E` escape on one revision only |
| `now handled: E` / `no longer handled: E` | the function catches exception `E` on one revision only |
| `return values changed (new ..., gone ...)` | values the function returns only on head (new) or only on base (gone) |
| `arguments changed (new ..., gone ...)` | argument combinations the function receives only on head or only on base |
| `newly called from f` / `no longer called from f` | the call edge from `f` exists on one revision only |
| `control flow changed (n newly taken, m no longer taken line transitions)` | transitions between lines that only one revision executes |

Values appear as `type:representation`, such as `int:120` or `str:'apple'`.
Long representations are shortened, and memory addresses, temporary directories, and paths into the checkout are replaced by placeholders, so that they do not differ between runs.

## What is not reported

- Transitions through lines that the diff edits. The diff already shows these lines.
- Observations that differ between the runs of the same revision. They are counted as unstable.
- Value changes in functions that reached the cap of recorded values per test. BeTell cannot compare them reliably, and the JSON output counts them as `saturated_skipped`.
- Code in test files, unless the recording used `--betell-include-tests`.

## JSON output

`betell run --json FILE` and `betell compare --json FILE` write the full comparison.

```json
{
  "base": "base",
  "head": "head",
  "compared_tests": 4,
  "added_tests": [],
  "removed_tests": [],
  "unstable_dropped": 0,
  "saturated_skipped": 0,
  "touched_functions": ["shop/util.py::discount"],
  "seconds": {"base": [0.07, 0.06], "head": [0.06, 0.06]},
  "changes": [
    {
      "kind": "return",
      "location": "shop/api.py::checkout",
      "detail": "values changed",
      "outside_diff": true,
      "silent": true,
      "tests": ["tests/test_shop.py::test_checkout_bulk"],
      "before": ["float:108.0"],
      "after": ["int:120"]
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `kind` | `outcome`, `exception`, `return`, `argument`, `call`, or `branch` (control flow) |
| `location` | the function, or the test for outcome changes |
| `outside_diff` | the diff does not edit this function |
| `silent` | the change occurs in at least one test whose outcome stays the same |
| `tests` | tests in which the change occurs |
| `before`, `after` | observations only on base and only on head |
