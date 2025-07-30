"""
ae.kivy.apps module
-------------------

this module is providing two application classes, one of them extending :class:`the Kivy App class <kivy.app.App>`.
the other app class is used as the main app class, extending the abstract/generic class
:class:`~ae.gui.app.MainAppBase` with additional attributes and helper methods.


application classes
^^^^^^^^^^^^^^^^^^^

the class :class:`~ae.kivy.apps.KivyMainApp` is implementing a main app class, reducing the amount of
code needed to create a Python application based on the `Kivy framework <https://kivy.org>`_.

:class:`~ae.kivy.apps.KivyMainApp` is based on the following classes:

    * the abstract base class :class:`~ae.gui.app.MainAppBase` which adds a context-sensitive help system,
      :ref:`application status`, :ref:`app-state-variables`, :ref:`app-state-constants`, :ref:`application flow`
      and generic :ref:`application events`.
    * :class:`~ae.console.ConsoleApp` is adding :ref:`config-files`, :ref:`config-variables` and :ref:`config-options`.
    * :class:`~ae.core.AppBase` is adding :ref:`application logging` and :ref:`application debugging`.

this namespace portion is also encapsulating the :class:`Kivy App class <kivy.app.App>` via the
:class:`~ae.kivy.apps.FrameworkApp` class. this Kivy app class instance can be directly accessed from the
main app class instance via the :attr:`~ae.gui.app.MainAppBase.framework_app` attribute.


kivy app config variables
^^^^^^^^^^^^^^^^^^^^^^^^^

all the :ref:`config-variables` and app constants inherited from the base app classes are available.

.. hint::
    please see the documentation of the namespace portions/modules :mod:`ae.console`and :mod:`ae.gui`
    for more detailed information on all the inherited :ref:`config-variables`,
    :ref:`config-options`, :ref:`config-files` and :ref:`app-state-constants`.

the additional :ref:`config-variables` `win_min_width` and `win_min_height`, added by this portion, you can optionally
restrict the minimum size of the kivy main window of your app. their default values are set on app startup in the
method :meth:`~ae.kivy.apps.KivyMainApp.on_app_run`.

more constants provided by this portion are declared in the :mod:`~ae.kivy.widgets` module.


kivy application events
^^^^^^^^^^^^^^^^^^^^^^^

the main app class is firing :ref:`application events`, additional to the ones provided by
:class:`~ae.gui.app.MainAppBase`, by redirecting events of Kivy's :class:`~kivy.app.App` class.
these framework app events get fired after the event :meth:`~ae.gui.app.MainAppBase.on_app_run`,
in the following order (the Kivy event/callback-method name is given in brackets):

    * on_app_build (kivy.app.App.build, after the main kv file gets loaded).
    * on_app_built (kivy.app.App.build, after the root widget gets to build).
    * on_app_start (kivy.app.App.on_start)
    * on_app_started (one clock tick after on_app_start/kivy.app.App.on_start)
    * on_app_pause (kivy.app.App.on_pause)
    * on_app_resume (kivy.app.App.on_resume)
    * on_app_stop (kivy.app.App.on_stop)
    * on_app_stopped (one clock tick after on_app_stop)

"""
import os

from typing import Any, Callable, Optional, Type, Union

from plyer import vibrator                                                                              # type: ignore

