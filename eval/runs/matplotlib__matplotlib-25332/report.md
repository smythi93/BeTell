## Behavioral diff `base` → `gold`

Compared 183 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 163 unstable observation(s) were dropped after repeated runs.

**601 functions behave differently.** Not edited by this pull request: 599. Different in tests whose outcome stays the same: 2. Test outcomes that changed: 2.

### Test outcomes that changed

- `lib/matplotlib/tests/test_pickle.py::test_complete[png]` failed → passed
- `lib/matplotlib/tests/test_pickle.py::test_pickle_load_from_subprocess[png]` failed → passed

### Silent changes in edited code

- `lib/matplotlib/cbook.py::Grouper.__getstate__` in 12 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 11 more: newly called from `Grouper.__getstate__`, `a test`.
- `lib/matplotlib/cbook.py::Grouper.__setstate__` in 9 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 8 more: newly called from `Grouper.__setstate__`, `a test`.

<details><summary>Behavior behind the changed test outcomes (599 function(s))</summary>

- `lib/matplotlib/__init__.py::rc_context` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: no longer handled: TypeError.
- `lib/matplotlib/_api/__init__.py::select_matching_signature` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: now handled: TypeError; newly called from `_compat_get_offset.get_offset`; control flow changed (7 newly taken line transitions).
- `lib/matplotlib/cm.py::ScalarMappable.set_clim` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: now handled: TypeError; newly called from `Figure.figimage`; control flow changed (8 newly taken line transitions).
- `lib/matplotlib/colors.py::_sanitize_extrema` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: now handled: AttributeError; control flow changed (3 newly taken line transitions).
- `lib/matplotlib/spines.py::Spines.__getitem__` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: now raised: KeyError; newly called from `XAxis._update_label_position`, `YAxis._update_label_position`, `YAxis._update_offset_text_position` (+1 more).
- `lib/matplotlib/style/core.py::context` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: no longer handled: TypeError.
- `lib/matplotlib/_api/__init__.py::define_aliases.make_alias.method` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `ndarray:array([], shape=(0, 4), dtype=float64)`); newly called from `QuadMesh.draw`.
- `lib/matplotlib/_pylab_helpers.py::Gcf.destroy_fig` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `int:3`); arguments changed (new `(fig=Figure:<Figure size 1000x600 with 0 Axes>)`, gone `(fig=Figure:<Figure size 640x480 with 0 Axes>)`).
- `lib/matplotlib/artist.py::Artist.get_figure` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `Figure:<Figure size 1000x600 with 10 Axes>`); newly called from `_AxesBase.apply_aspect`.
- `lib/matplotlib/axes/_base.py::_AxesBase.__getstate__` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `dict:{'_adjustable': 'box', '_agg_filter': None, '_alpha': None, '_anchor': 'C', '_animated': False, '...`).
- `lib/matplotlib/axes/_base.py::_AxesBase.autoscale_view` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `list:[[0, 10], [], [], [], [], [], ...]`, `list:[[0, 8], [], [], [], [], [], ...]` (+1 more)); newly called from `_AxesBase._unstale_viewLim`.
- `lib/matplotlib/axes/_base.py::_AxesBase.get_xbound` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(-0.5, 7.5)`, `tuple:(0.0, 7.0)`); newly called from `_AxesBase.get_data_ratio`.
- `lib/matplotlib/axes/_base.py::_AxesBase.get_xlim` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(-0.5, 7.5)`, `tuple:(0.0, 7.0)`).
- `lib/matplotlib/axes/_base.py::_AxesBase.get_ybound` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(-0.5, 9.5)`, `tuple:(0.0, 9.0)`); newly called from `_AxesBase.get_data_ratio`; control flow changed (2 newly taken line transitions).
- `lib/matplotlib/axes/_base.py::_AxesBase.get_ylim` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(0.0, 9.0)`, `tuple:(9.5, -0.5)`).
- `lib/matplotlib/axes/_base.py::_AxesBase.set_xlim` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(-0.35000000000000003, 7.35)`, `tuple:(-0.45, 9.45)` (+2 more)); arguments changed (new `(left=list:[-0.35000000000000003, 7.35], right=NoneType:None, emit=bool:True, auto=NoneType:None, xmin=NoneType:None, xmax=NoneType:None)`, `(left=list:[-0.45, 9.45], right=NoneType:None, emit=bool:True, auto=NoneType:None, xmin=NoneType:None, xmax=NoneType:None)` (+2 more)).
- `lib/matplotlib/axes/_base.py::_AxesBase.set_ylim` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `tuple:(-0.45, 9.45)`, `tuple:(-2.45, 51.45)` (+2 more)); arguments changed (new `(bottom=list:[-0.45, 9.45], top=NoneType:None, emit=bool:True, auto=NoneType:None, ymin=NoneType:None, ymax=NoneType:None)`, `(bottom=list:[-2.45, 51.45], top=NoneType:None, emit=bool:True, auto=NoneType:None, ymin=NoneType:None, ymax=NoneType:None)` (+2 more)).
- `lib/matplotlib/axes/_base.py::_process_plot_var_args.__getstate__` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `dict:{'axes': <Axes: ylabel='hello'>, 'command': 'fill'}`, `dict:{'axes': <Axes: ylabel='hello'>, 'command': 'plot'}` (+2 more)).
- `lib/matplotlib/backend_bases.py::FigureCanvasBase.mpl_connect` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `int:11`, `int:12` (+4 more)).
- `lib/matplotlib/cbook.py::safe_masked_invalid` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `MaskedArray:masked_array( data=[[[255, 2...l_value=999999, dtype=uint8)`); arguments changed (new `(x=memoryview:<memory at 0x?>, copy=bool:True)`).
- `lib/matplotlib/cm.py::ScalarMappable.get_array` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `MaskedArray:masked_array( data=[[ 0. , 0...ask=False, fill_value=1e+20)`, `MaskedArray:masked_array( data=[[0.0, 0...., False]], fill_value=1e+20)` (+1 more)); newly called from `_ImageBase.draw`.
- `lib/matplotlib/cm.py::ScalarMappable.to_rgba` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `ndarray:array([[0.267004, 0.004874, ..., 0.906157, 0.143936, 1. ]])`, `ndarray:array([[[0.267004, 0.004874,... 0.906157, 0.143936, 1. ]]])` (+2 more)); arguments changed (new `(x=MaskedArray:masked_array( data=[[ 0. , 0...ask=False, fill_value=1e+20), alpha=NoneType:None, bytes=bool:False, norm=bool:True)`, `(x=MaskedArray:masked_array( data=[[0.0, 0...., False]], fill_value=1e+20), alpha=NoneType:None, bytes=bool:False, norm=bool:True)` (+4 more)); newly called from `Collection.update_scalarmappable`, `_ImageBase._make_image`; control flow changed (9 newly taken line transitions).
- `lib/matplotlib/collections.py::Collection.get_paths` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `list:[Path(array([[ 0. , -0.4], [ 0. , 0.4]]), None), Path(array([[ 1. , -0.9], [ 1. , -0.1]]), None),...`, `list:[Path(array([[ 3.35410197e-03...03, 2.90473751e-03]]), None), Path(array([[ 2.87685035e-03...03, ...` (+2 more)); newly called from `Collection._prepare_points`.
- `lib/matplotlib/collections.py::PathCollection.get_paths` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `list:[Path(array([[ 0. , -0.5 ], [... 4, 4, 4, 79], dtype=uint8))]`, `list:[Path(array([[1. , 0. ], [2. ... 2, 2, 2, 79], dtype=uint8))]` (+6 more)); newly called from `Collection._prepare_points`.
- `lib/matplotlib/collections.py::PolyCollection.set_verts` in 2 test(s), e.g. `lib/matplotlib/tests/test_pickle.py::test_complete[png]` and 1 more: return values changed (new `list:[Path(array([[ 3.35410197e-03...03, 2.90473751e-03]]), None), Path(array([[ 2.87685035e-03...03, ...`); arguments changed (new `(.0=iterator:<iterator>)`, `(verts=ndarray:array([[[ 3.35410197e-03, 0....2440e-05, 3.35279341e-03]]]), closed=bool:False)`); newly called from `Quiver.draw`; control flow changed (1 newly taken line transitions).
- ... and 574 more function(s)

</details>

