"""
abstract Framework-independent base class for python applications with a graphical user interface
-------------------------------------------------------------------------------------------------
"""
import os

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Callable, Optional, Type, Union

from ae.base import (                                                                                   # type: ignore
    CFG_EXT, INI_EXT, UNSET,
    instantiate_config_parser, norm_name, now_str, os_path_basename, os_path_join, stack_var, stack_vars)
from ae.files import RegisteredFile                                                                     # type: ignore
from ae.paths import (                                                                                  # type: ignore
    copy_file, copy_tree, normalize, coll_folders, placeholder_key, Collector, FilesRegister)
from ae.updater import MOVES_SRC_FOLDER_NAME                                                            # type: ignore
from ae.dynamicod import try_call                                                                       # type: ignore
from ae.i18n import (                                                                                   # type: ignore
    default_language, get_f_string, get_text, load_language_texts, register_translations_path)
from ae.core import DEBUG_LEVELS, registered_app_names                                                  # type: ignore
from ae.console import USER_NAME_MAX_LEN, ConsoleApp                                                    # type: ignore

from .tours import TourBase
from .utils import (
    APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME, MAX_FONT_SIZE,
    MIN_FONT_SIZE, PORTIONS_IMAGES, PORTIONS_SOUNDS, THEME_SECTION_PREFIX, THEME_VARIABLE_PREFIX,
    AppStatesType, ColorOrInk, EventKwargsType, HelpVarsType,
    flow_action, flow_change_confirmation_event_name, flow_key, flow_key_split, flow_path_id, flow_path_strip,
    flow_popup_class_name, id_of_flow, id_of_flow_help, id_of_state_help, mix_colors, module_globals,
    popup_event_kwargs, replace_flow_action, translation_short_help_id, widget_page_id)


ACTIONS_EXTENDING_FLOW_PATH = ['add', 'confirm', 'edit', 'enter', 'open', 'show', 'suggest']
""" flow actions that are extending the flow path. """
ACTIONS_REDUCING_FLOW_PATH = ['close', 'leave']
""" flow actions that are shrinking/reducing the flow paths. """
ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION = ['', 'enter', 'focus', 'leave', 'suggest']
""" flow actions that are processed without the need to be confirmed. """

CLOSE_POPUP_FLOW_ID = id_of_flow('close', 'flow_popup')             #: flow id to close opened dropdown/popup
IGNORED_HELP_FLOWS = (CLOSE_POPUP_FLOW_ID, )                        #: tuple of flow ids never search/show help text for
IGNORED_HELP_STATES = ('flow_id', 'flow_path', 'win_rectangle')     #: tuple of app state names never searched help for

HIDDEN_GLOBALS = (
    'ABC', 'abstractmethod', '_add_base_globals', 'Any', '__builtins__', '__cached__', 'Callable', '_d_',
    '__doc__', '__file__', '__loader__', 'module_globals', '__name__', 'Optional', '__package__', '__path__',
    '__spec__', 'Type', '__version__')
""" tuple of global/module variable names that are hidden in :meth:`~MainAppBase.global_variables` """


