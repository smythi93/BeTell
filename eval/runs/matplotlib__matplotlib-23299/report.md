## Behavioral diff `base` → `gold`

Compared 208 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 54 unstable observation(s) were dropped after repeated runs.

**8 functions behave differently.** Not edited by this pull request: 8. Different in tests whose outcome stays the same: 0. Test outcomes that changed: 1.

### Test outcomes that changed

- `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext` failed → passed

<details><summary>Behavior behind the changed test outcomes (8 function(s))</summary>

- `lib/matplotlib/__init__.py::RcParams._get_backend_or_none` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: return values changed (new `str:'module://aardvark'`).
- `lib/matplotlib/__init__.py::RcParams.__setitem__` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`.
- `lib/matplotlib/cbook/__init__.py::_backend_module_name` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`; control flow changed (4 newly taken line transitions).
- `lib/matplotlib/pyplot.py::_get_required_interactive_framework` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`; control flow changed (3 newly taken line transitions).
- `lib/matplotlib/pyplot.py::close` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`.
- `lib/matplotlib/pyplot.py::install_repl_displayhook` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`; control flow changed (6 newly taken line transitions).
- `lib/matplotlib/pyplot.py::switch_backend` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: newly called from `switch_backend`, `use`; control flow changed (28 newly taken line transitions).
- `lib/matplotlib/__init__.py::use` in 1 test(s), e.g. `lib/matplotlib/tests/test_rcparams.py::test_no_backend_reset_rccontext`: control flow changed (5 newly taken line transitions).

</details>

