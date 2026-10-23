## Behavioral diff `base` → `gold`

Compared 180 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 4 unstable observation(s) were dropped after repeated runs.

**9 functions behave differently.** Not edited by this pull request: 8. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 1.

### Test outcomes that changed

- `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic` failed → passed

### Silent changes in edited code

- `astropy/nddata/mixins/ndarithmetic.py::NDArithmeticMixin._arithmetic_mask` in 2 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_arithmetics_data_masks[True-None]` and 1 more: control flow changed (1 newly taken, 1 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (9 function(s))</summary>

- `astropy/nddata/mixins/ndarithmetic.py::NDArithmeticMixin._arithmetic` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer raised: TypeError; return values changed (new `tuple:(array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), {'mask': array([[ 0, 1, 64], [ 8, 0, 1], [ 2, 1, 0]]),...`, `tuple:(array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), {'mask': array([[64, 1, 64], [10, 1, 1], [10, 1, 2]]),...` (+1 more)); control flow changed (1 no longer taken line transitions).
- `astropy/nddata/mixins/ndarithmetic.py::NDArithmeticMixin._arithmetic_mask` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer raised: TypeError; return values changed (new `ndarray:array([[ 0, 1, 64], [ 8, 0, 1], [ 2, 1, 0]])`, `ndarray:array([[64, 1, 64], [10, 1, 1], [10, 1, 2]])`).
- `astropy/nddata/mixins/ndarithmetic.py::NDArithmeticMixin._prepare_then_do_arithmetic` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer raised: TypeError; control flow changed (1 no longer taken line transitions).
- `astropy/nddata/mixins/ndarithmetic.py::NDArithmeticMixin.multiply` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer raised: TypeError.
- `astropy/nddata/nddata.py::NDData.__init__` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: arguments changed (new `(data=ndarray:array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), uncertainty=NoneType:None, mask=ndarray:array([[64, 1, 0], [ 2, 1, 0], [ 8, 0, 2]]), wcs=NoneType:None, meta=NoneType:None, unit=NoneType:None, copy=bool:False, psf=NoneType:None)`, `(data=ndarray:array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), uncertainty=NoneType:None, mask=ndarray:array([[64, 1, 64], [10, 1, 1], [10, 1, 2]]), wcs=NoneType:None, meta=NoneType:None, unit=NoneType:None, copy=bool:False, psf=NoneType:None)` (+1 more)).
- `astropy/nddata/nddata.py::NDData.mask` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: arguments changed (new `(value=ndarray:array([[64, 1, 0], [ 2, 1, 0], [ 8, 0, 2]]))`, `(value=ndarray:array([[64, 1, 64], [10, 1, 1], [10, 1, 2]]))`).
- `astropy/nddata/nddata.py::NDData.__repr__` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer called from `a test`; control flow changed (5 no longer taken line transitions).
- `astropy/nddata/nddata.py::NDData.data` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer called from `NDData.__repr__`.
- `astropy/nddata/nddata.py::NDData.unit` in 1 test(s), e.g. `astropy/nddata/mixins/tests/test_ndarithmetic.py::test_nddata_bitmask_arithmetic`: no longer called from `NDData.__repr__`.

</details>

