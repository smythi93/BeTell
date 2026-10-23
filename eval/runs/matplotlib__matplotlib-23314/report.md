## Behavioral diff `base` → `gold`

Compared 927 test(s) on both revisions. 0 test(s) exist only in head and 0 only in base. 6199 unstable observation(s) were dropped after repeated runs.

**259 functions behave differently.** Not edited by this pull request: 258. Different in tests whose outcome stays the same: 3. Test outcomes that changed: 1.

### Test outcomes that changed

- `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]` failed → passed

### Silent changes in code this pull request does not edit

These functions are textually unchanged and the tests keep their outcome, yet the functions behave differently.

- `lib/matplotlib/colors.py::_to_rgba_no_colorcycle` in 2 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_contourf3d_extend[png-both-levels0]` and 1 more: return values changed (new `tuple:(0.9, 0.9, 0.9, 1.0)`, gone `tuple:(0.9, 0.9, 0.9, 1.0)`); arguments changed (new `(c=tuple:(0.9, 0.9, 0.9, 1), alpha=NoneType:None)`, gone `(c=tuple:(0.9, 0.9, 0.9, 1), alpha=NoneType:None)`).
- `lib/matplotlib/artist.py::Artist.get_visible` in 82 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::TestVoxels::test_alpha[png]` and 81 more: newly called from `Axes3D.draw`.

### Silent changes in edited code

