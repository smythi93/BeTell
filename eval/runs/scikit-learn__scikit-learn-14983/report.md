## Behavioral diff `base` → `gold`

Compared 107 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 200 unstable observation(s) were dropped after repeated runs.

**3 functions behave differently.** Not edited by this pull request: 1. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 2.

### Test outcomes that changed

- `sklearn/model_selection/tests/test_split.py::test_repeated_cv_repr[RepeatedKFold]` failed → passed
- `sklearn/model_selection/tests/test_split.py::test_repeated_cv_repr[RepeatedStratifiedKFold]` failed → passed

### Silent changes in edited code

- `sklearn/model_selection/_split.py::_build_repr` in 4 test(s), e.g. `sklearn/model_selection/tests/test_split.py::test_build_repr` and 3 more: control flow changed (1 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (3 function(s))</summary>

- `sklearn/base.py::_pprint` in 2 test(s), e.g. `sklearn/model_selection/tests/test_split.py::test_repeated_cv_repr[RepeatedKFold]` and 1 more: newly called from `_build_repr`, `_pprint`; control flow changed (25 newly taken line transitions).
- `sklearn/model_selection/_split.py::_RepeatedSplits.__repr__` in 2 test(s), e.g. `sklearn/model_selection/tests/test_split.py::test_repeated_cv_repr[RepeatedKFold]` and 1 more: newly called from `a test`.
- `sklearn/model_selection/_split.py::_build_repr` in 2 test(s), e.g. `sklearn/model_selection/tests/test_split.py::test_repeated_cv_repr[RepeatedKFold]` and 1 more: newly called from `_RepeatedSplits.__repr__`, `_build_repr`; control flow changed (21 newly taken line transitions).

</details>

