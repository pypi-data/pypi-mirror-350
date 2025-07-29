"""
GUI app constants and helper functions
--------------------------------------
"""
import re

from math import cos, sin, sqrt
from typing import Any, Callable, Optional, Type, Union

from ae.base import (                                                                                   # type: ignore
    NAME_PARTS_SEP, norm_path, os_path_dirname, os_path_join, os_platform, snake_to_camel, stack_var)
from ae.paths import path_name, placeholder_path, FilesRegister                                         # type: ignore
from ae.i18n import get_text, translation                                                               # type: ignore


APP_STATE_SECTION_NAME = 'aeAppState'           #: config section name to store app state
APP_STATE_VERSION_VAR_NAME = 'app_state_version'  #: config variable name to store the current application state version

MIN_FONT_SIZE = 15.0                            #: minimum (see :attr:`~ae.kivy.apps.FrameworkApp.min_font_size`) and
MAX_FONT_SIZE = 99.0                            #: .. maximum font size in pixels

# inks for the non-colors black, gray and white (!= 0/1 to differentiate from the framework's pure black/white colors)
COLOR_BLACK = [0.009, 0.006, 0.003, 1.0]        #: black ink
COLOR_DARK_GREY = [0.309, 0.306, 0.303, 1.0]    #: dark grey ink
COLOR_GREY = [0.509, 0.506, 0.503, 1.0]         #: grey ink
COLOR_LIGHT_GREY = [0.699, 0.696, 0.693, 1.0]   #: light grey ink
COLOR_WHITE = [0.999, 0.996, 0.993, 1.0]        #: white ink

RELIEF_ANGLE_BEG = 69                           #: beginning angle for ellipse drawings via :func:`relief_colors`
RELIEF_ANGLE_END = 249                          #: ending angle for ellipse drawings via :func:`relief_colors`

THEME_DARK_BACKGROUND_COLOR = COLOR_BLACK       #: dark theme background color in rgba(0.0 ... 1.0)
THEME_DARK_FONT_COLOR = COLOR_WHITE             #: dark theme font color in rgba(0.0 ... 1.0)
THEME_LIGHT_BACKGROUND_COLOR = COLOR_WHITE      #: light theme background color in rgba(0.0 ... 1.0)
THEME_LIGHT_FONT_COLOR = COLOR_BLACK            #: light theme font color in rgba(0.0 ... 1.0)

THEME_SECTION_PREFIX = 'aeTheme_'               #: config-files section name prefix for to store app theme vars
THEME_VARIABLE_PREFIX = 'MUSASV_'               #: mangle app state var names to not be interpreted as user-specific

FLOW_KEY_SEP = ':'                              #: separator character between flow action/object and flow key

FLOW_ACTION_RE = re.compile("[a-z0-9]+")        #: regular expression detecting invalid characters in flow action string
FLOW_OBJECT_RE = re.compile("[A-Za-z0-9_]+")    #: regular expression detecting invalid characters in flow object string

APP_STATE_HELP_ID_PREFIX = 'help_app_state#'                        #: message id prefix for app state change help texts
FLOW_HELP_ID_PREFIX = 'help_flow#'                                  #: message id prefix for flow change help texts
TOUR_PAGE_HELP_ID_PREFIX = 'tour_page#'                             #: message id prefix of tour page text/dict

TOUR_START_DELAY_DEF = 0.15                                         #: default value of tour start delay in seconds
TOUR_EXIT_DELAY_DEF = 0.45                                          #: default value of tour exit delay in seconds

PORTIONS_IMAGES = FilesRegister()                                   #: app image files register
PORTIONS_SOUNDS = FilesRegister()                                   #: app audio/sound files register

REGISTERED_TOURS: dict[str, Type] = {}                              #: map(name: class) of all registered tour classes


AnchorSpecType = tuple[float, float, str]                           #: (see return value of :func:`anchor_spec`)

AppStatesType = dict[str, Any]                                      #: app state config variable type

ColorRGB = Union[tuple[float, float, float], list[float]]           #: color red, green and blue parts
ColorRGBA = Union[tuple[float, float, float, float], list[float]]   #: ink is rgb color and alpha
ColorOrInk = Union[ColorRGB, ColorRGBA]                             #: color or ink type

