## Behavioral diff `base` → `gold`

Compared 256 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 112 unstable observation(s) were dropped after repeated runs.

**1 function behave differently.** Not edited by this pull request: 0. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 1.

### Test outcomes that changed

- `lib/matplotlib/tests/test_colors.py::test_index_dtype[uint8]` failed → passed

### Silent changes in edited code

- `lib/matplotlib/colors.py::Colormap.__call__` in 9 test(s), e.g. `lib/matplotlib/tests/test_colors.py::test_BoundaryNorm` and 8 more: control flow changed (2 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (1 function(s))</summary>

- `lib/matplotlib/colors.py::Colormap.__call__` in 1 test(s), e.g. `lib/matplotlib/tests/test_colors.py::test_index_dtype[uint8]`: no longer raised: DeprecationWarning; arguments changed (new `(X=int:0, alpha=NoneType:None, bytes=bool:False)`); control flow changed (11 newly taken line transitions).

</details>

