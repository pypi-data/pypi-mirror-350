"""
app tour base classes
---------------------
"""
from copy import deepcopy
from typing import Any, Optional, Union

from ae.dynamicod import try_eval                                                                       # type: ignore
from ae.i18n import get_f_string, get_text                                                              # type: ignore

from .utils import (
    REGISTERED_TOURS, TOUR_EXIT_DELAY_DEF, TOUR_START_DELAY_DEF,
    ExplainedMatcherType,
    flow_action, id_of_flow, id_of_tour_help, tour_help_translation, translation_short_help_id,
    update_tap_kwargs, widget_page_id)


class TourBase:
    """ abstract tour base class, automatically registering subclasses as app tours.

    subclass this generic, UI-framework-independent base class to bundle pages of a tour and make sure that the
    attr:`~TourBase.page_ids` and :attr:`~TourBase.page_data` attributes are correctly set. a UI-framework-dependent
    tour overlay/layout instance, created and assigned to main_app.tour_layout, will automatically create an instance
    of your tour-specific subclass on tour start.
    """
    def __init_subclass__(cls, **kwargs):
        """ register tour class; called on declaration of tour subclass. """
        super().__init_subclass__(**kwargs)
        REGISTERED_TOURS[cls.__name__] = cls

    # noinspection PyUnresolvedReferences
    def __init__(self, main_app: 'MainAppBase'):                    # type: ignore # noqa: F821
        super().__init__()
        main_app.vpo(f"TourBase.__init__(): tour overlay={main_app.tour_layout}")
        self._auto_switch_page_request = None
        self._delayed_setup_layout_call = None
        self._initial_page_data = None
        self._saved_app_states: dict[str, Any] = {}

        self.auto_switch_pages: Union[bool, int] = False
        """ enable/disable automatic switch of tour pages.

        set to `True`, `1` or `-1` to automatically switch tour pages; `True` and `1` will switch to the next page
        until the last page is reached, while `-1` will switch back to the previous pages until the first page is
        reached; `-1` and `1` automatically toggles at the first/last page the to other value (endless ping-pong until
        back/next button gets pressed by the user).

        the seconds to display each page before switching to the next one can be specified via the item value of the
        the dict :attr:`.page_data` dict with the key `'next_page_delay'`.
        """

        self.page_data: dict[str, Any] = {
            'help_vars': {},
            'tour_start_delay': TOUR_START_DELAY_DEF,
            'tour_exit_delay': TOUR_EXIT_DELAY_DEF}
        """ additional/optional help variables (in `help_vars` key), tour and page text/layout/timing settings.

        the class attribute values are default values for all tour pages and get individually overwritten for each tour
        page by the i18n translations attributes on tour page change via :meth:`.load_page_data`.

        supported/implemented dict keys:

        * `app_flow_delay`: time in seconds to wait until app flow change is completed (def=1.2, >0.9 for auto-width).
        * `back_text`: caption of tour previous page button (def=get_text('back')).
        * `fade_out_app`: set to 0.0 to prevent the fade out of the app screen (def=1.0).
        * `help_vars`: additional help variables, e.g. `help_translation` providing context help translation dict/text.
        * `next_text`: caption of tour next page button (def=get_text('next')).
        * `next_page_delay`: time in seconds to read the current page before next request_auto_page_switch() (def=9.6).
        * `page_update_delay`: time in seconds to wait until tour layout/overlay is completed (def=0.9).
        * `tip_text` or '' (empty string): tour page tooltip text fstring message text template. alternatively put as
          first character a `'='` character followed by a tour page flow id to initialize the tip_text to the help
          translation text of the related flow widget, and the `self` help variable to the related flow widget instance.
        * `tour_start_delay`: seconds between tour.start() and on_tour_start main app event (def=TOUR_START_DELAY_DEF).
        * `tour_exit_delay`: seconds between tour.stop() and the on_tour_exit main app event (def=TOUR_EXIT_DELAY_DEF).
        """

        self.pages_explained_matchers: dict[str, Union[ExplainedMatcherType, tuple[ExplainedMatcherType, ...]]] = {}
        """ matchers (specified as callable or id-string) to determine the explained widget(s) of each tour page.

        each key of this dict is a tour page id (for which the explained widget(s) will be determined).

        the value of each dict item is a matcher or a tuple of matchers. each matcher specifies a widget to be
        explained/targeted/highlighted. for matcher tuples the minimum rectangle enclosing all widgets get highlighted.

        the types of matchers, to identify any visible widget, are:

        * :meth:`~ae.gui.app.MainAppBase.find_widget` matcher callable (scanning framework_win.children)
        * evaluation expression resulting in :meth:`~ae.gui.app.MainAppBase.find_widget` matcher callable
        * widget id string, declared via kv lang, identifying widget in framework_root.ids
        * page id string, compiled from widgets app state/flow/focus via :func:`widget_page_id` to identify widget

        """

        self.page_ids: list[str] = []
        """ list of tour page ids, either initialized via this class attribute or dynamically. """

        self.page_idx: int = 0                      #: index of the current tour page (in :attr:`.page_ids`)
        self.last_page_idx: Optional[int] = None    #: last tour page index (`None` on tour start)

        self.main_app = main_app                    #: shortcut to main app instance
        self.layout = main_app.tour_layout          #: tour overlay layout instance

        self.top_popup = None                       #: top most popup widget (in an app tour simulation)

        self.backup_app_states()

        main_app.call_method('on_tour_init', self)  # notify the main app to back up additional app-specific states

    def backup_app_states(self):
        """ back up the current states of this app, including flow. """
        main_app = self.main_app
        main_app.vpo("TourBase.backup_app_states")
        self._saved_app_states = deepcopy(main_app.retrieve_app_states())

    def cancel_auto_page_switch_request(self, reset: bool = True):
        """ cancel auto switch callback if requested, called e.g., from tour layout/overlay next/back buttons. """
        if self._auto_switch_page_request:
            self._auto_switch_page_request.cancel()
            self._auto_switch_page_request = None
        if reset:
            self.auto_switch_pages = False

    def cancel_delayed_setup_layout_call(self):
        """ cancel delayed setup layout call request. """
        if self._delayed_setup_layout_call:
            self._delayed_setup_layout_call.cancel()
            self._delayed_setup_layout_call = None

    @property
    def last_page_id(self) -> Optional[str]:
        """ determine the last displayed tour page id. """
        return None if self.last_page_idx is None else self.page_ids[self.last_page_idx]

    def load_page_data(self):
        """ load a page before switching to it; maybe reload after preparing app flow and before setup of layout. """
        page_idx = self.page_idx
        page_cnt = len(self.page_ids)
        assert 0 <= page_idx < page_cnt, f"page_idx ({page_idx}) has to be equal or greater zero and below {page_cnt}"
        page_id = self.page_ids[page_idx]
        if self._initial_page_data is None:     # reset page data to tour class default: dict(help_vars={}, ...)
            self._initial_page_data = self.page_data
            page_data = deepcopy(self.page_data)
        else:
            page_data = deepcopy(self._initial_page_data)

        help_translation = tour_help_translation(page_id)
        tour_translation = translation_short_help_id(id_of_tour_help(page_id))[0]
        if help_translation:
            if tour_translation:
                page_data['help_vars']['help_translation'] = help_translation
            else:
                tour_translation = help_translation

        page_data.update(tour_translation if isinstance(tour_translation, dict) else {'tip_text': tour_translation})

        self.main_app.vpo(f"TourBase.load_page_data(): tour page{page_idx}/{page_cnt} id={page_id} data={page_data}")
        self.page_data = page_data

    def next_page(self):
        """ switch to the next tour page. """
        self.teardown_app_flow()

        ids = self.page_ids
        assert self.page_idx + 1 < len(ids), f"TourBase.next_page missing {self.__class__.__name__}:{self.page_idx + 1}"
        self.last_page_idx = self.page_idx
        self.page_idx += 1
        self.main_app.vpo(f"TourBase.next_page #{self.page_idx} id={ids[self.last_page_idx]}->{ids[self.page_idx]}")

        self.setup_app_flow()

    def prev_page(self):
        """ switch to the previous tour page. """
        self.teardown_app_flow()

        ids = self.page_ids
        assert self.page_idx > 0, f"TourBase.prev_page wrong/missing page {self.__class__.__name__}:{self.page_idx - 1}"
        self.last_page_idx = self.page_idx
        self.page_idx -= 1
        self.main_app.vpo(f"TourBase.prev_page #{self.page_idx} id={ids[self.last_page_idx]}->{ids[self.page_idx]}")

        self.setup_app_flow()

    def request_auto_page_switch(self):
        """ initiate automatic switch to the next tour page. """
        self.cancel_auto_page_switch_request(reset=False)

        next_idx = self.page_idx + self.auto_switch_pages
        if not 0 <= next_idx < len(self.page_ids):
            if self.auto_switch_pages is True:
                self.cancel_auto_page_switch_request()  # only switch to next until the last page reached
                return
            self.auto_switch_pages = -self.auto_switch_pages
            next_idx += 2 * self.auto_switch_pages

        main_app = self.main_app
        delay = self.page_data.get('next_page_delay', 30.9)
        main_app.vpo(f"TourBase.request_auto_page_switch from #{self.page_idx} to #{next_idx} delay={delay}")
        self._auto_switch_page_request = main_app.call_method_delayed(
            delay, self.prev_page if self.auto_switch_pages < 0 else self.next_page)

    def restore_app_states(self):
        """ restore app states of this app - saved via :meth:`.backup_app_states`. """
        main_app = self.main_app
        main_app.vpo("TourBase.restore_app_states")
        main_app.setup_app_states(self._saved_app_states)

    def setup_app_flow(self):
        """ set up app flow and load page data to prepare a tour page. """
        self.main_app.vpo(f"TourBase.setup_app_flow page_data={self.page_data}")

        self.update_page_ids()
        self.load_page_data()

        app_flow_delay = self.page_data.get('app_flow_delay', 1.2)  # > 0.9 to complete auto width animation
        self._delayed_setup_layout_call = self.main_app.call_method_delayed(app_flow_delay, self.setup_layout)

    def setup_explained_widget(self) -> list:
        """ determine and set the explained widget for the actual tour page.

        :return:                list of explained widget instances.
        """
        main_app = self.main_app
        layout: Any = self.layout
        exp_wid = main_app.help_activator       # fallback widget
        widgets = []
        page_id = self.page_ids[self.page_idx]
        if page_id in self.pages_explained_matchers:
            matchers = self.pages_explained_matchers[page_id]
            for matcher in matchers if isinstance(matchers, (list, tuple)) else (matchers, ):
                if isinstance(matcher, str):
                    match_str = matcher
                    matcher = try_eval(match_str, ignored_exceptions=(Exception, ),     # NameError, SyntaxError, ...
                                       glo_vars=main_app.global_variables(layout=layout, tour=self))
                    if not callable(matcher):
                        # pylint: disable-next=unnecessary-lambda-assignment, cell-var-from-loop
                        matcher = lambda _w: widget_page_id(_w) == match_str            # noqa: E731
                else:
                    match_str = ""
                wid = main_app.find_widget(matcher)
                if not wid and match_str:
                    wid = main_app.widget_by_id(match_str)
                if wid:
                    widgets.append(wid)
                else:
                    main_app.vpo(f"{self.__class__.__name__}/{page_id}: no widget from matcher {match_str or matcher}")
            if len(widgets) > 1:
                exp_wid = layout.explained_placeholder
                exp_wid.x, exp_wid.y, exp_wid.width, exp_wid.height = main_app.widgets_enclosing_rectangle(widgets)
            elif widgets:
                exp_wid = widgets[0]
        else:
            exp_wid = main_app.widget_by_page_id(page_id) or exp_wid

        if not widgets:
            widgets.append(exp_wid)

        self.page_data['help_vars']['help_translation'] = tour_help_translation(widget_page_id(exp_wid))
        layout.explained_pos = main_app.widget_pos(exp_wid)
        layout.explained_size = main_app.widget_size(exp_wid)
        layout.explained_widget = exp_wid

        return widgets

    def setup_layout(self):
        """ setup/prepare tour overlay/layout after switch of tour page. """
        self._delayed_setup_layout_call = None
        main_app = self.main_app
        layout = self.layout
        main_app.vpo(f"TourBase.setup_layout(): page id={self.page_ids[self.page_idx]}")

        try:
            self.top_popup = main_app.popups_opened()[0]
        except IndexError:
            self.top_popup = None

        self.setup_explained_widget()
        self.setup_texts()

        main_app.ensure_top_most_z_index(layout)

        if self.auto_switch_pages:
            self.request_auto_page_switch()

        main_app.call_method_delayed(self.page_data.get('page_update_delay', 0.9), layout.page_updated)

    def setup_texts(self):
        """ setup texts in tour layout from page_data. """
        main_app = self.main_app
        layout = self.layout
        page_data = self.page_data
        page_idx = self.page_idx

        main_app.vpo(f"TourBase.setup_texts page_data={page_data}")

        glo_vars = main_app.global_variables(layout=layout, tour=self)
        help_vars = page_data['help_vars']
        help_vars['self'] = layout.explained_widget
        if self.top_popup:
            glo_vars['root'] = self.top_popup

        # pylint: disable-next=unnecessary-lambda-assignment
        _txt = lambda _t: _t is not None and get_f_string(_t, glo_vars=glo_vars, loc_vars=help_vars) or ""  # noqa: E731

        layout.title_text = _txt(page_data.get('title_text'))
        layout.page_text = _txt(page_data.get('page_text'))

        tip_text = page_data.get('tip_text', page_data.get(''))
        if tip_text is None:
            help_tra = help_vars.get('help_translation')
            tip_text = help_tra.get('', "") if isinstance(help_tra, dict) else help_tra
        if tip_text and tip_text[0] == '=':
            page_id = tip_text[1:]
            tip_text = tour_help_translation(page_id)
            if help_vars['self'] in (None, layout.ids.explained_placeholder):
                help_vars['self'] = main_app.widget_by_page_id(page_id)
        layout.tip_text = _txt(tip_text)

        layout.next_text = page_data.get('next_text', get_text('next')) if page_idx < len(self.page_ids) - 1 else ""
        layout.prev_text = page_data.get('back_text', get_text('back')) if page_idx > 0 else ""

    def start(self):
        """ prepare app tour start. """
        self.main_app.vpo("TourBase.start")
        self.main_app.close_popups()
        self.main_app.call_method_delayed(self.page_data.get('tour_start_delay', TOUR_START_DELAY_DEF),
                                          'on_tour_start', self)
        self.setup_app_flow()

    def stop(self):
        """ stop/cancel tour. """
        self.main_app.vpo("TourBase.stop")
        self.teardown_app_flow()
        # notify the main app to restore additional app-specific states (delayed, to be called after teardown events)
        self.main_app.call_method_delayed(self.page_data.get('tour_exit_delay', TOUR_EXIT_DELAY_DEF),
                                          'on_tour_exit', self)

    def teardown_app_flow(self):
        """ restore app flow and app states before tour finishing or before preparing/switching to prev/next page. """
        self.main_app.vpo("TourBase.teardown_app_flow")
        self.cancel_delayed_setup_layout_call()
        self.cancel_auto_page_switch_request(reset=False)
        self.restore_app_states()

    def update_page_ids(self):
        """ update/change page ids on app flow setup (before tour page loading and the tour overlay/layout setup).

        override this method to dynamically change the page_ids in a running tour. after adding/removing a page, the
        attribute values of :attr:`.last_page_idx` and :attr:`.page_idx` have to be corrected accordingly.
        """
        self.main_app.vpo(f"TourBase.update_page_ids {self.page_ids}")


