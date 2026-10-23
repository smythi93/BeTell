## Behavioral diff `05f6fd0^` → `05f6fd0`

Compared 2089 test(s) on both revisions. 3 test(s) exist only in head and 0 only in base. 440 unstable observation(s) were dropped after repeated runs.

**3 functions behave differently.** Not edited by this pull request: 1. Different in tests whose outcome stays the same: 3. Test outcomes that changed: 0.

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `src/click/core.py::Argument.make_metavar` in 35 test(s), e.g. `test_arguments.py::test_argument_help` and 34 more: newly called from `Argument.get_help_record`; no longer called from `Command.format_arguments`, `get_help_record`.

### Silent changes in edited code

- `src/click/core.py::Argument.get_help_record` in 35 test(s), e.g. `test_arguments.py::test_argument_help` and 34 more: newly called from `Command.format_arguments`, `Command.format_options`, `a test`.
- `src/click/core.py::Command.format_arguments` in 142 test(s), e.g. `test_arguments.py::test_argument_help` and 141 more: control flow changed (2 no longer taken line transitions).

