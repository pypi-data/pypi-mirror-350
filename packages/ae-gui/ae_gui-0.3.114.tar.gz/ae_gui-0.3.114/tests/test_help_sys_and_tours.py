""" test ae.gui.tours module """
import pytest

from typing import Any, Optional, Callable, Union
from unittest.mock import MagicMock, patch, call

from ae.core import DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_ENABLED
from ae.i18n import LOADED_TRANSLATIONS, default_language

# noinspection PyProtectedMember
from ae.gui.utils import (
    APP_STATE_HELP_ID_PREFIX, FLOW_HELP_ID_PREFIX, REGISTERED_TOURS, TOUR_PAGE_HELP_ID_PREFIX,
    anchor_points, anchor_spec, anchor_layout_x, anchor_layout_y,
    help_id_tour_class, help_sub_id, id_of_flow, id_of_flow_help, id_of_state_help, id_of_tour_help, tour_id_class)
from ae.gui.app import MainAppBase
# noinspection PyProtectedMember
from ae.gui.tours import (
    _OPEN_USER_PREFERENCES_FLOW_ID, OnboardingTour, TourBase, TourDropdownFromButton, UserPreferencesTour)


class AbstractsImplementation(MainAppBase):
    """ main app class used for tests """

    ensure_top_most_z_index_called = 0

    def init_app(self, _framework_app_class: Any = None) -> tuple[Optional[Callable], Optional[Callable]]:
        """ MainAppBase abstract method implementation """
        assert self
        return lambda x: None, lambda x: None

    def call_method_delayed(self, _delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ implement delayed callback - ignoring delay arg for tests. """
        return self.call_method(callback, *args, **kwargs)

    def call_method_repeatedly(self, _interval: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ implement repeated callback - repeating test calls are done by the UI-specific framework. """
        # not needed by unit tests: return self.call_method(callback, *args, **kwargs)

    def ensure_top_most_z_index(self, _widget: Any):
        """ MainAppBase abstract method implementation """
        self.ensure_top_most_z_index_called += 1

    def help_activation_toggle(self):
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """


@pytest.fixture
def app_test(restore_app_env):
    """ create an app instance for testing while restoring ae.core app environment after a test run. """
    yield AbstractsImplementation()


class TestMainAppHelpAndTourBaseMethods:
    def test_on_app_started(self, app_test):
        self._called = False
        app_test.start_app_tour = lambda: setattr(self, '_called', True)
        assert not self._called
        app_test.on_app_started()
        assert self._called

    def test_on_app_tour_toggle(self, app_test):
        self._called = 0
        app_test.start_app_tour = lambda: setattr(self, '_called', self._called + 1)
        app_test.close_popups = lambda: setattr(self, '_called', self._called + 1)
        assert not self._called
        app_test.on_app_tour_toggle("", {})
        assert self._called == 2

        app_test.tour_layout = MagicMock()
        app_test.tour_layout.stop_tour = lambda: setattr(self, '_called', self._called + 1)
        app_test.on_app_tour_toggle("", {})
        assert self._called == 3

    def test_help_display_basics(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.framework_win = MagicMock()

        help_id = 'help_id:with_key'
        help_target = MagicMock()
        help_vars = dict(self=help_target)

        with patch('ae.gui.utils.translation', lambda msg_id: msg_id == 'help_id'):
            assert app_test.help_display(help_id, help_vars)
        assert app_test.displayed_help_id == help_id
        assert 'self' in help_vars
        assert help_vars['self'] is help_target
        assert app_test.help_layout.targeted_widget is help_target
        assert app_test.ensure_top_most_z_index_called == 1

        # test without translation found and must_have
        app_test.debug_level = DEBUG_LEVEL_ENABLED
        app_test.help_layout.tip_text = ''
        assert app_test.help_display(help_id, help_vars, help_target, must_have=True)
        assert app_test.help_layout.tip_text

        app_test.debug_level = DEBUG_LEVEL_DISABLED
        app_test.help_layout.tip_text = ''
        assert app_test.help_display(help_id, help_vars, help_target, must_have=True)
        assert app_test.help_layout.tip_text

    def test_help_display_next_help_id(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.framework_win = MagicMock()
        help_id = 'this_hlp_id'

        help_target = MagicMock()
        help_vars = dict(self=help_target)

        app_test.debug_level = DEBUG_LEVEL_ENABLED
        with patch('ae.gui.utils.translation', lambda msg_id: dict(next_help_id='nxt_hlp_id')):
            assert app_test.help_display(help_id, help_vars, key_suffix='after', must_have=True)
        assert app_test.displayed_help_id == 'nxt_hlp_id'
        app_test.debug_level = DEBUG_LEVEL_DISABLED

    def test_help_display_wid_search(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.framework_win = MagicMock()
        hlp_id = 'tst_hlp_id'

        class TestWidget:
            """ test fake widget class """
            help_id = hlp_id
            children = []

        wid = TestWidget()
        app_test.framework_win.container = app_test.framework_win   # needed because widget_children() use it on mock
        app_test.framework_win.children = [wid]
        hlp_vars = {}
        with patch('ae.gui.utils.translation', lambda msg_id: True):
            assert app_test.help_display(hlp_id, hlp_vars)
        assert hlp_vars['self'] is wid

    def test_help_flow_display(self, app_test):
        flow_id = id_of_flow('do', 'xxx')

        class _Widget:
            children = []
            tap_flow_id = flow_id
        wid = _Widget()
        app_test.framework_win = MagicMock()
        app_test.framework_win.container = app_test.framework_win
        app_test.framework_win.children = []
        app_test.framework_win.children.append(wid)

        help_vars = dict(new_flow_id=flow_id)
        assert not app_test.help_flow_display(help_vars)
        assert help_vars['self'] == wid

    def test_help_target_and_id(self, app_test):
        app_test._next_help_id = ''
        target, help_id = app_test.help_target_and_id({})
        assert target is app_test.help_activator
        assert help_id == ''

        app_test.framework_win = MagicMock()
        app_test._next_help_id = 'any_help_id'
        target, help_id = app_test.help_target_and_id({})
        assert target is app_test.help_activator
        assert help_id == ''

        widget = object()
        app_test.help_widget = lambda *_args: widget

        app_test._next_help_id = 'any_help_id'
        target, help_id = app_test.help_target_and_id({})
        assert target is widget
        assert help_id == app_test._next_help_id

        app_test._next_help_id = ''
        app_test.flow_id = 'tst_flow_id'
        target, help_id = app_test.help_target_and_id({})
        assert target is widget
        assert app_test.flow_id in help_id

    def test_help_widget(self, app_test):
        self.help_id = 'test_find_val'
        app_test.framework_win = MagicMock()

        assert app_test.help_widget('not_existing_test_find_attr', {}) is None
        assert app_test.help_widget(self.help_id, {})

    def test_key_press_from_framework(self, app_test):
        assert not app_test.key_press_from_framework('Ctrl', 'x_')
        app_test.tour_layout = object()
        assert app_test.key_press_from_framework('Shift', '_z')

    def test_start_app_tour(self, app_test):
        assert not app_test.start_app_tour()    # tour start still canceled because the help activator button is missing
        app_test.help_activator = object()

        assert not app_test.start_app_tour()    # tour start canceled because layout not set

        assert not app_test.tour_overlay_class

        class _TourOverlayLayout:
            def __init__(self, *args, **kwargs):
                self.init_call_args = (args, kwargs)
                self.running = True
                app_test.tour_layout = self

            def stop_tour(self):
                """ stop tour method - called by starting tour on prev_layout """
                self.running = False

        app_test.tour_overlay_class = _TourOverlayLayout
        app_test.tour_layout = prev_layout = _TourOverlayLayout()

        assert app_test.start_app_tour()
        assert prev_layout.running is False
        assert app_test.tour_layout.running is True

    def test_widget_tourable_children_page_ids(self, app_test):
        class _Widget:
            def __init__(self):
                self.children = []
                self.width = 333
                self.height = 111

        parent = _Widget()
        chi = _Widget()
        chi.tap_flow_id = 'abc'
        parent.children.append(chi)
        chichi = _Widget()
        chichi.tap_flow_id = 'xyz'
        chi.children.append(chichi)

        assert not app_test.widget_tourable_children_page_ids(chichi)
        assert app_test.widget_tourable_children_page_ids(chi) == [chichi.tap_flow_id]
        assert app_test.widget_tourable_children_page_ids(parent) == [chi.tap_flow_id]

        del chi.tap_flow_id
        assert app_test.widget_tourable_children_page_ids(parent) == [chichi.tap_flow_id]


class TestAppStateHelp:
    def test_activated_change(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.change_app_state = MagicMock()
        app_test.change_app_state('app_state_name', 'app_state_val')
        assert app_test.change_app_state.mock_calls == [call('app_state_name', 'app_state_val')]

    def test_change(self, app_test):
        app_test.change_app_state = MagicMock()
        app_test.change_app_state('app_state_name', 'app_state_val', send_event=False)
        assert app_test.change_app_state.mock_calls[0] == call('app_state_name', 'app_state_val', send_event=False)

    def test_change_app_state_cancel_in_help_mode(self, app_test):
        with patch('ae.gui.app.MainAppBase.help_app_state_display', MagicMock(return_value=True)):
            assert not app_test.change_app_state('any_var_name', 'any_val')

    def test_help_app_state_display_basics(self, app_test):
        assert not app_test.help_app_state_display({})
        assert not app_test.help_app_state_display({}, changed=True)

        app_test.help_layout = MagicMock()
        app_state_name = 'app_state_name'
        help_vars = dict(app_state_name=app_state_name)

        assert not app_test.help_app_state_display(help_vars)
        assert not app_test.help_app_state_display(help_vars, changed=True)

        app_test.displayed_help_id = id_of_state_help(app_state_name)
        assert not app_test.help_app_state_display(help_vars)
        assert not app_test.help_app_state_display(help_vars, changed=True)

    def test_help_app_state_display_ignored_states(self, app_test):
        app_test.help_layout = MagicMock()
        assert not app_test.help_app_state_display(dict(app_state_name='flow_id'))
        assert not app_test.help_app_state_display(dict(app_state_name='flow_path'))
        assert not app_test.help_app_state_display(dict(app_state_name='win_rectangle'))
        assert not app_test.help_app_state_display(dict(app_state_name='unknown_state_name'))

    def test_help_app_state_display_next_help_id(self, app_test):
        app_state_name = 'app_state_name'
        with patch('ae.gui.utils.translation', lambda msg_id: True):
            app_test.help_app_state_display(dict(app_state_name=app_state_name))
            assert app_state_name in app_test._next_help_id

    def test_save_app_states(self, app_test):
        assert not app_test.tour_layout
        app_test.save_app_states()
        app_test.tour_layout = MagicMock()
        app_test.save_app_states()


class TestFlowHelp:
    def test_activated_change(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.framework_win = MagicMock()
        app_test.framework_win.children = []
        assert not app_test.change_flow('test_flow_id')

    def test_change_with_count_pluralization(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.help_flow_display = MagicMock(return_value=False)
        with patch('ae.gui.app.MainAppBase.help_flow_display', MagicMock(return_value=True)):
            assert not app_test.change_flow('test_flow_id', count=3)
            assert len(app_test.help_flow_display.mock_calls)
            assert app_test.help_flow_display.mock_calls[0] == call(
                {'new_flow_id': 'test_flow_id', 'event_kwargs': {}, 'count': 3})

    def test_help_flow_display_basics(self, app_test):
        assert not app_test.help_flow_display({})
        assert not app_test.help_flow_display({}, changed=True)

        app_test.help_layout = MagicMock()
        new_flow_id = 'hlp_flo:id'
        help_vars = dict(new_flow_id=new_flow_id)

        app_test.framework_win = MagicMock()
        app_test.framework_win.children = []
        assert app_test.help_flow_display(help_vars)
        assert not app_test.help_flow_display(help_vars, changed=True)

        app_test.displayed_help_id = id_of_flow_help(new_flow_id)
        assert app_test.help_flow_display(help_vars)
        assert not app_test.help_flow_display(help_vars, changed=True)

        app_test.framework_win = MagicMock()
        with patch('ae.gui.utils.translation', lambda msg_id: True):
            assert not app_test.help_flow_display(help_vars)

    def test_help_flow_display_ignored_ids(self, app_test):
        app_test.help_layout = MagicMock()
        app_test.framework_win = MagicMock()
        assert not app_test._closing_popup_open_flow_id
        assert not app_test.help_flow_display(dict(new_flow_id=id_of_flow('close', 'flow_popup')))
        app_test.flow_path.append(id_of_flow('do', 'anything'))
        assert not app_test.help_flow_display(dict(new_flow_id=id_of_flow('close', 'flow_popup')), changed=True)
        assert app_test._closing_popup_open_flow_id
        assert not app_test.help_flow_display(dict(new_flow_id=id_of_flow('close', 'flow_popup')), changed=True)

    def test_help_flow_display_next_help_id(self, app_test):
        app_test.framework_win = MagicMock()
        app_test.framework_win.children = []
        flow_id = 'tst_flo_id'
        with patch('ae.gui.utils.translation', lambda msg_id: True):
            app_test.help_flow_display(dict(new_flow_id=flow_id))
            assert flow_id in app_test._next_help_id

    def test_help_flow_display_returns_false(self, app_test):
        with patch('ae.gui.app.MainAppBase.help_flow_display', MagicMock(return_value=False)):
            app_test.framework_win = MagicMock()
            app_test.framework_win.children = []

            assert not app_test.change_flow('tst_flow_id', any_event_arg=True)

            # noinspection PyUnresolvedReferences
            mock_calls = app_test.help_flow_display.mock_calls
            assert len(mock_calls) == 1
            assert mock_calls[0] == call({'new_flow_id': 'tst_flow_id', 'event_kwargs': {'any_event_arg': True}})

    def test_help_flow_display_returns_true(self, app_test):
        with patch('ae.gui.app.MainAppBase.help_flow_display', MagicMock(return_value=True)):
            app_test.framework_win = MagicMock()
            app_test.framework_win.children = []

            assert not app_test.change_flow('tst_flow_id', any_event_arg=True)

            # noinspection PyUnresolvedReferences
            mock_calls = app_test.help_flow_display.mock_calls
            assert len(mock_calls) == 1
            assert mock_calls[0] == call({'new_flow_id': 'tst_flow_id', 'event_kwargs': {'any_event_arg': True}})

    def test_on_flow_popup_close(self, app_test):
        app_test.help_layout = MagicMock()
        assert app_test.on_flow_popup_close("", {})


class TourTestLayout:
    """ fake tour overlay layout for testing """
    def __init__(self):
        class _PlaceholderWid:
            x, y, width, height = 0, 0, 69, 69

        self.explained_widget = None
        self.explained_placeholder = _PlaceholderWid()
        self.ids = MagicMock()
        self.ids.explained_placeholder = self.explained_placeholder
        self.tip_text = None
        self.next_text = None
        self.prev_text = None

        self.setup_app_flow_called = 0
        self.page_updated_called = 0

    def page_updated(self):
        """ callback from tour.setup_layout() to layout """
        self.page_updated_called += 1

    def setup_app_flow(self):
        """ setup page method """
        # not needed by unit tests: self.setup_app_flow_called += 1


@pytest.fixture
def app_tour(app_test):
    """ create an app instance for testing while restoring ae.core app environment after a test run. """
    app_test.tour_layout = TourTestLayout()
    tour = TourBase(app_test)
    yield tour


class TestTourBase:
    def test_init(self, app_tour):
        assert app_tour.layout
        assert app_tour.main_app
        assert isinstance(app_tour.page_data, dict)
        assert app_tour.page_idx == 0

    def test_auto_switch_pages_end(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2']
        app_tour.page_idx = 1
        app_tour.auto_switch_pages = True
        cancel_called = False

        class _CallRequest:
            @staticmethod
            def cancel():
                """ call cancel method """
                # NOT called by this unit test
                nonlocal cancel_called
                cancel_called = True            # pragma: no cover
        app_tour._auto_switch_page_request = _CallRequest()

        app_tour._auto_switch_page_request = False
        app_tour.main_app.call_method_delayed = lambda delay, method: method == app_tour.prev_page

        with pytest.raises(AssertionError):
            app_tour.next_page()
        app_tour.request_auto_page_switch()

        assert cancel_called is False
        assert app_tour.auto_switch_pages is False
        assert app_tour._auto_switch_page_request is False

    def test_auto_switch_pages_ping_pong(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2']
        app_tour.auto_switch_pages = 1
        cancel_called = False

        class _CallRequest:
            @staticmethod
            def cancel():
                """ call cancel method """
                nonlocal cancel_called
                cancel_called = True            # pragma: no cover
        app_tour._auto_switch_page_request = _CallRequest()

        app_tour.page_idx = 1       # the first check bouncing back to prev on the last page
        app_tour._auto_switch_page_request = None
        app_tour.main_app.call_method_delayed = lambda delay, method: method == app_tour.prev_page

        with pytest.raises(AssertionError):
            app_tour.next_page()
        app_tour.request_auto_page_switch()

        assert cancel_called is False
        assert app_tour.auto_switch_pages == -1
        assert app_tour._auto_switch_page_request is True

        app_tour.page_idx = 0       # now check bounce back to forward/next on the first tour page
        app_tour._auto_switch_page_request = None
        app_tour.main_app.call_method_delayed = lambda delay, method: method == app_tour.next_page

        with pytest.raises(AssertionError):
            app_tour.prev_page()
        app_tour.request_auto_page_switch()

        assert cancel_called is False
        assert app_tour.auto_switch_pages == 1
        assert app_tour._auto_switch_page_request is True

    def test_cancel_auto_page_switch_request(self, app_tour):
        app_tour.auto_switch_pages = True
        cancel_called = False

        class _CallRequest:
            @staticmethod
            def cancel():
                """ call cancel method """
                nonlocal cancel_called
                cancel_called = True

        app_tour._auto_switch_page_request = _CallRequest()

        app_tour.cancel_auto_page_switch_request()

        assert cancel_called is True
        assert app_tour.auto_switch_pages is False
        assert app_tour._auto_switch_page_request is None

    def test_load_page_data(self, app_tour):
        assert app_tour.page_data.get('help_vars') == {}
        app_tour.page_idx = 0
        with pytest.raises(AssertionError):
            app_tour.load_page_data()

        app_tour.page_ids = ['page_id_1']
        app_tour.page_idx = 0
        app_tour.load_page_data()
        assert app_tour.page_data
        assert 'help_vars' in app_tour.page_data
        assert app_tour.page_data['tip_text'] is None

        default_language('en')

        app_tour.page_ids = [id_of_flow('open', 'user_preferences')]
        app_tour.load_page_data()
        assert app_tour.page_data
        assert '' in app_tour.page_data
        assert app_tour.page_data['']
        assert 'help_vars' in app_tour.page_data
        assert 'help_translation' not in app_tour.page_data['help_vars']

        flow_id = id_of_flow('close', 'popup')
        tour_tooltip_text = "app tour tooltip text"
        app_tour.page_ids = [flow_id]
        LOADED_TRANSLATIONS['en']['tour_page#' + flow_id] = tour_tooltip_text
        app_tour.load_page_data()
        assert app_tour.page_data
        assert app_tour.page_data['tip_text']
        assert app_tour.page_data['tip_text'] == tour_tooltip_text
        assert 'help_vars' in app_tour.page_data
        assert 'help_translation' in app_tour.page_data['help_vars']
        assert app_tour.page_data['help_vars']['help_translation']

    def test_next_page(self, app_tour):
        assert app_tour.page_idx == 0
        with pytest.raises(AssertionError):
            app_tour.next_page()

        app_tour.page_idx = 0
        app_tour.page_ids = ['page_id1', 'page_id2']
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.help_activator = MagicMock()

        app_tour.next_page()

        assert app_tour.page_idx == 1

    def test_prev_page(self, app_tour):
        assert app_tour.page_idx == 0
        with pytest.raises(AssertionError):
            app_tour.prev_page()

        app_tour.page_ids = ['page_id1', 'page_id2']
        app_tour.page_idx = 1
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.help_activator = MagicMock()

        app_tour.prev_page()

        assert app_tour.page_idx == 0

        app_tour.page_idx = 1
        app_tour.main_app.flow_path.append(id_of_flow('open', 'anything'))
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_win = MagicMock()
        app_tour.prev_page()
        assert app_tour.page_idx == 0
        app_tour.main_app.flow_path.remove(id_of_flow('open', 'anything'))

    def test_request_auto_page_switch(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2']
        app_tour.page_idx = 0
        app_tour.main_app.call_method_delayed = lambda *args: args

        assert not app_tour._auto_switch_page_request
        app_tour.request_auto_page_switch()
        assert app_tour._auto_switch_page_request
        assert app_tour._auto_switch_page_request[1] == app_tour.next_page

    def test_setup_explained_widget_callable_matcher(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []
        f_id = 'test_flow_id'
        app_tour.pages_explained_matchers = dict(page_id2=lambda _w: getattr(_w, 'tap_flow_id', '') == f_id)

        class _Widget:
            children = []
            tap_flow_id = f_id
            x, y, width, height = 0, 0, 99, 99
        wid = _Widget()
        app_tour.main_app.framework_win.children.append(wid)

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is wid

    def test_setup_explained_widget_eval_matcher(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []
        f_id = 'test_flow_id'
        app_tour.pages_explained_matchers = dict(page_id2="lambda _w: getattr(_w, 'tap_flow_id', '') == '" + f_id + "'")

        class _Widget:
            children = []
            tap_flow_id = f_id
            x, y, width, height = 0, 0, 99, 99
        wid = _Widget()
        app_tour.main_app.framework_win.children.append(wid)

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is wid

    def test_setup_explained_widget_id_matcher(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1

        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()

        app_tour.main_app.framework_root = root = MagicMock()
        root.children = []
        root.container = root
        win.children = [root]

        wid_id = 'wid_tst_id'
        app_tour.pages_explained_matchers = dict(page_id2=wid_id)
        wid = MagicMock()
        wid.id = wid_id
        root.ids = {wid_id: wid}
        root.children = [wid]

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is wid

    def test_setup_explained_widget_id_matcher_without_container(self, app_tour):
        assert app_tour.layout.explained_widget is None

        page_id = 'page_id2'
        wid_id = 'wid_tst_id'
        app_tour.pages_explained_matchers = {page_id: wid_id}

        wid = MagicMock()
        wid.id = wid_id

        app_tour.main_app.framework_root = root = MagicMock()
        delattr(root, 'container')
        root.children = [wid]
        root.ids = {wid_id: wid}

        app_tour.main_app.framework_win = win = MagicMock()
        delattr(win, 'container')
        win.children = [root]

        app_tour.page_ids = ['page_id1', page_id, 'page_id3']
        app_tour.page_idx = 1

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is wid

    def test_setup_explained_widget_with_flow_id(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []
        f_id = 'test_flow_id'
        app_tour.pages_explained_matchers = dict(page_id2=f_id)

        class _Widget:
            children = []
            tap_flow_id = f_id
            x, y, width, height = 0, 0, 99, 99
        wid = _Widget()
        app_tour.main_app.framework_win.children.append(wid)

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is wid

    def test_setup_explained_widget_multiple(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        app_tour.main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []
        f_id = 'test_flow_id'
        app_tour.pages_explained_matchers = dict(page_id2=(f_id, f_id))

        class _Widget:
            children = []
            tap_flow_id = f_id
            x, y, width, height = 0, 0, 99, 99
        wid = _Widget()
        app_tour.main_app.framework_win.children.append(wid)

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is app_tour.layout.explained_placeholder

    def test_setup_explained_widget_not_found(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        main_app = app_tour.main_app
        main_app.framework_win = win = MagicMock()
        win.container = win  # needed for widget_children()
        win.children = []
        main_app.framework_root = MagicMock()
        main_app.framework_root.children = []
        main_app.framework_root.ids = {}    # prevent that framework_root MagicMock returns other MagicMock
        wid_id = 'wid_not_existing'
        app_tour.pages_explained_matchers = dict(page_id2=wid_id)
        main_app.help_activator = MagicMock()

        app_tour.setup_explained_widget()

        assert app_tour.layout.explained_widget is main_app.help_activator

    def test_setup_layout(self, app_tour):
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3']
        app_tour.page_idx = 1
        app_tour.main_app.framework_win = MagicMock()
        app_tour.main_app.framework_win.children = []
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []

        class _Widget:
            x, y, width, height = 0, 0, 99, 99
        wid = _Widget()
        app_tour.main_app.help_activator = wid

        assert not app_tour.layout.explained_widget
        assert not app_tour.layout.tip_text
        assert not app_tour.layout.next_text
        assert not app_tour.layout.prev_text

        app_tour.page_data[''] = "test text"
        app_tour.page_data['back_text'] = "back button text"
        app_tour.page_data['next_text'] = "next button text"
        app_tour.page_data['help_vars'] = {}
        app_tour.setup_layout()

        assert app_tour.layout.explained_widget == wid
        assert app_tour.layout.tip_text
        assert app_tour.layout.next_text
        assert app_tour.layout.prev_text

        app_tour.page_idx = 0
        app_tour.setup_layout()
        assert app_tour.layout.next_text
        assert not app_tour.layout.prev_text

        app_tour.page_idx = 2
        app_tour.auto_switch_pages = True
        self.request_auto_page_switch_called = False
        app_tour.request_auto_page_switch = lambda *_args: setattr(self, 'request_auto_page_switch_called', True)
        app_tour.setup_layout()
        assert not app_tour.layout.next_text
        assert app_tour.layout.prev_text
        assert self.request_auto_page_switch_called is True

    def test_setup_texts_tip(self, app_tour):
        tt = "tip txt"
        app_tour.page_data['tip_text'] = tt
        app_tour.setup_texts()
        assert app_tour.layout.tip_text == tt

    def test_setup_texts_tip_via_id(self, app_tour):
        tt = "=page_id"
        app_tour.page_data['tip_text'] = tt

        class _Win:
            children = []
        app_tour.main_app.framework_win = _Win()
        app_tour.setup_texts()
        assert app_tour.layout.tip_text == ""

    def test_setup_texts_title(self, app_tour):
        tt = "tle txt"
        app_tour.page_data['title_text'] = tt
        app_tour.setup_texts()
        assert app_tour.layout.title_text == tt

    def test_setup_texts_popup2root_mapping(self, app_tour):
        app_tour.top_popup = pu = MagicMock()
        app_tour.page_data['title_text'] = "{root}"
        app_tour.setup_texts()
        assert app_tour.layout.title_text == str(pu)

    def test_start(self, app_tour):
        app_tour.main_app.framework_root = MagicMock()
        app_tour.main_app.framework_root.children = []
        app_tour.main_app.framework_win = MagicMock()
        app_tour.main_app.framework_win.children = []
        app_tour.main_app.help_activator = MagicMock()
        app_tour.page_ids = ['page_id1', 'page_id2', 'page_id3', 'page_id4']
        app_tour.page_idx = 3
        app_tour.start()
        assert app_tour.page_idx == 3

    def test_stop(self, app_tour):
        app_tour._delayed_setup_layout_call = MagicMock()
        app_tour.stop()
        assert app_tour.page_idx == 0
        assert app_tour._delayed_setup_layout_call is None


@pytest.fixture
def dropdown_from_button_tour(app_test):
    """ create a dropdown tour instance. """
    app_test.tour_layout = TourTestLayout()
    tour = TourDropdownFromButton(app_test)
    yield tour


class TestTourDropdownFromButton:
    def test_init(self, dropdown_from_button_tour):
        assert dropdown_from_button_tour.determine_page_ids
        assert dropdown_from_button_tour.layout
        assert dropdown_from_button_tour.main_app
        assert isinstance(dropdown_from_button_tour.page_data, dict)
        assert dropdown_from_button_tour.page_idx == 0

    def test_setup_app_flow_next(self, dropdown_from_button_tour):
        main_app = dropdown_from_button_tour.main_app
        flow_id = id_of_flow('open', 'x')
        dropdown_from_button_tour.page_ids = [flow_id, dropdown_from_button_tour.determine_page_ids]
        dropdown_from_button_tour.last_page_idx = 0
        dropdown_from_button_tour.page_idx = 1
        main_app.on_x_open = lambda *_args: True
        main_app.framework_win = MagicMock()
        main_app.framework_win.children = []
        main_app.framework_root = MagicMock()
        main_app.framework_root.children = []
        main_app.help_activator = MagicMock()

        dropdown_from_button_tour.setup_app_flow()
        assert main_app.flow_path[-1] == flow_id

    def test_setup_app_flow_prev(self, dropdown_from_button_tour):
        main_app = dropdown_from_button_tour.main_app
        flow_id = id_of_flow('open', 'y')
        dropdown_from_button_tour.page_ids = [flow_id, dropdown_from_button_tour.determine_page_ids]
        dropdown_from_button_tour.last_page_idx = 1
        dropdown_from_button_tour.page_idx = 0
        main_app.framework_root = MagicMock()
        main_app.framework_root.children = []
        main_app.framework_win = MagicMock()
        main_app.framework_win.children = []
        main_app.help_activator = MagicMock()

        class _Dropdown:
            children = []

            def open(self):
                """ open method"""
                main_app.framework_win.children.append(self)

            def close(self):
                """ close method """
                main_app.framework_win.children.remove(self)

        _Dropdown().open()
        assert main_app.framework_win.children
        dropdown_from_button_tour.setup_app_flow()
        assert not main_app.framework_win.children

    def test_setup_layout(self, dropdown_from_button_tour):
        main_app = dropdown_from_button_tour.main_app
        flow_id = id_of_flow('open', 'y')
        app_state_name = 'name_of_state'
        dropdown_from_button_tour.page_ids = [flow_id, dropdown_from_button_tour.determine_page_ids]
        dropdown_from_button_tour.page_idx = 1
        main_app.framework_root = MagicMock()
        main_app.framework_root.children = []
        main_app.framework_win = MagicMock()
        main_app.framework_win.children = []
        main_app.help_activator = MagicMock()

        class _Dropdown:
            children = []

            def open(self):
                """ open method - to be recognized as a popup """
                main_app.framework_win.children.append(self)

            def close(self):
                """ close method """
                main_app.framework_win.children.remove(self)    # pragma: no cover

        class _Child:
            """ child class """
            width = 333
            height = 111

        dd = _Dropdown()
        c1 = _Child()
        c1.tap_flow_id = flow_id
        dd.children.append(c1)
        c2 = _Child()
        c2.app_state_name = app_state_name
        dd.children.append(c2)
        dd.open()
        dropdown_from_button_tour.top_popup = main_app.popups_opened()[0]
        main_app.help_activator = MagicMock()

        dropdown_from_button_tour.setup_layout()

        assert TourDropdownFromButton.determine_page_ids not in dropdown_from_button_tour.page_ids
        assert len(dropdown_from_button_tour.page_ids) == 3

    def test_setup_layout_no_dropdown(self, dropdown_from_button_tour):
        main_app = dropdown_from_button_tour.main_app
        flow_id = id_of_flow('open', 'y')
        dropdown_from_button_tour.page_ids = [flow_id, dropdown_from_button_tour.determine_page_ids]
        dropdown_from_button_tour.page_idx = 1

        class _Win:
            children = []
        main_app.framework_win = _Win()
        main_app.framework_root = _Win()
        main_app.help_activator = MagicMock()

        dropdown_from_button_tour.setup_layout()

        assert TourDropdownFromButton.determine_page_ids in dropdown_from_button_tour.page_ids
        assert len(dropdown_from_button_tour.page_ids) == 2

    def test_setup_layout_no_children(self, dropdown_from_button_tour):
        main_app = dropdown_from_button_tour.main_app
        flow_id = id_of_flow('open', 'y')
        app_state_name = 'name_of_state'
        dropdown_from_button_tour.page_ids = [flow_id, dropdown_from_button_tour.determine_page_ids]
        dropdown_from_button_tour.page_idx = 1
        main_app.framework_root = MagicMock()
        main_app.framework_root.children = []
        main_app.framework_win = MagicMock()
        main_app.framework_win.children = []

        class _Dropdown:
            children = []

            def open(self):
                """ open method"""
                main_app.framework_win.children.append(self)

            def close(self):
                """ close method """
                main_app.framework_win.children.remove(self)    # pragma: no cover

        class _Child:
            """ child class """
            width = 999
            height = 0

        dd = _Dropdown()
        c1 = _Child()
        c1.tap_flow_id = flow_id
        dd.children.append(c1)
        c2 = _Child()
        c2.app_state_name = app_state_name
        dd.children.append(c2)
        dd.open()
        dropdown_from_button_tour.top_popup = dd
        main_app.help_activator = MagicMock()

        dropdown_from_button_tour.setup_layout()

        assert TourDropdownFromButton.determine_page_ids in dropdown_from_button_tour.page_ids
        assert len(dropdown_from_button_tour.page_ids) == 2


@pytest.fixture
def onboarding_tour(app_test):
    """ create a dropdown tour instance. """
    app_test.tour_layout = TourTestLayout()
    tour = OnboardingTour(app_test)
    yield tour


class TestTourOnboarding:
    def test_init(self, onboarding_tour):
        assert onboarding_tour.layout
        assert onboarding_tour.main_app
        assert isinstance(onboarding_tour.page_data, dict)
        assert onboarding_tour.page_idx == 0

    def test_init_after_lots_tour_starts(self, app_test):
        app_test.get_variable = lambda *_a, **_k: 9
        app_test.tour_layout = TourTestLayout()
        tour = OnboardingTour(app_test)

        assert tour.layout is app_test.tour_layout
        assert tour.main_app is app_test
        assert tour.page_idx > 0

    def test_setup_app_flow_layout_font_size(self, onboarding_tour):
        flo_id = id_of_flow('open', 'user_preferences')
        onboarding_tour.main_app.framework_root = MagicMock()
        onboarding_tour.main_app.framework_win = MagicMock()
        onboarding_tour.main_app.framework_win.container = onboarding_tour.main_app.framework_win
        onboarding_tour.main_app.framework_win.children = []
        onboarding_tour.main_app.help_activator = MagicMock()
        onboarding_tour.page_idx = onboarding_tour.page_ids.index('layout_font_size')
        onboarding_tour.main_app.widget_by_flow_id = lambda f_id: f_id
        onboarding_tour.main_app.change_flow = lambda f_id, **_kws: setattr(onboarding_tour, 'tst_f_id', f_id)
        onboarding_tour.setup_app_flow()
        # noinspection PyUnresolvedReferences
        assert onboarding_tour.tst_f_id == flo_id

    def test_setup_app_flow_user_registration(self, onboarding_tour):
        flo_id = id_of_flow('open', 'user_name_editor')
        onboarding_tour.main_app.framework_root = MagicMock()
        onboarding_tour.main_app.framework_win = MagicMock()
        onboarding_tour.main_app.framework_win.container = onboarding_tour.main_app.framework_win
        onboarding_tour.main_app.framework_win.children = []
        onboarding_tour.main_app.help_activator = MagicMock()
        onboarding_tour.page_idx = onboarding_tour.page_ids.index('user_registration')
        onboarding_tour.layout.stop_tour = lambda: setattr(onboarding_tour, '_called_stop_tour', True)
        onboarding_tour.main_app.change_flow = lambda f_id, **_kws: setattr(onboarding_tour, 'tst_f_id', f_id)
        onboarding_tour.setup_app_flow()
        # noinspection PyUnresolvedReferences
        assert onboarding_tour.tst_f_id == flo_id

    def test_teardown_app_flow_font_size(self, onboarding_tour):
        onboarding_tour.page_idx = onboarding_tour.page_ids.index('layout_font_size')

        class _Popup:
            def close(self):
                """ mock of popup close method """
                onboarding_tour.tst_close_called = self
            _real_dismiss = close

        popup = _Popup()
        onboarding_tour.top_popup = popup
        onboarding_tour.teardown_app_flow()

        # noinspection PyUnresolvedReferences
        assert onboarding_tour.tst_close_called is popup

    def test_update_page_ids_page_switching(self, onboarding_tour):
        assert 'page_switching' in onboarding_tour.page_ids
        remove_page_idx = onboarding_tour.page_ids.index('page_switching')
        neighbour_page_idx = remove_page_idx + 1
        onboarding_tour.last_page_idx = remove_page_idx
        onboarding_tour.page_idx = neighbour_page_idx

        onboarding_tour.update_page_ids()

        assert 'page_switching' not in onboarding_tour.page_ids
        assert onboarding_tour.last_page_idx == remove_page_idx - 1
        assert onboarding_tour.page_idx == neighbour_page_idx - 1

    def test_update_page_ids_page_switching_came_back(self, onboarding_tour):
        assert 'page_switching' in onboarding_tour.page_ids
        remove_page_idx = onboarding_tour.page_ids.index('page_switching')
        neighbour_page_idx = remove_page_idx - 1
        onboarding_tour.last_page_idx = remove_page_idx
        onboarding_tour.page_idx = neighbour_page_idx

        onboarding_tour.update_page_ids()

        assert 'page_switching' not in onboarding_tour.page_ids
        assert onboarding_tour.last_page_idx == remove_page_idx
        assert onboarding_tour.page_idx == neighbour_page_idx

    def test_update_page_ids_page_switching_removed(self, onboarding_tour):
        assert 'page_switching' in onboarding_tour.page_ids
        remove_page_idx = onboarding_tour.page_ids.index('page_switching')
        neighbour_page_idx = remove_page_idx + 1
        onboarding_tour.page_ids.remove('page_switching')
        assert 'page_switching' not in onboarding_tour.page_ids
        onboarding_tour.last_page_idx = remove_page_idx
        onboarding_tour.page_idx = neighbour_page_idx

        onboarding_tour.update_page_ids()

        assert onboarding_tour.last_page_idx == remove_page_idx
        assert onboarding_tour.page_idx == neighbour_page_idx


class TestTourRegister:
    # noinspection PyUnusedLocal
    def test_register_tour_class(self):
        reg_count = len(REGISTERED_TOURS)

        class Tst1Tour(TourBase):
            """ test tour class 1 """

        assert len(REGISTERED_TOURS) == reg_count + 1

    def test_tour_id_class(self):
        # using the tour class _Tst1Tour from the last test method
        assert tour_id_class(id_of_flow('open', 'tst1'))


class TestTourUserPreferences:
    def test_init(self, app_test):
        app_test.tour_layout = TourTestLayout()
        tour = UserPreferencesTour(app_test)

        assert tour.auto_switch_pages
        assert tour.page_data
        assert TourDropdownFromButton.determine_page_ids in tour.page_ids
        assert _OPEN_USER_PREFERENCES_FLOW_ID in tour.page_ids
