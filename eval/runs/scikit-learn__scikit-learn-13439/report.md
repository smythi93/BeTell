## Behavioral diff `base` → `gold`

Compared 41 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 239 unstable observation(s) were dropped after repeated runs.

**4 functions behave differently.** Not edited by this pull request: 3. Different in tests whose outcome stays the same: 3. Test outcomes that changed: 1.

### Test outcomes that changed

- `sklearn/tests/test_pipeline.py::test_make_pipeline_memory` failed → passed

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `sklearn/externals/joblib/func_inspect.py::get_func_code` in 1 test(s), e.g. `sklearn/tests/test_pipeline.py::test_pipeline_memory`: return values changed (new `tuple:('def _fit_transform_one(tran... res * weight, transformer\n', '<root>/sklearn/pipeline.py', 660)`, gone `tuple:('def _fit_transform_one(tran... res * weight, transformer\n', '<root>/sklearn/pipeline.py', 654)`).
- `sklearn/externals/joblib/_store_backends.py::StoreBackendMixin.store_cached_func_code` in 1 test(s), e.g. `sklearn/tests/test_pipeline.py::test_pipeline_memory`: arguments changed (new `(path=list:['sklearn/pipeline/_fit_transform_one'], func_code=str:"# first line: 660\ndef _fit_transform_one(transformer, X, y, weight, **fit_params):\n if hasattr...)`, gone `(path=list:['sklearn/pipeline/_fit_transform_one'], func_code=str:"# first line: 654\ndef _fit_transform_one(transformer, X, y, weight, **fit_params):\n if hasattr...)`).
- `sklearn/externals/joblib/memory.py::MemorizedFunc._write_func_code` in 1 test(s), e.g. `sklearn/tests/test_pipeline.py::test_pipeline_memory`: arguments changed (new `(func_code=str:"def _fit_transform_one(transformer, X, y, weight, **fit_params):\n if hasattr(transformer, 'fit_..., first_line=int:660)`, gone `(func_code=str:"def _fit_transform_one(transformer, X, y, weight, **fit_params):\n if hasattr(transformer, 'fit_..., first_line=int:654)`).

<details><summary>Behavior behind the changed test outcomes (1 function(s))</summary>

- `sklearn/pipeline.py::Pipeline.__len__` in 1 test(s), e.g. `sklearn/tests/test_pipeline.py::test_make_pipeline_memory`: newly called from `a test`.

</details>

