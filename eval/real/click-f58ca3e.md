## Behavioral diff `f58ca3e^` → `f58ca3e`

Compared 2016 test(s) on both revisions. 9 test(s) exist only in head and 0 only in base. 440 unstable observation(s) were dropped after repeated runs.

**1 function behave differently.** Not edited by this pull request: 1. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 0.

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `src/click/testing.py::_NamedTextIOWrapper.close` in 1 test(s), e.g. `test_utils/test_style.py::test_styling[styles6-\x1b[35mx y\x1b[0m]`: no longer called from `a test`; control flow changed (1 no longer taken line transitions).

