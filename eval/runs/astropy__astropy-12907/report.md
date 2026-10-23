## Behavioral diff `base` → `gold`

Compared 15 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 0 unstable observation(s) were dropped after repeated runs.

**16 functions behave differently.** Not edited by this pull request: 15. Different in tests whose outcome stays the same: 0. Test outcomes that changed: 2.

### Test outcomes that changed

- `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` failed → passed
- `astropy/modeling/tests/test_separable.py::test_separable[compound_model9-result9]` failed → passed

<details><summary>Behavior behind the changed test outcomes (16 function(s))</summary>

- `astropy/modeling/separable.py::_cstack` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: return values changed (new `ndarray:array([[1., 1., 0., 0., 0.],... 0.], [0., 0., 0., 0., 1.]])`, `ndarray:array([[1., 1., 0., 0.], [1.... 1., 0.], [0., 0., 0., 1.]])`, gone `ndarray:array([[1., 1., 0., 0., 0.],... 1.], [0., 0., 0., 1., 1.]])`, `ndarray:array([[1., 1., 0., 0.], [1.... 1., 1.], [0., 0., 1., 1.]])`).
- `astropy/modeling/separable.py::_separable` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: return values changed (new `ndarray:array([[1., 1., 0., 0., 0.],... 0.], [0., 0., 0., 0., 1.]])`, `ndarray:array([[1., 1., 0., 0.], [1.... 1., 0.], [0., 0., 0., 1.]])`, gone `ndarray:array([[1., 1., 0., 0., 0.],... 1.], [0., 0., 0., 1., 1.]])`, `ndarray:array([[1., 1., 0., 0.], [1.... 1., 1.], [0., 0., 1., 1.]])`); newly called from `separability_matrix`.
- `astropy/modeling/separable.py::is_separable` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: return values changed (new `ndarray:array([False, False, True, True, True])`, `ndarray:array([False, False, True, True])`, gone `ndarray:array([False, False, False, False])`, `ndarray:array([False, False, True, False, False])`).
- `astropy/modeling/core.py::CompoundModel.n_inputs` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: newly called from `separability_matrix`.
- `astropy/modeling/core.py::CompoundModel.param_names` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Model._format_repr`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/core.py::Model.__len__` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Model._format_repr`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/core.py::Model.__repr__` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `a test`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/core.py::Model._format_repr` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Model.__repr__`, `Model._format_repr`; control flow changed (15 no longer taken line transitions).
- `astropy/modeling/core.py::Model.name` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Model._format_repr`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/parameters.py::Parameter.internal_unit` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Parameter.value`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/parameters.py::Parameter.unit` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `param_repr_oneline`; control flow changed (2 no longer taken line transitions).
- `astropy/modeling/parameters.py::Parameter.value` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `param_repr_oneline`; control flow changed (7 no longer taken line transitions).
- `astropy/modeling/parameters.py::param_repr_oneline` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Model._format_repr`; control flow changed (4 no longer taken line transitions).
- `astropy/modeling/separable.py::separability_matrix` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: newly called from `a test`; control flow changed (5 newly taken line transitions).
- `astropy/modeling/utils.py::_to_orig_unit` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `Parameter.value`; control flow changed (3 no longer taken line transitions).
- `astropy/modeling/utils.py::array_repr_oneline` in 2 test(s), e.g. `astropy/modeling/tests/test_separable.py::test_separable[compound_model6-result6]` and 1 more: no longer called from `array_repr_oneline`, `param_repr_oneline`; control flow changed (5 no longer taken line transitions).

</details>