EventKwargsType = dict[str, Any]                                    #: change flow event kwargs type

ExplainedMatcherType = Union[Callable[[Any], bool], str]            #: single explained widget matcher type

HelpVarsType = dict[str, Any]                                       #: help context variables for help text rendering

PopupsToCloseType = Union[int, tuple]                               #: popups to close on button-press/flow-change

ReliefColors = Union[tuple[ColorRGB, ColorRGB], tuple]              #: tuple of top/bottom relief colors or empty tuple


def anchor_layout_x(anchor_spe: AnchorSpecType, layout_width: float, win_width: float) -> float:
    """ calculate the anchor's x position of the layout box.

    :param anchor_spe:      :data:`AnchorSpecType` instance (:func:`anchor_spec` return) with anchor position/direction.
    :param layout_width:    anchor layout width.
    :param win_width:       app window width.
    :return:                absolute x coordinate within the app window of anchor layout.
    """
    anchor_x, _anchor_y, anchor_dir = anchor_spe
    if anchor_dir == 'l':
        return anchor_x - layout_width
    if anchor_dir == 'r':
        return anchor_x
    return min(max(0.0, anchor_x - layout_width / 2), win_width - layout_width)


def anchor_layout_y(anchor_spe: AnchorSpecType, layout_height: float, win_height: float) -> float:
    """ calculate the layout box y position of an anchor.

    :param anchor_spe:      :data:`AnchorSpecType` tuple with anchor position and direction.
    :param layout_height:   anchor layout height.
    :param win_height:      app window height.
    :return:                the absolute y coordinate in the app window of anchor layout.
    """
    _anchor_x, anchor_y, anchor_dir = anchor_spe
    if anchor_dir == 'i':
        return anchor_y
    if anchor_dir == 'd':
        return anchor_y - layout_height
    return min(max(0.0, anchor_y - layout_height / 2), win_height - layout_height)


def anchor_points(font_size: float, anchor_spe: AnchorSpecType) -> tuple[float, ...]:
    """ recalculate points of the anchor triangle drawing.

    :param font_size:       font_size to calculate the size (radius == hypotenuse / 2) of the anchor triangle.
    :param anchor_spe:      anchor specification tuple: x/y coordinates and direction - see :func:`anchor_spec` return.
    :return:                6-item-tuple with the three x and y coordinates of the anchor triangle edges.
    """
    if not anchor_spe:
        return ()           # return empty tuple to prevent run-time-error at kv build/init

    radius = font_size * 0.69
    anchor_x, anchor_y, anchor_dir = anchor_spe
    return (anchor_x - (radius if anchor_dir in 'id' else 0),
            anchor_y - (radius if anchor_dir in 'lr' else 0),
            anchor_x + (0 if anchor_dir in 'id' else radius * (-1 if anchor_dir == 'r' else 1)),
            anchor_y + (0 if anchor_dir in 'lr' else radius * (-1 if anchor_dir == 'i' else 1)),
            anchor_x + (radius if anchor_dir in 'id' else 0),
            anchor_y + (radius if anchor_dir in 'lr' else 0),
            )