class MainAppBase(ConsoleApp, ABC):
    """ abstract base class to implement a GUIApp-conform app class """
    # app states attributes
    app_state_version: int = 0                              #: version number of the app state variables in <config>.ini

    cancel_ink: ColorOrInk = [0.99, 0.09, 0.09, 0.69]       #: rgba color for create/add/register actions
    confirm_ink: ColorOrInk = [0.09, 0.99, 0.09, 0.69]      #: rgba color for create/add/register actions
    create_ink: ColorOrInk = [0.39, 0.99, 0.69, 0.69]       #: rgba color for create/add/register actions
    delete_ink: ColorOrInk = [0.99, 0.69, 0.69, 0.69]       #: rgba color for delete/remove actions
    error_ink: ColorOrInk = [0.99, 0.09, 0.39, 0.69]        #: rgba color for error actions
    flow_id: str = ""                                       #: id of the current app flow (entered by the app user)
    flow_path: list[str] = []                               #: list of flow ids, reflecting recent user actions
    flow_id_ink: ColorOrInk = [0.99, 0.99, 0.69, 0.69]      #: rgba color for flow id / drag&drop node placeholder
    flow_path_ink: ColorOrInk = [0.99, 0.99, 0.39, 0.48]    #: rgba color for flow_path/drag&drop item placeholder
    font_size: float = 21.0                                 #: font size used toolbar and flow screens
    help_ink: ColorOrInk = [0.09, 0.69, 0.99, 0.69]         #: rgba color to mark widgets with context-sensitive help
    info_ink: ColorOrInk = [0.99, 0.99, 0.09, 0.69]         #: rgba color for info actions
    lang_code: str = ""                                     #: user language code (e.g., 'es' or 'es_ES' for Spanish)
    light_theme: bool = False                               #: True=light theme/background, False=dark theme
    read_ink: ColorOrInk = [0.09, 0.99, 0.69, 0.69]         #: rgba color for read actions
    selected_ink: ColorOrInk = [0.69, 0.99, 0.39, 0.18]     #: rgba color for selected list items
    sound_volume: float = 0.12                              #: sound volume of current app (0.0=mute, 1.0=max)
    theme_names: list[str] = []                             #: list of theme names
    unselected_ink: ColorOrInk = [0.39, 0.39, 0.39, 0.18]   #: rgba color for unselected list items
    update_ink: ColorOrInk = [0.99, 0.09, 0.99, 0.69]       #: rgba color for edit/modify/update actions
    vibration_volume: float = 0.3                           #: vibration volume of current app (0.0=mute, 1.0=max)
    warn_ink: ColorOrInk = [0.99, 0.99, 0.09, 0.69]         #: rgba color for hint/warn actions
    win_rectangle: tuple = (0, 0, 1920, 1080)               #: window coordinates (x, y, width, height)

    # generic run-time shortcut references
    framework_app: Any = None                               #: app class instance of the used GUI framework
    framework_win: Any = None                               #: window instance of the used GUI framework
    framework_root: Any = None                              #: app root layout widget

    space_width: float = 8.1                                #: width of a space char in pixels; depends on font size

    # optional app resources caches
    image_files: Optional[FilesRegister] = None             #: image/icon files
    sound_files: Optional[FilesRegister] = None             #: sound/audio files

    # other attributes
    theme_specific_cfg_vars: set[str] = set()               #: config-variables that changes when the theme gets changed

    # help/tour
    displayed_help_id: str = ''                 #: message id of currently explained/focused target widget in help mode
    help_activator: Any = None                  #: help mode de-/activator button widget
    help_layout: Optional[Any] = None           #: help text container widget in active help mode else None
    tour_layout: Optional[Any] = None           #: tour layout/overlay widget in active tour mode else None
    tour_overlay_class: Optional[Type] = None   #: UI-framework-specific tour overlay class, set by main app subclass

    _next_help_id: str = ''                     #: last app-state/flow change to show help text on help mode activation
    _closing_popup_open_flow_id: str = ''       #: flow id of just closed popup

    def __init__(self, **console_app_kwargs):
        """ create an instance of app class.

        :param console_app_kwargs:  kwargs to be passed to the __init__ method of :class:`~ae.console.ConsoleApp`.
        """
        self._exit_code = 0                             #: init by stop_app() and passed onto OS by run_app()
        self._last_focus_flow_id = id_of_flow('')       #: id of the last valid focused window/widget/item/context

        self._start_event_loop: Optional[Callable]      #: callable to start event loop of the GUI framework
        self._stop_event_loop: Optional[Callable]       #: callable to start event loop of the GUI framework

        self.flow_path = []         # init for literal type recognition - will be overwritten by setup_app_states()

        super().__init__(**console_app_kwargs)

        self.call_method('on_app_init')

        self._start_event_loop, self._stop_event_loop = self.init_app()

        self.load_app_states()

    def _init_default_theme_cfg_vars(self):
        """ called from self._init_default_user_cfg_vars() to extend user config vars after/in self.__init__() """
        self.theme_specific_cfg_vars = {
            'cancel_ink', 'confirm_ink', 'create_ink', 'delete_ink', 'error_ink', 'flow_id_ink', 'flow_path_ink',
            'font_size', 'help_ink', 'info_ink', 'light_theme', 'read_ink', 'selected_ink', 'unselected_ink',
            'update_ink', 'warn_ink',
        }

    def _init_default_user_cfg_vars(self):
        super()._init_default_user_cfg_vars()

        self.user_specific_cfg_vars |= {
            (APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME),
            (APP_STATE_SECTION_NAME, 'flow_id'),
            (APP_STATE_SECTION_NAME, 'flow_path'),
            (APP_STATE_SECTION_NAME, 'lang_code'),
            (APP_STATE_SECTION_NAME, 'selected_ink'),
            (APP_STATE_SECTION_NAME, 'unselected_ink'),
            (APP_STATE_SECTION_NAME, 'win_rectangle'),
        }

        self._init_default_theme_cfg_vars()
        for var_name in self.theme_specific_cfg_vars:
            self.user_specific_cfg_vars.add((APP_STATE_SECTION_NAME, var_name))

    @abstractmethod
    def call_method_delayed(self, delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ delayed call of passed callable/method with args/kwargs catching and logging exceptions preventing app exit.

        :param delay:           delay in seconds before calling the callable/method specified by
                                :paramref:`~call_method_delayed.callback`.
        :param callback:        either callable or name of the main app method to call.
        :param args:            args passed to the callable/main-app-method to be called.
        :param kwargs:          kwargs passed to the callable/main-app-method to be called.
        :return:                delayed call event object instance, providing a `cancel` method to allow
                                the cancellation of the delayed call within the delay time.
        """

    @abstractmethod
    def call_method_repeatedly(self, interval: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ repeated call of passed callable/method with args/kwargs catching and logging exceptions preventing app exit

        :param interval:        interval in seconds between two calls of the callable/method specified by
                                :paramref:`~call_method_repeatedly.callback`.
        :param callback:        either callable or name of the main app method to call.
        :param args:            args passed to the callable/main-app-method to be called.
        :param kwargs:          kwargs passed to the callable/main-app-method to be called.
        :return:                repeatedly call event object instance, providing a `cancel` method to allow
                                the cancellation of the repeated call within the interval time.
        """

    @abstractmethod
    def ensure_top_most_z_index(self, widget: Any):
        """ ensure visibility of the passed widget to be the top most in the z index/order.

        :param widget:          the popup/dropdown/container widget to be moved to the top.
        """

    @abstractmethod
    def help_activation_toggle(self):
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """

    @abstractmethod
    def init_app(self, framework_app_class: Any = None) -> tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and root window/layout, return GUI event loop start/stop methods.

        :param framework_app_class: class to create an app instance (optionally extended by the app project).
        :return:                    tuple of two callable, the 1st to start and the 2nd to stop/exit
                                    the GUI event loop.
        """

    def app_state_keys(self) -> tuple[str, ...]:
        """ determine current config variable names/keys of the app state section :data:`APP_STATE_SECTION_NAME`.

        :return:                tuple of all app state item keys (config variable names).
        """
        as_keys = []
        usr_keys = set(self.cfg_section_variable_names(self.user_section(APP_STATE_SECTION_NAME)))
        gen_keys = set(self.cfg_section_variable_names(APP_STATE_SECTION_NAME))
        for key in usr_keys | gen_keys:
            if hasattr(self, key):
                as_keys.append(key)
            else:
                self.dpo(f"app state {key=} ignored because it is not declared as MainAppBase attribute")
        return tuple(as_keys)

    def backup_config_resources(self) -> str:   # pragma: no cover
        """ backup config files and image/sound/translations resources to {ado}<now_str>.

        config files are collected from {ado}, {usr} or {cwd} (the first found file name only - see/sync-with
        :meth:`ae.console.ConsoleApp.add_cfg_files`).

        resources are copied from {ado} or {cwd} (only the first found resources root path).
        """
        backup_root = normalize("{ado}") + now_str(sep="_")
        try:
            os.makedirs(backup_root)

            coll = Collector()
            app_configs = tuple(ana + ext for ana in registered_app_names() for ext in (INI_EXT, CFG_EXT))
            coll.collect("{ado}", "{usr}", "{cwd}", append=app_configs)
            for file in coll.files:
                copy_file(file, os_path_join(backup_root, placeholder_key(file) + "_" + os_path_basename(file)))

            coll = Collector(item_collector=coll_folders)
            coll.collect("{ado}", "{cwd}", append=('img', 'loc', 'snd'))
            for path in coll.paths:
                copy_tree(path, os_path_join(backup_root, placeholder_key(path) + "_" + os_path_basename(path)))
        except (PermissionError, Exception) as ex:      # pylint: disable=broad-except
            self.show_message(f"backup to '{backup_root}' failed with exception '{ex}'")

        return backup_root

    def change_app_state(self, app_state_name: str, state_value: Any, send_event: bool = True, old_name: str = ''):
        """ change app state and show help text in active help mode.

        :param app_state_name:  app state name to change.
        :param state_value:     the new value of the app status to change.
        :param send_event:      pass False to prevent send/call of the main_app.on_<app_state_name> event.
        :param old_name:        pass to add state to the main config file: old state name to rename/migrate or
                                :data:`~ae.base.UNSET` to only add a new app state variable with the name specified in
                                :paramref:`~change_app_state.app_state_name`.
        """
        self.vpo(f"MainAppBase.change_app_state({app_state_name=}, {state_value=!r}, {send_event=}, {old_name=!r})"
                 f" {self.flow_id=} {self._last_focus_flow_id=} {self.flow_path=}")

        help_vars = {'app_state_name': app_state_name, 'state_value': state_value, 'old_name': old_name}
        if self.help_app_state_display(help_vars):
            return

        self.change_observable(app_state_name, state_value, is_app_state=True)

        if old_name or old_name is UNSET:
            self.set_var(app_state_name, state_value, section=APP_STATE_SECTION_NAME, old_name=old_name or "")

        if send_event:
            self.call_method('on_' + app_state_name)

        self.help_app_state_display(help_vars, changed=True)

    def change_flow(self, new_flow_id: str, **event_kwargs) -> bool:
        """ try to change/switch the current flow id to the value passed in :paramref:`~change_flow.new_flow_id`.

        :param new_flow_id:     new flow id (maybe overwritten by flow change confirmation event handlers by assigning a
                                flow id to event_kwargs['flow_id']).

        :param event_kwargs:    optional args to pass additional data or info onto and from the flow change confirmation
                                event handler.

                                the following keys are currently supported/implemented by this module/portion
                                (additional keys can be added by the modules/apps using this method):

                                * `changed_event_name`: optional main app event method name to be called if the flow got
                                  confirmed and changed.
                                * `count`: optional number used to render a pluralized help text for this flow change
                                  (this number gets also passed to the help text formatter by/in
                                  :meth:`~MainAppBase.change_flow`).
                                * `edit_widget`: optional widget instance for edit/input.
                                * `flow_id`: process :attr:`~MainAppBase.flow_path` as specified by the
                                  :paramref:`~change_flow.new_flow_id` argument, but then overwrite this flow id with
                                  this event arg value to set :attr:`~MainAppBase.flow_id`.
                                * `popup_kwargs`: optional dict passed to the Popup `__init__` method,
                                  like e.g., `dict(opener=opener_widget_of_popup, data=...)`.
                                * `popups_to_close`: optional, either the number of top/most-recent popups to close,
                                  or a tuple of popup instances to be closed. the closing is done by this method after
                                  the flow change got confirmed.
                                * 'reset_last_focus_flow_id': pass `True` to reset the last focus flow id, pass `False`
                                  or `None` to ignore the last focus id (and not use to set flow id) or pass a flow id
                                  string value to change the last focus flow id to the passed value.
                                * `tap_widget`: optional tapped button widget instance (initiating this flow change).

                                some of these keys get specified directly on the call of this method, e.g., via
                                :attr:`~ae.kivy.widgets.FlowButton.tap_kwargs` or
                                :attr:`~ae.kivy.widgets.FlowToggler.tap_kwargs`,
                                where others get added by the flow change confirmation handlers/callbacks.

        :return:                boolean True if flow got confirmed by a declared custom flow change confirmation event
                                handler (either event method or Popup class) of the app, and if the flow changed
                                accordingly.

                                returning False if the help mode is active and the calling widget is not selected.

                                some flow actions are handled internally independent of the return value of a
                                custom event handler, like e.g. `'enter'` or `'leave'` will always extend or reduce the
                                flow path and the action `'focus'` will give the indexed widget the input focus (these
                                exceptions are configurable via :data:`ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION`).
        """
        self.vpo(f"MainAppBase.change_flow({new_flow_id!r}, {event_kwargs}) {self.flow_id=!r} {self.flow_path=}")

        help_vars: HelpVarsType = {'new_flow_id': new_flow_id, 'event_kwargs': event_kwargs}
        count = event_kwargs.pop('count', None)
        if count is not None:
            help_vars['count'] = count

        if self.help_flow_display(help_vars):
            return False

        prefix = " " * 12
        action = flow_action(new_flow_id)
        if not self.call_method(flow_change_confirmation_event_name(new_flow_id), flow_key(new_flow_id), event_kwargs) \
                and not self.on_flow_change(new_flow_id, event_kwargs) \
                and action not in ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION:
            self.vpo(f"{prefix}REJECTED {new_flow_id=} {event_kwargs=}")
            return False

        has_flow_focus = flow_action(self.flow_id) == 'focus'
        empty_flow = id_of_flow('')
        if action in ACTIONS_EXTENDING_FLOW_PATH:
            if action == 'edit' and self.flow_path_action() == 'edit' \
                    and flow_key_split(self.flow_path[-1])[0] == flow_key_split(new_flow_id)[0]:
                _flow_id = self.flow_path.pop()
                self.vpo(f"{prefix}PATH EDIT: removed '{_flow_id}', to replace it with ...")
            self.vpo(f"{prefix}PATH EXTEND: appending '{new_flow_id}' to {self.flow_path}")
            self.flow_path.append(new_flow_id)
            self.change_app_state('flow_path', self.flow_path)
            flow_id = empty_flow if action == 'enter' else new_flow_id
        elif action in ACTIONS_REDUCING_FLOW_PATH:
            # dismiss gets sent sometimes twice (e.g., on heavy double-clicking on drop-down-open-buttons)
            # therefore, prevent run-time error
            if not self.flow_path:
                self.dpo(f"{prefix}FIX empty flow path because of missing popups_to_close for {self.popups_opened()=}")
                self.close_popups(force=True)     # fix/close all popups to reset run-time to match an empty flow path
                self.help_flow_display(help_vars, changed=True)
                return True
            ended_flow_id = self.flow_path.pop()
            self.vpo(f"{prefix}PATH REDUCE: popped '{ended_flow_id}' now resulting in {self.flow_path=}")
            self.change_app_state('flow_path', self.flow_path)
            if action == 'leave':
                flow_id = replace_flow_action(ended_flow_id, 'focus')
            else:
                flow_id = self.flow_id if has_flow_focus else empty_flow
        else:
            flow_id = new_flow_id if action == 'focus' else (self.flow_id if has_flow_focus else empty_flow)

        popups_to_close = event_kwargs.get('popups_to_close', ())
        if isinstance(popups_to_close, int):
            self.close_popups(count=popups_to_close)
        else:
            for popup in reversed(popups_to_close):
                popup.close()

        if action not in ACTIONS_REDUCING_FLOW_PATH or not has_flow_focus:
            flow_id = event_kwargs.get('flow_id', flow_id)  # update flow_id from event_kwargs
        if 'reset_last_focus_flow_id' in event_kwargs:
            last_flow_id = event_kwargs['reset_last_focus_flow_id']
            if last_flow_id is True:
                self._last_focus_flow_id = empty_flow
            elif isinstance(last_flow_id, str):
                self._last_focus_flow_id = last_flow_id
        elif flow_id == empty_flow and self._last_focus_flow_id and action not in ACTIONS_EXTENDING_FLOW_PATH:
            flow_id = self._last_focus_flow_id
        self.change_app_state('flow_id', flow_id)

        changed_event_name = event_kwargs.get('changed_event_name', '')
        if changed_event_name:
            self.call_method(changed_event_name)

        if flow_action(flow_id) == 'focus':
            self.call_method('on_flow_widget_focused')
            self._last_focus_flow_id = flow_id

        self.vpo(f"{prefix}CHANGED {self.flow_path=} {event_kwargs=} {self._last_focus_flow_id=}")

        self.help_flow_display(help_vars, changed=True)

        return True

    def change_observable(self, name: str, value: Any, is_app_state: bool = False):
        """ change observable attribute/member/property in framework_app instance (and shadow copy in the main app).

        :param name:            name of the observable attribute/member or key of an observable dict property.
        :param value:           new value of the observable.
        :param is_app_state:    pass True for an app state observable.
        """
        setattr(self, name, value)
        if is_app_state:
            if hasattr(self.framework_app, 'app_states'):       # has observable DictProperty duplicates
                self.framework_app.app_states[name] = value
            name = 'app_state_' + name
        if hasattr(self.framework_app, name):                   # has observable attribute duplicate
            setattr(self.framework_app, name, value)

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ search class name in framework modules as well as in app main.py to return the related class/type object.

        :param class_name:      name of the class.
        :return:                class object with the specified class name or :data:`~ae.base.UNSET` if not found.
        """
        return stack_var(class_name)

    @property
    def color_attr_names(self) -> set[str]:
        """ determine the app state attribute/config-var names of all UI colors, including app-specific colors.

        :return:                set of app state attribute names of all colors, declared/configured by ae-framework+app.
        """
        return set(color_name for color_name in self.app_state_keys() if color_name.endswith('_ink'))

    @staticmethod
    def dpi_factor() -> float:
        """ dpi scaling factor - override if the used GUI framework supports dpi scaling. """
        return 1.0

    def close_popups(self, classes: tuple = (), count: int = -1, force: bool = False):
        """ close specified/all opened popups (starting with the foremost popup).

        :param classes:         optional class filter - if not passed, then only the first foremost widgets underneath
                                the app win with an `open` method will be closed. pass tuple to restrict found popup
                                widgets to certain classes. like e.g., pass `(Popup, DropDown, FlowPopup)` to get
                                all popups of an app (in Kivy use Factory.WidgetClass if the widget is declared only in
                                kv lang).
        :param count:           maximum number of popups to close (if it is negative or not specified, then all
                                currently opened popups will be closed).
        :param force:           pass True force the remove of popup without calling its close/dismiss method.
        """
        for popup in self.popups_opened(classes=classes):
            if count:
                if force:
                    self.framework_win.remove_widget(popup)     # pragma: no cover
                else:
                    popup.close()
                count -= 1

    def find_image(self, image_name: str, height: float = 32.0, light_theme: bool = True) -> Optional[RegisteredFile]:
        """ find the best fitting image in the registered img folders.

        :param image_name:      name of the image (file name without extension).
        :param height:          preferred height of the image/icon.
        :param light_theme:     preferred theme (dark/light) of the image.
        :return:                image file object (RegisteredFile/CachedFile) if found else None.
        """
        def property_matcher(file) -> bool:
            """ find images with matching theme.

            :param file:        RegisteredFile instance.
            :return:            True if the theme is matching.
            """
            return bool(file.properties.get('light', 0)) == light_theme

        def file_sorter(file) -> float:
            """ sort images files by height delta.

            :param file:        RegisteredFile instance.
            :return:            height delta.
            """
            return abs(file.properties.get('height', -MAX_FONT_SIZE) - height)

        if self.image_files:
            return self.image_files(image_name, property_matcher=property_matcher, file_sorter=file_sorter)
        return None

    def find_sound(self, sound_name: str) -> Optional[RegisteredFile]:
        """ find sound by name.

        :param sound_name:      name of the sound to search for.
        :return:                cached sound file object (RegisteredFile/CachedFile) if sound name was found else None.
        """
        if self.sound_files:    # prevent error on app startup (setup_app_states() called before load_images()
            return self.sound_files(sound_name)
        return None

    def find_widget(self, match: Callable[[Any], bool], root_widget: Optional[Any] = None) -> Optional[Any]:
        """ bottom-up-search the widget tree returning the first matching widget in reversed z-order (foremost first).

        :param match:           callable called with the widget as an argument, returning True if the widget matches.
        :param root_widget:     optional root widget to start searching from.
                                if None, then the root of the widget tree is used.
        :return:                the first found widget in reversed z-order (top-most widget first).
        """
        def child_wid(children):
            """ bottom-up search within children for a widget with matching attribute name and value. """
            for widget in children:
                found = child_wid(self.widget_children(widget))
                if found:
                    return found
                if match(widget):
                    return widget
            return None

        return child_wid(self.widget_children(root_widget or self.framework_win))

    def flow_path_action(self, flow_path: Optional[list[str]] = None, path_index: int = -1) -> str:
        """ determine the action of the last (newest) entry in the flow_path.

        :param flow_path:       optional flow path to get the flow action from (default=self.flow_path).
        :param path_index:      optional index in the flow_path (default=-1).
        :return:                flow action string
                                or an empty string if the flow path is empty or the index does not exist.
        """
        if flow_path is None:
            flow_path = self.flow_path
        return flow_action(flow_path_id(flow_path=flow_path, path_index=path_index))

    def global_variables(self, **patches) -> dict[str, Any]:
        """ determine generic/most-needed global variables to evaluate expressions/macros.

        :param patches:         dict of variable names and values to add/replace on top of generic globals.
        :return:                dict of global variables patched with :paramref:`~global_variables.patches`.
        """
        glo_vars = {k: v for k, v in module_globals.items() if k not in HIDDEN_GLOBALS}
        glo_vars.update((k, v) for k, v in globals().items() if k not in HIDDEN_GLOBALS)
        glo_vars['app'] = self.framework_app
        glo_vars['main_app'] = self
        glo_vars['_add_base_globals'] = ""          # instruct ae.dynamicod.try_eval to add generic/base globals

        self.vpo(f"MainAppBase.global_variables patching {patches} over {glo_vars}")

        glo_vars.update(**patches)

        return glo_vars

    def help_app_state_display(self, help_vars: dict[str, Any], changed: bool = False) -> bool:
        """ actualize the help layout if active, before and after the change of the app state.

        :param help_vars:       help context args/kwargs of the :meth:`~MainAppBase.change_flow` method.

                                items passed to the help text formatter:
                                    * `count`: optional number used to render a pluralized help text
                                      for this app state change.

        :param changed:         pass False before change of the app state, or True if the app state has already changed.
        :return:                boolean True if help mode and layout are active and the found target widget is locked,
                                else False.
        """
        app_state_name = help_vars.get('app_state_name')
        if not app_state_name or app_state_name in IGNORED_HELP_STATES:
            return False

        help_id = id_of_state_help(app_state_name)

        if self.help_is_inactive(help_id):
            return False

        ret = self.help_display(help_id, help_vars, key_suffix='after' if changed else '')
        if help_id == self.displayed_help_id and not changed:
            ret = False             # allow app state change
        return ret

    def help_display(self, help_id: str, help_vars: dict[str, Any], key_suffix: str = '', must_have: bool = False
                     ) -> bool:
        """ display help text to the user in activated help mode.

        :param help_id:         help id to show help text for.
        :param help_vars:       variables used in the conversion of the f-string expression to a string.
                                optional items passed to the help text formatter:
                                * `count`: optional number used to render a pluralized help text.
                                * `self`: target widget to show help text for.
        :param key_suffix:      suffix to the key used if the translation is a dict.
        :param must_have:       pass True to display error help text and console output if no help text exists.
        :return:                boolean True if help text got found and displayed.
        """
        has_trans, short_help_id = translation_short_help_id(help_id)
        if not has_trans:
            if not must_have:
                return False
            if self.debug:
                help_id = f"No translation found for help id [b]'{help_id}/{key_suffix}'[/b] in '{default_language()}'"
            else:
                help_id = ''        # show at least the initial help text as fallback
            short_help_id = help_id
            key_suffix = ''
            self.play_beep()
        elif key_suffix == 'after' and 'next_help_id' in has_trans and not self._closing_popup_open_flow_id:
            help_id = short_help_id = has_trans['next_help_id']     # type: ignore # silly mypy, Pycharm is more clever
            key_suffix = ''

        glo_vars = self.global_variables()
        hlw: Any = self.help_layout
        hlw.tip_text = get_f_string(short_help_id, key_suffix=key_suffix, glo_vars=glo_vars, loc_vars=help_vars)
        hlw.targeted_widget = self.help_widget(help_id, help_vars)     # set the help target widget

        self.ensure_top_most_z_index(hlw)
        self.change_observable('displayed_help_id', help_id)
        self._next_help_id = ''

        self.call_method_delayed(0.12, 'on_help_displayed')

        return True

    def help_flow_display(self, help_vars: dict[str, Any], changed: bool = False) -> bool:
        """ actualize the help layout if active, exclusively called by :meth:`~MainAppBase.change_flow`.

        :param help_vars:       help context args/kwargs of the :meth:`~MainAppBase.change_flow` method.
        :param changed:         pass/specify False before the change to the new flow,
                                else pass True if the flow got changed already.
        :return:                boolean True if the help layout is active and the found target widget is locked,
                                else False.
        """
        flow_id = help_vars.get('new_flow_id')
        if not flow_id or flow_id in IGNORED_HELP_FLOWS:
            if not changed or flow_id != CLOSE_POPUP_FLOW_ID or not self._closing_popup_open_flow_id:
                if flow_id == CLOSE_POPUP_FLOW_ID:  # check on close to save opening flow id, to reset in changed call
                    self._closing_popup_open_flow_id = flow_path_id(self.flow_path)
                return False
            flow_id = self._closing_popup_open_flow_id  # reset after call of self.help_display()
        wid = self.widget_by_flow_id(flow_id)
        if wid and 'self' not in help_vars:
            help_vars['self'] = wid                     # set the help widget to opening button after closing the popup

        help_id = id_of_flow_help(flow_id)
        if self.help_is_inactive(help_id):
            return False                                # inactive help layout

        key_suffix = 'after' if changed and not self._closing_popup_open_flow_id else ''
        ret = self.help_display(help_id, help_vars, key_suffix=key_suffix, must_have=not changed)
        self._closing_popup_open_flow_id = ''
        if not changed and (help_id == self.displayed_help_id or flow_action(flow_id) == 'open'):
            # allow flow change of the currently explained flow button or on an open flow action with no help text
            ret = False
        return ret

    def help_is_inactive(self, help_id: str) -> bool:
        """ check if help mode is inactive and reserve/notedown current help id for next help mode activation.

        :param help_id:         help id to be reserved for next help activation with empty help id.
        :return:                boolean True if help mode is inactive, else False.
        """
        hlw = self.help_layout
        if hlw is None:
            if translation_short_help_id(help_id)[0]:
                self._next_help_id = help_id
            return True            # inactive help layout
        return False

    def help_target_and_id(self, help_vars: dict[str, Any]) -> tuple[Any, str]:
        """ find a help widget/target and help id on help mode activation.

        :param help_vars:       optional help vars.
        :return:                tuple of the help target widget and the help id.
        """
        activator = self.help_activator
        if self._next_help_id:
            help_id = self._next_help_id
        elif self.flow_id:
            help_id = id_of_flow_help(self.flow_id)
        else:
            return activator, ''

        target = self.help_widget(help_id, help_vars)
        if target is activator:
            help_id = ''
        return target, help_id

    def help_widget(self, help_id: str, help_vars: dict[str, Any]) -> Any:
        """ ensure/find the help target widget via attribute name/value and extend :paramref:`~help_widget.help_vars`.

        :param help_id:         widget.help_id attribute value to detect widget and call stack locals.
        :param help_vars:       help env variables to be extended with event activation stack frame locals
                                and a 'self' key with the help target widget.
        :return:                the found target widget or self.help_activator if not found.
        """
        wid = help_vars.get('self')
        if not wid or help_id and not getattr(wid, 'help_id', "").startswith(help_id):
            if help_id:
                # look for the widget with help_id attr in kv/enaml rule call stack frame for translation text context
                depth = 1
                while depth <= 15:
                    _gfv, lfv, _deep = stack_vars("", min_depth=depth, max_depth=depth)  # "" to not skip ae.kivy module
                    widget = lfv.get('self')
                    if getattr(widget, 'help_id', None) == help_id:
                        help_vars.update(lfv)
                        return widget
                    depth += 1

                # then search the widget tree
                wid = self.widget_by_attribute('help_id', help_id)
                if not wid:
                    self.vpo(f"MainAppBase.help_widget(): widget with help_id '{help_id}' not found")

            if not wid:
                wid = self.help_activator
            help_vars['self'] = wid

        return wid

    def img_file(self, image_name: str, font_size: Optional[float] = None, light_theme: Optional[bool] = None) -> str:
        """ shortcutting :meth:`~MainAppBase.find_image` method w/o bound property to get the image file path.

        :param image_name:      image name (file name stem).
        :param font_size:       optional font size in pixels.
        :param light_theme:     optional theme (True=light, False=dark).
        :return:                file path of an image file or empty string if a matching image file could not be found.
        """
        if image_name:
            if font_size is None:
                font_size = self.font_size
            if light_theme is None:
                light_theme = self.light_theme

            img_obj = self.find_image(image_name, height=font_size, light_theme=light_theme)
            if img_obj:
                return img_obj.path
        return ''

    def key_press_from_framework(self, modifiers: str, key: str) -> bool:
        """ dispatch key press event, coming normalized from the UI framework.

        :param modifiers:       modifier keys.
        :param key:             key character.
        :return:                boolean True if the key got consumed/used else False.
        """
        self.vpo(f"MainAppBase.key_press_from_framework({modifiers}+{key})")
        if self.help_layout or self.tour_layout:
            return True

        event_name = f'on_key_press_of_{modifiers}_{"space" if key == " " else key}'
        en_lower = event_name.lower()
        if self.call_method(en_lower):
            return True

        if event_name != en_lower and self.call_method(event_name):
            return True

        # call the default handler; pass lower key code; enaml/Qt sends upper-case key code if the Shift key is pressed
        return self.call_method('on_key_press', modifiers, key.lower()) or False

    def load_app_states(self):
        """ prepare app.run_app by loading app states from config files and check for added/updated state vars """
        app_states = {}
        for key in self.app_state_keys():
            pre = f"   #  app state {key=} "
            type_class = type(getattr(self, key))
            value = self.get_variable(key, section=APP_STATE_SECTION_NAME)
            if not isinstance(value, type_class):   # type mismatch - try to autocorrect
                self.dpo(f"{pre}type mismatch: {type_class=} {type(value)=}")
                corr_val = try_call(type_class, value, ignored_exceptions=(Exception, TypeError, ValueError))
                if corr_val is UNSET:
                    self.po(f"{pre}type mismatch in '{value}' could not be corrected to {type_class}")
                else:
                    value = corr_val

            app_states[key] = value

        self.setup_app_states(app_states, send_event=False)  # do not send event because the app framework is not init

        current_version = app_states.get(APP_STATE_VERSION_VAR_NAME, 0)
        if current_version:
            upgrade_version = self.upgraded_config_app_state_version()
            if upgrade_version > current_version:
                for from_version in range(current_version, upgrade_version):
                    self.call_method('on_app_state_version_upgrade', from_version)
                self.change_app_state(APP_STATE_VERSION_VAR_NAME, upgrade_version, send_event=False, old_name=UNSET)

    def load_images(self):
        """ load images from app folder img. """
        file_reg = FilesRegister()
        file_reg.add_register(PORTIONS_IMAGES)
        file_reg.add_paths('img/**')
        file_reg.add_paths('{ado}/img/**')
        self.image_files = file_reg

    def load_sounds(self):
        """ load audio sounds from the app folder snd. """
        file_reg = FilesRegister()
        file_reg.add_register(PORTIONS_SOUNDS)
        file_reg.add_paths('snd/**')
        file_reg.add_paths('{ado}/snd/**')
        self.sound_files = file_reg

    def load_translations(self, lang_code: str):
        """ load translation texts for the passed language code.

        :param lang_code:       the new language code to be set (passed as flow key). empty on first app run/start.
        """
        is_empty = not lang_code
        old_lang = self.lang_code

        lang_code = load_language_texts(lang_code)
        self.change_app_state('lang_code', lang_code)

        if is_empty or lang_code != old_lang:
            default_language(lang_code)
            self.set_var('lang_code', lang_code, section=APP_STATE_SECTION_NAME)  # add optional app state var to config

    def mix_background_ink(self):
        """ remix background ink if one of the basic back colors changes. """
        self.framework_app.mixed_back_ink = mix_colors(self.flow_id_ink, self.flow_path_ink, self.selected_ink)

    def on_app_build(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_build default/fallback event handler called")

    def on_app_exit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_exit default/fallback event handler called")

    def on_app_init(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_init default/fallback event handler called")

    def on_app_quit(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_quit default/fallback event handler called")

    def on_app_run(self):
        """ default/fallback flow change confirmation event handler. """
        self.vpo("MainAppBase.on_app_run default/fallback event handler called - loading resources (img, audio, i18n)")

        self.load_images()

        self.load_sounds()

        register_translations_path()
        register_translations_path("{ado}")
        self.load_translations(self.lang_code)

    def on_app_started(self):
        """ app initialization event - the last one on app startup. """
        self.vpo("MainAppBase.on_app_started default/fallback event handler called - check delayed app tour start")
        # request_app_permissions()   # migrated/moved this call into the ae.core V 0.3.63

        if self.user_id not in self.registered_users:
            # delay self.start_app_tour() call to display tour layout in the correct position (navigation_pos_hint_y)
            self.call_method_delayed(1.2, self.start_app_tour)

    def on_app_state_version_upgrade(self, from_version: int):
        """ upgrade app state config vars from the specified app state version to the next one.

        :param from_version:        app state version to upgrade from.
        """
        if from_version == 4:  # add theme_names, 7 generic colors, and rename (item_) colors
            self.change_app_state('theme_names', self.theme_names, send_event=False, old_name=UNSET)

            self.change_app_state('create_ink', self.create_ink, send_event=False, old_name=UNSET)
            self.change_app_state('delete_ink', self.delete_ink, send_event=False, old_name=UNSET)
            self.change_app_state('error_ink', self.error_ink, send_event=False, old_name=UNSET)
            self.change_app_state('info_ink', self.info_ink, send_event=False, old_name=UNSET)
            self.change_app_state('read_ink', self.read_ink, send_event=False, old_name=UNSET)
            self.change_app_state('update_ink', self.update_ink, send_event=False, old_name=UNSET)
            self.change_app_state('warn_ink', self.warn_ink, send_event=False, old_name=UNSET)

            val = self.get_variable('selected_item_ink', APP_STATE_SECTION_NAME, self.selected_ink)
            self.change_app_state('selected_ink', val, send_event=False, old_name='selected_item_ink')

            val = self.get_variable('unselected_item_ink', APP_STATE_SECTION_NAME, self.unselected_ink)
            self.change_app_state('unselected_ink', val, send_event=False, old_name='unselected_item_ink')

        elif from_version == 5:  # until V6 release/for V5: not in app.app_states, but available as main_app attributes
            self.change_app_state('cancel_ink', self.cancel_ink, send_event=False, old_name=UNSET)
            self.change_app_state('confirm_ink', self.confirm_ink, send_event=False, old_name=UNSET)
            self.change_app_state('help_ink', self.confirm_ink, send_event=False, old_name=UNSET)

    def on_app_tour_toggle(self, _flow_key: str, _event_kwargs: EventKwargsType) -> bool:
        """ event handler for to start/stop an app onboarding tour.

        :param _flow_key:       (unused)
        :param _event_kwargs:   (unused)
        :return:                always True.
        """
        if self.tour_layout:
            self.tour_layout.stop_tour()
            return True

        self.close_popups()
        return self.start_app_tour()

    def on_debug_level_change(self, level_name: str, _event_kwargs: EventKwargsType) -> bool:
        """ debug level app state change flow change confirmation event handler.

        :param level_name:      the new debug level name to be set (passed as the flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                boolean True to confirm the debug level change.
        """
        debug_level = next(num for num, name in DEBUG_LEVELS.items() if name == level_name)
        self.vpo(f"MainAppBase.on_debug_level_change to {level_name} -> {debug_level}")
        self.set_opt('debug_level', debug_level)
        return True

    def on_flow_change(self, flow_id: str, event_kwargs: EventKwargsType) -> bool:
        """ checking if exists a Popup class for the new flow and if yes, then open it.

        :param flow_id:         new flow id.
        :param event_kwargs:    optional event kwargs; the optional item with the key `popup_kwargs`
                                will be passed onto the `__init__` method of the found Popup class.
        :return:                boolean True if Popup class was found and displayed.

        this method is mainly used as the last fallback clicked flow change confirmation event handler of a FlowButton.
        """
        class_name = flow_popup_class_name(flow_id)
        self.vpo(f"MainAppBase.on_flow_change {flow_id=} {event_kwargs=} {class_name=}")

        if flow_id:
            popup_class = self.class_by_name(class_name)
            if popup_class:
                popup_kwargs = event_kwargs.get('popup_kwargs', {})
                self.open_popup(popup_class, **popup_kwargs)
                return True
        return False

    def on_flow_id_ink(self):
        """ redirect flow id back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_flow_path_ink(self):
        """ redirect flow path back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_flow_popup_close(self, _flow_key: str, _event_kwargs: EventKwargsType) -> bool:
        """ default popup close handler of FlowPopup widget, updates of :attr:`flow_path` and resets help widget/text.

        :param _flow_key:       unused flow key.
        :param _event_kwargs:   unused popup args.
        :return:                always returning True.
        """
        if self.help_layout and self.help_widget(self.displayed_help_id, {}) is self.help_activator:
            self.help_display('', {})
        return True

    def on_font_size(self):
        """ app state change event handler to synchronize the :attr:`MainAppBase.space_width` attribute. """
        self.space_width = self.font_size / 2.25

    def on_key_press(self, modifiers: str, key_code: str) -> bool:
        """ check key press event to be handled and processed as command/action.

        :param modifiers:       modifier keys.
        :param key_code:        code of the pressed key.
        :return:                boolean True if the key press event got handled, else False.
        """
        popups_open = list(self.popups_opened())
        self.vpo(f"MainAppBase.on_key_press {modifiers=} {key_code=} {popups_open=}")
        if popups_open and key_code == 'escape':
            popups_open[0].dismiss()
            return True
        return False

    def on_lang_code_change(self, lang_code: str, _event_kwargs: EventKwargsType) -> bool:
        """ language app state change flow change confirmation event handler.

        :param lang_code:       the new language code to be set (passed as flow key). empty on first app run/start.
        :param _event_kwargs:   unused event kwargs.
        :return:                boolean True to confirm the language change.
        """
        self.vpo(f"MainAppBase.on_lang_code_change to {lang_code}")
        self.load_translations(lang_code)
        return True

    def on_light_theme_change(self, _flow_key: str, event_kwargs: EventKwargsType) -> bool:
        """ app theme app state change flow change confirmation event handler.

        :param _flow_key:       flow key.
        :param event_kwargs:    event kwargs with the key `'light_theme'` containing True|False for light|dark theme.
        :return:                boolean True to confirm the change of the flow id.
        """
        light_theme: bool = event_kwargs['light_theme']
        self.vpo(f"MainAppBase.on_light_theme_change to {light_theme}")
        self.change_app_state('light_theme', light_theme)
        return True

    def on_selected_ink(self):
        """ redirect the selected item back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_theme_change(self, theme_id: str, _event_kwargs: EventKwargsType) -> bool:
        """ change app theme event handler.

        :param theme_id:        flow key with the id/name of the theme to switch to.
        :param _event_kwargs:   unused event kwargs.
        :return:
        """
        self.vpo(f"MainAppBase.on_theme_change to '{theme_id}'")

        self.theme_load(theme_id)

        return True

    def on_theme_delete(self, theme_id: str, _event_kwargs: EventKwargsType) -> bool:
        """ change app theme event handler.

        :param theme_id:        flow key with the id/name of the theme to delete.
        :param _event_kwargs:   unused event kwargs.
        :return:
        """
        self.vpo(f"MainAppBase.on_theme_delete '{theme_id}'")

        self.theme_delete(theme_id)

        return True

    def on_theme_save(self, theme_id: str, _event_kwargs: EventKwargsType) -> bool:
        """ event handler to save app theme if not exist, or overwrite it after confirmation.

        :param theme_id:        flow key with the name/id of the theme to add/update.
        :param _event_kwargs:   unused event kwargs.
        :return:                a True value if the flow got accepted/redirected and changed, else False.
        """
        self.vpo(f"MainAppBase.on_theme_save of '{theme_id}'")

        if theme_id in self.theme_names:
            return self.show_confirmation(get_text("confirm the update of this theme with the actual configuration"),
                                          title=get_f_string(f"update theme {theme_id}"),
                                          confirm_flow_id=id_of_flow('update', 'theme', theme_id),
                                          )

        self.theme_save(theme_id)       # saving and adding a new theme

        return True

    def on_theme_update(self, theme_id: str, _event_kwargs: EventKwargsType) -> bool:
        """ event handler to update/overwrite an existing app theme.

        :param theme_id:        flow key with the name/id of the theme to update.
        :param _event_kwargs:   unused event kwargs.
        :return:                boolean True if the flow got accepted and changed, else False.
        """
        self.vpo(f"MainAppBase.on_theme_update of '{theme_id}'")

        self.theme_save(theme_id)           # save/update the existing theme

        return True

    def on_unselected_ink(self):
        """ redirect unselected item back ink app state color change event handler to actualize mixed_back_ink. """
        self.mix_background_ink()

    def on_user_register(self, user_id: str, event_kwargs: dict[str, Any]) -> bool:
        """ called on close of UserNameEditorPopup to check user input and create/register the current os user.

        :param user_id:         new/old user id, passed as :paramref:`~ae.console.ConsoleApp.register_user.new_user_id`
                                kwarg to the method :meth:`ConsoleApp.register_user`.
        :param event_kwargs:    event kwargs, plus optionally the following kwargs which will be extracted from the
                                event kwargs and passed onto the :meth:`ae.console.ConsoleApp.register_user` method:
                                * :paramref:`~ae.console.ConsoleApp.register_user.reset_cfg_vars`
                                * :paramref:`~ae.console.ConsoleApp.register_user.set_as_default`
        :return:                True if user got registered else False.
        """
        if not user_id:
            self.show_message(get_text("please enter your user or nick name"))
            return False
        if len(user_id) > USER_NAME_MAX_LEN:
            self.show_message(get_f_string(
                "please shorten your user name to not more than {USER_NAME_MAX_LEN} characters", glo_vars=globals()))
            return False

        chk_id = norm_name(user_id)
        if user_id != chk_id:
            self.show_message(get_f_string(
                "please remove spaces and the characters "
                "'{''.join(ch for ch in user_id if ch not in chk_id)}' from your user name",
                glo_vars=locals().copy()))
            return False

        reg_usr_args = {_key: _arg for _key in ('reset_cfg_vars', 'set_as_default')
                        if (_arg := event_kwargs.pop(_key, None)) is not None}
        self.register_user(new_user_id=user_id, **reg_usr_args)

        return True

    def open_popup(self, popup_class: Type, **popup_kwargs) -> Any:
        """ open Popup/DropDown, calling the `open`/`show` method of the instance created from the passed popup class.

        :param popup_class:     class of the Popup/DropDown widget/window.
        :param popup_kwargs:    args to instantiate and show/open the popup.
        :return:                the created and displayed/opened popup class instance.

        .. hint::
            overwrite this method if the used GUI framework is providing a different method to open a popup window or if
            a widget in the Popup/DropDown needs to get the input focus.
        """
        self.dpo(f"MainAppBase.open_popup {popup_class} {popup_kwargs}")
        popup_instance = popup_class(**popup_kwargs)
        open_method = getattr(popup_instance, 'open', getattr(popup_instance, 'show', None))
        if callable(open_method):
            open_method()
        return popup_instance

    def play_beep(self):
        """ make a short beep sound, should be overwritten by the used GUI framework. """
        self.po(chr(7), "MainAppBase.BEEP")

    def play_sound(self, sound_name: str):
        """ play an audio/sound file, should be overwritten by the GUI framework.

        :param sound_name:  name of the sound to play.
        """
        self.po(f"MainAppBase.play_sound {sound_name}")

    def play_vibrate(self, pattern: tuple = (0.0, 0.09, 0.21, 0.3, 0.09, 0.09, 0.21, 0.09)):
        """ play a vibration pattern, to be overwritten by GUI-framework-specific implementation.

        :param pattern:     optional tuple of pause and vibrate time sequence - use an error pattern if not passed.
        """
        self.po(f"MainAppBase.play_vibrate {pattern}")

    def popups_opened(self, classes: tuple = ()) -> list:
        """ determine all popup-like container widgets that are currently opened.

        :param classes:         optional class filter - if not passed, then only the widgets underneath win/root with an
                                `open` method will be added. pass tuple of popup widget classes to restrict the returned
                                popup instances. like e.g., pass `(Popup, DropDown, FlowPopup)` to get all popups of
                                an ae/Kivy app (in Kivy use Factory.WidgetClass if widget is declared only in kv lang).
        :return:                list of the foremost opened/visible popup class instances (children of the app window),
                                matching the :paramref:`classes` or having an `open` method, ordered by their
                                z-coordinate (the most front widget first).
        """
        filter_func = (lambda _wg: isinstance(_wg, classes)) if classes else \
            (lambda _wg: callable(getattr(_wg, 'open', None)))

        popups = []
        for wid in self.framework_win.children:
            if filter_func(wid):
                popups.append(wid)

        return popups

    def register_user(self, **kwargs) -> bool:          # pragma: no cover # pylint: disable=arguments-differ
        """ on user registration always disable app onboarding tours on app start

        :param kwargs:          see the :meth:`ConsoleApp.register_user` method.
        :return:                see the :meth:`ConsoleApp.register_user` method.

        .. hint::
            also called on the tour end, after the user has entered a valid username/id in UserNameEditorPopup
            and confirmed it via the FlowButton id_of_flow('register', 'user').
        """
        ret = super().register_user(**kwargs)

        var_name = 'onboarding_tour_started'
        self.set_variable(var_name + '_' + self.user_id, self.get_variable(var_name, default_value=-3))
        self.set_variable(var_name, 0)  # reset onboarding tour start counter cfg var for other/non-registered users

        return ret

    def retrieve_app_states(self) -> AppStatesType:
        """ determine the state of a running app from the main app instance and return it as dict.

        :return:                dict with all app states available in the config files.
        """
        app_states = {}
        for key in self.app_state_keys():
            if (value := getattr(self, key, UNSET)) is not UNSET:   # is-UNSET/skip if app state variable got renamed
                app_states[key] = value

        self.dpo(f"MainAppBase.retrieve_app_states {app_states}")
        return app_states

    def run_app(self):
        """ startup main and framework applications. """
        super().run_app()                               # parse command line arguments into config options
        self.dpo(f"MainAppBase.run_app {self.app_name}")

        self.call_method('on_app_run')

        if self._start_event_loop:                  # not needed for sub-apps/-threads or additional Window instances
            try:
                self._start_event_loop()
            finally:
                self.call_method('on_app_quit')
                self.shutdown(self._exit_code or None)  # don't call sys.exit() for zero exit code

    def save_app_states(self) -> str:
        """ save app state in the main config file.

        :return:                empty string if app status could be saved into config files else error message.
        """
        if self.tour_layout:
            return "running app tour prevent to save app states into config file"   # was: self.tour_layout.stop_tour()

        err_msg = ""

        app_states = self.retrieve_app_states()
        for key, state in app_states.items():
            if isinstance(state, (list, dict)):
                state = deepcopy(state)

            new_state = self.call_method(f'on_app_state_{key}_save', state)
            if new_state is not None:
                state = new_state

            if key == 'flow_id' and flow_action(state) != 'focus':
                state = id_of_flow('')
            elif key == 'flow_path':
                state = flow_path_strip(state)

            err_msg = self.set_var(key, state, section=APP_STATE_SECTION_NAME)
            self.vpo(f"MainAppBase.save_app_state {key=} {state=} {err_msg=}")
            if err_msg:
                break

        self.load_cfg_files()

        if self.debug_level:
            self.play_sound('error' if err_msg else 'debug_save')

        return err_msg

    def setup_app_states(self, app_states: AppStatesType, send_event: bool = True):
        """ put app state variables into the main app instance to prepare framework app.run_app.

        :param app_states:      dict of the app states.
        :param send_event:      pass False to prevent send/call of the main_app.on_<app_state_name> event.
        """
        self.vpo(f"MainAppBase.setup_app_states {app_states=} {send_event=}")

        # init/add app states (e.g. for self.img_file() calls in .kv with font_size/light_theme bindings)
        font_size = app_states.get('font_size') or 0.0          # ensure it is a float
        if not MIN_FONT_SIZE <= font_size <= MAX_FONT_SIZE:
            if font_size < 0.0:
                font_size = self.dpi_factor() * -font_size      # adopt device scaling on the very first app start
            elif font_size == 0.0:
                font_size = self.font_size
            app_states['font_size'] = min(max(MIN_FONT_SIZE, font_size), MAX_FONT_SIZE)
        if 'light_theme' not in app_states:
            app_states['light_theme'] = self.light_theme

        for key, val in app_states.items():
            self.change_app_state(key, val, send_event=send_event)   # on_{app_state}-events if the UI framework is init
            if key == 'flow_id' and flow_action(val) == 'focus':
                self._last_focus_flow_id = val

    def show_confirmation(self, message: str, title: str = "", confirm_flow_id: str = '',
                          confirm_kwargs: Optional[EventKwargsType] = None, confirm_text: str = "") -> bool:
        """ display a simple confirmation popup to the user, implemented by the used UI-framework.

        :param message:         message string to display.
        :param title:           title of confirmation box.
        :param confirm_flow_id: tap_flow_id of the 'confirm' button.
        :param confirm_kwargs:  tap_kwargs event args of the 'confirm' button.
        :param confirm_text:    confirmation button text. if not passed, then the i18n translation of "confirm" is used.
        :return:                boolean True if the flow got accepted and changed, else False.
        """
        event_kwargs = popup_event_kwargs(message, title, confirm_flow_id, confirm_kwargs, confirm_text)
        return self.change_flow(id_of_flow('show', 'confirmation'), **event_kwargs)

    def show_input(self, message: str, title: str = "", input_default: str = "", enter_confirms: bool = True,
                   confirm_flow_id: str = '', confirm_kwargs: Optional[EventKwargsType] = None, confirm_text: str = ""
                   ) -> bool:
        """ display a simple input box popup to the user, implemented by the used UI-framework.

        :param message:         prompt message to display.
        :param title:           title of input box. no title string will be displayed if not specified.
        :param input_default:   input default text. if not specified, then the input field will be empty.
        :param enter_confirms:  pass False to disable the confirmation via pressing the enter key in the input field.
        :param confirm_flow_id: tap_flow_id of the 'confirm' button. the string entered by
                                the user will be amended as the flow key to it.
        :param confirm_kwargs:  tap_kwargs event args of the 'confirm' button.
        :param confirm_text:    confirmation button text. if not passed, then the i18n translation of "confirm" is used.
        :return:                boolean True value if the flow got accepted and changed, else False.
        """
        event_kwargs = popup_event_kwargs(message, title, confirm_flow_id, confirm_kwargs, confirm_text,
                                          input_default=input_default, enter_confirms=enter_confirms)
        return self.change_flow(id_of_flow('show', 'input'), **event_kwargs)

    def show_message(self, message: str, title: str = "", is_error: bool = True) -> bool:
        """ display (error) message popup to the user, implemented by the used UI-framework.

        :param message:         message string to display.
        :param title:           title of message box.
        :param is_error:        pass False to not emit error tone/vibration.
        :return:                boolean True if the flow got accepted and changed, else False.
        """
        if is_error:
            self.play_vibrate()
            self.play_beep()

        event_kwargs = popup_event_kwargs(message, title)
        return self.change_flow(id_of_flow('show', 'message'), **event_kwargs)

    def start_app_tour(self, tour_class: Optional[Type[TourBase]] = None) -> bool:
        """ start a new app tour, automatically cancelling a currently running app tour.

        :param tour_class:          optional tour (pages) class, default: tour of current help id or `OnboardingTour`.
        :return:                    boolean True if the UI-framework supports tours/has tour_overlay_class set and tour
                                    got started.
        """
        if not self.help_activator:
            self.po("MainAppBase.start_app_tour(): tour start cancelled because help activator button is missing")
            return False

        tour_layout_class = self.tour_overlay_class
        if not tour_layout_class:
            self.po("MainAppBase.start_app_tour(): tour start cancelled because tour overlay/layout class is not set")
            return False

        if self.tour_layout:
            self.tour_layout.stop_tour()
        tour_layout_class(self, tour_class=tour_class)  # pylint: disable=not-callable # false positive
        return bool(self.tour_layout)   # overlay instance sets main_app./framework_app.tour_layout on tour start

    def stop_app(self, exit_code: int = 0):
        """ quit this application.

        :param exit_code:   optional exit code.
        """
        self.dpo(f"MainAppBase.stop_app {exit_code}")
        self._exit_code = exit_code

        if self.framework_win:
            self.framework_win.close()      # close the GUI-framework window to save app state data and fire on_app_stop

        self.call_method('on_app_exit')

        if self._stop_event_loop:
            self._stop_event_loop()         # will exit the self._start_event_loop() method called by self.run_app()

    def theme_load(self, theme_id: str):
        """ load app theme-specific app state variables from the config file.

        :param theme_id:        name (id string) of the theme to be loaded (overwrites main config theme variables).
        """
        self.vpo(f"MainAppBase.theme_load({theme_id})")

        app_states: AppStatesType = {}
        for var_name in self.theme_specific_cfg_vars:
            var_value = self.get_variable(THEME_VARIABLE_PREFIX + var_name, section=THEME_SECTION_PREFIX + theme_id)
            if var_value is None:
                var_value = getattr(self, var_name, None)
            if var_value is not None:
                app_states[var_name] = var_value
        self.setup_app_states(app_states)

        self.theme_update_names(theme_id)

    def theme_delete(self, theme_id: str):
        """ delete the app theme from the main config file.

        :param theme_id:        name (id string) of the theme to delete.
        """
        self.vpo(f"MainAppBase.theme_delete({theme_id})")

        self.theme_update_names(theme_id, delete=True)
        self.del_section(THEME_SECTION_PREFIX + theme_id)

    def theme_save(self, theme_id: str):
        """ save app theme-specific app state variables to the main config file.

        :param theme_id:        name (id string) of the theme to be saved.
        """
        self.vpo(f"MainAppBase.theme_save({theme_id})")
        if not theme_id:        # skip save if the user entered empty string as theme id/name
            return

        for var_name in self.theme_specific_cfg_vars:
            var_value = getattr(self, var_name)
            self.set_variable(THEME_VARIABLE_PREFIX + var_name, var_value, section=THEME_SECTION_PREFIX + theme_id)

        self.theme_update_names(theme_id)

    def theme_update_names(self, theme_id: str, delete: bool = False):
        """ delete or update the app state list of available themes, on update sets the specified theme as the 1st item.

        :param theme_id:        name (id string) of the actual theme to delete/update.
        :param delete:          pass True to remove the theme specified by :paramref:`~theme_update_names.theme_id`
                                from the app state list of theme names.
        """
        themes = self.theme_names
        if theme_id in themes:
            themes.remove(theme_id)                     # first remove specified theme if already exists
        if not delete:
            themes = [theme_id] + themes                # move the specified theme to the 1st item of the theme list
        self.change_app_state('theme_names', themes)
        self.save_app_states()

    def upgraded_config_app_state_version(self) -> int:
        """ determine the app state version of an app upgrade.

        :return:                value of app state variable APP_STATE_VERSION_VAR_NAME if the app got upgraded (and has
                                a config file from a previous app installation), else 0.
        """
        cfg_file_name = os_path_join(MOVES_SRC_FOLDER_NAME, self.app_name + INI_EXT)
        cfg_parser = instantiate_config_parser()
        cfg_parser.read(cfg_file_name, encoding='utf-8')
        return cfg_parser.getint(APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME, fallback=0)

    def widget_by_app_state_name(self, app_state_name: str) -> Optional[Any]:
        """ determine the first (top-most on z-axis) widget having the passed app state name (app_state_name).

        :param app_state_name:  app state name of the widget's `app_state_name` attribute.
        :return:                widget that has an ` app_state_name ` attribute with the passed app state name
                                or None if not found.
        """
        return self.widget_by_attribute('app_state_name', app_state_name)

    def widget_by_attribute(self, att_name: str, att_value: str, root_widget: Optional[Any] = None) -> Optional[Any]:
        """ determine the first (top-most on z-axis) widget having the passed attribute name and value.

        :param att_name:        attribute name of the searched widget.
        :param att_value:       attribute value of the searched widget.
        :param root_widget:     optional root widget to start the search from, else search from the widget tree root.
        :return:                widget that has the specified attribute with the specified value or None if not found.
        """
        return self.find_widget(lambda widget: getattr(widget, att_name, None) == att_value, root_widget=root_widget)

    def widget_by_id(self, widget_id: str, root_widget: Optional[Any] = None) -> Optional[Any]:
        """ determine the first (top-most on z-axis) widget identified by the passed widget_id.

        :param widget_id:       id of the widget to search for.
        :param root_widget:     optional root widget to start the search from, else search from the widget tree root.
        :return:
        """
        return self.widget_by_attribute('id', widget_id, root_widget=root_widget)

    def widget_by_flow_id(self, flow_id: str) -> Optional[Any]:
        """ determine the first (top-most on z-axis) widget having the passed flow_id.

        :param flow_id:         flow id value of the searched widget's `tap_flow_id`/`focus_flow_id` attribute.
        :return:                widget that has a `tap_flow_id`/`focus_flow_id` attribute with the value of the passed
                                flow id or None if not found.
        """
        return self.widget_by_attribute('tap_flow_id', flow_id) or self.widget_by_attribute('focus_flow_id', flow_id)

    def widget_by_page_id(self, page_id: str) -> Optional[Any]:
        """ determine the first (top-most on z-axis) widget having the passed tour page id.

        :param page_id:         widgets tour page id from `tap_flow_id`/`focus_flow_id`/`app_state_name` attribute.
        :return:                widget that has a `tap_flow_id`/`focus_flow_id`/`app_state_name` attribute with the
                                value of the passed page id or None if not found.
        """
        return self.widget_by_flow_id(page_id) or self.widget_by_app_state_name(page_id)

    def widget_children(self, wid: Any, only_visible: bool = False) -> list:
        """ determine the children of the widget or its container (if exists) in z-order (top-/foremost first).

        :param wid:             widget to determine the children from.
        :param only_visible:    pass True to only return visible widgets.
        :return:                list of the wid's children widgets.
        """
        wid_visible = self.widget_visible
        return [chi for chi in getattr(wid, 'container', wid).children if not only_visible or wid_visible(chi)]

    @staticmethod
    def widget_pos(wid: Any) -> tuple[float, float]:
        """ return the absolute window x and y position of the passed widget.

        :param wid:             widget to determine the position of.
        :return:                tuple of x and y screen/window coordinate.
        """
        return getattr(wid, 'x', 0.0), getattr(wid, 'y', 0.0)  # use getattr because None/framework_win doesn't have x/y

    def widget_tourable_children_page_ids(self, parent_widget: Any) -> list:
        """ determine all visible and tourable children widgets of the passed parent and its child container widgets.

        :param parent_widget:   parent widget to determine all children that are tourable.
        :return:                tourable children page ids list of the passed parent widget.
        """
        tourable_children = []
        for wid in self.widget_children(parent_widget, only_visible=True):
            page_id = widget_page_id(wid)
            if not page_id:
                tourable_children.extend(self.widget_tourable_children_page_ids(wid))
            elif page_id not in tourable_children:
                tourable_children.append(page_id)
        return tourable_children

    def widgets_enclosing_rectangle(self, widgets: Union[list, tuple]) -> tuple[float, float, float, float]:
        """ calculate the minimum bounding rectangle of all the passed widgets.

        :param widgets:         list/tuple of widgets to determine the minimum bounding rectangle for.
        :return:                tuple of floats, with the x, y, width, height values of the bounding rectangle.
        """
        min_x = min_y = 999999.9
        max_x = max_y = 0.0

        for wid in widgets:
            w_x, w_y = self.widget_pos(wid)
            min_x = min(min_x, w_x)
            min_y = min(min_y, w_y)

            w_w, w_h = self.widget_size(wid)
            max_x = max(max_x, w_x + w_w)
            max_y = max(max_y, w_y + w_h)

        return min_x, min_y, max_x - min_x, max_y - min_y

    @staticmethod
    def widget_size(wid: Any) -> tuple[float, float]:
        """ return the size (width and height) in pixels of the passed widget.

        :param wid:             widget to determine the size of.
        :return:                tuple of width and height in pixels.
        """
        return getattr(wid, 'width', 0.0), getattr(wid, 'height', 0.0)      # wid==None does not have width/height

    @staticmethod
    def widget_visible(wid: Any) -> bool:
        """ determine if the passed widget is visible (has width and height and (visibility or opacity) set).

        :param wid:             widget to determine visibility of.
        :return:                boolean True if the widget is visible (or visibility cannot be determined),
                                False if hidden.
        """
        return bool(wid.width and wid.height and
                    getattr(wid, 'visible', True) in (True, None) and   # containers/BoxLayout.visible is None ?!?!?
                    getattr(wid, 'opacity', True))

    def width_spaces(self, width: int) -> str:
        """ return the number of spaces that result in the specified width by using the app font_size. """
        return " " * round(width / self.space_width)

    def win_pos_size_change(self, *win_pos_size):
        """ screen resize handler called on window resize or when the app will exit/stop via closed event.

        :param win_pos_size:    window geometry/coordinates: x, y, width, height.
        """
        app = self.framework_app
        win_width, win_height = win_pos_size[2:]
        app.landscape = win_width >= win_height                 # update landscape flag

        self.vpo(f"MainAppBase.win_pos_size_change {win_pos_size=} {app.landscape=}")

        self.change_app_state('win_rectangle', win_pos_size)
        self.call_method('on_win_pos_size')
