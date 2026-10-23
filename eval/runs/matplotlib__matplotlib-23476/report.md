## Behavioral diff `base` → `gold`

Compared 112 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 940 unstable observation(s) were dropped after repeated runs.

**5 functions behave differently.** Not edited by this pull request: 4. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 1.

### Test outcomes that changed

- `lib/matplotlib/tests/test_figure.py::test_unpickle_with_device_pixel_ratio` failed → passed

### Silent changes in edited code

- `lib/matplotlib/figure.py::Figure.__getstate__` in 2 test(s), e.g. `lib/matplotlib/tests/test_figure.py::test_deepcopy` and 1 more: control flow changed (1 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (4 function(s))</summary>

- `lib/matplotlib/figure.py::Figure.__repr__` in 1 test(s), e.g. `lib/matplotlib/tests/test_figure.py::test_unpickle_with_device_pixel_ratio`: no longer called from `a test`; control flow changed (6 no longer taken line transitions).
- `lib/matplotlib/figure.py::Figure.axes` in 1 test(s), e.g. `lib/matplotlib/tests/test_figure.py::test_unpickle_with_device_pixel_ratio`: no longer called from `Figure.__repr__`.
- `lib/matplotlib/transforms.py::BboxBase.size` in 1 test(s), e.g. `lib/matplotlib/tests/test_figure.py::test_unpickle_with_device_pixel_ratio`: no longer called from `Figure.__repr__`; control flow changed (3 no longer taken line transitions).
- `lib/matplotlib/transforms.py::TransformedBbox.get_points` in 1 test(s), e.g. `lib/matplotlib/tests/test_figure.py::test_unpickle_with_device_pixel_ratio`: no longer called from `BboxBase.size`; control flow changed (3 no longer taken line transitions).

</details>