class TourDropdownFromButton(TourBase):
    """ generic tour base class to auto-explain a dropdown menu, starting with the button opening the dropdown. """
    determine_page_ids = '_v_'

    def setup_app_flow(self):
        """ manage the opening state of the dropdown: open it or close it if the opening button gets explained. """
        super().setup_app_flow()
        page_id = self.page_ids[0]
        assert flow_action(page_id) == 'open', f"TourDropdownFromButton 1st page '{page_id}' missing 'open' flow action"
        lpi = self.last_page_idx
        pgi = self.page_idx
        if lpi is None and pgi == 0 or lpi == 0 and pgi == 1 and not self.top_popup:
            main_app = self.main_app
            main_app.change_flow(page_id, **update_tap_kwargs(main_app.widget_by_page_id(page_id)))

        elif lpi == 1 and pgi == 0 and self.top_popup:
            self.top_popup.close()

    def setup_layout(self):
        """ prepare the layout for all tour pages - first page explains opening dropdown button. """
        super().setup_layout()
        page_ids = self.page_ids
        if page_ids[-1] == TourDropdownFromButton.determine_page_ids:
            main_app = self.main_app
            if not self.top_popup:
                main_app.po("TourDropDownFromButton.setup_layout: dropdown not opened")
                return

            children = main_app.widget_tourable_children_page_ids(self.top_popup)
            if not children:
                main_app.po(f"TourDropDownFromButton.setup_layout missing tour-able child in {self.top_popup}")
                return

            page_ids.remove(TourDropdownFromButton.determine_page_ids)
            page_ids.extend(children)


