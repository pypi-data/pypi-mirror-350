""" test ae.gui.utils module """
from math import pi, tau
from unittest.mock import MagicMock

from ae.i18n import get_text

from ae.gui.utils import (
    APP_STATE_HELP_ID_PREFIX, COLOR_BLACK, COLOR_DARK_GREY, COLOR_GREY, COLOR_LIGHT_GREY, COLOR_WHITE,
    FLOW_HELP_ID_PREFIX,
    TOUR_PAGE_HELP_ID_PREFIX,
    anchor_layout_x, anchor_layout_y, anchor_points, anchor_spec,
    brighten_color, complementary_color, darken_color, ellipse_polar_radius, ensure_tap_kwargs_refs,
    flow_action, flow_class_name, flow_change_confirmation_event_name, flow_key, flow_object, flow_path_id,
    flow_path_strip, flow_popup_class_name, help_id_tour_class, help_sub_id, id_of_flow, id_of_flow_help,
    id_of_state_help, id_of_tour_help, merge_popups_to_close, mix_colors, popup_event_kwargs,
    register_package_images, register_package_sounds, relief_colors, replace_flow_action, update_tap_kwargs)

from tst_constants import *


class TestAppHelperFunctions:
    def test_ellipse_polar_radius_circle(self):
        assert ellipse_polar_radius(1, 1, 1) == 1.0
        assert ellipse_polar_radius(3, 3, 3) == 3.0
        assert ellipse_polar_radius(9, 9, 9) == 9.0

    def test_ellipse_polar_radius_square(self):
        assert ellipse_polar_radius(9.0, 6.0, pi / 2) == 6.0
        assert ellipse_polar_radius(9.0, 6.0, pi) == 9.0
        assert ellipse_polar_radius(9, 6, pi * 3 / 2) == 6.0
        assert ellipse_polar_radius(9, 6, tau) == 9.0

    def test_ellipse_polar_radius_failing(self):
        assert ellipse_polar_radius(0, 9, 9) == 0.0
        assert ellipse_polar_radius(9, 0, 9) == 0.0
        assert ellipse_polar_radius(0, 9, 0) == 0.0

        with pytest.raises(ZeroDivisionError):
            ellipse_polar_radius(0, 0, 0)

    def test_ensure_tap_kwargs_refs_empty(self):
        kwargs = {}
        wid = object()

        ensure_tap_kwargs_refs(kwargs, wid)
        assert 'tap_kwargs' in kwargs

        assert 'tap_widget' in kwargs['tap_kwargs']
        assert kwargs['tap_kwargs']['tap_widget'] is wid

        assert 'popup_kwargs' in kwargs['tap_kwargs']
        assert 'opener' in kwargs['tap_kwargs']['popup_kwargs']
        assert kwargs['tap_kwargs']['popup_kwargs']['opener'] is wid

    def test_ensure_tap_kwargs_refs_parent_from_tap_widget(self):
        wid = object()
        wid2 = object()
        assert wid != wid2
        kwargs = dict(tap_kwargs=dict(tap_widget=wid))

        ensure_tap_kwargs_refs(kwargs, wid2)
        assert 'tap_kwargs' in kwargs

        assert 'tap_widget' in kwargs['tap_kwargs']
        assert kwargs['tap_kwargs']['tap_widget'] is wid

        assert 'popup_kwargs' in kwargs['tap_kwargs']
        assert 'opener' in kwargs['tap_kwargs']['popup_kwargs']
        # noinspection PyUnresolvedReferences
        assert kwargs['tap_kwargs']['popup_kwargs']['opener'] is wid

    def test_ensure_tap_kwargs_refs_full(self):
        wid = object()
        wid2 = object()
        assert wid != wid2
        kwargs = dict(tap_kwargs=dict(tap_widget=wid, popup_kwargs=dict(opener=wid)))

        ensure_tap_kwargs_refs(kwargs, wid2)
        assert 'tap_kwargs' in kwargs

        assert 'tap_widget' in kwargs['tap_kwargs']
        assert kwargs['tap_kwargs']['tap_widget'] is wid

        assert 'popup_kwargs' in kwargs['tap_kwargs']
        assert 'opener' in kwargs['tap_kwargs']['popup_kwargs']
        assert kwargs['tap_kwargs']['popup_kwargs']['opener'] is wid

    def test_flow_action(self):
        action = 'action'
        assert flow_action(id_of_flow(action, 'b', 'c')) == action

    def test_flow_change_confirmation_event_name(self):
        assert flow_change_confirmation_event_name(id_of_flow('a', 'b', 'c')) == 'on_b_a'
        assert flow_change_confirmation_event_name(id_of_flow('abc', 'bxy', 'c')) == 'on_bxy_abc'

    def test_flow_class_name(self):
        assert flow_class_name(id_of_flow('a', 'b', 'c'), 'Tour') == 'BATour'
        assert flow_class_name(id_of_flow('abc', 'bxy', 'c'), 'HuHu') == 'BxyAbcHuHu'
        assert flow_class_name(id_of_flow('open', 'bxy', 'c'), '') == 'Bxy'

    def test_flow_key(self):
        key = 'flow key example'
        assert flow_key(id_of_flow('a', 'b', key)) == key

    def test_flow_object(self):
        obj = 'flow_object_example'
        assert flow_object(id_of_flow('a', obj, 'xy')) == obj

    def test_flow_path_id(self):
        flow_id = id_of_flow('start', 'zzz')
        flow_path = [flow_id]

        assert flow_path_id(flow_path) == flow_id
        assert flow_path_id(flow_path, path_index=0) == flow_id

        assert flow_path_id(flow_path, path_index=1) == ""
        assert flow_path_id(flow_path, path_index=-2) == ""

    def test_flow_path_strip(self):
        assert flow_path_strip([]) == []

        flow_path = [id_of_flow('enter', 'xxx')]

        assert flow_path_strip(flow_path) == flow_path
        assert flow_path_strip(flow_path) is not flow_path

        flow_path_ext = [id_of_flow('enter', 'xxx'), id_of_flow('some', 'flow')]
        assert flow_path_strip(flow_path_ext) == flow_path

    def test_flow_popup_class_name(self):
        assert flow_popup_class_name(id_of_flow('a', 'b', 'c')) == 'BAPopup'
        assert flow_popup_class_name(id_of_flow('abc', 'bxy', 'c')) == 'BxyAbcPopup'
        assert flow_popup_class_name(id_of_flow('open', 'bxy', 'c')) == 'BxyPopup'

    def test_id_of_flow(self):
        assert id_of_flow('action', 'obj', 'key') == id_of_flow('action', 'obj', 'key')
        with pytest.raises(AssertionError):
            id_of_flow('Action', 'obj')
        with pytest.raises(AssertionError):
            id_of_flow('act:ion', 'obj')
        with pytest.raises(AssertionError):
            id_of_flow('action', 'o:bj')
        with pytest.raises(AssertionError):
            id_of_flow('act ion', 'obj')

    def test_merge_popups_to_close(self):
        assert isinstance(merge_popups_to_close({}, {}), tuple)

        assert merge_popups_to_close({'popups_to_close': 3}, {'popups_to_close': 6}) == 9

        with pytest.raises(AssertionError):
            merge_popups_to_close({'popups_to_close': ("any", )}, {'popups_to_close': 33})

        assert merge_popups_to_close({}, {}) == ()

        tup = ("place_holder1", "place_holder2", 999, object())
        assert merge_popups_to_close({'popups_to_close': tup}, {'popups_to_close': tup}) == tup

        ptc = merge_popups_to_close({'popups_to_close': ("place_holder0", "place_holder2", 333)},
                                    {'popups_to_close': ("place_holder1", "place_holder2", 999)})
        assert ptc == ("place_holder0", "place_holder2", 333, "place_holder1", 999)

    def test_popup_event_kwargs(self):
        assert popup_event_kwargs("msg", "t i t l e") == {
            'popup_kwargs': {'message': "msg", 'title': "t i t l e"}}
        assert popup_event_kwargs("msg", "tit", "cfid", {'kws': "ck"}) == {
            'popup_kwargs': {'message': "msg", 'title': "tit", 'confirm_flow_id': "cfid",
                             'confirm_kwargs': {'kws': "ck"}}}
        assert popup_event_kwargs("msg", "tit", "cfid", {'kws': "ck"}, "ct") == {
            'popup_kwargs': {'message': "msg", 'title': "tit", 'confirm_flow_id': "cfid",
                             'confirm_kwargs': {'kws': "ck"}, 'confirm_text': "ct"}}
        assert popup_event_kwargs("msg", "tit", "cfid", {'kws': "ck"}, "") == {
            'popup_kwargs': {'message': "msg", 'title': "tit", 'confirm_flow_id': "cfid",
                             'confirm_kwargs': {'kws': "ck"}, 'confirm_text': get_text("confirm")}}

    def test_register_package_images(self, image_files_to_test):
        assert len(PORTIONS_IMAGES) == PORTION_IMG_COUNT + TST_IMG_COUNT
        assert TST_IMG_COUNT != len(image_files_to_test)
        register_package_images()
        assert len(PORTIONS_IMAGES) == PORTION_IMG_COUNT + TST_IMG_COUNT

    def test_register_package_sounds(self, sound_files_to_test):
        old_count = len(PORTIONS_SOUNDS)
        assert PORTION_SND_COUNT == old_count
        assert TST_SND_COUNT == len(sound_files_to_test)
        register_package_sounds()
        assert len(PORTIONS_SOUNDS) == PORTION_SND_COUNT + TST_SND_COUNT

    def test_replace_flow_action(self):
        assert replace_flow_action(id_of_flow('a', 'b', 'c'), 'action') == id_of_flow('action', 'b', 'c')

    def test_replace_flow_action_error(self):
        with pytest.raises(AssertionError):
            replace_flow_action(id_of_flow('a', 'b', 'c'), 'new_Action')

    def test_update_tap_kwargs(self):
        wid = MagicMock()  # create real Widget instance fails at gitlab-CI
        event_dict = {}

        assert update_tap_kwargs(event_dict) == event_dict
        assert update_tap_kwargs(event_dict) is not event_dict

        wid.tap_kwargs = event_dict
        assert update_tap_kwargs(wid) is event_dict

        assert 'tap_widget' in update_tap_kwargs(wid)
        assert 'popup_kwargs' in update_tap_kwargs(wid)
        assert 'opener' in update_tap_kwargs(wid)['popup_kwargs']

        popup_dict = dict(popup_extra_kwarg='tst')
        assert 'popup_kwargs' in update_tap_kwargs(wid, popup_kwargs=popup_dict)
        assert 'popup_extra_kwarg' in update_tap_kwargs(wid)['popup_kwargs']
        assert update_tap_kwargs(wid)['popup_kwargs']['popup_extra_kwarg'] == 'tst'

        assert 'popups_to_close' in update_tap_kwargs(wid, popups_to_close=("popup1", ))
        assert update_tap_kwargs(wid)['popups_to_close'] == ("popup1", )

        assert 'extra_kwarg' in update_tap_kwargs(wid, extra_kwarg='extra_tst')
        assert update_tap_kwargs(wid)['extra_kwarg'] == 'extra_tst'


