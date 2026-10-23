## Behavioral diff `f67c2bb^` → `f67c2bb`

Compared 2095 test(s) on both revisions. 22 test(s) exist only in head and 0 only in base. 441 unstable observation(s) were dropped after repeated runs.

**1 function behave differently.** Not edited by this pull request: 0. Different in tests whose outcome stays the same: 1. Test outcomes that changed: 0.

### Silent changes in edited code

- `src/click/utils.py::_make_default_short_help` in 31 test(s), e.g. `test_basic.py::test_basic_group` and 30 more: arguments changed (new `(help=str:'123 567 9. Aaaa bbb', max_length=int:10)`, `(help=str:'\n\x08\n123 567 9. Aaaa bbb\n', max_length=int:10)`, gone `(help=str:'123 567 9. aaaa bbb', max_length=int:10)`, `(help=str:'\n\x08\n123 567 9. aaaa bbb\n', max_length=int:10)`); control flow changed (3 newly taken, 3 no longer taken line transitions).

