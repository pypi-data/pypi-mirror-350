""" test ae.gui.app module """
from configparser import ConfigParser, ExtendedInterpolation
from typing import Callable, Any, Union

from unittest.mock import MagicMock, patch

from ae.gui import register_package_images, register_package_sounds
from conftest import skip_gitlab_ci

from ae.base import INI_EXT, UNSET, norm_path, os_user_name
from ae.paths import normalize, FilesRegister
from ae.core import DEBUG_LEVELS, DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_ENABLED
from ae.console import USER_NAME_MAX_LEN
from ae.updater import MOVES_SRC_FOLDER_NAME

from ae.gui.utils import (
    APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME, MAX_FONT_SIZE, MIN_FONT_SIZE,
    flow_key, id_of_flow, replace_flow_action)
from ae.gui.app import MainAppBase

from tst_constants import *


VER_VAR = APP_STATE_VERSION_VAR_NAME        # == 'app_state_version'
VER_INI_VAL = 4
VER_SET_VAL = 69
TST_VAR = 'tst_var'
TST_VAL = 'tstVal'
TST_DICT = {VER_VAR: VER_INI_VAL, TST_VAR: TST_VAL}


def _create_ini_file(fn):
    write_file(fn, f"[{APP_STATE_SECTION_NAME}]"
                   f"\n{VER_VAR} = {VER_INI_VAL}"
                   f"\n{TST_VAR} = {TST_VAL}")


@pytest.fixture
def ini_file(restore_app_env):
    """ provide a test config file """
    fn = "tests/tst" + INI_EXT
    _create_ini_file(fn)
    yield fn
    if os.path.exists(fn):      # some exception/error-check tests need to delete the INI
        os.remove(fn)


class FrameworkApp:
    """ gui framework app stub """
    def __init__(self):
        self.app_states = {}
        self.landscape = False
        self.mixed_back_ink = []

    def start_event_loop(self):
        """ start the GUI event loop. """

    def stop_event_loop(self):
        """ stop the GUI event loop. """


class MainWindow:
    """ gui framework main window class stub """
    def __init__(self):
        self.children = []

    def close(self):
        """ app close method """


class RootLayout:
    """ gui framework root layout class stub """
    def __init__(self):
        self.children = []


setattr(FrameworkApp, 'app_state_' + VER_VAR, None)
setattr(FrameworkApp, 'app_state_' + TST_VAR, None)