class TestColorHelperFunctions:
    def test_brighten_color(self):
        assert brighten_color([1, 1, 1]) == [1, 1, 1]
        assert brighten_color([1, 1, 1], factor=-.3) == [1, 1, 1]
        assert brighten_color([.6, .6, .6]) == [.78, .78, .78]
        assert brighten_color([.6, .6, .6], factor=-0.3) == [.72, .72, .72]
        assert brighten_color([0, 0, 0]) == [0.0, 0.0, 0.0]
        assert brighten_color([0, 0, 0], factor=-.3) == [0.3, 0.3, 0.3]

        assert brighten_color([0, 0, 0], factor=0) == [0.0, 0., 0.]
        assert brighten_color([0, 0, 0], factor=.6) == [0.0, 0.0, 0.0]
        assert brighten_color([0, 0, 0], factor=-.6) == [.6, 0.6, 0.6]
        assert brighten_color([0, 0, 0], factor=1) == [.0, 0, 0]
        assert brighten_color([0, 0, 0], factor=-1) == [1, 1, 1]

    def test_brighten_color_ink(self):
        assert brighten_color([1, 1, 1, 1]) == [1, 1, 1, 1]
        assert brighten_color([1, 1, 1, 1], factor=-.3) == [1, 1, 1, 1]
        assert brighten_color([.6, .6, .6, 0]) == [0.78, 0.78, 0.78, 0]
        assert brighten_color([.6, .6, .6, 0], factor=-.3) == [.72, .72, .72, 0]
        assert brighten_color([0, 0, 0, 1]) == [0.0, 0.0, 0.0, 1]
        assert brighten_color([0, 0, 0, 1], factor=-.3) == [0.3, 0.3, 0.3, 1]

        assert brighten_color([0, 0, 0, 0], factor=0) == [.0, 0, 0, 0]
        assert brighten_color([0, 0, 0, 0], factor=-0) == [0, 0, 0, 0]
        assert brighten_color([0, 0, 0, 0], factor=.6) == [0, 0, 0, 0]
        assert brighten_color([0, 0, 0, 0], factor=-.6) == [.6, .6, .6, 0]
        assert brighten_color([0, 0, 0, 1], factor=1) == [0.0, 0, 0, 1]
        assert brighten_color([0, 0, 0, 1], factor=-1) == [1., 1, 1, 1]

    def test_brighten_color_throws(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            brighten_color()

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            brighten_color(None)

        with pytest.raises(ValueError):
            brighten_color([])

    def test_complementary_color(self):
        assert complementary_color([0, 0, 0]) == [0, 0, 0]
        assert complementary_color([0, 0, 0], delta_h=0) == [1, 1, 1]
        assert complementary_color([1, 0, 0]) == [0, 1, 1]
        assert complementary_color([1, 0, 0], delta_h=0) == [0, 1, 1]
        assert complementary_color([0, 1, 0]) == [1, 0, 1]
        assert complementary_color([0, 1, 0], delta_h=0) == [1, 0, 1]
        assert complementary_color([0, 0, 1]) == [1, 1, 0]
        assert complementary_color([0, 0, 1], delta_h=0) == [1, 1, 0]

        assert complementary_color([1., .6, .3]) == [0.30000000000000004, 0.6999999999999993, 1.0]
        assert complementary_color([1., .6, .3], delta_h=0) == [.0, .4, .7]
        assert complementary_color([.48, .5, .51]) == [0.51, 0.49, 0.48]
        assert complementary_color([.48, .5, .51], delta_h=0) == [0.52, 0.5, 0.49]
        assert complementary_color([.5, .5, .5]) == [0.5, 0.5, 0.5]
        assert complementary_color([.5, .5, .5], delta_h=0) == [.5, .5, .5]
        assert complementary_color([.3, 1., .6]) == [1.0, 0.30000000000000004, 0.6999999999999993]
        assert complementary_color([.3, 1., .6], delta_h=0) == [.7, 0., .4]
        assert complementary_color([.1, .3, .9]) == [0.9, 0.7000000000000001, 0.09999999999999995]
        assert complementary_color([.1, .3, .9], delta_h=0) == [0.9, 0.7, 0.09999999999999998]
        assert complementary_color([1, 1, 1]) == [1, 1, 1]
        assert complementary_color([1, 1, 1], delta_h=0) == [0, 0, 0]

        for delta_h in range(0, 360, 2):  # some more test deltas also to cover all 6 h_i-cases in color_from_hsv()
            assert complementary_color([.5, .5, .5], delta_h=delta_h) == [0.5, 0.5, 0.5]

    def test_complementary_color_ink(self):
        assert complementary_color([1, 0, 0, 1]) == [0, 1, 1, 1]

        assert complementary_color([1, 1, 1, 1]) == [1, 1, 1, 1]
        assert complementary_color([1, 1, 1, 1], delta_h=0) == [.0, .0, .0, 1]
        assert complementary_color([.6, .6, .6, 0]) == [0.6, 0.6, 0.6, 0]
        assert complementary_color([.6, .6, .6, 0], delta_h=0) == [.4, .4, .4, 0]
        assert complementary_color([0, 0, 0, 1]) == [0, 0, 0, 1]
        assert complementary_color([0, 0, 0, 1], delta_h=0) == [1, 1, 1, 1]

    def test_complementary_color_throws(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            complementary_color()

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            complementary_color(None)

        with pytest.raises(ValueError):
            complementary_color([])

    def test_darken_color(self):
        assert darken_color([1, 1, 1]) == [.7, .7, .7]
        assert darken_color([.6, .6, .6]) == [.42, .42, .42]
        assert darken_color([0, 0, 0]) == [0, 0, 0]

        assert darken_color([1, 1, 1], factor=0) == [1.0, 1., 1.]
        assert darken_color([1, 1, 1], factor=.6) == [.4, .4, .4]
        assert darken_color([1, 1, 1], factor=1) == [.00, .0, .0]

    def test_darken_color_ink(self):
        assert darken_color([1, 1, 1, 1]) == [.7, .7, .7, 1]
        assert darken_color([.6, .6, .6, 0]) == [.42, .42, .42, 0]
        assert darken_color([0, 0, 0, 1]) == [0, 0, 0, 1]

        assert darken_color([1, 1, 1, 1], factor=0) == [1.0, 1., 1., 1]
        assert darken_color([1, 1, 1, 1], factor=.6) == [.4, .4, .4, 1]
        assert darken_color([1, 1, 1, 0], factor=1) == [.00, .0, .0, 0]

    def test_darken_color_throws(self):
        with pytest.raises(TypeError):
            # noinspection PyArgumentList
            darken_color()

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            darken_color(None)

        with pytest.raises(ValueError):
            darken_color([])

    def test_mix_colors(self):
        assert mix_colors() == []
        assert mix_colors([0, 0, 0, 0], [1, 1, 1, 1]) == [0.5, 0.5, 0.5, 0.5]
        assert mix_colors([0, .3, .6, .9], [.3, .6, .9, 1]) == [0.15, 0.44999999999999996, 0.75, 0.95]

    def test_relief_colors_default_args(self):
        assert relief_colors() == (
            [0.8144, 0.81248, 0.81056], [0.3563, 0.35357, 0.35084])
        assert relief_colors(top_factor=-0.6, bottom_factor=-0.3) == (
            [0.8036, 0.8024, 0.8011999999999999], [0.3563, 0.35419999999999996, 0.35209999999999997])

        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5]) == (
            [0.8, 0.8, 0.8], [0.35, 0.35, 0.35])
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5], top_factor=-0.6, bottom_factor=-0.3) == (
            [0.8, 0.8, 0.8], [0.35, 0.35, 0.35])

        assert relief_colors(color_or_ink=COLOR_WHITE) == (
            [1.0, 0.9987987987987988, 0.9975975975975976], [0.6992999999999999, 0.6965699999999999, 0.6938399999999999])
        assert relief_colors(color_or_ink=COLOR_WHITE, top_factor=-0.6, bottom_factor=-0.3) == (
            [0.9996, 0.9984, 0.9972], [0.6992999999999999, 0.6971999999999999, 0.6950999999999999])

        assert relief_colors(color_or_ink=COLOR_LIGHT_GREY) == (
            [1.0, 0.9982832618025751, 0.9965665236051502], [0.48929999999999996, 0.48657, 0.48383999999999994])
        assert relief_colors(color_or_ink=COLOR_LIGHT_GREY, top_factor=-0.6, bottom_factor=-0.3) == (
            [0.8795999999999999, 0.8784, 0.8772], [0.48929999999999996, 0.4871999999999999, 0.4850999999999999])

        assert relief_colors(color_or_ink=COLOR_GREY) == (
            [0.8144, 0.81248, 0.81056], [0.3563, 0.35357, 0.35084])
        assert relief_colors(color_or_ink=COLOR_GREY, top_factor=-0.6, bottom_factor=-0.3) == (
            [0.8036, 0.8024, 0.8011999999999999], [0.3563, 0.35419999999999996, 0.35209999999999997])

        assert relief_colors(color_or_ink=COLOR_DARK_GREY) == (
            [0.4944, 0.49248000000000003, 0.49056], [0.2163, 0.21356999999999998, 0.21083999999999997])
        assert relief_colors(color_or_ink=COLOR_DARK_GREY, top_factor=-0.6, bottom_factor=-0.3) == (
            [0.7236, 0.7223999999999999, 0.7212000000000001], [0.2163, 0.21419999999999997, 0.21209999999999998])

        assert relief_colors(color_or_ink=COLOR_BLACK) == (
            [0.0144, 0.01248, 0.01056], [0.006299999999999999, 0.0035700000000000003, 0.0008399999999999997])
        assert relief_colors(color_or_ink=COLOR_BLACK, top_factor=-0.6, bottom_factor=-0.3) == (
            [0.6036, 0.6023999999999999, 0.6012], [0.006299999999999999, 0.0042, 0.0021])

        assert relief_colors(color_or_ink=[1.0, 0.5, 0.5]) == (
            [1.0, 0.8, 0.8], [0.7, 0.24499999999999997, 0.24499999999999997])
        assert relief_colors(color_or_ink=[1.0, 0.5, 0.5], top_factor=-0.6, bottom_factor=-0.3) == (
            [1.0, 0.8, 0.8], [0.7, 0.35, 0.35])

        assert relief_colors(top_factor=0.3, bottom_factor=0.6) == (
            [0.6617000000000001, 0.6589700000000001, 0.65624], [0.2036, 0.20168, 0.19976])
        assert relief_colors(top_factor=-.3, bottom_factor=-.6) == (
            [0.6563, 0.6542, 0.6521], [0.2036, 0.20240000000000002, 0.20120000000000002])

        assert relief_colors(top_factor=0.1, bottom_factor=0.9, sunken=True) == (
            [0.4581, 0.45513000000000003, 0.45216], [0.9671, 0.96653, 0.9659599999999999])
        assert relief_colors(top_factor=-.1, bottom_factor=-.9, sunken=True) == (
            [0.4581, 0.4554, 0.4527], [0.9509000000000001, 0.9506, 0.9503])

    def test_relief_colors_using_ink_and_auto_hide(self):
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0.1]) == ([0.8, 0.8, 0.8], [0.35, 0.35, 0.35])
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0.0]) == ()
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0]) == ()


