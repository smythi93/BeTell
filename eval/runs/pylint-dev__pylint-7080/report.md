## Behavioral diff `base` → `gold`

Compared 125 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 2 unstable observation(s) were dropped after repeated runs.

**158 functions behave differently.** Not edited by this pull request: 157. Different in tests whose outcome stays the same: 2. Test outcomes that changed: 1.

### Test outcomes that changed

- `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir` failed → passed

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `pylint/lint/expand_modules.py::_is_in_ignore_list_re` in 3 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir` and 2 more: arguments changed (new `(element=str:'<root>/tests/regrtest_data/regression_missing_init_3564/subdirectory', ignore_list_re=list:[])`, `(element=str:'ignored_subdirectory', ignore_list_re=list:[re.compile('^ignored_subdire...*|^ignored_subdirectory/.*')])` (+10 more), gone `(element=str:'', ignore_list_re=tuple:(re.compile('^\\.#'),))`, `(element=str:'./ignored_subdirectory', ignore_list_re=list:[re.compile('^ignored_subdire...*|^ignored_subdirectory/.*')])` (+10 more)).

### Silent changes in edited code

- `pylint/lint/expand_modules.py::_is_ignored_file` in 90 test(s), e.g. `tests/test_self.py::TestCallbackOptions::test_enable_all_extensions` and 89 more: control flow changed (1 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (158 function(s))</summary>

- `pylint/checkers/deprecated.py::DeprecatedMixin.visit_import` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer raised: StopIteration; no longer called from `ASTWalker.walk`, `DeprecatedMixin.visit_import`; control flow changed (6 no longer taken line transitions).
- `pylint/checkers/format.py::FormatChecker.visit_default` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer handled: AttributeError; arguments changed (gone `(node=Import:<Import l.1 at 0x?>)`, `(node=Module:<Module.failing l.0 at 0x?>)`); control flow changed (23 no longer taken line transitions).
- `pylint/checkers/utils.py::in_type_checking_block` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer handled: StopIteration; no longer called from `VariablesChecker._check_imports`; control flow changed (6 no longer taken line transitions).
- `pylint/lint/message_state_handler.py::_MessageStateHandler._is_one_message_enabled` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer handled: KeyError; no longer called from `stripped_lines`; control flow changed (7 no longer taken line transitions).
- `pylint/lint/pylinter.py::PyLinter._add_one_message` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer handled: KeyError; no longer called from `PyLinter.add_message`; control flow changed (52 no longer taken line transitions).
- `pylint/utils/utils.py::get_module_and_frameid` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: no longer handled: AttributeError; no longer called from `PyLinter._add_one_message`; control flow changed (12 no longer taken line transitions).
- `pylint/checkers/format.py::FormatChecker.specific_splitlines` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `list:['import re\n']`); arguments changed (gone `(lines=str:'import re\n')`); control flow changed (4 no longer taken line transitions).
- `pylint/checkers/format.py::TokenWrapper.line` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `str:'import re\n'`); arguments changed (gone `(idx=int:4)`).
- `pylint/checkers/format.py::TokenWrapper.start_line` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `int:2`); arguments changed (gone `(idx=int:4)`).
- `pylint/checkers/format.py::TokenWrapper.type` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `int:1`); arguments changed (gone `(idx=int:4)`).
- `pylint/checkers/imports.py::ImportsChecker._check_imports_order` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `tuple:([(<Import l.1 at 0x?>, 're')], [], [])`); arguments changed (gone `(_module_node=Module:<Module.failing l.0 at 0x?>)`); control flow changed (18 no longer taken line transitions).
- `pylint/checkers/similar.py::LineSet.__len__` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `int:1`).
- `pylint/checkers/similar.py::SimilarChecker.close` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `int:1`).
- `pylint/checkers/similar.py::stripped_lines` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `dict:{1: True}`, `tuple:(1, True)`); arguments changed (gone `(lines=list:['import re\n'], ignore_comments=bool:True, ignore_docstrings=bool:True, ignore_imports=bool:True, ignore_signatures=bool:True, line_enabled_callback=method:<_MessageStateHandler._is_one_message_enabled>)`); no longer called from `stripped_lines`; control flow changed (30 no longer taken line transitions).
- `pylint/checkers/unicode.py::_fix_utf16_32_line_stream` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `bytes:b'import re\n'`).
- `pylint/checkers/utils.py::get_node_last_lineno` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `int:1`); arguments changed (gone `(node=Import:<Import l.1 at 0x?>)`, `(node=Module:<Module.failing l.0 at 0x?>)`); no longer called from `get_node_last_lineno`; control flow changed (2 no longer taken line transitions).
- `pylint/checkers/variables.py::NamesConsumer.to_consume` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `dict:{'re': [<Import l.1 at 0x?>]}`).
- `pylint/checkers/variables.py::_fix_dot_imports` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `list:[('re', <Import l.1 at 0x?>)]`); arguments changed (gone `(not_consumed=dict:{'re': [<Import l.1 at 0x?>]})`); no longer called from `_fix_dot_imports`; control flow changed (28 no longer taken line transitions).
- `pylint/lint/caching.py::_get_pdata_path` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (new `PosixPath:PosixPath('/root/.cache/pylint/package_1.stats')`, `str:'package'`, gone `PosixPath:PosixPath('/root/.cache/pylint/failing_1.stats')`, `str:'failing'`); arguments changed (new `(base_name=PosixPath:PosixPath('package'), recurs=int:1, pylint_home=PosixPath:PosixPath('/root/.cache/pylint'))`, gone `(base_name=PosixPath:PosixPath('failing'), recurs=int:1, pylint_home=PosixPath:PosixPath('/root/.cache/pylint'))`).
- `pylint/lint/expand_modules.py::_is_ignored_file` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (new `bool:True`).
- `pylint/lint/expand_modules.py::_is_in_ignore_list_re` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (new `bool:True`).
- `pylint/lint/pylinter.py::PyLinter._iterate_file_descrs` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `FileItem:FileItem(name='failing', fil...ling.py', modpath='failing')`).
- `pylint/lint/pylinter.py::PyLinter._report_evaluation` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (new `NoneType:None`, gone `int:0`); control flow changed (2 newly taken, 19 no longer taken line transitions).
- `pylint/lint/pylinter.py::PyLinter.any_fail_on_issues` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (gone `bool:False`); control flow changed (1 no longer taken line transitions).
- `pylint/lint/pylinter.py::PyLinter.generate_reports` in 1 test(s), e.g. `tests/test_self.py::TestRunTC::test_ignore_path_recursive_current_dir`: return values changed (new `NoneType:None`, gone `int:0`).
- ... and 133 more function(s)

</details>