def anchor_spec(wid_x: float, wid_y: float, wid_width: float, wid_height: float, win_width: float, win_height: float
                ) -> AnchorSpecType:
    """ calculate anchor center pos (x, y) and anchor direction to the targeted widget.

    :param wid_x:           the absolute x coordinate in the main app window of the targeted widget.
    :param wid_y:           the absolute y coordinate in the main app window of the targeted widget.
    :param wid_width:       width of targeted widget.
    :param wid_height:      height of targeted widget.
    :param win_width:       app window width.
    :param win_height:      app window height.
    :return:                tooltip anchor specification tuple (:data:`AnchorSpecType`) with the three items:

                            * anchor_x (the absolute anchor center x-coordinate in the app main window),
                            * anchor_y (the absolute anchor center y-coordinate in the app main window) and
                            * anchor_dir (anchor direction: 'r'=right, 'i'=increase-y, 'l'=left, 'd'=decrease-y)

                            .. note::
                                the direction in the y-axis got named increase for higher y values and `decrease` for
                                lower y values to support different coordinate systems of the GUI frameworks.

                                e.g., Kivy has the y-axis zero value at the bottom of the app window, whereas in
                                enaml/Qt it is at the top.

    """
    max_width = win_width - wid_x - wid_width
    if max_width < wid_x:
        max_width = wid_x
        anchor_dir_x = 'l'
    else:
        anchor_dir_x = 'r'
    max_height = win_height - wid_y - wid_height
    if max_height < wid_y:
        max_height = wid_y
        anchor_dir_y = 'd'
    else:
        anchor_dir_y = 'i'
    if max_width > max_height:
        anchor_dir = anchor_dir_x
        anchor_x = wid_x + (0 if anchor_dir_x == 'l' else wid_width)
        anchor_y = wid_y + wid_height / 2
    else:
        anchor_dir = anchor_dir_y
        anchor_x = wid_x + wid_width / 2
        anchor_y = wid_y + (0 if anchor_dir_y == 'd' else wid_height)

    return anchor_x, anchor_y, anchor_dir


def brighten_color(color_or_ink: ColorOrInk, factor: float = 0.3) -> ColorOrInk:
    """ brightens the specified color/ink without changing an optionally passed alpha/occupancy value.

    :param color_or_ink:    the color or ink to be brightened.
    :param factor:          the factor to brighten the color or ink by. its value must range between -1 and 1,
                            0 results in no brightening at all (original color), positive values are using the
                            more complex HSV algorithm, and negative values the efficient RGB brightening algorithm.
                            so +1 returns the brightest value of the specified color, whereas -1 results as white.
    :return:                the brightened color or ink, as the same type as the input.
    """
    if factor > 0:
        hsv = color_to_hsv(color_or_ink)
        hsv = hsv[0], hsv[1] * (1.0 - factor), min(1.0, hsv[2] * (1.0 + factor))
        rgb = list(color_from_hsv(hsv))
    else:
        rgb = list(min(1.0, _ + (1.0 - _) * -factor) for _ in color_or_ink[:3])
    return rgb + list(color_or_ink[3:])


def color_from_hsv(hsv: tuple[float, float, float]) -> ColorRGB:
    """ convert HSV-color (H: 0-360, S: 0-1, V: 0-1) into its corresponding RGB color.

    :param hsv:             HSV color tuple to convert into its corresponding RGB value.
    :return:                the corresponding RGB color, with normalized color channel values between 0 and 1.
    """
    h, s, v = hsv
    h_i = int(h / 60)
    f = (h / 60) - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    else:  # if h_i == 5:
        r, g, b = v, p, q

    return r, g, b


def color_to_hsv(color_or_ink: ColorOrInk) -> tuple[float, float, float]:
    """ convert color/ink to its HSV values.

    :param color_or_ink:    the color or ink to convert into its hsv value.
    :return:                the HSV values (H: 0-360, S: 0-1, V: 0-1) of the specified color or ink.
    """
    r, g, b, *_a = color_or_ink
    max_wert: float = max(r, g, b)
    delta = max_wert - min(r, g, b)

    if delta == 0:
        h: float = 0
    elif max_wert == r:
        h = 60 * (((g - b) / delta) % 6)
    elif max_wert == g:
        h = 60 * (((b - r) / delta) + 2)
    else:  # if max_wert == b:
        h = 60 * (((r - g) / delta) + 4)

    return h, delta / max_wert if max_wert else 0, max_wert


