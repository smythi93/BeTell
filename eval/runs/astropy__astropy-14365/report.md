## Behavioral diff `base` → `gold`

Compared 9 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 0 unstable observation(s) were dropped after repeated runs.

**73 functions behave differently.** Not edited by this pull request: 71. Different in tests whose outcome stays the same: 0. Test outcomes that changed: 1.

### Test outcomes that changed

- `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]` failed → passed

<details><summary>Behavior behind the changed test outcomes (73 function(s))</summary>

- `astropy/io/ascii/qdp.py::_get_tables_from_qdp_file` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: no longer raised: ValueError; now handled: ValueError; arguments changed (new `(qdp_file=str:'/tmp/<pytest-tmp>/test_roundtrip_True_0/test2.qdp', input_colnames=list:['MJD', 'Rate'], delimiter=NoneType:None)`); newly called from `_get_tables_from_qdp_file`; control flow changed (73 newly taken, 1 no longer taken line transitions).
- `astropy/io/ascii/qdp.py::_get_type_from_list_of_lines` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: no longer raised: ValueError; arguments changed (new `(lines=list:['!swift/xrt hardness ratio of trigger: xxxx, name: bubu x-2', '!columns are as labelled', 'READ ..., delimiter=NoneType:None)`); control flow changed (12 newly taken, 1 no longer taken line transitions).
- `astropy/io/ascii/qdp.py::_line_type` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: no longer raised: ValueError; control flow changed (2 newly taken, 2 no longer taken line transitions).
- `astropy/io/ascii/qdp.py::_read_table_qdp` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: no longer raised: ValueError; arguments changed (new `(qdp_file=str:'/tmp/<pytest-tmp>/test_roundtrip_True_0/test2.qdp', names=list:['MJD', 'Rate'], table_id=int:0, delimiter=NoneType:None)`); control flow changed (2 newly taken, 1 no longer taken line transitions).
- `astropy/io/ascii/qdp.py::_write_table_qdp` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: now handled: StopIteration; newly called from `_write_table_qdp`, `a test`; control flow changed (50 newly taken line transitions).
- `astropy/table/column.py::Column.__setattr__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: now handled: AttributeError; newly called from `BaseColumn.__array_finalize__`, `BaseColumn.__array_wrap__`, `BaseColumn.__new__` (+11 more); control flow changed (9 newly taken line transitions).
- `astropy/table/row.py::Row.__init__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: now raised: IndexError; newly called from `Table.__getitem__`; control flow changed (10 newly taken line transitions).
- `astropy/table/table.py::Table.__getitem__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: now raised: IndexError; newly called from `Table.itercols`, `_write_table_qdp`, `a test`; control flow changed (6 newly taken line transitions).
- `astropy/table/table.py::Table._init_from_cols` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: now raised: StopIteration; newly called from `Table._init_from_cols`, `Table._init_from_list`; control flow changed (14 newly taken line transitions).
- `astropy/io/ascii/qdp.py::_get_lines_from_file` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: return values changed (new `list:['!swift/xrt hardness ratio of trigger: xxxx, name: bubu x-2', '!columns are as labelled', 'READ ...`); arguments changed (new `(qdp_file=str:'/tmp/<pytest-tmp>/test_roundtrip_True_0/test2.qdp')`).
- `astropy/config/configuration.py::ConfigItem.__call__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `ConfigItem.__get__`; control flow changed (16 newly taken line transitions).
- `astropy/config/configuration.py::ConfigItem.__get__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `_auto_names`; control flow changed (3 newly taken line transitions).
- `astropy/config/configuration.py::ConfigItem._validate_val` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `ConfigItem.__call__`; control flow changed (2 newly taken line transitions).
- `astropy/config/configuration.py::get_config` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `ConfigItem.__call__`; control flow changed (12 newly taken line transitions).
- `astropy/extern/configobj/configobj.py::Section.__getitem__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `ConfigItem.__call__`, `get_config`; control flow changed (4 newly taken line transitions).
- `astropy/extern/configobj/validate.py::Validator._check_value` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `Validator.check`; control flow changed (4 newly taken line transitions).
- `astropy/extern/configobj/validate.py::Validator._parse_with_caching` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `Validator.check`; control flow changed (6 newly taken line transitions).
- `astropy/extern/configobj/validate.py::Validator.check` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `ConfigItem._validate_val`; control flow changed (5 newly taken line transitions).
- `astropy/extern/configobj/validate.py::_is_num_param` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `is_string`; control flow changed (8 newly taken line transitions).
- `astropy/extern/configobj/validate.py::is_string` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `Validator._check_value`; control flow changed (8 newly taken line transitions).
- `astropy/io/ascii/qdp.py::_interpret_err_lines` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `_get_tables_from_qdp_file`, `_interpret_err_lines`; control flow changed (37 newly taken line transitions).
- `astropy/io/ascii/qdp.py::_understand_err_col` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `_write_table_qdp`; control flow changed (17 newly taken line transitions).
- `astropy/table/column.py::BaseColumn.__array_finalize__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `BaseColumn.__array_wrap__`, `BaseColumn.__new__`, `MaskedColumn.__new__` (+1 more); control flow changed (12 newly taken line transitions).
- `astropy/table/column.py::BaseColumn.__array_wrap__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `a test`; control flow changed (10 newly taken line transitions).
- `astropy/table/column.py::BaseColumn.__new__` in 1 test(s), e.g. `astropy/io/ascii/tests/test_qdp.py::test_roundtrip[True]`: newly called from `Column.__new__`, `MaskedColumn.__new__`; control flow changed (16 newly taken line transitions).
- ... and 48 more function(s)

</details>