# ====== app tours =============================================================

_OPEN_USER_PREFERENCES_FLOW_ID = id_of_flow('open', 'user_preferences')


class OnboardingTour(TourBase):
    """ onboarding tour for first app start. """
    # noinspection PyUnresolvedReferences
    def __init__(self, main_app: 'MainAppBase'):                    # type: ignore # noqa: F821
        """ count and persistently store in config variable, the onboarding tour starts since app installation. """
        started = main_app.get_variable('onboarding_tour_started', default_value=0) + 1
        # finally, :meth:`~ae.gui.app.MainAppBase.register_user` disables automatic tour start on app start
        main_app.set_variable('onboarding_tour_started', started)

        super().__init__(main_app)

        self.page_ids.extend([
            '', 'page_switching', 'responsible_layout', 'tip_help_intro', 'tip_help_tooltip', 'layout_font_size',
            'tour_end', 'user_registration'])

        self.pages_explained_matchers.update({
            'tip_help_intro': lambda widget: widget.__class__.__name__ == 'HelpToggler',
            'tip_help_tooltip': _OPEN_USER_PREFERENCES_FLOW_ID,
            'layout_font_size': lambda widget: getattr(widget, 'app_state_name', None) == 'font_size'})

        if started > main_app.get_variable('onboarding_tour_max_started', default_value=9):
            # this would remove welcome and base pages, unreachable for the user: ids[:] = ids[ids.index('tour_end'):]
            self.page_idx = self.page_ids.index('tour_end')   # instead, jump to the last page before user registration

    def setup_app_flow(self):
        """ overridden to open user preferences dropdown in the responsible_layout tour page. """
        super().setup_app_flow()
        page_id = self.page_ids[self.page_idx]
        if page_id == 'layout_font_size':
            main_app = self.main_app
            flow_id = _OPEN_USER_PREFERENCES_FLOW_ID
            wid = main_app.widget_by_flow_id(flow_id)
            main_app.change_flow(flow_id, **update_tap_kwargs(wid))

        elif page_id == 'user_registration':
            self.layout.stop_tour()
            self.main_app.change_flow(id_of_flow('open', 'user_name_editor'))

    def teardown_app_flow(self):
        """ overridden to close the opened user preferences dropdown on leaving layout_font_size tour page. """
        if self.top_popup and self.page_ids[self.page_idx] == 'layout_font_size':
            # self.top_popup.close() no longer works; redirected via kivy.uix.DropDown.dismiss() and Clock.schedule to:
            # noinspection PyProtectedMember
            self.top_popup._real_dismiss()  # pylint: disable=protected-access # needed for this layout_font_size page
        super().teardown_app_flow()

    def update_page_ids(self):
        """ overridden to remove 2nd-/well-done-page (only showing once on next-page-jump from 1st-/welcome-page). """
        super().update_page_ids()
        if 'page_switching' in self.page_ids and self.last_page_id:  # last page id not in (None=tour-start,''=1st page)
            self.page_ids.remove('page_switching')
            if self.page_idx:   # correct if not back from the removed page: self.page_idx == 0; self.last_page_idx == 1
                self.last_page_idx -= 1
                self.page_idx -= 1


class UserPreferencesTour(TourDropdownFromButton):
    """ user preferences menu tour. """
    # noinspection PyUnresolvedReferences
    def __init__(self, main_app: 'MainAppBase'):                    # type: ignore # noqa: F821
        super().__init__(main_app)

        self.auto_switch_pages = 1
        self.page_data['next_page_delay'] = 3.6
        self.page_ids.extend([_OPEN_USER_PREFERENCES_FLOW_ID, TourDropdownFromButton.determine_page_ids])