def complementary_color(color_or_ink: ColorOrInk, delta_h: float = 180.0) -> ColorOrInk:
    """ determine the complementary color or ink without changing an optionally passed alpha/occupancy value.

    :param color_or_ink:    the color or ink to convert into its complementary value.
    :param delta_h:         specify a value between -360 and +360 to get a complementary color. specify -180 or 180
                            to get the opposite value using the HSV algorithm, or a
                            zero value to get the opposite color with the more efficient RGB algorithm.
                            any other value will use the HSV algorithm, which adds this value as a delta angle in
                            the HSV color circle. some harmonic delta angles are:
                                * 30: analogous colors
                                * 90, 180 and 270: tetradic colors 2, 3 and 4
                                * 120 and 240: triadic color 2 and 3
                                * 180: opposite color

    :return:                the complementary color or ink, as the same type as the input. note that the HSV algorithm
                            does not change any monochrom/greyscale colors; pass a zero value to the delta_h parameter
                            to get an "opposite"-like color from a gray-scale color (see the unit tests on how
                            the RGB algorithm does behave in relation to the HSV algorithm).
    """
    if delta_h:
        hsv = color_to_hsv(color_or_ink)
        hsv = (hsv[0] + delta_h + 360) % 360, hsv[1], hsv[2]
        rgb = list(color_from_hsv(hsv))
    else:
        rgb = list(1.0 - _ for _ in color_or_ink[:3])
    return rgb + list(color_or_ink[3:])


def darken_color(color_or_ink: ColorOrInk, factor: float = 0.3) -> ColorOrInk:
    """ darkens the specified color/ink without changing an optionally passed alpha/occupancy value.

    :param color_or_ink:    the color or ink to be darkened.
    :param factor:          the factor to darken the color or ink by. its value must range between -1 and 1,
                            where 0 results in no darkening (original color), positive values are using the
                            more complex HSV algorithm, and negative values the efficient RGB darkening algorithm.
                            so +1 returns the darkest value of the specified color, whereas -1 results in a black color.
    :return:                the darkened color or ink, as the same type as the input.
    """
    if factor > 0:
        hsv = color_to_hsv(color_or_ink)
        hsv = hsv[0], min(1.0, hsv[1] * (1.0 + factor)), hsv[2] * (1.0 - factor)
        rgb = list(color_from_hsv(hsv))
    else:
        rgb = list(_ * (1.0 + factor) for _ in color_or_ink[:3])
    return rgb + list(color_or_ink[3:])


def ellipse_polar_radius(ell_a: float, ell_b: float, radian: float) -> float:
    """ calculate the radius from polar for the given ellipse and radian.

    :param ell_a:               ellipse x-radius.
    :param ell_b:               ellipse y-radius.
    :param radian:              angle radian.
    :return:                    ellipse radius at the angle specified by :paramref:`~ellipse_polar_radius.radian`.
    """
    return ell_a * ell_b / sqrt((ell_a * sin(radian)) ** 2 + (ell_b * cos(radian)) ** 2)


def ensure_tap_kwargs_refs(init_kwargs: EventKwargsType, tap_widget: Any):
    """ ensure that the passed widget.__init__ kwargs dict contains a reference to itself within kwargs['tap_kwargs'].

    :param init_kwargs:         kwargs of the widgets __init__ method.
    :param tap_widget:          reference to the tap widget.

    this alternative version is only 10 % faster but much less clean than the current implementation::

        if 'tap_kwargs' not in init_kwargs:
            init_kwargs['tap_kwargs'] = {}
        tap_kwargs = init_kwargs['tap_kwargs']

        if 'tap_widget' not in tap_kwargs:
            tap_kwargs['tap_widget'] = tap_widget

        if 'popup_kwargs' not in tap_kwargs:
            tap_kwargs['popup_kwargs'] = {}
        popup_kwargs = tap_kwargs['popup_kwargs']
        if 'opener' not in popup_kwargs:
            popup_kwargs['opener'] = tap_kwargs['tap_widget']

    """
    init_kwargs['tap_kwargs'] = tap_kwargs = init_kwargs.get('tap_kwargs', {})
    tap_kwargs['tap_widget'] = tap_widget = tap_kwargs.get('tap_widget', tap_widget)
    tap_kwargs['popup_kwargs'] = popup_kwargs = tap_kwargs.get('popup_kwargs', {})
    popup_kwargs['opener'] = popup_kwargs.get('opener', tap_widget)


def flow_action(flow_id: str) -> str:
    """ determine the action string of a flow_id.

    :param flow_id:             flow id.
    :return:                    flow action string.
    """
    return flow_action_split(flow_id)[0]


