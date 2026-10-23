## Behavioral diff `base` → `gold`

Compared 10 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 0 unstable observation(s) were dropped after repeated runs.

**171 functions behave differently.** Not edited by this pull request: 168. Different in tests whose outcome stays the same: 3. Test outcomes that changed: 1.

### Test outcomes that changed

- `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows` failed → passed

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `astropy/io/ascii/core.py::BaseReader.read` in 9 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_read_normal` and 8 more: newly called from `RST.read`; no longer called from `a test`.
- `astropy/io/ascii/fixedwidth.py::FixedWidth.__init__` in 10 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_read_normal` and 9 more: control flow changed (11 newly taken, 1 no longer taken line transitions).

### Silent changes in edited code

- `astropy/io/ascii/rst.py::RST.read` in 8 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_read_normal` and 7 more: newly called from `a test`.

<details><summary>Behavior behind the changed test outcomes (171 function(s))</summary>

- `astropy/io/ascii/connect.py::io_read` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer raised: TypeError.
- `astropy/io/ascii/core.py::BaseData._replace_vals` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: StopIteration; now raised: StopIteration; newly called from `BaseData._replace_vals`, `BaseData.str_vals`; control flow changed (12 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseData._set_fill_values` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: StopIteration; now handled: TypeError; newly called from `BaseData._set_fill_values`, `BaseData.masks`, `BaseData.str_vals`; control flow changed (29 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseData._set_masks` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: StopIteration; now raised: StopIteration; newly called from `BaseData._set_masks`, `BaseData.masks`; control flow changed (12 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseData.process_lines` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now raised: StopIteration; newly called from `BaseData.get_data_lines`, `BaseData.process_lines`; control flow changed (9 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseInputter.get_lines` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: TypeError; newly called from `BaseReader.read`; control flow changed (12 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseOutputter._validate_and_copy` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: AssertionError; newly called from `BaseOutputter._convert_vals`; control flow changed (15 newly taken line transitions).
- `astropy/io/ascii/core.py::BaseReader.read` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: StopIteration; now handled: TypeError; control flow changed (29 newly taken line transitions).
- `astropy/io/ascii/core.py::_check_multidim_table` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now raised: StopIteration; newly called from `BaseReader._check_multidim_table`, `_check_multidim_table`; control flow changed (7 newly taken line transitions).
- `astropy/io/ascii/core.py::_get_reader` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer raised: TypeError; control flow changed (24 newly taken, 1 no longer taken line transitions).
- `astropy/io/ascii/ui.py::get_reader` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer raised: TypeError; control flow changed (2 newly taken, 1 no longer taken line transitions).
- `astropy/io/ascii/ui.py::read` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer raised: TypeError; control flow changed (10 newly taken, 1 no longer taken line transitions).
- `astropy/io/registry/core.py::UnifiedInputRegistry.read` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer handled: TypeError; return values changed (new `QTable:<QTable length=2> wave respo...---- 350.0 1.0 1 950.0 2.0 2`, gone `NoneType:None`); control flow changed (6 newly taken, 2 no longer taken line transitions).
- `astropy/table/column.py::Column.__setattr__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: AttributeError; newly called from `BaseColumn.__array_finalize__`, `BaseColumn.__new__`, `BaseColumn._copy_attrs` (+9 more); control flow changed (11 newly taken line transitions).
- `astropy/table/connect.py::TableRead.__call__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: no longer raised: TypeError; control flow changed (5 newly taken, 1 no longer taken line transitions).
- `astropy/table/table.py::Table._convert_data_to_col` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: IndexError; newly called from `Table._init_from_list`; control flow changed (36 newly taken line transitions).
- `astropy/table/table.py::Table._init_from_cols` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now raised: StopIteration; newly called from `Table._init_from_cols`, `Table._init_from_list`; control flow changed (14 newly taken line transitions).
- `astropy/units/quantity.py::Quantity.__getattr__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now raised: AttributeError; newly called from `BaseData._replace_vals`, `BaseData._set_fill_values`; control flow changed (5 newly taken line transitions).
- `astropy/units/quantity.py::Quantity.__getitem__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now handled: IndexError; newly called from `Table._convert_data_to_col`, `Table._new_from_slice`, `TableFormatter._pformat_col_iter.format_col_str`; control flow changed (12 newly taken line transitions).
- `astropy/utils/data_info.py::BaseColumnInfo.iter_str_vals` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: now raised: StopIteration; newly called from `BaseData.str_vals`; control flow changed (6 newly taken line transitions).
- `astropy/config/configuration.py::ConfigItem.__call__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: return values changed (new `str:'col{0}'`).
- `astropy/config/configuration.py::ConfigItem.__get__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: return values changed (new `str:'col{0}'`); newly called from `_auto_names`.
- `astropy/config/configuration.py::ConfigItem._validate_val` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: return values changed (new `str:'col{0}'`); arguments changed (new `(val=str:'col{0}')`).
- `astropy/extern/configobj/validate.py::Validator._check_value` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: return values changed (new `str:'col{0}'`); arguments changed (new `(value=str:'col{0}', fun_name=str:'string', fun_args=list:[], fun_kwargs=dict:{})`).
- `astropy/extern/configobj/validate.py::Validator._parse_with_caching` in 1 test(s), e.g. `astropy/io/ascii/tests/test_rst.py::test_rst_with_header_rows`: return values changed (new `tuple:('string', [], {}, None)`); arguments changed (new `(check=str:'string')`).
- ... and 146 more function(s)

</details>

