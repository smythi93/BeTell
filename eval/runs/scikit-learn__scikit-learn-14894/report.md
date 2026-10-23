## Behavioral diff `base` → `gold`

Compared 86 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 298 unstable observation(s) were dropped after repeated runs.

**12 functions behave differently.** Not edited by this pull request: 11. Different in tests whose outcome stays the same: 0. Test outcomes that changed: 1.

### Test outcomes that changed

- `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty` failed → passed

<details><summary>Behavior behind the changed test outcomes (12 function(s))</summary>

- `sklearn/svm/base.py::BaseLibSVM._sparse_fit` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer raised: ZeroDivisionError.
- `sklearn/svm/base.py::BaseLibSVM.fit` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer raised: ZeroDivisionError; control flow changed (6 newly taken, 1 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_EstimatorPrettyPrinter._format_params_or_dict_items` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer handled: StopIteration; no longer called from `_EstimatorPrettyPrinter._format_params`; control flow changed (43 no longer taken line transitions).
- `sklearn/_config.py::get_config` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `_EstimatorPrettyPrinter.__init__`.
- `sklearn/base.py::BaseEstimator.__repr__` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `a test`; control flow changed (10 no longer taken line transitions).
- `sklearn/base.py::BaseEstimator._get_param_names` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `BaseEstimator._get_param_names`, `BaseEstimator.get_params`; control flow changed (15 no longer taken line transitions).
- `sklearn/base.py::BaseEstimator.get_params` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `_EstimatorPrettyPrinter._pprint_estimator`, `_safe_repr`; control flow changed (9 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_EstimatorPrettyPrinter.__init__` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `BaseEstimator.__repr__`; control flow changed (7 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_EstimatorPrettyPrinter._format_params` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `_EstimatorPrettyPrinter._pprint_estimator`; control flow changed (3 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_EstimatorPrettyPrinter._pprint_estimator` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `BaseEstimator.__repr__`, `_EstimatorPrettyPrinter._pprint_estimator`; control flow changed (15 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_EstimatorPrettyPrinter.format` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `BaseEstimator.__repr__`, `_EstimatorPrettyPrinter._format_params_or_dict_items`; control flow changed (3 no longer taken line transitions).
- `sklearn/utils/_pprint.py::_safe_repr` in 1 test(s), e.g. `sklearn/svm/tests/test_svm.py::test_sparse_fit_support_vectors_empty`: no longer called from `_EstimatorPrettyPrinter.format`, `_safe_repr`; control flow changed (35 no longer taken line transitions).

</details>