def flow_action_split(flow_id: str) -> tuple[str, str]:
    """ split flow id string into the action part and the rest.

    :param flow_id:             flow id.
    :return:                    tuple of (flow action string, flow obj and key string)
    """
    idx = flow_id.find(NAME_PARTS_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_change_confirmation_event_name(flow_id: str) -> str:
    """ determine the name of the event method for the change confirmation of the passed flow_id.

    :param flow_id:             flow id.
    :return:                    tuple with 2 items containing the flow action and the object name (and id).
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    return f'on_{obj}_{action}'


def flow_class_name(flow_id: str, name_suffix: str) -> str:
    """ determine the class name for the given flow id and class name suffix.

    :param flow_id:             flow id.
    :param name_suffix:         class name suffix.
    :return:                    name of the class. please note that the flow action `open` will not be added
                                to the returned class name.
    """
    flow, _index = flow_key_split(flow_id)
    action, obj = flow_action_split(flow)
    if action == 'open':
        action = ''
    return f'{snake_to_camel(obj)}{action.capitalize()}{name_suffix}'


def flow_key(flow_id: str) -> str:
    """ return the key of a flow id.

    :param flow_id:             flow id string.
    :return:                    flow key string.
    """
    _action_object, index = flow_key_split(flow_id)
    return index


def flow_key_split(flow_id: str) -> tuple[str, str]:
    """ split flow id into an action, object and flow key.

    :param flow_id:             flow id to split.
    :return:                    tuple of (flow action and object string, flow key string).
    """
    idx = flow_id.find(FLOW_KEY_SEP)
    if idx != -1:
        return flow_id[:idx], flow_id[idx + 1:]
    return flow_id, ""


def flow_object(flow_id: str) -> str:
    """ determine the object string of the passed flow_id.

    :param flow_id:             flow id.
    :return:                    flow object string.
    """
    return flow_action_split(flow_key_split(flow_id)[0])[1]


def flow_path_id(flow_path: list[str], path_index: int = -1) -> str:
    """ determine the flow id of the newest/last entry in the flow_path.

    :param flow_path:           flow path to determine the flow id from its newest/latest entry.
    :param path_index:          index in the flow_path.
    :return:                    flow id string or empty string if the flow path is empty or index does not exist.
    """
    if len(flow_path) >= (abs(path_index) if path_index < 0 else path_index + 1):
        return flow_path[path_index]
    return ''


def flow_path_strip(flow_path: list[str]) -> list[str]:
    """ return a copy of the specified flow_path with all non-enter actions stripped from the end.

    :param flow_path:           flow path list to strip.
    :return:                    stripped flow path copy.
    """
    deep = len(flow_path)
    while deep and flow_action(flow_path_id(flow_path, path_index=deep - 1)) != 'enter':
        deep -= 1
    return flow_path[:deep]


def flow_popup_class_name(flow_id: str) -> str:
    """ determine the name of the Popup class for the given flow id.

    :param flow_id:             flow id.
    :return:                    name of the Popup class. please note that the action `open` will not be added
                                to the returned class name.
    """
    return flow_class_name(flow_id, 'Popup')


def help_id_tour_class(help_id: str) -> Optional[Any]:
    """ determine the tour class if passed help id has attached tour pages.

    :param help_id:         help id to determine the tour class from.
    :return:                tour class of an existing tour for the passed help id or None if no associated tour exists.
    """
    tour_id = help_sub_id(help_id)
    if tour_id:
        return tour_id_class(tour_id)
    return None


def help_sub_id(help_id: str) -> str:
    """ determine sub id (flow id, tour id or app state name) of the current/specified/passed help id.

    opposite of :func:`id_of_flow_help` / :func:`id_of_state_help` / :func:`id_of_tour_help`.

    :param help_id:         help id to extract the sub id from.
    :return:                flow id, tour id, app state name or empty string if help id does not contain a sub id.
    """
    if help_id.startswith(APP_STATE_HELP_ID_PREFIX):
        return help_id[len(APP_STATE_HELP_ID_PREFIX):]
    if help_id.startswith(FLOW_HELP_ID_PREFIX):
        return help_id[len(FLOW_HELP_ID_PREFIX):]
    if help_id.startswith(TOUR_PAGE_HELP_ID_PREFIX):
        return help_id[len(TOUR_PAGE_HELP_ID_PREFIX):]
    return ''


def id_of_flow(action: str, obj: str = '', key: str = '') -> str:
    """ create flow id string.

    :param action:              flow action string.
    :param obj:                 flow object (defined by app project).
    :param key:                 flow index/item_id/field_id/... (defined by app project).
    :return:                    complete flow_id string.
    """
    assert action == '' or FLOW_ACTION_RE.fullmatch(action), \
        f"flow action only allows lowercase letters and digits: got '{action}'"
    assert obj == '' or FLOW_OBJECT_RE.fullmatch(obj), \
        f"flow object only allows letters, digits and underscores: got '{obj}'"
    cid = f'{action}{NAME_PARTS_SEP if action and obj else ""}{obj}'
    if key:
        cid += f'{FLOW_KEY_SEP}{key}'
    return cid


def id_of_flow_help(flow_id: str) -> str:
    """ compose help id for specified flow id.

    :param flow_id:         flow id to make help id for.
    :return:                help id for the specified flow id.
    """
    return f'{FLOW_HELP_ID_PREFIX}{flow_id}'


def id_of_state_help(app_state_name: str) -> str:
    """ compose help id for app state name/key.

    :param app_state_name:  name of the app state variable.
    :return:                help id for the specified app state.
    """
    return f'{APP_STATE_HELP_ID_PREFIX}{app_state_name}'


def id_of_tour_help(page_id: str) -> str:
    """ compose help id for specified tour page id.

    :param page_id:         tour page id to make help id for.
    :return:                help id for the specified tour page.
    """
    return f'{TOUR_PAGE_HELP_ID_PREFIX}{page_id}'


def merge_popups_to_close(tap_kwargs: EventKwargsType, add_kwargs: EventKwargsType) -> PopupsToCloseType:
    """ merge the popups_to_close item values of the two specified tap_kwargs dicts.

    :param tap_kwargs:          the initial tap kwargs dict, with an optional popups_to_close key.
    :param add_kwargs:          additional tap kwargs dict, whose optional popups to close will get merged to the end.
    :return:                    either tuple with the merged popup widgets (ensuring to have no duplicates),
                                or an integer with the number of popups to close,
                                or an empty tuple if both parameters do not have a popups_to_close key.
    :raise AssertionError:      if the types of the popups_to_close values are not matching.
    """
    if 'popups_to_close' not in tap_kwargs or 'popups_to_close' not in add_kwargs:
        return tap_kwargs.get('popups_to_close', ())

    tap_pups, add_pups = tap_kwargs['popups_to_close'], add_kwargs.get('popups_to_close', ())
    if isinstance(tap_pups, int) and isinstance(add_pups, int):
        popups_to_close: PopupsToCloseType = tap_pups + add_pups
    else:
        assert isinstance(tap_pups, tuple) and isinstance(add_pups, tuple), \
            f"type mismatch for popups_to_close values: {tap_pups=} {add_pups=} (expected both as {PopupsToCloseType})"
        popups_to_close = ()
        for wid in tap_pups + add_pups:
            if wid not in popups_to_close:
                popups_to_close += (wid, )

    return popups_to_close


def mix_colors(*colors: ColorOrInk) -> ColorOrInk:
    """ mix multiple colors or inks into a single one.

    :param colors:              colors or inks to mix.
    :return:                    mixed color or ink.
    """
    return [sum(_) / len(_) for _ in zip(*colors)]


def popup_event_kwargs(message: str, title: str,
                       confirm_flow_id: Optional[str] = None, confirm_kwargs: Optional[EventKwargsType] = None,
                       confirm_text: Optional[str] = None, **popup_kwargs) -> EventKwargsType:
    """ type-check and bundle args of the MainAppClass.show_*() methods into a single event kwargs dict for a FlowPopup.

    :param message:         message string to display in the popup.
    :param title:           title of the popup.
    :param confirm_flow_id: tap_flow_id of the popup's 'confirm' button.
    :param confirm_kwargs:  tap_kwargs event args of the popup's 'confirm' button.
    :param confirm_text:    popup confirmation button text. if empty, then the i18n translation of "confirm" is used.
    :param popup_kwargs:    any other extra popup kwargs (not type checked).
    :return:                dict with at least a 'popup_kwargs' key to be passed as event_kwargs argument to the
                            :meth:`~MainAppBase.change_flow` method.
    """
    popup_kwargs['message'] = message

    if title:
        popup_kwargs['title'] = title
    if confirm_flow_id is not None:
        popup_kwargs['confirm_flow_id'] = confirm_flow_id
    if confirm_kwargs is not None:
        popup_kwargs['confirm_kwargs'] = confirm_kwargs
    if confirm_text is not None:
        popup_kwargs['confirm_text'] = confirm_text or get_text("confirm")

    return {'popup_kwargs': popup_kwargs}


def register_package_images():
    """ call from the module scope of the package to register/add the image/img resources path.

    no parameters needed because we use here :func:`~ae.base.stack_var` helper function to determine the
    module file path via the `__file__` module variable of the caller module in the call stack. in this call
    we have to overwrite the default value (:data:`~ae.base.SKIPPED_MODULES`) of the
    :paramref:`~ae.base.stack_var.skip_modules` parameter to not skip ae portions that are providing
    package resources and are listed in the :data:`~ae.base.SKIPPED_MODULES`, like e.g., :mod:`ae.gui.app` and
    :mod:`ae.gui.utils` (passing empty string '' to overwrite the default skip list).
    """
    package_path = os_path_dirname(norm_path(stack_var('__file__', '')))
    search_path = os_path_join(package_path, 'img/**')
    PORTIONS_IMAGES.add_paths(search_path)


def register_package_sounds():
    """ call from the module scope of the package to register/add sound file resources.

    no parameters needed because we use here :func:`~ae.base.stack_var` helper function to determine the
    module file path via the `__file__` module variable of the caller module in the call stack. in this call,
    we have to overwrite the default value (:data:`~ae.base.SKIPPED_MODULES`) of the
    :paramref:`~ae.base.stack_var.skip_modules` parameter to not skip ae portions that are providing
    package resources and are listed in the :data:`~ae.base.SKIPPED_MODULES`.
    """
    package_path = os_path_dirname(norm_path(stack_var('__file__', '')))
    search_path = os_path_join(package_path, 'snd/**')
    PORTIONS_SOUNDS.add_paths(search_path)


def relief_colors(color_or_ink: Optional[ColorOrInk] = None, top_factor: float = 0.6, bottom_factor: float = 0.3,
                  sunken: bool = False) -> ReliefColors:
    """ calculate the top-left and bottom-right colors used for square/ellipse relief effects.

    :param color_or_ink:        optional color used to calculate the relief colors from. if not specified, then
                                the :data:`COLOR_GREY` constant will be used to draw the relief effect.
    :param top_factor:          factor to brighten/darken the top-left part of a square/ellipse with a relief effect,
                                via the HSV calculation method. pass a negative factor to use the more efficient
                                RGB method.
    :param bottom_factor:       factor to brighten/darken the bottom part of a square/ellipse with a relief effect,
                                via tbe HSV calculation method. pass a negative factor to use the more efficient
                                RGB method.
    :param sunken:              if True, then the top-left part of the relief colors will be darkened instead of
                                brightened. a raised relief effect will be produced if False (default).
    :return:                    tuple with the brightened/darkened top and bottom colors, calculated from the argument
                                specified in :paramref:`~relief_colors.color_or_ink`,
                                or an empty tuple if the alpha value of :paramref:`~relief_colors.color_or_ink` is zero.
    """
    if not color_or_ink:
        color_or_ink = COLOR_GREY
    elif len(color_or_ink) > 3 and not color_or_ink[3]:
        return ()

    top_fun, bot_fun = (darken_color, brighten_color) if sunken else (brighten_color, darken_color)
    return top_fun(color_or_ink[:3], factor=top_factor), bot_fun(color_or_ink[:3], factor=bottom_factor)


def replace_flow_action(flow_id: str, new_action: str):
    """ replace action in the given flow id.

    :param flow_id:             flow id.
    :param new_action:          action to be set/replaced within passed flow id.
    :return:                    flow id with the new action and object/key from passed flow id.
    """
    return id_of_flow(new_action, *flow_key_split(flow_action_split(flow_id)[1]))


def tour_help_translation(page_id: str) -> Optional[Union[str, dict[str, str]]]:
    """ determine help translation for the passed page id (flow id or app state name).

    :param page_id:         tour page id.
    :return:                help translation text/dict (if exists) or None if translation is not found.
    """
    return (translation_short_help_id(id_of_flow_help(page_id))[0] or
            translation_short_help_id(id_of_state_help(page_id))[0])


def tour_id_class(tour_id: str) -> Optional[Any]:
    """ determine the tour class of the passed tour id.

    :param tour_id:         tour/flow id to determine tour class for.
    :return:                tour class of an existing tour for the passed tour id or None if no tour exists.
    """
    return REGISTERED_TOURS.get(flow_class_name(tour_id, 'Tour'))


def translation_short_help_id(help_id: str) -> tuple[Optional[Union[str, dict[str, str]]], str]:
    """ check if a help text exists for the passed help id.

    :param help_id:         help id to check if a translation/help with texts exists.
    :return:                tuple of translation text/dict (if exists) and maybe shortened help id(removed detail)
                            or tuple of (None, help_id) if translation is not found.
    """
    trans_text_or_dict = translation(help_id)
    short_help_id = help_id
    if not trans_text_or_dict and FLOW_KEY_SEP in help_id:
        short_help_id = help_id[:help_id.index(FLOW_KEY_SEP)]  # remove detail (e.g. flow key or app state value)
        trans_text_or_dict = translation(short_help_id)
    return trans_text_or_dict, short_help_id


def update_tap_kwargs(widget_or_kwargs: Union[EventKwargsType, Any], popup_kwargs: Optional[EventKwargsType] = None,
                      **tap_kwargs) -> EventKwargsType:
    """ update or simulate a widget's tap_kwargs property and return the updated dictionary (for kv rule of tap_kwargs).

    :param widget_or_kwargs:    either the tap widget (with optional tap_kwargs property, to be extended),
                                or a tap_kwargs dict to be updated (returning an extended shallow copy of it).
    :param popup_kwargs:        dict with items to update popup_kwargs key of.
    :param tap_kwargs:          additional tap_kwargs items to update.
    :return:                    tap_kwargs dict extended with the specified argument values.
                                if the :paramref:`~update_tap_kwargs.widget` parameter is a widget, then the
                                'opener' and 'tap_widget' keys will be set to this widget if they are not already set.
                                if the :paramref:`~update_tap_kwargs.tap_kwargs` parameter as well as widget.tap_kwargs
                                are having the key 'popups_to_close', then both values will be returned merged.
    """
    if isinstance(widget_or_kwargs, dict):
        new_kwargs = widget_or_kwargs.copy()    # .copy prevents endless-recursion; Kivy property don't support deepcopy
    else:
        ini_kwargs = {'tap_kwargs': widget_or_kwargs.tap_kwargs} if hasattr(widget_or_kwargs, 'tap_kwargs') else {}
        ensure_tap_kwargs_refs(ini_kwargs, widget_or_kwargs)
        new_kwargs = ini_kwargs['tap_kwargs']

    if popup_kwargs:
        new_kwargs['popup_kwargs'].update(popup_kwargs)

    if tap_kwargs:
        if popups_to_close := merge_popups_to_close(new_kwargs, tap_kwargs):
            tap_kwargs['popups_to_close'] = popups_to_close
        new_kwargs.update(tap_kwargs)

    return new_kwargs


def widget_page_id(wid: Optional[Any]) -> str:
    """ determine tour page id of passed widget.

    :param wid:                 widget to determine tour page id from (can be None).
    :return:                    tour page id or empty string if the widget has no page id or is None.
    """
    page_id = getattr(wid, 'tap_flow_id', '')
    if not page_id:
        page_id = getattr(wid, 'app_state_name', '')
        if not page_id:
            page_id = getattr(wid, 'focus_flow_id', '')
    return page_id


# reference imported but unused names in pseudo variable `_d_`, to be available in :meth:`MainAppBase.global_variables`
_d_ = (os_platform, path_name, placeholder_path)
module_globals = globals()
""" used. e.g., for execution/evaluation of dynamic code, expressions and f-strings of the app tour and help systems """
