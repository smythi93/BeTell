## Behavioral diff `base` → `gold`

Compared 30 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 56 unstable observation(s) were dropped after repeated runs.

**35 functions behave differently.** Not edited by this pull request: 34. Different in tests whose outcome stays the same: 3. Test outcomes that changed: 1.

### Test outcomes that changed

- `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values` failed → passed

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `sklearn/linear_model/ridge.py::RidgeClassifierCV.fit` in 2 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_class_weight_vs_sample_weight` and 1 more: return values changed (new `RidgeClassifierCV:RidgeClassifierCV(alphas=(0....None, store_cv_values=False)`, `RidgeClassifierCV:RidgeClassifierCV(alphas=[0....None, store_cv_values=False)`, gone `RidgeClassifierCV:RidgeClassifierCV(alphas=(0....rmalize=False, scoring=None)`, `RidgeClassifierCV:RidgeClassifierCV(alphas=[0....rmalize=False, scoring=None)`).
- `sklearn/linear_model/ridge.py::_BaseRidgeCV.fit` in 2 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_class_weight_vs_sample_weight` and 1 more: return values changed (new `RidgeClassifierCV:RidgeClassifierCV(alphas=(0....None, store_cv_values=False)`, `RidgeClassifierCV:RidgeClassifierCV(alphas=[0....None, store_cv_values=False)`, gone `RidgeClassifierCV:RidgeClassifierCV(alphas=(0....rmalize=False, scoring=None)`, `RidgeClassifierCV:RidgeClassifierCV(alphas=[0....rmalize=False, scoring=None)`).

### Silent changes in edited code

- `sklearn/linear_model/ridge.py::RidgeClassifierCV.__init__` in 2 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_class_weight_vs_sample_weight` and 1 more: arguments changed (new `(alphas=list:[0.01, 0.1, 1, 10], fit_intercept=bool:True, normalize=bool:False, scoring=NoneType:None, cv=NoneType:None, class_weight=dict:{1: 0.001}, store_cv_values=bool:False)`, `(alphas=list:[0.01, 0.1, 1], fit_intercept=bool:True, normalize=bool:False, scoring=NoneType:None, cv=NoneType:None, class_weight=NoneType:None, store_cv_values=bool:False)` (+3 more), gone `(alphas=list:[0.01, 0.1, 1, 10], fit_intercept=bool:True, normalize=bool:False, scoring=NoneType:None, cv=NoneType:None, class_weight=dict:{1: 0.001})`, `(alphas=list:[0.01, 0.1, 1], fit_intercept=bool:True, normalize=bool:False, scoring=NoneType:None, cv=NoneType:None, class_weight=NoneType:None)` (+3 more)).

<details><summary>Behavior behind the changed test outcomes (35 function(s))</summary>

- `sklearn/__init__.py::get_config` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_assert_all_finite`; control flow changed (2 newly taken line transitions).
- `sklearn/linear_model/base.py::LinearModel._set_intercept` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (4 newly taken line transitions).
- `sklearn/linear_model/base.py::_preprocess_data` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (14 newly taken line transitions).
- `sklearn/linear_model/ridge.py::RidgeClassifierCV.__init__` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `a test`; control flow changed (3 newly taken line transitions).
- `sklearn/linear_model/ridge.py::RidgeClassifierCV.fit` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `a test`; control flow changed (11 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_BaseRidgeCV.__init__` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `RidgeClassifierCV.__init__`; control flow changed (8 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_BaseRidgeCV.fit` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `RidgeClassifierCV.fit`; control flow changed (15 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV.__init__` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_BaseRidgeCV.fit`; control flow changed (8 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV._decomp_diag` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV._errors_and_values_svd_helper`; control flow changed (2 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV._diag_dot` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV._errors_and_values_svd_helper`; control flow changed (4 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV._errors_and_values_svd_helper` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV._errors_svd`; control flow changed (9 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV._errors_svd` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (3 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV._pre_compute_svd` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (8 newly taken line transitions).
- `sklearn/linear_model/ridge.py::_RidgeGCV.fit` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_BaseRidgeCV.fit`; control flow changed (43 newly taken line transitions).
- `sklearn/metrics/scorer.py::check_scoring` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (8 newly taken line transitions).
- `sklearn/preprocessing/label.py::LabelBinarizer.__init__` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `RidgeClassifierCV.fit`; control flow changed (6 newly taken line transitions).
- `sklearn/preprocessing/label.py::LabelBinarizer.fit` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `LabelBinarizer.fit_transform`; control flow changed (7 newly taken line transitions).
- `sklearn/preprocessing/label.py::LabelBinarizer.fit_transform` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `RidgeClassifierCV.fit`; control flow changed (2 newly taken line transitions).
- `sklearn/preprocessing/label.py::LabelBinarizer.transform` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `LabelBinarizer.fit_transform`; control flow changed (8 newly taken line transitions).
- `sklearn/preprocessing/label.py::label_binarize` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `LabelBinarizer.transform`; control flow changed (45 newly taken line transitions).
- `sklearn/utils/extmath.py::safe_sparse_dot` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `_RidgeGCV.fit`; control flow changed (3 newly taken line transitions).
- `sklearn/utils/multiclass.py::_unique_indicator` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `unique_labels`; control flow changed (2 newly taken line transitions).
- `sklearn/utils/multiclass.py::_unique_multiclass` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `unique_labels`; control flow changed (3 newly taken line transitions).
- `sklearn/utils/multiclass.py::is_multilabel` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `type_of_target`; control flow changed (9 newly taken line transitions).
- `sklearn/utils/multiclass.py::type_of_target` in 1 test(s), e.g. `sklearn/linear_model/tests/test_ridge.py::test_ridge_classifier_cv_store_cv_values`: newly called from `LabelBinarizer.fit`, `LabelBinarizer.transform`, `label_binarize` (+1 more); control flow changed (20 newly taken line transitions).
- ... and 10 more function(s)

</details>

