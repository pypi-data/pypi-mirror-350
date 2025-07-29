"""
helper functions and base application classes for GUI applications
==================================================================

this ae portion is providing base constants, helper functions and classes, independent of any GUI framework,
to implement upon them Python applications with a graphical user interfaces (GUI).

in concrete this portion is providing the generic functionality for:

    * app- and user-specific configurations
    * persistent app state variables
    * a multilingual context-sensitive help system
    * generic and app-specific app tours
    * app flows (to monitor and control user interaction and app context)
    * app state and key press events
    * app colors and (light/dark) themes

this portion is composed of the following modules:

    * :mod:`~ae.gui.app`: an abstract app class to implement GUI-framework-specific main app classes upon
    * :mod:`~ae.gui.tours`: base classes to offer guiding app tours
    * :mod:`~ae.gui.utils`: generic GUI-specific constants and helper functions


base resources for your gui app
-------------------------------

this portion is also providing base resources of commonly used i18n translation texts, images, and audio sounds.

generic i18n translation texts are provided by this portion in the `loc` folder, and can be extended and overloaded
with app-specific translation texts.

.. hint::
    the data-driven approach allows ad-hoc-changes of your app's help texts without the need of code changes or
    recompilation.

the license free image resources provided by this portion are taken from:

    * `iconmonstr <https://iconmonstr.com/interface/>`_.

the audio/sounds provides by this portion are taken from:

    * `Erokia <https://freesound.org/people/Erokia/>`_ at `freesound.org <https://freesound.org>`_.
    * `plasterbrain <https://freesound.org/people/plasterbrain/>`_ at `freesound.org <https://freesound.org>`_.


extended console application environment
----------------------------------------

the abstract base class :class:`~ae.gui.app.MainAppBase`, provided by this portion, inherits directly from the
:class:`ae console application environment class <ae.console.ConsoleApp>` of the ae namespace.
such inherited helper methods are used to log, configure, and control the run-time of your GUI app
via command line arguments.

.. hint::
    please see the documentation of :ref:`config-options` and :ref:`config-files` in the :mod:`ae.console` namespace
    portion/module for more detailed information.

the class :class:`~ae.gui.app.MainAppBase` adds on top of the :class:`~ae.console.ConsoleApp` the concepts of:

    * :ref:`application events`
    * :ref:`application status`
    * :ref:`application flow`
    * a :ref:`context-sensitive help system`
    * :ref:`user guiding application tours`
    * :ref:`generic key press events`.


application events
------------------

some of the events described in this section are fired on application startup and shutdown.

additional events get fired e.g., in relation to the app states (documented further down in the section
:ref:`app state events`) or on start or stop of an :ref:`app tour <app tour start and stop events>`.

the following application events are fired exactly one time at startup in the following order:

    * `on_app_init`: fired **after** :class:`ConsoleApp` app instance got initialized (detected config files)
      and **before** the image and sound resources and app states get loaded and the GUI framework app class instance
      gets initialized.
    * `on_app_run`: fired **from within** the method :meth:`~ae.gui.app.MainAppBase.run_app`, **after** the parsing of
      the command line arguments and options, and **before** all portion resources got imported.
    * `on_app_build`: fired **after** all portion resources got loaded/imported, and **before** the framework event
      loop of the used GUI framework gets started.
    * `on_app_started`: fired **after** all app initializations, and the start of and the initial processing of the
      framework event loop.

.. note::
    the application events `on_app_build` and `on_app_started` have to be fired by the used GUI framework.

.. hint::
    depending on the used GUI framework, there can be more app start events. e.g., the :mod:`ae.kivy.apps` module
    fires the events :meth:`~ae.kivy.apps.KivyMainApp.on_app_built` and :meth:`~ae.kivy.apps.KivyMainApp.on_app_start`
    (all of them fired after :meth:`~ae.kivy.apps.KivyMainApp.on_app_run` and
    :meth:`~ae.kivy.apps.KivyMainApp.on_app_build`). more detailed info is available in the
    section :ref:`kivy application events`.

when an application gets stopped, then the following events get fired in the following order:

    * `on_app_exit`: fired **after* framework win got closed and just **before** the event loop of the GUI framework
      will be stopped and the app shutdown.
    * `on_app_quit`: fired **after** the event loop of the GUI framework got stopped and before
      the :meth:`AppBase.shutdown` method will be called.

.. note::
    the `on_app_exit` events will only be fired if the app is explicitly calling the
    :meth:`~ae.gui.app.MainAppBase.stop_app` method.

.. hint::
    depending on the used GUI framework, there can be more events. e.g., the :mod:`~ae.kivy.apps` module fires
    the event :meth:`~ae.kivy.apps.KivyMainApp.on_app_stop`, and one clock tick later
    the event :meth:`~ae.kivy.apps.KivyMainApp.on_app_stopped`
    (both of them before :meth:`~ae.kivy.apps.KivyMainApp.on_app_quit` get fired).
    see also :ref:`kivy application events`.


application status
------------------

any application- and user-specific configurations like e.g., the last app window position/size, the app
theme/font/language or the last selected app flow, could be included in the app status variables.

this namespace portion adds/introduces the section `aeAppState` to the app :ref:`config-files`, where any
status variable values can be stored persistently to be recovered on the next startup of your application.

.. hint::
    the section name `aeAppState` is declared by the :data:`APP_STATE_SECTION_NAME` constant. to access this
    config section directly, use this constant instead of the hardcoded section name.


.. _app-state-variables:

app state variables
^^^^^^^^^^^^^^^^^^^

this module is providing/pre-defining the following application state variables:

    * :attr:`~ae.gui.app.MainAppBase.app_state_version`: the version of the app states implementation
    * :attr:`~ae.gui.app.MainAppBase.cancel_ink`: cancel color, e.g. for cancellation buttons
    * :attr:`~ae.gui.app.MainAppBase.confirm_ink`: confirm color, e.g. for confirmation buttons
    * :attr:`~ae.gui.app.MainAppBase.create_ink`: color to add/create new app data/items
    * :attr:`~ae.gui.app.MainAppBase.delete_ink`: color to delete app data/item
    * :attr:`~ae.gui.app.MainAppBase.error_ink`: color to display error messages/popups
    * :attr:`~ae.gui.app.MainAppBase.flow_id`: current working flow id
    * :attr:`~ae.gui.app.MainAppBase.flow_id_ink`: color to display/highlight widget(s) with the current flow id
    * :attr:`~ae.gui.app.MainAppBase.flow_path`: stack of entered/opened app flows
    * :attr:`~ae.gui.app.MainAppBase.flow_path_ink`: color to display the current flow path
    * :attr:`~ae.gui.app.MainAppBase.font_size`: size of the main app font (also used to calculate the grid row height)
    * :attr:`~ae.gui.app.MainAppBase.help_ink`: color to mark widgets with context-sensitive help
    * :attr:`~ae.gui.app.MainAppBase.info_ink`: color to display info messages
    * :attr:`~ae.gui.app.MainAppBase.lang_code`: id of the selected user language
    * :attr:`~ae.gui.app.MainAppBase.light_theme`: light/dark background (for app themes)
    * :attr:`~ae.gui.app.MainAppBase.read_ink`: color to display read-only data/items
    * :attr:`~ae.gui.app.MainAppBase.selected_ink`: color to highlight currently selected app data/items
    * :attr:`~ae.gui.app.MainAppBase.sound_volume`: audio volume of sound resources
    * :attr:`~ae.gui.app.MainAppBase.theme_names`: list of user-generated themes (set of foreground/background colors)
    * :attr:`~ae.gui.app.MainAppBase.unselected_ink`: color to display currently unselected app data/items
    * :attr:`~ae.gui.app.MainAppBase.update_ink`: color to display/highlight an updated app data/item
    * :attr:`~ae.gui.app.MainAppBase.vibration_volume`: intensity of vibration resources (on mobile devices)
    * :attr:`~ae.gui.app.MainAppBase.warn_ink`: color to display warning messages/popups
    * :attr:`~ae.gui.app.MainAppBase.win_rectangle`: the current window rectangle (position and size)

.. hint::
    the two built-in app state variables are :attr:`~ae.gui.app.MainAppBase.flow_id` and
    :attr:`~ae.gui.app.MainAppBase.flow_path` will be explained in more detail in the next section.

which app state variables are finally available in your app project depends (fully data-driven) on the app state
:ref:`config-variables` detected in all the :ref:`config-files` that are found/available at run-time of your app. the
names of all the available application state variables can be determined with the main app helper method
:meth:`~ae.gui.app.MainAppBase.app_state_keys`.

.. note::
    if no config-file is provided, then this package ensures at least the proper initialization of the above
    app state variables.

the :meth:`~ae.gui.app.MainBaseApp.load_app_states` method is called on instantiation from the implemented
main app class to load the values of all app state variables from the :ref:`config-files`, and is then calling
:meth:~ae.gui.app.MainAppBase.setup_app_states` for pass them into their corresponding instance attributes.

use the main app instance attribute to read/get the actual value of a single app state variable. the actual
app state variables dict is determining the method :meth:`~ae.gui.app.MainBaseApp.retrieve_app_states`, and can be saved
into the :ref:`config-files` for the next app run via the method :meth:`~ae.gui.app.MainBaseApp.save_app_states`.
this could be done e.g., after the app state has changed or at least on quiting the application.

always call the method :meth:`~ae.gui.app.MainBaseApp.change_app_state` to change an app state value to ensure:

    (1) the propagation to any duplicated (observable/bound) framework property and
    (2) the event notification of the related (optionally declared) main app instance method.

so e.g., if your application is supporting a user-defined font size, using the provided/pre-defined app state variable
:attr:`~ae.gui.app.MainAppBase.font_size`, then the :meth:`~ae.gui.app.MainBaseApp.change_app_state` method has to
be called with the :paramref:`~ae.gui.app.MainAppBase.change_app_state.app_state_name` argument set to `font_size`,
and the :paramref:`~ae.gui.app.MainAppBase.change_app_state.state_value` argument set to the new font size.


app theme variables
^^^^^^^^^^^^^^^^^^^

to allow the app user to quickly change the appearance of the app, some of the app state variables are classified
as app theme variables via the :attr:`~ae.gui.app.MainAppBase.theme_specific_cfg_vars` attribute, including by default
e.g., the font size (:attr:`~ae.gui.app.MainAppBase.font_size`), the used colors and if it is a light or dark theme
(:attr:`~ae.gui.app.MainAppBase.light_theme`).

to create or update an existing app theme call the method :meth:`~ae.gui.app.MainAppBase.theme_save`.
the method :meth:`~ae.gui.app.MainAppBase.theme_load` loads an existing theme from its config-file theme section.

.. hint::
    the theme config section name consists of the prefix :data:`THEME_SECTION_PREFIX` followed by the name of the theme.


.. _app-state-constants:

app state constants
^^^^^^^^^^^^^^^^^^^

this portion is also providing some pre-defined constants that can be optionally used in your application in relation to
the app states data store and for the app state config variables :attr:`~ae.gui.app.MainAppBase.app_state_version`,
:attr:`~ae.gui.app.MainAppBase.font_size` and :attr:`~ae.gui.app.MainAppBase.light_theme`:

    * :data:`APP_STATE_SECTION_NAME`: app states config section name
    * :data:`APP_STATE_VERSION_VAR_NAME`: app state variable name of the current app state variable version
    * :data:`MIN_FONT_SIZE`: minimum font size
    * :data:`MAX_FONT_SIZE`: maximum font size
    * :data:`DEFAULT_FONT_SIZE`: default font size
    * :data:`THEME_LIGHT_BACKGROUND_COLOR`: light theme background color
    * :data:`THEME_LIGHT_FONT_COLOR`: light theme foreground/font color
    * :data:`THEME_DARK_BACKGROUND_COLOR`: dark theme background color
    * :data:`THEME_DARK_FONT_COLOR`: dark theme foreground/font color


app state events
^^^^^^^^^^^^^^^^

there are three types of notification events get fired in relation to the app state variables, using the
following method names of the main app instance:

* `on_<app_state_name>`: fired if the value of an app state variable is changing
* `on_<app_state_name>_save`: fired if an app state gets saved to the config file
* `on_app_state_version_upgrade`: fired if the user upgrades a previously installed app to a higher version

the method name of the first app state change event consists of the prefix ``on_`` followed by the variable name
of the app state. so e.g., on a change of the `font_size` app state the notification event `on_font_size` will be
fired/called (if it exists as a method of the main app instance). these events don't provide any event arguments.

the second event gets fired for each app state value just after the app states getting retrieved from the main app
instance, and before they get stored into the main config file. the method name of this event includes also the name of
the app state with the suffix `_save`, so e.g., for the app state `flow_id` the event method name will result in
:meth:`on_app_state_flow_id_save`. this event is providing one event argument with the value of the app state. if the
event method returns a value that is not `None`, then this value will be stored/saved.

the third event gets fired on app startup when the app state version (in APP_STATE_VERSION_VAR_NAME, respective
`app_state_version`) got upgraded to a higher value. then this event handler method will be called providing the
version number for each version to upgrade, starting with the version of the previously installed main config file,
until the upgrade version of the main config file gets reached. so if e.g., the previously installed app state version
was `3` and the new version number is `6`, then this event will be fired 3 times with the arguments 3, 4, and 5.
this functionality can be used e.g., to change or add app state variables or to adapt the app environment.


application flow
----------------

to control the current state and user interaction flow (or context) of your application, and to persist it until the
next app start, :class:`MainBaseApp` provides two :ref:`app-state-variables`: :attr:`~ae.gui.app.MainAppBase.flow_id`
to store the currently working flow and :attr:`~ae.gui.app.MainAppBase.flow_path` to store the history of
 entered/opened flows.


app flow id and path
^^^^^^^^^^^^^^^^^^^^

an application flow is represented by an id string that defines three things: (1) the action to enter into the flow, (2)
the data or object that gets currently worked on and (3) an optional key string that is identifying/indexing a widget or
data item of your application context/flow.

.. note::
    never concatenate a flow id string manually, use the :func:`id_of_flow` function instead.

the flow id is initially an empty string. as soon as the user is starting a new work flow or is changing
the app context (e.g., the current selection of a data item or the opening of a popup), your
application could call the method :meth:`~ae.gui.app.MainBaseApp.change_flow` passing the flow id string into the
:paramref:`~ae.gui.app.MainAppBase.change_flow.new_flow_id` argument.

for more complex applications you can specify a path of nested flows. this flow path gets represented by the app state
variable :attr:`~ae.gui.app.MainAppBase.flow_path`, which is a list of flow id strings.

to enter into a deeper/nested flow, you call :meth:`~ae.gui.app.MainBaseApp.change_flow` with one of the actions
defined in :data:`ACTIONS_EXTENDING_FLOW_PATH`.

to go back to a previous flow in the flow path, call :meth:`~ae.gui.app.MainBaseApp.change_flow` passing one of
the actions defined in :data:`ACTIONS_REDUCING_FLOW_PATH`.

.. hint::
    check the ACTIONS_* constants declared on top of the module :mod:`~ae.gui.app` for this and other app flow action
    classifications.


application flow change events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the flow actions specified by :data:`~ae.gui.app.ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` don't need a
flow change confirmation event handler, which are in concrete:

* `'enter'` or `'leave'`: extend/reduce the flow path.
* `'focus'`: pass/change the input focus.
* `'suggest'`: for autocompletion or other suggestions.

all other flow actions need a confirmation before they get changed by :meth:`~ae.gui.app.MainAppBase.change_flow`,
either by a custom flow change confirmation method/event-handler or by declaring a related popup class. the name
of the event handler and of the popup class gets determined from the flow id.

.. hint::
    the name of the flow change confirmation method that gets fired when the app wants to change the flow (via the
    method :meth:`~ae.gui.app.MainAppBase.change_flow`) gets determined by the function
    :func:`flow_change_confirmation_event_name`, whereas the name of the popup class gets determined by the function
    :func:`flow_popup_class_name`.

if the flow-specific change confirmation event handler does not exist or returns in a boolean `False` or a `None`
value, then the main app instance method :meth:`~ae.gui.app.MainAppBase.on_flow_change` will be called.
if this call also returns `False`, then the action of the new flow id will be searched within
:data:`~ae.gui.app.ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION` and if not found, then the
flow change will be rejected and :meth:`~ae.gui.app.MainAppBase.change_flow` returns `False`.

if in contrary, either the flow change confirmation event handler exists and does return `True`,
or the method :meth:`~ae.gui.app.MainAppBase.on_flow_change` returns True,
or the flow action of the new flow id is in :data:`~ae.gui.app.ACTIONS_CHANGING_FLOW_WITHOUT_CONFIRMATION`
then the flow id and path will be changed accordingly.

after a positive flow id/path change confirmation, the method :meth:`~ae.gui.app.MainAppBase.change_flow` checks if
the optional `event_kwargs` key `changed_event_name` got specified, and if yes, then it calls this method.

finally, if a confirmed flow change results in a `'focus'` flow action, then the event `on_flow_widget_focused` will be
fired. this event can be used by the GUI framework to set the focus to the widget associated with the new focus flow id.


flow actions `'open'` and `'close'`
__________________________________

to display an instance of a properly named popup class, initiate the change the app flow to an appropriate
flow id (with an `'open'` flow action). in this case no change confirmation event handler is needed, because
:meth:`~ae.gui.app.MainAppBase.on_flow_change` is then automatically opening the popup.

when the popup is visible, the flow path will be extended with the respective flow id.

calling the `close` method of the popup will hide it. on closing the popup, the flow id will be reset and the opening
flow id will be removed from the flow path.

all popup classes are providing the events `on_pre_open`, `on_open`, `on_pre_dismiss` and `on_dismiss`.
the `on_dismiss` event handler can be used for data validation: returning a non-False value from it will cancel
the close.

.. hint::
    see the documentation of each popup class for more details on the features of popup classes (for Kivy apps e.g.
    :class:`~ae.kivy.widgets.FlowDropDown`, :class:`~ae.kivy.widgets.FlowPopup` or
    :class:`~ae.kivy.widgets.FlowSelector`).


context-sensitive help system
-----------------------------

the generic functionality of a context-sensitive help system is provided by this portion. only the user interface
widgets to display the help texts have to be implemented and provided by the finally used GUI-framework.

.. hint::
    help message texts are based on the multilingual translation messages, provided by the
    ae namespace portion :mod:`ae.i18n`.

    more details on these and other features of this help system, e.g., the usage of f-strings in the help texts, are
    documented in the doc string of the :mod:`ae.i18n` module.

    an example demonstrating the features of this context help system can be found in the repository of
    the `kivy lisz demo app <https://gitlab.com/ae-group/kivy_lisz>`_.


i18n help ids and texts
^^^^^^^^^^^^^^^^^^^^^^^

each multilingual help text is associated to a unique help id, the message id.

the help texts of an app are spread over multiple translation message files, which are text files
declaring a single dict literal, where the message ids are the dict keys.

each package/portion required by an app can declare and register its translation message files for their help texts.
your app can provide additional i18n translation message files for the app's help texts.

separate message files are created for each supported language. the multilingual ae namespace portions are providing
help texts for the languages English, Spanish and German. additional languages can be provided by your app, also
for the help texts of the imported ae namespace portions.


help ids of flow-changing widgets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the help id to identify the help texts for each widget is composed by the :func:`id_of_flow_help`, using the
prefix marker string defined by the constant :data:`~ae.gui.utils.FLOW_HELP_ID_PREFIX` followed by the flow id
of the flow widget.

.. hint:: more information regarding the flow id you find in the section :ref:`application flow`.

for example, the help/message id for a flow button with the flow action `'open'`, the object `'item'`
and the (optional) flow key `'456'` is resulting in the following help text message id::

    'help_flow#open_item:456'

if there is no need for a detailed message id that is taking the flow key into account, then use a help id
without the flow key. the method :meth:`~ae.gui.app.MainAppBase.help_display` does first search for a message id
including the flow key in the available help text files, and if not found, it will automatically fall back to use
a message id without the flow key::

    'help_flow#open_item'


help ids of app-state-changing widgets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the help message id for a widget changing an app state is composed by the method :func:`id_of_state_help`,
using the prefix marker string defined by the :data:`~ae.gui.utils.APP_STATE_HELP_ID_PREFIX` constant,
followed by the name of the app state.

so, the help id for a widget changing the `font_size` app state is resulting in the following help id::

    'help_app_state#font_size'


help message text f-strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^

help message texts can be f-strings with access to the widget properties via the `self` variable, which
gets automatically prepared within the `help_vars` context dict by this portion.

so, the help message text of the following translation message item gets displayed with the actual slider value
of the widget that allows the user to change the font size::

    {
        'help_app_state#font_size': \"\"\"move the slider to adjust the font size

        the current font size is {self.value}\"\"\",
        ...
    }


pre- and post-change help texts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

to display a different help message before and after the change of the flow id or the app state, use
instead of a simple message text, a message dict with the two keys `''` (an empty string) and `'after'`,
and then put the message texts as their values, like shown in the following example::

    {
        'help_id': {
            '': "help text displayed before the flow/app-state change.",
            'after': "help text displayed after the flow/app-state change",
        },
        ...
    }

if you want to move/change the help target to another widget after a change, then the
'`next_help_id'` message dict key can be appended to the message dict::

    {
        'help_id': {
            '': "help text",
            ...
            'next_help_id': "id_of_the_next_help_message",
        },
        ...
    }

in this case the help target will automatically change to the widget specified by the flow id in the '`next_help_id'`
key, if the user was tapping the second time on the first/initial help target widget.


pluralize-able help texts
^^^^^^^^^^^^^^^^^^^^^^^^^

additional a message dict keys can be used to auto-select pluralized help texts. for that add a `count`
item to the `help_vars` context property of the help target widget and then define a help text for all
the possible count cases in the message dict like shown in the following example::

    {
        'help_id': {
            '': "fallback help text if count is None",
            'zero': "help text if {count} == 0",
            'one': "help text if {count} == 1",
            'many': "help text if {count} > 1",
            'negative': "help text if {count} < 0",
        },
        ...
    }

the provided `count` value can also be included/displayed in the help text, so the help message text of
the`'zero'` count case in the above example will result in "help text if 0 == 0".


help layout implementation example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the layout of the user interface for this help system has to be provided externally on top of this module.
it can either be implemented directly in your app project or in a separate GUI-framework-specific package/portion.

use :class:`~ae.gui.app.MainAppBase` as the base class of the GUI framework specific main application class
to implementing all its abstract methods, like e.g., :meth:`~ae.gui.app.MainAppBase.init_app` and
:meth:`~ae.gui.app.MainAppBase.ensure_top_most_z_index`::

    from ae.gui.app import MainAppBase

    class MyMainApp(MainAppBase):
        def init_app(self, framework_app_class=None):
            self.framework_app = framework_app_class()
            ...
            return self.framework_app.run, self.framework_app.stop

        def ensure_top_most_z_index(self, widget):
            framework_method_to_push_widget_to_top_most(widget)
        ...

to activate the help mode, the widget to display the help texts has to be assigned to the main app instance attribute
:attr:`~ae.gui.app.MainAppBase.help_layout` and to its related framework app property via
the :meth:`~ae.gui.app.MainAppBase.change_observable` method::

    main_app.change_observable('help_layout', HelpScreenContainerOrWindow())

.. hint::
    for example, see :attr:`~ae.kivy.apps.FrameworkApp.help_layout` as the help layout property implemented for the
    `Kivy framework <https://kivy.org/>`.

the :attr:`~ae.gui.app.MainAppBase.help_layout` property is also used as a flag of the help mode activity.
by assigning `None` to this observable attribute, the help mode will get deactivated::

    main_app.change_observable('help_layout', None)

use the attribute :attr:`~ae.gui.app.MainAppBase.help_activator` to specify the widget that allows the user
to toggle the help mode activation. the :meth:`~ae.gui.app.MainAppBase.help_display` is using it as the fallback widget
if no help target (or widget to be explained) got found.

.. hint::
    the de-/activation method :meth:`~ae.kivy.apps.KivyMainApp.help_activation_toggle` together with the classes
    :class:`~ae.kivy.behaviors.HelpBehavior`, :class:`~ae.kivy.widgets.HelpToggler` and
    :class:`~ae.kivy.widgets.Tooltip` are demonstrating a typical implementation of help activator
    and help text tooltip widgets.


user guiding application tours
------------------------------

the following classes provided by this portion build a solid fundament to implement tours for your app:

    * :class:`~ae.gui.tours.TourBase`: abstract base class of all app tours.
    * :class:`~ae.gui.tours.TourDropdownFromButton`: abstract base class for tours on dropdown/menu widgets.
    * :class:`~ae.gui.tours.OnboardingTour`: minimal app onboarding tour, extendable with app-specific tour pages.
    * :class:`~ae.gui.tours.UserPreferencesTour`: minimal user preferences dropdown tour.


app tour start and stop events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the following main app event methods get called (if they exist) in relation to the start/stop of an app tour:

* `on_tour_init`: fired when the app tour instance got initialized and the app states backup got saved.
* `on_tour_start`: fired after the tour start method gets called.
* `on_tour_exit`: fired after an app tour got finished and the app states got restored to the values of the tour start.


UI-specific implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^

to complete the implementation of the app tours, the UI-specific framework has to provide a tour layout class, which is
highlighting the explained widget, displaying a tooltip and another widget to display the tour page texts.

.. hint::
    the :class:`~ae.kivy.tours.TourOverlay` class, provided by the ae portion :mod:`ae.kivy`, is a
    good example of a GUI-framework-specific implementation of a tour layout class for the
    `Kivy framework <https://kivy.org/>`_.


generic key press events
------------------------

to provide key press events to the applications that will use the new GUI framework, you have to catch the key press
events of the framework, convert/normalize them, and then call the method
:meth:`~ae.gui.app.MainAppBase.key_press_from_framework` with the normalized modifiers and key args.

the :paramref:`~ae.gui.app.MainAppBase.key_press_from_framework.modifiers` arg is a string that can contain several
of the following sub-strings, always in the alphabetic order (like listed below):

    * Alt
    * Ctrl
    * Meta
    * Shift

the :paramref:`~ae.gui.app.MainAppBase.key_press_from_framework.key` arg is a string specifying the last pressed key.
if the key is not representing a single character but a command key, then `key` will be one of the following
key name strings:

    * escape
    * tab
    * backspace
    * enter
    * del
    * enter
    * up
    * down
    * right
    * left
    * home
    * end
    * pgup
    * pgdown

on call of :meth:`~ae.gui.app.MainAppBase.key_press_from_framework` this method will dispatch the key press
event to your application. first it will check the app instance if it has declared a method with the name
`on_key_press_of_<modifiers>_<key>` and if so, it will call this method.

if this method does return False (or any other value resulting in False), then the method
:meth:`~ae.gui.app.MainAppBase.key_press_from_framework` will check for a method with the same name in lower-case,
and if it exits, it will call this method.

if also the second method is not declared or does return False, then it will try to call the event handler method
`on_key_press` of the main app instance (if it exists) with the modifiers and the key as arguments.

if the `on_key_press` method does also return False, then :meth:`~ae.gui.app.MainAppBase.key_press_from_framework`
will finally pass the key press event to the original key press handler of the GUI framework for further processing.


integrate a new gui framework
-----------------------------

the abstract class :class:`~ae.gui.app.MainAppBase`, provided by the module :mod:`ae.gui.app`, is a generic base
for the implementation of any Python GUI framework.

to integrate a new Python GUI framework, you have to declare a new class that inherits from the class
:class:`~ae.gui.app.MainAppBase` and implements at least their five abstract methods:

    * :meth:`~ae.gui.app.MainAppBase.call_method_delayed`
    * :meth:`~ae.gui.app.MainAppBase.call_method_repeatedly`
    * :meth:`~ae.gui.app.MainAppBase.ensure_top_most_z_index`
    * :meth:`~ae.gui.app.MainAppBase.help_activation_toggle`
    * :meth:`~ae.gui.app.MainAppBase.init_app`

additionally and to load the resources of the app (after the portion resources got loaded), the event `on_app_build`
has to be fired, executing the :meth:`MainAppBase.on_app_build` method. this could be done directly from within
the implementation of the abstract method :meth:`~ae.gui.app.MainAppBase.init_app` or by forwarding/redirecting one
of the app instance events of the used GUI framework.

am example of a minimal implementation of the :meth:`~ae.gui.app.MainAppBase.init_app` method
could look like the following::

    def init_app(self):
        self.call_method('on_app_build')
        return None, None

most GUI frameworks are providing classes that need to be instantiated on application startup, like e.g., the instance
of the GUI framework app class, the root widget or layout of the main GUI framework window(s). to keep a reference to
these instances within your main app class, the attributes :attr:`~ae.gui.app.MainAppBase.framework_app`,
:attr:`~ae.gui.app.MainAppBase.framework_root` and :attr:`~ae.gui.app.MainAppBase.framework_win` of the
class :class:`MainAppBase` can be used.

the initialization of the attributes :attr:`~ae.gui.app.MainAppBase.framework_app`,
:attr:`~ae.gui.app.MainAppBase.framework_root` and
:attr:`~ae.gui.app.MainAppBase.framework_win` is optional and can be done e.g., within the implementation of
:meth:`~ae.gui.app.MainAppBase.init_app` or in the `on_app_build` application event fired later
by the framework app instance.

.. note::
    if :attr:`~ae.gui.app.MainAppBase.framework_win` is set to a window instance, then the window instance has
    to provide a `close` method, which will be called automatically by the :meth:`~ae.gui.app.MainAppBase.stop_app`.

a typical framework-specific main app class implementation example and its `init_app` method looks like::

    from new_gui_framework import NewFrameworkApp, MainWindowClassOfNewFramework

    class NewFrameworkMainApp(MainAppBase):
        def init_app(self):
            self.framework_app = NewFrameworkAppClass()
            self.framework_win = MainWindowClassOfNewFramework()

            # return callables to start/stop the event loop of the GUI framework
            return self.framework_app.start, self.framework_app.stop

in this example the `on_app_build` application event gets fired either from within the `start` method of the framework
app instance or by an event provided by the used GUI framework.

the method :meth:`~ae.gui.app.MainAppBase.init_app` will be executed only once at the main app class instantiation.
only the main app instance has to initialize the GUI framework to prepare the app startup and has to return at least
a callable to start the event loop of the GUI framework.

to initiate the app startup, the :meth:`~MainAppClass.run_app` method has to be called from the main module of your
app project. :meth:`~ae.gui.app.MainAppBase.run_app` will then start the GUI event loop by calling the first callable
that got returned by :meth:`~ae.gui.app.MainAppBase.init_app`.

.. hint::
    an actual overview about the available GUI-framework-specific ae namespace portions can be found in the
    documentation of the ae namespace demo app portion :mod:`ae.lisz_app_data`.

    check out the ae namespace portion :mod:`ae.kivy` for a more detailed integration example of the
    `Kivy framework <https://kivy.org/>`_.


TODO:
implement OS-independent detection of dark/light screen mode and automatic notification on day/night mode switch.
- see https://github.com/albertosottile/darkdetect for macOS, MSWindows and Ubuntu
- see https://github.com/kvdroid/Kvdroid/blob/master/kvdroid/tools/darkmode.py for Android

"""
from ae.i18n import register_package_translations                               # type: ignore

from .utils import register_package_images, register_package_sounds


__version__ = '0.3.114'


register_package_images()
register_package_sounds()
register_package_translations()