class ImplementationOfMainApp(MainAppBase):
    """ test abc implementation stub class """
    app_state_save_called = False
    app_state_version_upgrade_call_counter = 0
    app_state_version_upgrade_last_version = -1
    build_called = False
    started_called = False
    load_state_called = False
    init_called = False
    run_called = False
    setup_state_called = False
    flow_id_called = False
    flow_path_called = False
    font_size_called = False
    key_press_called = False
    hot_key_case_called = False
    hot_key_lower_called = False

    tst_var: str = ""
    font_size: float = 0.0
    ensure_top_most_z_index_called: int = 0

    framework_app: FrameworkApp = None
    framework_win: MainWindow = None
    framework_root: RootLayout = None

    def init_app(self, _framework_app_class=None):
        """ init app
        :param _framework_app_class:    not used in unit tests.
        """
        self.framework_app = FrameworkApp()
        self.framework_win = MainWindow()
        self.framework_root = RootLayout()
        self.init_called = True
        self.call_method('on_app_run')
        self.call_method('on_app_build')
        self.tst_var = ""

        return self.framework_app.start_event_loop, self.framework_app.stop_event_loop

    def call_method_delayed(self, _delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ implement delayed callback - ignoring delay arg for tests. """
        return self.call_method(callback, *args, **kwargs)

    def call_method_repeatedly(self, _interval: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ implement repeated callback - repeating test calls are done by the UI-specific framework. """
        return self.call_method(callback, *args, **kwargs)      # pragma: no cover

    def ensure_top_most_z_index(self, _widget: Any):
        """ MainAppBase abstract method implementation """
        self.ensure_top_most_z_index_called += 1                # pragma: no cover

    def help_activation_toggle(self):
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """

    def load_app_states(self):
        """ get app state """
        self.load_state_called = True
        super().load_app_states()

    def setup_app_states(self, app_states: dict[str, Any], send_event: bool = True):
        """ setup app state """
        self.setup_state_called = True
        super().setup_app_states(app_states, send_event=send_event)

    def on_app_run(self):
        """ init app """
        super().on_app_run()
        self.run_called = True

    def on_app_build(self):
        """ build app """
        super().on_app_build()
        self.build_called = True
        self.on_app_started()

    def on_app_started(self):
        """ app fully started event handler """
        super().on_app_started()
        self.started_called = True

    def on_app_state_tst_var_save(self, font_size: float) -> float:
        """ test save event for TST_VAR app state. """
        self.app_state_save_called = True
        return font_size

    def on_app_state_version_upgrade(self, version: int):
        """ test app state version upgrade. """
        self.app_state_version_upgrade_call_counter += 1
        self.app_state_version_upgrade_last_version = version
        super().on_app_state_version_upgrade(version)

    def on_flow_id(self):
        """ flow id changed. """
        self.flow_id_called = True

    def on_flow_path(self):
        """ the flow path changed. """
        self.flow_path_called = True

    def on_font_size(self):
        """ font size changed. """
        self.font_size_called = True

    def on_key_press(self, _mod, _key):
        """ dispatched key press event """
        self.key_press_called = True
        return super().on_key_press(_mod, _key)

    # noinspection PyPep8Naming
    def on_key_press_of_Alt_A(self):
        """ test hot key event """
        self.hot_key_case_called = True
        return True

    def on_key_press_of_ctrl_t(self):
        """ test hot key event used/processed and lower method name event """
        self.hot_key_lower_called = True
        return False        # test isn't processed/used hot key

    def on_key_press_of_meta_z(self):
        """ test hot key lower method name event """
        self.hot_key_lower_called = True
        return True


class TestProperties:
    def test_color_attr_names(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert len(app.color_attr_names) == 0

        with patch("ae.gui.app.MainAppBase.app_state_keys", lambda *_args: ('any_xy_ink', 'any_other_app_state_var')):
            assert len(app.color_attr_names) == 1
            assert 'any_xy_ink' in app.color_attr_names


class TestCallbacks:
    def test_setup_app_states(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.setup_state_called

    def test_load_app_states(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.load_state_called

    def test_build(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.build_called

    def test_init(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.init_called

    def test_run(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.run_called

    def test_flow_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert not app.flow_id_called
        app.on_flow_id()
        assert app.flow_id_called

    def test_flow_path(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert not app.flow_path_called
        app.on_flow_path()
        assert app.flow_path_called

    def test_font_size(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert not app.font_size_called
        app.on_font_size()
        assert app.font_size_called

    def test_key_press_of_empty_mod_and_key(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.key_press_from_framework("", "") is False
        assert not app.hot_key_case_called
        assert not app.hot_key_lower_called
        assert app.key_press_called

    def test_hot_key_case_sensitive(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.key_press_from_framework("Alt", "A")
        assert app.hot_key_case_called
        assert not app.hot_key_lower_called
        assert not app.key_press_called

    def test_hot_key_lower_case(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.key_press_from_framework("Meta", "Z")
        assert not app.hot_key_case_called
        assert app.hot_key_lower_called
        assert not app.key_press_called

    def test_hot_key_not_processed_in_lower_case(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.key_press_from_framework("Ctrl", "t") is False
        assert not app.hot_key_case_called
        assert app.hot_key_lower_called     # gets called, but because not processed also on_key_press will be called
        assert app.key_press_called

    def test_on_app_state_version_upgrade(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.on_app_state_version_upgrade(4)

    def test_on_debug_level_change(self, restore_app_env):
        app = ImplementationOfMainApp()

        old_level = app.debug_level
        app.on_debug_level_change(DEBUG_LEVELS[0], {})
        assert app.debug_level == DEBUG_LEVEL_DISABLED

        app.on_debug_level_change(DEBUG_LEVELS[1], {})
        assert app.debug_level == DEBUG_LEVEL_ENABLED

        app.on_debug_level_change(DEBUG_LEVELS[old_level], {})
        assert app.debug_level == old_level

    def test_on_flow_id_ink(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = 0

        def _patched_mix_background_ink():
            nonlocal called
            called += 1
        app.mix_background_ink = _patched_mix_background_ink

        assert not called
        app.on_flow_id_ink()
        assert called == 1

    def test_on_flow_path_ink(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = 0

        def _patched_mix_background_ink():
            nonlocal called
            called += 1
        app.mix_background_ink = _patched_mix_background_ink

        assert not called
        app.on_flow_path_ink()
        assert called == 1

    def test_on_flow_popup_close(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_flow_popup_close('flow_id', {})

    def test_on_lang_code_change(self, restore_app_env):
        app = ImplementationOfMainApp()

        old_lang = app.lang_code

        app.on_lang_code_change('xx', {})
        assert app.lang_code == 'xx'

        app.on_lang_code_change(old_lang, {})
        assert app.lang_code == old_lang or 'xx'    # when old_lang is empty string then 'xx' should be kept

    def test_on_light_theme_change(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.on_light_theme_change('', dict(light_theme=False))
        assert not app.light_theme

        app.on_light_theme_change('', dict(light_theme=True))
        assert app.light_theme

    def test_on_key_press(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_key_press("", "") is False
        with patch('ae.gui.app.MainAppBase.popups_opened', lambda *_args: (MagicMock(), )):
            assert app.on_key_press("", "escape") is True

    def test_on_selected_ink(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = 0

        def _patched_mix_background_ink():
            nonlocal called
            called += 1
        app.mix_background_ink = _patched_mix_background_ink

        assert not called
        app.on_selected_ink()
        assert called == 1

    def test_on_theme_change(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_theme_change("Pastel", {}) is True

    def test_on_theme_delete(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_theme_delete("Pastel", {}) is True

    def test_on_theme_save(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_theme_save("Pastel", {}) is True

        app.theme_names.append("TstTheme")
        assert app.on_theme_save("TstTheme", {}) is False   # show_confirmation fails

    def test_on_theme_update(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.on_theme_update("Pastel", {}) is True

    def test_on_unselected_ink(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = 0

        def _patched_mix_background_ink():
            nonlocal called
            called += 1
        app.mix_background_ink = _patched_mix_background_ink

        assert not called
        app.on_unselected_ink()
        assert called == 1

    def test_on_user_register_args(self, restore_app_env):
        app = ImplementationOfMainApp()
        call_count = 0

        def _callback(*_args, **_kwargs):
            nonlocal call_count
            call_count += 1
        app.show_message = _callback

        def _register_user(new_user_id: str = "", **_kwargs):
            if new_user_id not in app.registered_users:
                app.registered_users.append(new_user_id)
            return True

        app.register_user = _register_user

        assert call_count == 0
        assert app.user_id == os_user_name()
        assert app.registered_users == []

        assert not app.on_user_register('', {})
        assert len(app.registered_users) == 0
        assert call_count == 1

        assert app.on_user_register('x' * USER_NAME_MAX_LEN, {})
        assert call_count == 1
        app.registered_users = []

        assert not app.on_user_register('x' * (USER_NAME_MAX_LEN + 1), {})
        assert len(app.registered_users) == 0
        assert call_count == 2

        assert not app.on_user_register(' ', {})
        assert len(app.registered_users) == 0
        assert call_count == 3

        assert not app.on_user_register('x y', {})
        assert len(app.registered_users) == 0
        assert call_count == 4

        assert not app.on_user_register('a.b', {})
        assert len(app.registered_users) == 0
        assert call_count == 5

        assert not app.on_user_register('3%3', {})
        assert len(app.registered_users) == 0
        assert call_count == 6

        assert not app.on_user_register('x,y', {})
        assert len(app.registered_users) == 0
        assert call_count == 7

        assert not app.on_user_register('', {})
        assert len(app.registered_users) == 0
        assert call_count == 8

        assert not app.on_user_register('=xy', {})
        assert len(app.registered_users) == 0
        assert call_count == 9

        usr_id = 'xy'
        assert app.on_user_register(usr_id, {})
        assert call_count == 9
        assert len(app.registered_users) == 1
        assert usr_id in app.registered_users

        assert app.on_user_register(usr_id, {})
        assert call_count == 9
        assert len(app.registered_users) == 1
        assert usr_id in app.registered_users

        usr_id = 'x' * (USER_NAME_MAX_LEN - 1)
        assert app.on_user_register(usr_id, {})
        assert call_count == 9
        assert len(app.registered_users) == 2
        assert usr_id in app.registered_users


class TestAppState:
    def test_app_state_keys(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        keys = app.app_state_keys()
        assert isinstance(keys, tuple)
        assert len(keys) >= 2
        assert len(keys) == len(set(keys))
        assert VER_VAR in keys
        assert TST_VAR in keys

    def test_app_state_keys_undef_var(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ), debug_level=DEBUG_LEVEL_ENABLED)
        tst_var = "undefined_tst_var"
        assert not hasattr(app, tst_var)

        app.set_variable(tst_var, "any_value", cfg_fnam=ini_file, section=APP_STATE_SECTION_NAME)
        assert tst_var not in app.app_state_keys()
        assert VER_VAR in app.app_state_keys()
        assert TST_VAR in app.app_state_keys()

    def test_app_state_upgrade_config_moved_or_not_exists(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app._main_cfg_fnam == norm_path(ini_file)

        assert app.app_state_version_upgrade_call_counter == 0
        assert app.app_state_version_upgrade_last_version == -1

    @skip_gitlab_ci  # failing on GitLab CI because app_path='/usr/local/bin' != cwd_path='/builds/ae-group/ae_gui'
    def test_app_state_upgrade_from_bundled_config(self, ini_file, restore_app_env):
        global VER_INI_VAL
        old_val = VER_INI_VAL
        bundled_ini = os.path.join(MOVES_SRC_FOLDER_NAME, os.path.basename(ini_file))
        try:
            VER_INI_VAL = VER_SET_VAL
            os.mkdir(MOVES_SRC_FOLDER_NAME)
            _create_ini_file(bundled_ini)

            app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
            old_app_name = app.app_name
            app.app_name = os.path.splitext(os.path.basename(bundled_ini))[0]
            app.load_app_states()
            app.app_name = old_app_name
            assert app.app_state_version_upgrade_call_counter == VER_SET_VAL - old_val
            assert app.app_state_version_upgrade_last_version == VER_SET_VAL - 1
        finally:
            if os.path.exists(bundled_ini):
                os.remove(bundled_ini)
            if os.path.exists(MOVES_SRC_FOLDER_NAME):
                os.rmdir(MOVES_SRC_FOLDER_NAME)
            VER_INI_VAL = old_val

    def test_app_state_version(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.get_var(VER_VAR, section=APP_STATE_SECTION_NAME) == VER_INI_VAL
        assert app.app_state_version == VER_INI_VAL

        app.change_app_state(VER_VAR, VER_SET_VAL)
        assert app.app_state_version == VER_SET_VAL
        assert app.get_var(VER_VAR, section=APP_STATE_SECTION_NAME) == VER_INI_VAL

        app.change_app_state(VER_VAR, VER_SET_VAL + 1, old_name=UNSET)
        assert app.app_state_version == VER_SET_VAL + 1
        assert app.get_var(VER_VAR, section=APP_STATE_SECTION_NAME) == VER_SET_VAL + 1

    def test_change_app_state(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        # assert app.retrieve_app_states() + light_theme/sound_volume/... == TST_DICT
        assert all(k in app.retrieve_app_states().keys() and app.retrieve_app_states()[k] == v
                   for k, v in TST_DICT.items())

        chg_val = 'ChangedVal'
        chg_dict = {VER_VAR: VER_SET_VAL, TST_VAR: chg_val}
        app.change_app_state(TST_VAR, chg_val)
        app.change_app_state(VER_VAR, VER_SET_VAL)

        assert getattr(app, TST_VAR) == chg_val
        assert getattr(app.framework_app, 'app_state_' + VER_VAR) == VER_SET_VAL
        assert getattr(app.framework_app, 'app_state_' + TST_VAR) == chg_val
        assert all(k in app.framework_app.app_states.keys() and app.framework_app.app_states[k] == v
                   for k, v in chg_dict.items())
        # assert app.retrieve_app_states() == chg_dict
        assert all(k in app.retrieve_app_states().keys() and app.retrieve_app_states()[k] == v
                   for k, v in chg_dict.items())

        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val

    def test_load_app_states(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL

        app.load_app_states()
        assert getattr(app, TST_VAR) == TST_VAL
        assert getattr(app.framework_app, 'app_state_' + VER_VAR) == VER_INI_VAL
        assert all(k in app.framework_app.app_states.keys() and app.framework_app.app_states[k] == v
                   for k, v in TST_DICT.items())
        assert all(k in app.retrieve_app_states().keys() and app.retrieve_app_states()[k] == v
                   for k, v in TST_DICT.items())

    def test_load_app_states_debug_type_warning(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ), debug_level=DEBUG_LEVEL_ENABLED)

        try:
            setattr(app, TST_VAR, -33)
            app.load_app_states()
        finally:
            setattr(ImplementationOfMainApp, TST_VAR, "")   # restore tst_var to not break the following tests
            setattr(app, TST_VAR, "")

    def test_load_app_states_debug_attr_exist_warning(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ), debug_level=DEBUG_LEVEL_ENABLED)
        try:
            delattr(app, TST_VAR)
            delattr(ImplementationOfMainApp, TST_VAR)
            app.load_app_states()
        finally:
            setattr(ImplementationOfMainApp, TST_VAR, "")   # restore tst_var to not break the following tests
            setattr(app, TST_VAR, "")

    def test_load_app_states_type_autocorrection(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ), debug_level=DEBUG_LEVEL_ENABLED)
        try:
            value = "tst"
            app.set_variable(TST_VAR, list(value), cfg_fnam=ini_file, section=APP_STATE_SECTION_NAME)
            app.load_app_states()

            assert type(getattr(app, TST_VAR)) is str
            assert getattr(app, TST_VAR) == str(list(value))
        finally:
            setattr(ImplementationOfMainApp, TST_VAR, "")   # restore tst_var to not break the following tests
            setattr(app, TST_VAR, "")

    def test_load_app_states_undefined_version_default(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        fw_app = app.framework_app
        ver = getattr(app, APP_STATE_VERSION_VAR_NAME)
        assert isinstance(ver, int) and ver == VER_INI_VAL
        assert fw_app.app_states[APP_STATE_VERSION_VAR_NAME] == ver

        assert app.set_variable(APP_STATE_VERSION_VAR_NAME, VER_INI_VAL, section=APP_STATE_SECTION_NAME) == ""

        app.load_app_states()

        assert getattr(app, APP_STATE_VERSION_VAR_NAME) == VER_INI_VAL

    def test_retrieve_app_states(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        for k, v in TST_DICT.items():
            assert k in app.retrieve_app_states().keys()
            assert app.retrieve_app_states()[k] == v

    def test_save_app_states(self, ini_file, restore_app_env):
        global TST_DICT
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        old_dict = TST_DICT.copy()
        try:
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
            for k, v in TST_DICT.items():
                assert k in app.retrieve_app_states().keys()
                assert app.retrieve_app_states()[k] == v

            chg_val = 'ChangedVal'
            TST_DICT = {VER_VAR: VER_SET_VAL, TST_VAR: chg_val}
            setattr(app, VER_VAR, VER_SET_VAL)
            setattr(app, TST_VAR, chg_val)
            assert app.save_app_states() == ""
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val
            for k, v in TST_DICT.items():
                assert k in app.retrieve_app_states().keys()
                assert app.retrieve_app_states()[k] == v
        finally:
            TST_DICT = old_dict

    def test_save_app_states_flow_id_var(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert hasattr(app, 'flow_id')
        assert not app.get_variable('flow_id')
        flo_id = id_of_flow('focus', 'obj', 'key')
        app.change_app_state('flow_id', flo_id, send_event=False)
        assert not app.set_variable('flow_id', flo_id, section=APP_STATE_SECTION_NAME)

        app.save_app_states()

        assert app.get_variable('flow_id', section=APP_STATE_SECTION_NAME) == flo_id

    def test_save_app_states_flow_id_path_cleanup(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        flo_id = id_of_flow('nof', 'obj', 'key')    # any non-focus flow action
        app.change_app_state('flow_id', flo_id, send_event=False)
        assert not app.set_variable('flow_id', flo_id, section=APP_STATE_SECTION_NAME)
        enter_id = id_of_flow('enter', 'obj', 'x')
        flo_path = [enter_id, 'open_something']
        app.change_app_state('flow_path', flo_path, send_event=False)
        assert not app.set_variable('flow_path', flo_path, section=APP_STATE_SECTION_NAME)

        app.save_app_states()

        assert app.get_variable('flow_id', section=APP_STATE_SECTION_NAME) == ''
        assert app.get_variable('flow_path', section=APP_STATE_SECTION_NAME) == [enter_id]

    def test_save_app_state_key_save(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))

        app.save_app_states()

        assert app.app_state_save_called

    def test_save_app_states_debug_sound(self, restore_app_env, capsys):
        app = ImplementationOfMainApp()
        app.debug_level = DEBUG_LEVEL_ENABLED
        assert app.save_app_states() == ""
        assert 'debug_save' in capsys.readouterr()[0]
        app.debug_level = DEBUG_LEVEL_DISABLED

    def test_save_app_states_exception(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        os.remove(ini_file)
        assert app.save_app_states() != ""

    def test_set_flow_path(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert not app.flow_path
        assert not app.flow_path_called

        flow_path = [id_of_flow('action', 'test_obj'), ]
        app.change_app_state('flow_path', flow_path)
        assert app.flow_path == flow_path
        assert app.flow_path_called

    def test_set_font_size(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.font_size == MIN_FONT_SIZE
        assert not app.font_size_called

        font_size = MAX_FONT_SIZE
        app.change_app_state('font_size', font_size)
        assert app.font_size == font_size

    def test_set_scaled_font_size(self, ini_file, restore_app_env):
        cfg_parser = ConfigParser(interpolation=ExtendedInterpolation())
        setattr(cfg_parser, 'optionxform', str)
        cfg_parser.read(ini_file)
        cfg_parser.set(APP_STATE_SECTION_NAME, 'font_size', str(-MIN_FONT_SIZE))
        with open(ini_file, 'w') as configfile:
            # noinspection PyTypeChecker
            cfg_parser.write(configfile)

        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.font_size >= MIN_FONT_SIZE
        assert not app.font_size_called

    def test_set_win_scaled_font_size(self, ini_file, restore_app_env):
        cfg_parser = ConfigParser(interpolation=ExtendedInterpolation())
        setattr(cfg_parser, 'optionxform', str)
        cfg_parser.read(ini_file)
        cfg_parser.set(APP_STATE_SECTION_NAME, 'font_size', str(-1))
        with open(ini_file, 'w') as configfile:
            # noinspection PyTypeChecker
            cfg_parser.write(configfile)

        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.font_size >= MIN_FONT_SIZE
        assert not app.font_size_called

    def test_setup_app_states_tst_vars(self, ini_file, restore_app_env):
        assert ImplementationOfMainApp.tst_var == ""
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert getattr(app, TST_VAR) == TST_VAL
        app.setup_app_states(TST_DICT)
        assert getattr(app, TST_VAR) == TST_VAL

        td = TST_DICT.copy()
        td['flow_id'] = id_of_flow('focus', 'uhu')
        app.setup_app_states(td)
        assert app.flow_id == td['flow_id']


class TestFlow:
    def test_change_flow_undefined(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert not app.change_flow('undefined')
        assert not app.change_flow('undefined', flo='flow')

    def test_change_flow_focus(self, restore_app_env):
        app = ImplementationOfMainApp()

        fid = id_of_flow('focus', 'flow_obj', 'flo_key')
        assert app.change_flow(fid)
        assert app.flow_id == fid

        fid = id_of_flow('focus', 'other_flow_obj', 'other_flo_key')
        assert app.change_flow(fid)
        assert app.flow_id == fid

    def test_change_flow_empty(self, restore_app_env):
        app = ImplementationOfMainApp()

        fid = id_of_flow('')
        assert app.change_flow(fid)
        assert app.flow_id == fid

    def test_change_flow_keep_focus(self, restore_app_env):
        app = ImplementationOfMainApp()

        fid = id_of_flow('focus', 'flow_obj', 'flo_key')
        assert app.change_flow(fid)
        assert app.flow_id == fid
        empty_id = id_of_flow('')
        assert app.change_flow(empty_id)
        assert app.flow_id == fid

    def test_change_flow_remember_focus(self, restore_app_env):
        app = ImplementationOfMainApp()

        fid = id_of_flow('focus', 'flow_obj', 'flo_key')
        assert app.change_flow(fid)
        assert app.flow_id == fid
        save_id = id_of_flow('save', 'obj')
        app.flow_id = save_id
        assert app.flow_id == save_id
        empty_id = id_of_flow('')
        assert app.change_flow(empty_id)
        assert app.flow_id == fid

    def test_change_flow_with_send_event(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.flow_id_called
        assert not app.flow_path_called

        flow1 = id_of_flow('action', 'first_flow')
        app.change_app_state('flow_id', flow1)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert app.flow_id_called
        assert not app.flow_path_called

    def test_change_flow_without_send_event(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.flow_id_called
        assert not app.flow_path_called

        flow1 = id_of_flow('action', 'first_flow')
        app.change_app_state('flow_id', flow1, send_event=False)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert not app.flow_id_called
        assert not app.flow_path_called

    def test_flow_enter(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert len(app.flow_path) == 0
        flow1 = id_of_flow('enter', 'first_flow')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1

    def test_flow_enter_next_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        flow1 = id_of_flow('enter', 'first_flow')
        flow2 = id_of_flow('action', '2nd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == flow2

    def test_flow_close(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow1 = id_of_flow('open', 'first_flow', 'tst_key')
        app.on_first_flow_open = lambda *_: True
        assert app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == flow1

        flow2 = id_of_flow('close', 'first_flow', 'tst_key')
        app.on_first_flow_close = lambda *_: True
        assert app.change_flow(flow2)
        assert len(app.flow_path) == 0
        assert app.flow_id == id_of_flow('')

    def test_flow_close_after_focus(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow1 = id_of_flow('open', 'first_flow', 'tst_key')
        app.on_first_flow_open = lambda *_: True
        assert app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == flow1

        flow2 = id_of_flow('close', 'first_flow', 'tst_key')
        focus_flo = id_of_flow('focus', 'xx')
        app.flow_id = focus_flo
        app.on_first_flow_close = lambda *_: True
        assert app.change_flow(flow2)
        assert len(app.flow_path) == 0
        assert app.flow_id == focus_flo

    def test_flow_close_next_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        flow2 = id_of_flow('action', '2nd_flow', 'tst_key2')
        flow3 = id_of_flow('leave', '3rd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert app.flow_id == flow2

        app.change_flow(flow3, flow_id=flow3)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow3

    def test_flow_close_no_exception_if_path_empty(self, restore_app_env):
        app = ImplementationOfMainApp()

        flow1 = id_of_flow('close', 'flow_obj', 'flo_key')
        assert not app.flow_path

        assert not app.change_flow(flow1)

        app.on_flow_obj_close = lambda *_: True
        assert app.change_flow(flow1)

    def test_flow_leave(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == id_of_flow('')

        flow2 = id_of_flow('leave', 'first_flow', 'tst_key')
        app.change_flow(flow2)
        assert len(app.flow_path) == 0
        assert app.flow_id == replace_flow_action(flow1, 'focus')
        assert flow_key(app.flow_id) == 'tst_key'

    def test_flow_leave_next_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        flow2 = id_of_flow('action', '2nd_flow', 'tst_key2')
        flow3 = id_of_flow('leave', '3rd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert app.flow_id == flow2

        app.change_flow(flow3, flow_id=flow2)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow2

    def test_flow_path_action(self, restore_app_env):
        app = ImplementationOfMainApp()
        act1 = 'action'
        flow1 = id_of_flow(act1, 'flow_obj', 'tst_key2')
        app.flow_path.append(flow1)
        assert app.flow_path_action() == act1
        assert app.flow_path_action(path_index=0) == act1

        assert app.flow_path_action(path_index=1) == ''
        assert app.flow_path_action(path_index=-2) == '' == id_of_flow('')

        act2 = 'other'
        app.flow_path.append(id_of_flow(act2, 'obj'))
        assert app.flow_path_action() == act2
        assert app.flow_path_action(path_index=1) == act2
        assert app.flow_path_action(path_index=-2) == act1
        assert app.flow_path_action(path_index=0) == act1

    def test_flow_popup_show(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = False
        tst_arg_val = 'tst_arg'

        # noinspection PyUnusedLocal
        class TstObjectEditPopup:
            """ fake popup class """
            def __init__(self, tst_arg=''):
                assert tst_arg == tst_arg_val

            @staticmethod
            def open():
                """ open popup method """
                nonlocal called
                called = True

        # STRANGE: in the next test method there is no need to patch class_by_name
        def _find_class(cls_nam):
            return dict(TstObjectEditPopup=TstObjectEditPopup).get(cls_nam)
        setattr(app, 'class_by_name', _find_class)

        app.change_flow(id_of_flow('edit', 'tst_object'), popup_kwargs=dict(tst_arg=tst_arg_val))
        assert called

    def test_flow_popup_close_calls_popup_close(self, restore_app_env):
        app = ImplementationOfMainApp()
        called = False

        class TstObjectEditPopup:
            """ fake popup class """
            @staticmethod
            def close():
                """ close popup """
                nonlocal called
                called = True

        popup = TstObjectEditPopup()

        assert app.change_flow(id_of_flow('focus', 'obj'), popups_to_close=(popup, ))

        assert called

    def test_flow_popup_close_with_count(self, restore_app_env):
        app = ImplementationOfMainApp()
        count_arg = -999

        def _close_popups_mock(*_args, count: int = -1):
            nonlocal count_arg
            count_arg = count

        app.close_popups = _close_popups_mock

        assert app.change_flow(id_of_flow('focus', 'xy'), popups_to_close=9)

        assert count_arg == 9

    def test_change_flow_edit_replace(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.on_obj_edit = lambda *_: True
        assert len(app.flow_path) == 0
        flow1 = id_of_flow('edit', 'obj', 'first')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        flow2 = id_of_flow('edit', 'obj', 'second')
        app.change_flow(flow2)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow2

    def test_change_flow_changed_event_name(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.on_obj_edit = lambda *_: True
        called = {}
        app.tst_chg_evt = lambda *_: called.update(tst=True)
        flow1 = id_of_flow('edit', 'obj')
        app.change_flow(flow1, changed_event_name='tst_chg_evt')
        assert 'tst' in called and called['tst'] is True

    def test_change_flow_reset_last_focus_flow_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.on_obj_edit = lambda *_: True

        flow1 = id_of_flow('focus', 'obj', '1st_key')
        assert app.change_flow(flow1)
        assert app._last_focus_flow_id == flow1

        flow2 = id_of_flow('edit', 'obj', '1st_key')
        assert app.change_flow(flow2)
        assert app._last_focus_flow_id == flow1

        empty_flow = id_of_flow('')
        assert app.change_flow(empty_flow, reset_last_focus_flow_id=False)  # don't reset but ignore the last focus id
        assert app._last_focus_flow_id == flow1
        assert app.flow_id == empty_flow

        assert app.change_flow(empty_flow, reset_last_focus_flow_id=True)
        assert app._last_focus_flow_id == empty_flow
        assert app.flow_id == empty_flow

        flow3 = id_of_flow('edit', 'obj', '2nd_key')
        assert app.change_flow(flow3, reset_last_focus_flow_id=flow1)
        assert app._last_focus_flow_id == flow1
        assert app.flow_id == flow3


class TestOtherMainAppMethods:
    def test_app_stop_no_exit_code_passed(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.run_app()
        app.stop_app()
        assert app._exit_code == 0

    def test_app_stop_with_exit_code_passed(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.run_app()
        app.stop_app(69)
        assert app._exit_code == 69

    def test_call_method_valid_method(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert not app.flow_id_called
        app.call_method('on_flow_id')
        assert app.flow_id_called

    def test_call_method_invalid_method(self, ini_file, restore_app_env):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        assert app.call_method('invalid_method_name') is None

    def test_call_method_raise_if_not_callable(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.call_method('init_called')  # TypeError: 'bool' object app.init_called is not callable caught
        assert isinstance(app.init_called, bool)
        assert app.init_called

    def test_call_method_catch_attr_error_exception(self, restore_app_env):
        app = ImplementationOfMainApp()

        def _raising_ex():
            """ fake method raising exception """
            raise AttributeError
        setattr(app, 'test_raiser', _raising_ex)
        app.call_method('test_raiser')

    def test_call_method_catch_lookup_error_exception(self, restore_app_env):
        app = ImplementationOfMainApp()

        def _raising_ex():
            """ fake method raising exception """
            raise LookupError
        setattr(app, 'test_raiser', _raising_ex)
        app.call_method('test_raiser')

    def test_call_method_catch_value_error_exception(self, restore_app_env):
        app = ImplementationOfMainApp()

        def _raising_ex():
            """ fake method raising exception """
            raise ValueError
        setattr(app, 'test_raiser', _raising_ex)
        app.call_method('test_raiser')

    def test_close_popups(self, restore_app_env):
        app = ImplementationOfMainApp()

        class _Popup:
            """ dummy popup """
            def open(self):
                """ popup open method """
                app.framework_win.children.append(self)

            def close(self):
                """ popup close method """
                app.framework_win.children.remove(self)

        app.open_popup(_Popup)

        popups = app.popups_opened()
        assert popups
        app.close_popups()
        popups = app.popups_opened()
        assert not popups

    def test_dpi_factor(self, restore_app_env):
        app = ImplementationOfMainApp()
        # would need to import kivy modules (which does not work on gitlab CI): assert app.dpi_factor() == dp(1.0)
        assert isinstance(app.dpi_factor(), float)
        assert app.dpi_factor() != 0.0

    def test_find_image_file(self, restore_app_env, image_files_to_test):
        i1, im2, im3 = image_files_to_test
        register_package_images()
        app = ImplementationOfMainApp()
        assert app.find_image(image_file_name).path
        assert app.find_image(image_file_name).path in (norm_path(i1), norm_path(im2), norm_path(im3))

    def test_find_image_file_not_exists(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.find_image("not_existing_image_file.xzy") is None

        app.image_files = FilesRegister()   # reset for coverage
        assert app.find_image("not_existing_image_file.xzy") is None

    def test_find_image_file_with_matcher(self, restore_app_env, image_files_to_test):
        im1, im2, im3 = image_files_to_test
        app = ImplementationOfMainApp()
        assert app.find_image(image_file_name).path
        assert app.find_image(image_file_name).path == norm_path(im3)
        assert app.find_image(image_file_name, height=0.6).path == norm_path(im2)
        assert app.find_image(image_file_name, height=1.5).path == norm_path(im2)
        assert app.find_image(image_file_name, height=96.0).path == norm_path(im3)
        assert app.find_image(image_file_name, light_theme=bool(1)).path == norm_path(im3)

    def test_find_image_file_with_matcher_and_sorter(self, restore_app_env, image_files_to_test):
        im1, im2, im3 = image_files_to_test
        app = ImplementationOfMainApp()
        assert app.find_image(image_file_name, height=0.6, light_theme=False).path == norm_path(im2)
        assert app.find_image(image_file_name, height=1.5, light_theme=False).path == norm_path(im2)

        assert app.find_image(image_file_name, height=3.0, light_theme=False).path == norm_path(im3)
        assert app.find_image(image_file_name, light_theme=False).path == norm_path(im3)   # default height==32.0

        assert app.image_files(image_file_name, property_matcher=lambda f: True).path in (
            norm_path(im1), norm_path(im2), norm_path(im3))
        assert app.image_files(image_file_name, property_matcher=lambda f: True).path in (
            norm_path(im1), norm_path(im2), norm_path(im3))

    def test_find_image_file_without_image_name(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.find_image('') is None

    def test_find_sound_cov(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.sound_files = None
        assert app.find_sound('any_sound') is None

    def test_find_widget(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.find_widget(lambda _w: False) is None

        class _Layout:
            """ fake layout widget """
            children = []

        class _Widget:
            """ dummy widget """
            children = []

        lay = _Layout()
        wid = _Widget()
        lay.children.append(wid)
        app.framework_win.children.append(lay)
        assert app.find_widget(lambda _w: _w.__class__.__name__ == '_Widget') is wid

    def test_global_variables(self, restore_app_env):
        app = ImplementationOfMainApp()
        glo = app.global_variables()

        assert 'app' in glo
        assert 'get_text' in glo and callable(glo['get_text'])
        assert 'get_f_string' in glo
        assert 'id_of_flow' in glo
        assert 'normalize' in glo
        assert 'os_platform' in glo
        assert 'main_app' in glo and glo['main_app'] is app

    def test_global_variables_patched(self, restore_app_env):
        app = ImplementationOfMainApp()
        tst_val = 'tst_val'
        glo = app.global_variables(app=tst_val, get_text=tst_val, new_val=tst_val)

        assert glo['app'] == tst_val
        assert glo['get_text'] == tst_val
        assert glo['new_val'] == tst_val

    def test_img_file(self, restore_app_env, image_files_to_test):
        im1, im2, im3 = image_files_to_test
        app = ImplementationOfMainApp()
        assert app.img_file('') == ''
        assert app.img_file(image_file_name)
        assert app.img_file(image_file_name) in (norm_path(im1), norm_path(im2), norm_path(im3))

    def test_ini_file_cwd_default(self, restore_app_env, tst_app_key):
        app = ImplementationOfMainApp()
        ini_file_path = norm_path(tst_app_key + INI_EXT)
        assert app._main_cfg_fnam == ini_file_path

    def test_ini_file_added_in_tests_subdir(self, restore_app_env, tst_app_key, ini_file):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        ini_file_path = norm_path(ini_file)
        assert app._main_cfg_fnam == ini_file_path

    def test_ini_file_added_in_tests_subdir_after_get_opt(self, restore_app_env, tst_app_key, ini_file):
        app = ImplementationOfMainApp(additional_cfg_files=(ini_file, ))
        ini_file_path = norm_path(ini_file)
        app.get_opt('debug_level')
        assert app._main_cfg_fnam == ini_file_path

    def test_ini_file_app_doc_path(self, restore_app_env, tst_app_key):
        os.makedirs(os.path.join(normalize("{doc}"), tst_app_key), exist_ok=True)  # pyTstConsAppKey will not be deleted
        ini_file_path = norm_path(os.path.join(normalize('{doc}'), tst_app_key, tst_app_key + INI_EXT))
        try:
            _create_ini_file(ini_file_path)
            app = ImplementationOfMainApp(app_name=tst_app_key)
            assert app._main_cfg_fnam == ini_file_path
        finally:
            if os.path.exists(ini_file_path):
                os.remove(ini_file_path)

    def test_ini_file_app_doc_path_after_get_opt(self, restore_app_env, tst_app_key):
        os.makedirs(os.path.join(normalize("{doc}"), tst_app_key), exist_ok=True)  # pyTstConsAppKey will not be deleted
        ini_file_path = norm_path(os.path.join(normalize('{doc}'), tst_app_key, tst_app_key + INI_EXT))
        try:
            _create_ini_file(ini_file_path)
            app = ImplementationOfMainApp(app_name=tst_app_key)
            app.get_opt('debug_level')
            assert app._main_cfg_fnam == ini_file_path
        finally:
            if os.path.exists(ini_file_path):
                os.remove(ini_file_path)

    def test_load_images(self, restore_app_env):
        app = ImplementationOfMainApp(debug_level=DEBUG_LEVEL_ENABLED)
        assert isinstance(app.image_files, FilesRegister)
        assert len(app.image_files) == PORTION_IMG_COUNT + TST_IMG_COUNT

    def test_load_sounds(self, restore_app_env):
        app = ImplementationOfMainApp(debug_level=DEBUG_LEVEL_ENABLED)
        assert isinstance(app.sound_files, FilesRegister)
        assert len(app.sound_files) == PORTION_SND_COUNT

        snd_path = os.path.join(TESTS_FOLDER, 'snd')
        snd_file = 'dummy_sound.file'
        try:
            os.mkdir(snd_path)
            write_file(os.path.join(snd_path, snd_file), "dummy sound")
            app.sound_files.add_paths(os.path.join(snd_path, '**'))
            assert isinstance(app.sound_files, FilesRegister)
            assert app.sound_files
            assert app.find_sound(os.path.splitext(snd_file)[0])
        finally:
            if os.path.exists(snd_path):
                shutil.rmtree(snd_path)

    def test_mix_background_ink(self, restore_app_env):
        app = ImplementationOfMainApp()

        assert not app.framework_app.mixed_back_ink
        app.mix_background_ink()
        assert app.framework_app.mixed_back_ink

        assert app.flow_id_ink == [0.99, 0.99, 0.69, 0.69]  # change with MainAppBase color defaults

    def test_open_popup(self, restore_app_env):
        app = ImplementationOfMainApp()

        called = False

        class _Popup:
            """ dummy popup """
            @staticmethod
            def open():
                """ popup open/show method """
                nonlocal called
                called = True
        app.open_popup(_Popup)
        assert called

    def test_play_beep(self, restore_app_env):
        app = ImplementationOfMainApp()
        assert app.play_beep() is None

    def test_play_sound(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.play_sound('error')     # cov

    def test_play_vibrate(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.play_vibrate()     # cov

    def test_popups_opened(self, restore_app_env):
        app = ImplementationOfMainApp()

        class _Popup:
            """ dummy popup """
            def open(self):
                """ popup open method """
                app.framework_win.children.append(self)

        popups = app.popups_opened()
        assert not popups

        app.open_popup(_Popup)

        popups = app.popups_opened()
        assert popups
        assert isinstance(popups[0], _Popup)

        popups = app.popups_opened((_Popup, ))
        assert popups
        assert isinstance(popups[0], _Popup)

        popups = app.popups_opened((self.__class__, ))
        assert not popups

    def test_show_confirmation(self, restore_app_env):
        def _chg_flow(flow_id, popup_kwargs):
            """ mock of app.change_flow """
            assert flow_id == id_of_flow('show', 'confirmation')
            assert popup_kwargs['message'] == 'tst msg'
            assert popup_kwargs['title'] == 'tst tit'
        app = ImplementationOfMainApp()
        app.change_flow = _chg_flow
        app.show_confirmation('tst msg', 'tst tit')

    def test_show_input(self, restore_app_env):
        def _chg_flow(flow_id, popup_kwargs):
            """ mock of app.change_flow """
            assert flow_id == id_of_flow('show', 'input')
            assert popup_kwargs['message'] == 'tst msg'
            assert popup_kwargs['title'] == 'tst tit'
        app = ImplementationOfMainApp()
        app.change_flow = _chg_flow
        app.show_input('tst msg', 'tst tit')

    def test_show_message(self, restore_app_env):
        def _chg_flow(flow_id, popup_kwargs):
            """ mock of app.change_flow """
            assert flow_id == id_of_flow('show', 'message')
            assert popup_kwargs['message'] == 'tst msg'
            assert popup_kwargs['title'] == 'tst tit'
        app = ImplementationOfMainApp()
        app.change_flow = _chg_flow
        app.show_message('tst msg', 'tst tit')

    def test_theme_load(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.theme_load("")

    def test_theme_delete(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.theme_delete("")

    def test_theme_save(self, restore_app_env):
        app = ImplementationOfMainApp()
        app.theme_save("")

    def test_theme_update_names(self, restore_app_env):
        app = ImplementationOfMainApp()
        th_id = 'TestThemeId'

        app.theme_update_names("")
        assert app.theme_names == [""]

        app.theme_update_names(th_id)
        assert app.theme_names == [th_id, ""]

        app.theme_update_names("")
        assert app.theme_names == ["", th_id]

        app.theme_update_names(th_id, delete=True)
        assert app.theme_names == [""]

        app.theme_update_names("", delete=True)
        assert app.theme_names == []

    def test_widget_by_attribute(self, restore_app_env):
        app = ImplementationOfMainApp()
        attr_val = 'attr_val'
        assert app.widget_by_attribute('attr_name', attr_val) is None

        class Layout:
            """ fake layout widget """
            children = []

        class Widget:
            """ dummy widget """
            attr_name = attr_val
            children = []

        lay = Layout()
        wid = Widget()
        lay.children.append(wid)
        app.framework_win.children.append(lay)
        assert app.widget_by_attribute('attr_name', attr_val) is wid

    def test_widget_by_flow_id(self, restore_app_env):
        app = ImplementationOfMainApp()
        flow_id = id_of_flow('action', 'obj')
        assert app.widget_by_flow_id(flow_id) is None

        class Widget:
            """ dummy widget """
            tap_flow_id = flow_id
            children = []
        wid = Widget()
        app.framework_win.children.append(wid)
        assert app.widget_by_flow_id(flow_id) is wid

    def test_widget_by_app_state_name(self, restore_app_env):
        app = ImplementationOfMainApp()
        sta_val = 'state_value'
        assert app.widget_by_app_state_name(sta_val) is None

        class Widget:
            """ dummy widget """
            app_state_name = sta_val
            children = []
        wid = Widget()
        app.framework_win.children.append(wid)
        assert app.widget_by_app_state_name(sta_val) is wid

    def test_widget_children(self, restore_app_env):
        app = ImplementationOfMainApp()

        class Widget:
            """ dummy widget """
            children = []
            width = 99
            height = 99
        wid = Widget()
        app.framework_win.children.append(wid)
        assert app.widget_children(app.framework_win) == [wid]

        assert app.widget_children(app.framework_win, only_visible=True) == [wid]
        wid.width = 0
        assert app.widget_children(app.framework_win, only_visible=True) == []

    def test_widget_pos(self, restore_app_env):
        app = ImplementationOfMainApp()
        tst_pos = (36, 99)

        class Widget:
            """ dummy widget """
            x, y = tst_pos

        assert app.widget_pos(Widget()) == tst_pos

    def test_widgets_enclosing_rectangle(self, restore_app_env):
        app = ImplementationOfMainApp()

        tst_pos_size = (36, 69, 123, 234)

        class Widget1:
            """ dummy widget """
            x, y, width, height = tst_pos_size

        assert app.widgets_enclosing_rectangle((Widget1(), )) == tst_pos_size

    def test_widget_size(self, restore_app_env):
        app = ImplementationOfMainApp()
        tst_size = (36, 99)

        class Widget:
            """ dummy widget """
            width, height = tst_size

        assert app.widget_size(Widget()) == tst_size

    def test_widget_visible(self, restore_app_env):
        app = ImplementationOfMainApp()

        class Widget:
            """ dummy widget """
            children = []
            width = 99
            height = 99
            opacity = 1.0
            visible = True
        wid = Widget()
        assert app.widget_visible(wid)

        wid = Widget()
        wid.width = 0
        assert not app.widget_visible(wid)

        wid = Widget()
        wid.height = 0
        assert not app.widget_visible(wid)

        wid = Widget()
        wid.opacity = 0.0
        assert not app.widget_visible(wid)

        wid = Widget()
        wid.visible = False
        assert not app.widget_visible(wid)

    def test_width_spaces(self, restore_app_env):
        app = ImplementationOfMainApp()

        assert app.width_spaces(999)
        assert isinstance(app.width_spaces(999), str)
        assert all(_ == " " for _ in app.width_spaces(999))

    def test_win_pos_size_change(self, restore_app_env):
        app = ImplementationOfMainApp()

        rectangle = (6, 9, 600, 900)
        app.win_pos_size_change(*rectangle)
        assert app.win_rectangle == rectangle
        assert not app.framework_app.landscape

        called = False

        def _event():
            """ test on_win_pos_size event handler """
            nonlocal called
            called = True
        setattr(app, 'on_win_pos_size', _event)

        rectangle = (9, 6, 900, 600)
        app.win_pos_size_change(*rectangle)
        assert app.win_rectangle == rectangle
        assert app.framework_app.landscape

        assert called
