## Behavioral diff `67fcf64^` → `67fcf64`

Compared 767 test(s) on both revisions. 1 test(s) exist only in head and 0 only in base. 5 unstable observation(s) were dropped after repeated runs.

**1 function behave differently.** Not edited by this pull request: 0. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 0.

### Silent changes in edited code

- `more_itertools/more.py::bucket.__init__` in 6 test(s), e.g. `test_more.py::BucketTests::test_basic` and 5 more: newly called from `bucket.__contains__`, `bucket.__getitem__`, `bucket._get_values`.