from kivy import kivy_home_dir                                                                          # type: ignore
from kivy.app import App                                                                                # type: ignore
from kivy.clock import Clock                                                                            # type: ignore
from kivy.core.audio import SoundLoader                                                                 # type: ignore
from kivy.core.clipboard import Clipboard                                                               # type: ignore
from kivy.core.window import Window                                                                     # type: ignore
from kivy.factory import Factory, FactoryException                                                      # type: ignore
from kivy.metrics import dp, sp                                                                         # type: ignore
from kivy.properties import (                                                                           # type: ignore
    BooleanProperty, DictProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.dropdown import DropDown                                                                  # type: ignore
from kivy.uix.popup import Popup                                                                        # type: ignore
from kivy.uix.widget import Widget                                                                      # type: ignore
from kivy.utils import escape_markup, get_hex_from_color                                                # type: ignore

from ae.base import os_path_basename, os_path_isfile, os_path_join, os_platform, write_file             # type: ignore
from ae.files import CachedFile                                                                         # type: ignore
from ae.paths import PATH_PLACEHOLDERS, app_docs_path, copy_file, normalize, Collector                  # type: ignore
from ae.core import DEBUG_LEVELS, DEBUG_LEVEL_ENABLED                                                   # type: ignore
from ae.gui.utils import (                                                                              # type: ignore
    APP_STATE_SECTION_NAME, APP_STATE_VERSION_VAR_NAME, MAX_FONT_SIZE, MIN_FONT_SIZE,
    THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR, THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR,
    id_of_flow)
from ae.gui.app import MainAppBase                                                                      # type: ignore

from .i18n import get_txt
from .tours import TourOverlay
from .widgets import ERROR_VIBRATE_PATTERN, MAIN_KV_FILE_NAME, FlowPopup, HelpLayout, HelpMenu


def keyboard_command_key(win_inst: Any, key_code: int) -> str:
    """ get keyboard command key from code, encapsulating in this function to make WindowX11 compatible to WindowSDL2.

    :param win_inst:            used Window instance (on linux either of WindowX11 or WindowSDL/2).
    :param key_code:            key code to get the command key string for.
    :return:                    command key string or empty string on X11 or if no command key was found.
    """
    # noinspection PyBroadException
    try:    # when using X11 Window provider (to fix debugger mouse click locks issue #8273), ignore the AttributeError:
        cmd_key = win_inst.command_keys.get(key_code, "")           # 'WindowX11' object has no attribute 'command_keys'
    except:                                             # noqa: E722 # pragma: no cover # pylint: disable=bare-except
        cmd_key = ""
    return cmd_key


class FrameworkApp(App):
    """ Kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    app_states = DictProperty()                         #: duplicate of MainAppBase app state for events/binds
    button_height = NumericProperty('45sp')             #: default button height, dynamically calculated from font size
    displayed_help_id = StringProperty()                #: help id of the currently explained/help-target widget
    font_color = ObjectProperty(THEME_DARK_FONT_COLOR)  #: rgba color of the font used for labels/buttons/...
    help_layout = ObjectProperty(allownone=True)        #: layout widget if help mode is active else None
    landscape = BooleanProperty()                       #: True if app win width is bigger than the app win height
    max_font_size = NumericProperty(MAX_FONT_SIZE)      #: maximum font size in pixels bound to window size
    min_font_size = NumericProperty(MIN_FONT_SIZE)      #: minimum - " -
    mixed_back_ink = ListProperty([.69, .69, .69, 1.])  #: background color mixed from available back inks
    tour_layout = ObjectProperty(allownone=True)        #: overlay layout widget if tour is active else None

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        super().__init__(**kwargs)

        self.main_app = main_app                            #: set reference to KivyMainApp instance

        self.title = main_app.app_title                     #: set kivy.app.App.title
        self.icon = os_path_join("img", "app_icon.jpg")     #: set kivy.app.App.icon
        self.use_kivy_settings = main_app.debug             #: set kivy.app.App.use_kivy_settings

    def build(self) -> Widget:
        """ kivy build app callback.

        :return:                root widget (Main instance) of this app.
        """
        self.main_app.vpo("FrameworkApp.build")
        self.main_app.call_method('on_app_build')

        Window.bind(on_resize=self.win_pos_size_change,
                    left=self.win_pos_size_change,
                    top=self.win_pos_size_change,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        def _set_button_height(*_args):
            new_height = round(self.main_app.font_size * 1.95)
            if self.button_height != new_height:
                self.button_height = new_height
        self.bind(app_states=_set_button_height)

        self.main_app.framework_root = root = Factory.Main()
        self.main_app.framework_win = Window    # == root.parent (after the calling method has finished)
        self.main_app.call_method('on_app_built')
        return root

    def key_press_from_kivy(self, win_inst: Any, key_code: int, _scan_code: int, key_text: Optional[str],
                            modifiers: list[str]) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param win_inst:        configured/used Window instance.
        :param key_code:        key code of the pressed key.
        :param _scan_code:      unused key scan code of the pressed key.
        :param key_text:        key text of the pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                a boolean True value if the key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            keyboard_command_key(win_inst, key_code) or key_text or str(key_code))

    def key_release_from_kivy(self, win_inst: Any, key_code: int, _scan_code: int) -> bool:
        """ key release/up event.

        :return:                return the value of the call to `on_key_release` (True if ke got processed/used).
        """
        return self.main_app.call_method('on_key_release', keyboard_command_key(win_inst, key_code) or str(key_code))

    def on_pause(self) -> bool:
        """ app pause event automatically saving the app states.

        emits the `on_app_pause` event.

        :return:                always True.
        """
        self.main_app.vpo("FrameworkApp.on_pause")
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event automatically loading the app states.

        emits the `on_app_resume` event.

        :return:                always True.
        """
        self.main_app.vpo("FrameworkApp.on_resume")
        self.main_app.load_app_states()
        self.main_app.call_method('on_app_resume')
        return True

    def on_start(self):
        """ kivy app start event.

        called after the :meth:`~ae.gui.app.MainAppBase.run_app` method,
        after Kivy created the main layout (by calling its :meth:`~kivy.app.App.build` method) and has
        attached it to the main window.

        emits the events: `on_app_start` and `on_app_started`.
       """
        self.main_app.vpo("FrameworkApp.on_start")

        # self.win_pos_size_change()  # init. app./self.landscape (on app startup and after build)

        self.main_app.call_method('on_app_start')
        Clock.schedule_once(lambda dt: self.main_app.call_method('on_app_started'))

    def on_stop(self):
        """ quit app event automatically saving the app states.

        emits the `on_app_stopped` event, whereas the method :meth:`~ae.gui.app.MainAppBase.stop_app`
        emits the `on_app_stop` event.
        """
        self.main_app.vpo("FrameworkApp.on_stop")

        self.main_app.save_app_states()

        self.main_app.call_method('on_app_stop')
        Clock.schedule_once(lambda dt: self.main_app.call_method('on_app_stopped'))

    def win_pos_size_change(self, *_):
        """ resize handler updates: :attr:`~ae.gui.app.MainAppBase.win_rectangle`, :attr:`~FrameworkApp.landscape`. """
        # noinspection PyBroadException
        try:  # ignore under Window provider X11 (instead of sdl2), used to fix debugger mouse click locks issue #8273
            self.main_app.win_pos_size_change(Window.left, Window.top, Window.width, Window.height)
        except:                                         # noqa: E722 # pragma: no cover # pylint: disable=bare-except
            pass


class KivyMainApp(MainAppBase):
    """ Kivy application """
    documents_root_path: str = "."                      #: the root file path for app documents; for import/export
    get_txt_: Any = get_txt                             #: make i18n translations available via main app instance
    help_dropdown: Optional[Widget] = None              #: instance of an opened help menu
    kbd_input_mode: str = 'scale'                       #: optional app state to set Window[Base].softinput_mode
    tour_overlay_class: Optional[Any] = TourOverlay     #: Kivy main app tour overlay class

    _debug_enable_clicks: int = 0

    # implementation of abstract methods

    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp
                 ) -> tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and prepare app startup.

        :param framework_app_class:     class to create the framework app instance (optionally extended by the
                                        app project).
        :return:                        callable to start and stop/exit the GUI event loop.
        """
        self.documents_root_path = app_docs_path()

        self.framework_app = framework_app_class(self)
        if os_path_isfile(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME          # pylint: disable=W0201

        return self.framework_app.run, self.framework_app.stop

    # overwritten and helper methods

    def _init_path_placeholders(self):
        """ add Kivy-specific paths """
        PATH_PLACEHOLDERS['khd'] = kivy_home_dir
        super()._init_path_placeholders()

    def app_env_dict(self) -> dict[str, Any]:
        """ collect run-time app environment data and settings.

        :return:                dict with app environment data/settings.
        """
        app_env_info = super().app_env_dict()

        app_env_info['dpi_factor'] = f"{self.dpi_factor()}; {dp(1000)=} {sp(1000)=} {Window.size=} {Window.dpi=}"

        if self.debug:
            app_env_info['image_files'] = self.image_files
            app_env_info['sound_files'] = self.sound_files

            app_states_data: dict[str, Any] = {APP_STATE_VERSION_VAR_NAME: self.app_state_version,
                                               'app_state_keys': self.app_state_keys()}
            if self.verbose:
                app_states_data["framework app states"] = self.framework_app.app_states
                app_states_data['kbd_input_mode'] = self.kbd_input_mode

                app_env_info['help data'] = {
                    'displayed_help_id': self.displayed_help_id,
                    'global_variables': self.global_variables(),
                    '_last_focus_flow_id': self._last_focus_flow_id,
                    '_next_help_id': self._next_help_id,
                }

                app_env_info['app data']['documents_root_path'] = self.documents_root_path
            app_env_info['app states data'] = app_states_data

        return app_env_info

    def backup_config_resources(self) -> str:   # pragma: no cover
        """ backup kivy-specific config files and logs to {ado}<now_str>. """
        backup_root = super().backup_config_resources()     # MainAppBase backup also creates the backup_root folder
        backup_kivy_home_dir = os_path_join(backup_root, 'khd')

        try:
            os.makedirs(backup_kivy_home_dir)

            coll = Collector()
            coll.collect("{khd}", append='config.ini')    # 'config.ini' name set in kivy/__init__.py
            coll.collect("{khd}/logs", append="*.txt")    # .. 'logs' in kivy/config.py&kivy/logger.py
            for file in coll.files:
                copy_file(file, os_path_join(backup_kivy_home_dir, os_path_basename(file)))

        except (PermissionError, Exception) as ex:                  # pylint: disable=broad-exception-caught
            self.show_message(f"kivy-specific backup to '{backup_kivy_home_dir}' failed with exception '{ex}'")

        return backup_root

    def call_method_delayed(self, delay: float, callback: Union[Callable, str], *args, **kwargs) -> Any:
        """ delayed call of passed callable/method with args/kwargs catching and logging exceptions preventing app exit.

        :param delay:           delay in seconds before calling the callable/method specified by
                                :paramref:`~call_method_delayed.callback`.
        :param callback:        either callable or name of the main app method to call.
        :param args:            args passed to the callable/main-app-method to be called.
        :param kwargs:          kwargs passed to the callable/main-app-method to be called.
        :return:                delayed call event (in Kivy of Type[ClockEvent]) providing a `cancel` method to allow
                                the cancellation of the delayed call within the delay time.
        """
        return Clock.schedule_once(lambda dt: self.call_method(callback, *args, **kwargs), timeout=delay)

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
        return Clock.schedule_interval(lambda dt: self.call_method(callback, *args, **kwargs), timeout=interval)

    def change_light_theme(self, light_theme: bool):
        """ change font and window clear/background colors to match 'light'/'black' themes.

        :param light_theme:     pass True for light theme, False for black theme.
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ resolve kv widgets """
        try:
            return Factory.get(class_name)
        except (FactoryException, AttributeError):
            return None

    @staticmethod
    def dpi_factor() -> float:
        """ dpi scaling factor - overridden to use Kivy's dpi scaling. """
        return dp(1.0)

    def ensure_top_most_z_index(self, widget: Widget):
        """ ensure visibility of the passed widget to be the foremost in the z index/order.

        :param widget:          widget to check and possibly correct to be the foremost one.

        if other dropdown/popup opened after the passed widget/layout, then only correct z index/order to show this
        widget as a popup (in front, as foremost widget). if the passed widget has a method named `activate_modal`
        (like, for example, the method :meth:`ae.kivy.behaviors.ModalBehavior.activate_modal`), then it will be called.
        """
        popups_parent = self.framework_win
        if widget not in popups_parent.children or popups_parent.children[0] == widget:
            return

        reactivate_modal = getattr(widget, 'activate_modal', None)
        if callable(reactivate_modal):
            reactivate_modal()
        else:
            popups_parent.remove_widget(widget)
            popups_parent.add_widget(widget)

    def global_variables(self, **patches) -> dict[str, Any]:
        """ overridden to add Kivy-specific globals. """
        return super().global_variables(escape_markup=escape_markup, get_hex_from_color=get_hex_from_color, **patches)

    def help_activation_toggle(self):  # pragma: no cover
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """
        help_layout = self.help_layout
        if help_layout:
            help_layout.stop_help()

        tour_layout = self.tour_layout
        if tour_layout:
            tour_layout.stop_tour()

        if self.help_dropdown:
            self.help_dropdown.dismiss()
            self.help_dropdown = None
        elif help_layout is None and tour_layout is None:
            self.help_dropdown = self.open_popup(HelpMenu, opener=self.help_activator)

    def help_layout_activation(self):  # pragma: no cover
        """ button tapped event handler to switch help mode between active and inactive (also inactivating tour). """
        help_vars = {}
        target, help_id = self.help_target_and_id(help_vars)

        help_layout = HelpLayout(targeted_widget=target)
        self.framework_win.add_widget(help_layout)

        self.change_observable('help_layout', help_layout)

        self.help_display(help_id, help_vars)  # show found/initial help text (after self.help_layout got set)

        help_layout.ani_start()
        self.help_activator.ani_start()

    def load_sounds(self):
        """ override to preload audio sounds from app folder snd into sound file cache. """
        super().load_sounds()  # load from sound file paths all files into :class:`~ae.files.RegisteredFile` instances
        self.sound_files.reclassify(object_loader=lambda f: SoundLoader.load(f.path))  # :class:`~ae.files.CachedFile`

    def on_app_build(self):
        """ kivy App build event handler called at the beginning of :meth:`kivy.app.App.build`. """
        super().on_app_build()
        self.vpo("KivyMainApp.on_app_build - reload image resources from kv file late imports, e.g. ae.kivy_user_prefs")
        self.load_images()

    def on_app_built(self):
        """ kivy App build event handler called at the end of :meth:`kivy.app.App.build`. """
        self.vpo("KivyMainApp.on_app_built default/fallback event handler called")

    def on_app_pause(self):
        """ kivy :meth:`~kivy.app.App.on_pause` event handler. """
        self.vpo("KivyMainApp.on_app_pause default/fallback event handler called")

    def on_app_resume(self):
        """ kivy :meth:`~kivy.app.App.on_resume` event handler. """
        self.vpo("KivyMainApp.on_app_resume default/fallback event handler called")

    def on_app_run(self):  # pragma: no cover
        """ run app event handler - used to set the user preference app states and initial window pos and size. """
        super().on_app_run()
        self.vpo("KivyMainApp.on_app_run - setting lang, theme, win-pos/-size and softinput mode")

        get_txt.switch_lang(self.lang_code)
        self.change_light_theme(self.light_theme)
        Window.softinput_mode = self.kbd_input_mode
        Window.minimum_size = (self.get_var('win_min_width', default_value=405),
                               self.get_var('win_min_height', default_value=303))

        if os_platform not in ('android', 'ios'):  # ignore last win pos on android/iOS, use always the full screen
            win_rect = self.win_rectangle or KivyMainApp.win_rectangle  # self val is empty tuple on first app start
            # although using KIVY_WINDOW=x11 (instead of the default: window_sdl2) fixes Kivy issue #8273, X11 throws
            # on window position restore the exception: kivy/core/window/__init__.py, line 897, in _set_left
            #     self._set_window_pos(value, pos[1])
            # TypeError: 'NoneType' object is not subscriptable
            # noinspection PyBroadException
            try:
                Window.left, Window.top = win_rect[:2]
            except:                                         # noqa: E722 # pylint: disable=bare-except
                pass
            # noinspection PyBroadException
            try:
                Window.size = win_rect[2:]
            except:                                         # noqa: E722 # pylint: disable=bare-except
                pass

    def on_app_start(self):  # pragma: no cover
        """ app start event handler - triggered by FrameworkApp.on_start(). """
        self.vpo("KivyMainApp.on_app_start")

    def on_app_started(self):
        """ kivy :meth:`~kivy.app.App.on_start` event handler (called after on_app_build/on_app_built). """
        self.vpo("KivyMainApp.on_app_started event handler called - calling ae.gui.app.MainAppBase.on_app_started")
        super().on_app_started()    # check user registration/onboarding tour start in ae.gui.app.MainAppBase

    def on_app_stopped(self):
        """ kivy :meth:`~kivy.app.App.on_stop` event handler (called after on_app_stop). """
        self.vpo("KivyMainApp.on_app_stopped default/fallback event handler called")

    def on_clipboard_file_delete_confirmed(self, file_path: str, _kwargs: dict[str, Any]) -> bool:  # pragma: no cover
        """ delete the file at the specified file path (after the user copied 'DELETE_FILE' into Clipboard).

        :param file_path:       file name to delete (with an optional path relative to the CWD).
        :param _kwargs:         unused flow event kwargs.
        :return:                a boolean True value if the file could be deleted, else False.
        """
        try:
            os.remove(file_path)
            self.show_message(f"successfully deleted {file_path=}")
        except Exception as ex:             # pylint: disable=broad-exception-caught
            # FileExistsError, FileNotFoundError, OSError, PermissionError
            self.po(f"KivyMainApp.on_clipboard_file_delete_confirmed exception {ex=} on deletion of {file_path=}")
            return False

        return True

    def on_clipboard_file_overwrite_confirmed(self, file_path: str, _event_kwargs: dict[str, Any]) -> bool:
        """ save Clipboard content to specified, and maybe existing, file path relative to the cwd of the running app.

        :param file_path:       file name (with an optional path relative to the CWD).
        :param _event_kwargs:   unused flow event kwargs.
        :return:                boolean True if clipboard content is not empty and could be saved to file, else False.

        called from on_clipboard_file_save directly or indirectly via :meth:`~ae.gui.app.MainAppBase.show_confirmation`.
        used to store ini or env files into the current working directory (on Android the inaccessible `files/app`
        folder within the app installation folder; prefix file path with `../app-name/` or `../` for files that have to
        be kept on app update).
        """
        content = Clipboard.paste()
        if not content or content == 'DELETE_FILE':     # pragma: no cover
            self.show_message(f"wrong clipboard {content=}; expected nonempty content or 'DELETE_FILE' if file existed")
            return False

        self.vpo(f"KivyMainApp.on_clipboard_file_overwrite_confirmed {len(content)=} bytes to {file_path=}")
        try:
            write_file(file_path, content)
            if file_path == self._main_cfg_fnam:        # pragma: no cover
                self.load_app_states()                  # load app states from the just overwritten main config file
            self.show_message("restart app to take affect", title="file saved")
        except Exception as ex:                         # pragma: no cover # pylint: disable=broad-exception-caught
            # FileExistsError, FileNotFoundError, OSError, PermissionError
            self.po(f"KivyMainApp.on_clipboard_file_overwrite_confirmed exception {ex=} on writing to {file_path=}")
            return False

        return True

    def on_clipboard_file_save(self, file_path: str, _event_kwargs: dict[str, Any]) -> bool:
        """ debug event handler to check save of Clipboard content to the specified file path.

        :param file_path:       file name (with an optional path relative to the app cwd).
        :param _event_kwargs:   unused flow event kwargs.
        :return:                the boolean True if the file path in the specified flow key is not empty, else False.

        called from InputShowPopup opened from the user prefs debug menu item, declared in UserPreferencesPopup.
        """
        if not file_path:
            self.show_message(f"empty {file_path=}", title="incomplete data error")
            return False

        file_path = normalize(file_path)
        if os_path_isfile(file_path):
            file_action = 'delete' if Clipboard.paste() == 'DELETE_FILE' else 'overwrite'
            self.show_confirmation(f"¿{file_action} {file_path=}?",
                                   title=f"confirm file {file_action}",
                                   confirm_flow_id=id_of_flow('confirmed', f'clipboard_file_{file_action}', file_path),
                                   confirm_kwargs={'popups_to_close': ('replace_with_data_map_popup',)})
        else:
            self.on_clipboard_file_overwrite_confirmed(file_path, _event_kwargs)

        return True

    def on_flow_widget_focused(self):
        """ set focus to the widget referenced by the current flow id. """
        liw = self.widget_by_flow_id(self.flow_id)
        self.vpo(f"KivyMainApp.on_flow_widget_focused() '{self.flow_id}'"
                 f" {liw} has={getattr(liw, 'focus', 'unsupported') if liw else ''}")
        if liw and getattr(liw, 'is_focusable', False) and not liw.focus:
            liw.focus = True

    def on_kbd_input_mode_change(self, mode: str, _event_kwargs: dict[str, Any]) -> bool:
        """ language app state change event handler.

        :param mode:            the new softinput_mode string (passed as a flow key).
        :param _event_kwargs:   unused event kwargs.
        :return:                the boolean value True to confirm the language change.
        """
        self.vpo(f"KivyMainApp.on_kbd_input_mode_change to {mode}")
        self.change_app_state('kbd_input_mode', mode)
        self.set_var('kbd_input_mode', mode, section=APP_STATE_SECTION_NAME)  # add optional app state var to config
        Window.softinput_mode = mode
        return True

    def on_lang_code(self):
        """ language code app-state-change-event-handler to refresh kv rules. """
        self.vpo(f"KivyMainApp.on_lang_code: language got changed to {self.lang_code}")
        get_txt.switch_lang(self.lang_code)

    def on_light_theme(self):
        """ theme app-state-change-event-handler. """
        self.vpo(f"KivyMainApp.on_light_theme: theme got changed to {self.light_theme}")
        self.change_light_theme(self.light_theme)

    def on_user_preferences_open(self, _flow_key: str, _event_kwargs: dict[str, Any]) -> bool:
        """ enable debug mode after clicking 3 times within 6 seconds.

        :return:                False for :meth:`~.on_flow_change` get called, opening the user preferences popup.
        """
        def _timeout_reset(_dt: float):
            self._debug_enable_clicks = 0

        if not self.debug:
            self._debug_enable_clicks += 1
            if self._debug_enable_clicks >= 3:
                self.on_debug_level_change(DEBUG_LEVELS[DEBUG_LEVEL_ENABLED], {})  # also enable for all sub-apps
                self._debug_enable_clicks = 0
            elif self._debug_enable_clicks == 1:
                Clock.schedule_once(_timeout_reset, 6.0)

        return False        # side-run:returning False (allowing user prefs dropdown to be found and opened)

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play an audio/sound file. """
        self.vpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.app_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:         # pragma: no cover # pylint: disable=broad-exception-caught
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: tuple = ERROR_VIBRATE_PATTERN):
        """ play a vibration pattern. """
        self.vpo(f"KivyMainApp.play_vibrate {pattern}")
        if self.framework_app.app_states.get('vibration_volume', 1.):  # no volume available, at least disable if 0.0
            try:  # added because it's crashing with the current plyer version (master should work)
                vibrator.pattern(pattern)
            # except jnius.jnius.JavaException as ex:
            #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
            except Exception as ex:         # pylint: disable=broad-exception-caught
                self.po(f"KivyMainApp.play_vibrate exception {ex}")

    def open_popup(self, popup_class: Type[Union[FlowPopup, Popup, DropDown]], **popup_kwargs) -> Widget:
        """ open Popup or DropDown using the `open` method. overwriting the main app class method.

        :param popup_class:     class of the Popup or DropDown widget.
        :param popup_kwargs:    args to be set as attributes of the popup class instance plus an optional
                                `opener` kwarg that will pass the popup opener widget to the popup.open() method; if
                                `opener` gets not specified, then the framework window will be used.
        :return:                the created and displayed/opened popup class instance.
        """
        self.dpo(f"KivyMainApp.open_popup {popup_class} {popup_kwargs}")

        # use framework_root as opener default, having absolute screen coordinates (framework_win lacks pos property)
        opener = popup_kwargs.pop('opener', self.framework_root)
        popup_instance = popup_class(**popup_kwargs)
        popup_instance.open(opener)

        return popup_instance

    def text_size_guess(self, text: str, font_size: float = 0.0, padding: tuple[float, float] = (0.0, 0.0)
                        ) -> tuple[float, float]:
        """ quickly roughly pre-calculate the texture size of a multi-line string without rendering.

        :param text:            text string which can contain line feed characters.
        :param font_size:       the font size to pseudo-render the passed text; using the value of
                                :attr:`~ae.gui.app.MainAppBase.font_size` as default if not passed.
        :param padding:         optional padding in pixels for x and y coordinate (totals for left+right/top+bottom).
        :return:                roughly the size (width, height) to display the string passed into
                                :paramref:`~text_size_guess.text`. more exactly size would need to use internal render
                                methods of Kivy, like e.g. :meth:`~kivy.uix.textinput.TextInput._get_text_width` and
                                :meth:`~kivy.core.text.LabelBase.get_extents`.
        """
        if not font_size:
            font_size = self.font_size

        char_width = font_size / 1.77
        line_height = font_size * 1.29 if text else 0
        max_width = lines_height = 0.0
        for line in text.split("\n"):
            line_width = len(line) * char_width
            max_width = max(max_width, line_width)
            lines_height += line_height

        return max_width + (padding[0] if text else 0.0), lines_height + (padding[1] if text else 0.0)

    def widget_by_id(self, widget_id: str, root_widget: Optional[Widget] = None) -> Optional[Widget]:  # pragma:no cover
        """ search the z-axis top/foremost widget within/underneath the specified root widget by its id.

        :param widget_id:       widget id string to bottom-up-search for.
        :param root_widget:     widget/container to start search underneath from, else from the widget tree root/win.
        :return:                either the found widget or None if not found.
        """
        if not root_widget:
            root_widget = self.framework_win

        if hasattr(root_widget, 'ids'):                                     # framework_win has no ids attribute
            ids_objects = root_widget.ids.items()
        else:
            ids_objects = [('', child) for child in root_widget.children]   # popups are before the framework_root.
        for wid_id, wid_obj in ids_objects:
            if wid_obj.ids:
                if sub_obj := self.widget_by_id(widget_id, root_widget=wid_obj):
                    return sub_obj

            if wid_id == widget_id:
                return wid_obj

        return None

    @staticmethod
    def widget_pos(wid) -> tuple[float, float]:
        """ return widget's window x/y position (overridden for absolute coordinates relative/scrollable layouts).

        :param wid:             widget to determine the position of.
        :return:                tuple of x and y screen coordinate.
        """
        return wid.to_window(*wid.pos)