- `lib/mpl_toolkits/mplot3d/axes3d.py::Axes3D.draw` in 82 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::TestVoxels::test_alpha[png]` and 81 more: control flow changed (33 no longer taken line transitions).

<details><summary>Behavior behind the changed test outcomes (259 function(s))</summary>

- `lib/matplotlib/artist.py::Artist._cm_set` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `dict:{'text': '0.0'}`, `dict:{'text': '0.2'}` (+4 more)); no longer called from `Text.draw`.
- `lib/matplotlib/artist.py::Artist.get_zorder` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `float:2.5`); no longer called from `Axes3D.draw`.
- `lib/matplotlib/axis.py::Axis.convert_units` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `ndarray:array([-0.02666972, -0.08332496])`, `ndarray:array([-0.02666972, 0.04972718])` (+4 more)); arguments changed (gone `(x=ndarray:array([-0.02666972, -0.08332496]))`, `(x=ndarray:array([-0.02666972, 0.04972718]))` (+4 more)); no longer called from `Artist.convert_xunits`, `Artist.convert_yunits`.
- `lib/matplotlib/axis.py::Ticker.locator` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `NullLocator:<NullLocator>`); no longer called from `Axis.get_majorticklocs`, `Axis.get_minorticklocs`.
- `lib/matplotlib/collections.py::LineCollection.set_segments` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `list:[Path(array([[ 0.07816138, -0...10339, -0.04788639]]), None), Path(array([[ 0.07881073, -0...8027...`, `list:[Path(array([[-0.07905758, -0...883862, 0.07518361]]), None), Path(array([[-5.99019885e-02...05, ...` (+1 more)); arguments changed (gone `(segments=list:[array([[ 0.07816138, -0.0252...[-0.08110339, -0.04788639]]), array([[ 0.07881073, -0.0110...[-0....)`, `(segments=list:[array([[-0.07905758, -0.0500... [-0.01883862, 0.07518361]]), array([[-5.99019885e-02, -5....0855...)` (+1 more)); no longer called from `Line3DCollection.do_3d_projection`; control flow changed (5 no longer taken line transitions).
- `lib/matplotlib/colors.py::to_rgba_array` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `ndarray:array([[0.9, 0.9, 0.9, 1. ]])`); arguments changed (gone `(c=tuple:(0.9, 0.9, 0.9, 1), alpha=NoneType:None)`).
- `lib/matplotlib/transforms.py::Bbox.from_bounds` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `Bbox:Bbox([[-13.125, -18.0], [13.125, 0.0]])`, `Bbox:Bbox([[-13.1875, -18.0], [13.1875, 0.0]])`); arguments changed (gone `(x0=float64:-13.125, y0=float64:-18.0, width=float64:26.25, height=float64:18.0)`, `(x0=float64:-13.1875, y0=float64:-18.0, width=float64:26.375, height=float64:18.0)`); no longer called from `Text._get_layout`.
- `lib/matplotlib/transforms.py::BboxBase.bounds` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `tuple:(169.99999999999997, 59.999999999999986, 480.0, 480.0)`).
- `lib/matplotlib/transforms.py::BboxBase.size` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `ndarray:array([480., 480.])`, `ndarray:array([640., 480.])`); no longer called from `Axis.draw`, `Figure.__repr__`.
- `lib/matplotlib/transforms.py::TransformedBbox.get_points` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: return values changed (gone `ndarray:array([[ 0., 0.], [640., 480.]])`, `ndarray:array([[170., 60.], [650., 540.]])`).
- `lib/matplotlib/backend_bases.py::GraphicsContextBase.set_alpha` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(alpha=float:0.5)`); no longer called from `Text.draw`; control flow changed (3 no longer taken line transitions).
- `lib/matplotlib/cbook/__init__.py::_str_lower_equal` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(obj=tuple:(0.9, 0.9, 0.9, 1), s=str:'face')`, `(obj=tuple:(0.9, 0.9, 0.9, 1), s=str:'none')`).
- `lib/matplotlib/collections.py::Collection._set_edgecolor` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(c=tuple:(0.9, 0.9, 0.9, 1))`); no longer called from `Collection.update_scalarmappable`; control flow changed (1 no longer taken line transitions).
- `lib/matplotlib/collections.py::Collection.set_edgecolor` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(c=tuple:(0.9, 0.9, 0.9, 1))`); no longer called from `LineCollection.set_color`.
- `lib/matplotlib/collections.py::Collection.set_linestyle` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(ls=str:'-')`); no longer called from `Axis.draw`.
- `lib/matplotlib/collections.py::Collection.set_linewidth` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(lw=float:1.0)`); no longer called from `Axis.draw`; control flow changed (1 no longer taken line transitions).
- `lib/matplotlib/patches.py::Polygon.set_xy` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(xy=ndarray:array([[-0.01993818, 0.00182... [-0.02078743, 0.07567758]]))`, `(xy=ndarray:array([[-0.08103122, -0.0493... [-0.01993818, 0.00182447]]))` (+1 more)); no longer called from `Axis.set_pane_pos`; control flow changed (1 no longer taken line transitions).
- `lib/matplotlib/transforms.py::nonsingular` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(vmin=float64:0.0, vmax=float64:1.0, expander=float:1e-13, tiny=float:1e-14, increasing=bool:True)`); no longer called from `MaxNLocator.tick_values`.
- `lib/matplotlib/units.py::_is_natively_supported` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(x=ndarray:array([-0.02666972, -0.08332496]))`, `(x=ndarray:array([-0.02666972, 0.04972718]))` (+4 more)); control flow changed (4 no longer taken line transitions).
- `lib/mpl_toolkits/mplot3d/art3d.py::Line3DCollection.set_segments` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: arguments changed (gone `(segments=ndarray:array([[[ 0. , -0.02083333, ..., 1.02083333, 1.02083333]]]))`, `(segments=ndarray:array([[[ 1.02083333, 1.0208...083333, -0.02083333, 1. ]]]))` (+1 more)); no longer called from `Axis.draw`.
- `lib/matplotlib/__init__.py::RcParams.__getitem__` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: no longer called from `Formatter.fix_minus`, `MaxNLocator._raw_ticks`, `RendererAgg.draw_text` (+2 more).
- `lib/matplotlib/_api/__init__.py::check_in_list` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: no longer called from `RendererAgg.get_text_width_height_descent`.
- `lib/matplotlib/_api/__init__.py::check_isinstance` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: no longer called from `TransformedPath.__init__`.
- `lib/matplotlib/_api/__init__.py::define_aliases.make_alias.method` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: no longer called from `Axes3D.get_proj`, `Axis.draw`; control flow changed (2 no longer taken line transitions).
- `lib/matplotlib/artist.py::Artist._set_gc_clip` in 1 test(s), e.g. `lib/mpl_toolkits/tests/test_mplot3d.py::test_invisible_axes[png]`: no longer called from `Collection.draw`, `Line2D.draw`, `Text.draw`.
- ... and 234 more function(s)

</details>