class TestTourHelperFunctions:
    def test_anchor_layout_x(self):
        a_dir = 'r'
        a_x = 6
        w = 9
        w_w = 12
        assert anchor_layout_x((a_x, 0.0, a_dir), w, w_w) == a_x

        a_dir = 'i'
        a_x = 6
        w = 9
        w_w = 12
        assert anchor_layout_x((a_x, 0.0, a_dir), w, w_w) == a_x - w / 2

        a_dir = 'l'
        a_x = 6
        w = 9
        w_w = 12
        assert anchor_layout_x((a_x, 0.0, a_dir), w, w_w) == a_x - w

    def test_anchor_layout_y(self):
        a_dir = 'r'
        a_y = 6
        h = 9
        w_h = 12
        assert anchor_layout_y((0.0, a_y, a_dir), h, w_h) == a_y - h / 2

        a_dir = 'i'
        a_y = 6
        h = 9
        w_h = 12
        assert anchor_layout_y((0.0, a_y, a_dir), h, w_h) == a_y

        a_dir = 'd'
        a_y = 6
        h = 9
        w_h = 12
        assert anchor_layout_y((0.0, a_y, a_dir), h, w_h) == a_y - h

    def test_anchor_points(self):
        # noinspection PyTypeChecker
        assert anchor_points(0, ()) == ()

        font_size = 12
        radius = font_size * 0.69
        spec: tuple[float, float, str] = (99, 999, 'r')
        anchor_x, anchor_y, anchor_dir = spec

        points = anchor_points(font_size, spec)
        assert len(points) == 6
        assert points[0] == anchor_x
        assert points[1] == anchor_y - radius
        assert points[2] == anchor_x - radius
        assert points[3] == anchor_y
        assert points[4] == anchor_x
        assert points[5] == anchor_y + radius

        points = anchor_points(font_size, spec[:2] + ('i', ))
        assert len(points) == 6
        assert points[0] == anchor_x - radius
        assert points[1] == anchor_y
        assert points[2] == anchor_x
        assert points[3] == anchor_y - radius
        assert points[4] == anchor_x + radius
        assert points[5] == anchor_y

        points = anchor_points(font_size, spec[:2] + ('l', ))
        assert len(points) == 6
        assert points[0] == anchor_x
        assert points[1] == anchor_y - radius
        assert points[2] == anchor_x + radius
        assert points[3] == anchor_y
        assert points[4] == anchor_x
        assert points[5] == anchor_y + radius

        points = anchor_points(font_size, spec[:2] + ('d', ))
        assert len(points) == 6
        assert points[0] == anchor_x - radius
        assert points[1] == anchor_y
        assert points[2] == anchor_x
        assert points[3] == anchor_y + radius
        assert points[4] == anchor_x + radius
        assert points[5] == anchor_y

    def test_anchor_spec(self):
        w_x = 18
        w_y = 15
        w_w = 12
        w_h = 9
        win_w = 69
        win_h = 33
        anchor_x, anchor_y, anchor_dir = anchor_spec(w_x, w_y, w_w, w_h, win_w, win_h)
        assert anchor_dir == 'r'
        assert anchor_x == w_x + w_w
        assert anchor_y == w_y + w_h / 2

        w_x = 6
        w_y = 3
        w_w = 12
        w_h = 9
        win_w = 24
        win_h = 27
        anchor_x, anchor_y, anchor_dir = anchor_spec(w_x, w_y, w_w, w_h, win_w, win_h)
        assert anchor_dir == 'i'
        assert anchor_x == w_x + w_w / 2
        assert anchor_y == w_y + w_h

        w_x = 18
        w_y = 15
        w_w = 12
        w_h = 9
        win_w = 6
        win_h = 3
        anchor_x, anchor_y, anchor_dir = anchor_spec(w_x, w_y, w_w, w_h, win_w, win_h)
        assert anchor_dir == 'l'
        assert anchor_x == w_x
        assert anchor_y == w_y + w_h / 2

        w_x = 3
        w_y = 6
        w_w = 9
        w_h = 12
        win_w = 15
        win_h = 18
        anchor_x, anchor_y, anchor_dir = anchor_spec(w_x, w_y, w_w, w_h, win_w, win_h)
        assert anchor_dir == 'd'
        assert anchor_x == w_x + w_w / 2
        assert anchor_y == w_y

    def test_help_id_tour_class(self):
        assert help_id_tour_class('invalid_help_id_without_prefix') is None

        flow_id = 'tst_flow_id'
        assert help_id_tour_class(id_of_flow_help(flow_id)) is None

    def test_help_sub_id(self):
        assert help_sub_id('') == ''

        flow_id = 'tst_flow_id'
        assert help_sub_id(id_of_flow_help(flow_id)) == flow_id
        assert help_sub_id(id_of_tour_help(flow_id)) == flow_id
        assert help_sub_id(id_of_state_help(flow_id)) == flow_id

    def test_id_of_flow_help(self):
        flow_id = 'test_flow_id'
        assert id_of_flow_help(flow_id) == f'help_flow#{flow_id}'
        assert id_of_flow_help(flow_id) == f'{FLOW_HELP_ID_PREFIX}{flow_id}'

    def test_id_of_state_help(self):
        app_state_name = 'app_state_name'
        assert id_of_state_help(app_state_name) == f'{APP_STATE_HELP_ID_PREFIX}{app_state_name}'

        app_state = 'test_app_state'
        assert id_of_state_help(app_state) == f'help_app_state#{app_state}'

    def test_id_of_tour_help(self):
        page_id = 'test_page_id'
        assert id_of_tour_help(page_id) == f'{TOUR_PAGE_HELP_ID_PREFIX}{page_id}'
        assert id_of_tour_help(page_id) == f'tour_page#{page_id}'
