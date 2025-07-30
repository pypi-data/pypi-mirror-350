""" test ae.kivy package """
import datetime
import os
import pytest
import shutil

from conftest import skip_gitlab_ci
from unittest.mock import MagicMock, patch

from kivy.base import stopTouchApp
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.lang import Builder, Observable
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup

from ae.base import INI_EXT, TESTS_FOLDER, read_file, write_file
from ae.core import DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_ENABLED, DEBUG_LEVEL_VERBOSE
from ae.i18n import default_language
from ae.gui.utils import (
    APP_STATE_SECTION_NAME, MAX_FONT_SIZE, MIN_FONT_SIZE, flow_key, id_of_flow, replace_flow_action)
from ae.gui.app import MainAppBase

from ae.kivy.i18n import get_txt
from ae.kivy.widgets import (
    MAIN_KV_FILE_NAME, LOVE_VIBRATE_PATTERN, ERROR_VIBRATE_PATTERN, CRITICAL_VIBRATE_PATTERN,
    AbsolutePosSizeBinder, Tooltip, HelpToggler)
from ae.kivy.tours import TourOverlay
from ae.kivy.apps import KivyMainApp, FrameworkApp


def test_widget_declaration():
    """ we need at least one test to prevent pytest exit code 5 (no tests collected) """
    assert AbsolutePosSizeBinder
    assert Tooltip
    assert HelpToggler
    assert TourOverlay


TST_VAR = 'win_rectangle'
TST_VAL = (90, 60, 900, 600)

TST_DICT = {TST_VAR: TST_VAL}
def_app_states = TST_DICT.copy()


MAIN_KV_LAYOUT = '''
<Main@FloatLayout>:
'''
Builder.load_string(MAIN_KV_LAYOUT)


@pytest.fixture
def ini_file(restore_app_env):
    """ provide a test config file """
    fn = "tests/tst" + INI_EXT
    with open(fn, 'w') as file_handle:
        file_handle.write(f"[{APP_STATE_SECTION_NAME}]\n")
        file_handle.write("\n".join(k + " = " + repr(v) for k, v in def_app_states.items()))
    yield fn
    if os.path.exists(fn):      # some exception/error-check tests need to delete the INI
        os.remove(fn)


class KeyboardStub:
    """ stub to simulate a keyboard instance for key events. """
    def __init__(self, **kwargs):
        self.command_keys = kwargs


class KivyAppTest(KivyMainApp):
    """ kivy main app test implementation """
    app_state_list: list
    app_state_bool: bool
    app_title: str

    on_init_called = None
    on_pause_called = None
    on_resume_called = None
    on_run_called = None
    on_start_called = None
    on_started_called = None
    on_stop_called = None

    on_flow_id_called = 0
    on_font_size_called = False

    on_key_press_called = False
    on_key_release_called = False
    last_keys = ()

    def init_app(self, framework_app_class=FrameworkApp):
        """ called from MainAppBase """
        self.on_init_called = datetime.datetime.now()
        self.app_title = "KivyAppTest Stub"
        return super().init_app(framework_app_class=framework_app_class)

    # events

    def on_app_run(self):
        """ called from KivyMainApp """
        super().on_app_run()
        self.on_run_called = datetime.datetime.now()

    def on_app_start(self):
        """ called from KivyMainApp """
        super().on_app_start()
        self.on_start_called = datetime.datetime.now()

    def on_app_started(self):
        """ called from KivyMainApp """
        super().on_app_started()
        self.on_started_called = datetime.datetime.now()

    def on_app_pause(self):
        """ called from KivyMainApp """
        super().on_app_pause()
        self.on_pause_called = datetime.datetime.now()

    def on_app_resume(self):
        """ called from KivyMainApp """
        super().on_app_resume()
        self.on_resume_called = datetime.datetime.now()

    def on_app_stopped(self):
        """ called from KivyMainApp """
        super().on_app_stopped()
        self.on_stop_called = datetime.datetime.now()

    def on_flow_id(self):
        """ called from KivyMainApp.call_method_delayed() and KivyMainApp.call_method_repeatedly() """
        self.on_flow_id_called += 1

    def on_font_size(self):
        """ called from KivyMainApp """
        self.on_font_size_called = True

    def on_key_press(self, modifiers, key):
        """ key press callback """
        self.on_key_press_called = True
        self.last_keys = modifiers, key
        return True

    def on_key_release(self, key):
        """ key release callback """
        self.on_key_release_called = True
        self.last_keys = key,
        return True


# some basic constant tests (running also on gitlab ci image, because pytest returns exit code 5 if all tests skip)
def test_vibrate_pattern_types():
    assert isinstance(LOVE_VIBRATE_PATTERN, tuple)
    assert isinstance(ERROR_VIBRATE_PATTERN, tuple)
    assert isinstance(CRITICAL_VIBRATE_PATTERN, tuple)


def test_kv_default_file_name():
    assert isinstance(MAIN_KV_FILE_NAME, str)


def test_main_app_class_abstracts():
    assert hasattr(MainAppBase, 'init_app')


@skip_gitlab_ci
class TestAppState:
    def test_change_app_state(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

        chg_val = 'ChangedVal'
        chg_dict = {TST_VAR: chg_val}
        app.change_app_state(TST_VAR, chg_val)

        assert getattr(app, TST_VAR) == chg_val
        fas = app.framework_app.app_states
        assert all(k in fas and v == fas[k] for k, v in chg_dict.items())
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in chg_dict.items())

        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val

    def test_default_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file, ))
        assert getattr(app, TST_VAR) == def_app_states[TST_VAR]

    def test_load_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL

        app.load_app_states()
        assert getattr(app, TST_VAR) == TST_VAL
        fas = app.framework_app.app_states
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

    def test_retrieve_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

    def test_save_app_states(self, ini_file, restore_app_env):
        global TST_DICT
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        old_dict = TST_DICT.copy()
        try:
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
            fas = app.retrieve_app_states()
            assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

            chg_val = 'ChangedVal'
            TST_DICT = {TST_VAR: chg_val}
            setattr(app, TST_VAR, chg_val)
            assert app.save_app_states() == ""
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val
            fas = app.retrieve_app_states()
            assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())
        finally:
            TST_DICT = old_dict

    def test_save_app_states_exception(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        os.remove(ini_file)
        assert app.save_app_states() != ""

    def test_set_font_size(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert app.font_size == MainAppBase.font_size

        assert MIN_FONT_SIZE <= app.font_size <= MAX_FONT_SIZE

        assert not app.on_font_size_called

        font_size = MAX_FONT_SIZE
        app.change_app_state('font_size', font_size)
        assert app.font_size == font_size
        assert app.on_font_size_called

    def test_setup_app_states(self, ini_file, restore_app_env):
        assert KivyMainApp.win_rectangle == MainAppBase.win_rectangle   # (0, 0, 800, 600)
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert getattr(app, TST_VAR) == TST_VAL
        app.setup_app_states(TST_DICT)
        assert getattr(app, TST_VAR) == TST_VAL
        assert app.win_rectangle == def_app_states[TST_VAR]
        app.setup_app_states(dict(font_size=-12))
        assert isinstance(app.font_size, (int, float))
        TST_DICT.pop('font_size')       # remove font_size for the following tests


@skip_gitlab_ci
class TestHelperMethods:
    def test_app_env_dict(self, restore_app_env):
        app = KivyMainApp()
        app.set_opt('debug_level', DEBUG_LEVEL_VERBOSE)
        data = app.app_env_dict()
        assert 'dpi_factor' in data
        assert 'app data' in data

    def test_call_method_delayed_invalid_callback(self, restore_app_env):
        app = KivyMainApp()
        app.call_method_delayed(0.0, app.__doc__)

    def test_call_method_delayed_valid_callback(self, restore_app_env):
        app = KivyAppTest()
        assert app.on_flow_id_called == 0
        app.call_method_delayed(0.0, app.on_flow_id)
        assert app.on_flow_id_called == 0
        Clock.tick()
        assert app.on_flow_id_called == 1

    def test_call_method_delayed_invalid_method(self, restore_app_env):
        app = KivyMainApp()
        app.call_method_delayed(0.0, 'invalid_method_name')

    def test_call_method_delayed_valid_method(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert app.on_flow_id_called == 0
        app.call_method_delayed(0.0, 'on_flow_id')
        assert app.on_flow_id_called == 0
        Clock.tick()
        assert app.on_flow_id_called == 1

    def test_call_method_repeatedly_invalid_callback(self, restore_app_env):
        app = KivyMainApp()
        app.call_method_repeatedly(0.0, app.__doc__)

    def test_call_method_repeatedly_valid_callback(self, restore_app_env):
        app = KivyAppTest()
        assert app.on_flow_id_called == 0
        app.call_method_repeatedly(0.0, app.on_flow_id)
        assert app.on_flow_id_called == 0
        Clock.tick()
        assert app.on_flow_id_called == 1
        Clock.tick()
        assert app.on_flow_id_called > 1

    def test_call_method_repeatedly_invalid_method(self, restore_app_env):
        app = KivyMainApp()
        app.call_method_repeatedly(0.0, 'invalid_method_name')

    def test_call_method_repeatedly_valid_method(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert app.on_flow_id_called == 0
        app.call_method_repeatedly(0.0, 'on_flow_id')
        assert app.on_flow_id_called == 0
        Clock.tick()
        assert app.on_flow_id_called == 1
        Clock.tick()
        assert app.on_flow_id_called > 1

    def test_call_method_valid_method(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_flow_id_called
        assert app.call_method('on_flow_id') is None
        assert app.on_flow_id_called

    def test_call_method_return(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_run_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_run_called

    def test_call_method_invalid_method(self, restore_app_env):
        app = KivyMainApp()
        assert app.call_method('invalid_method_name') is None

    def test_ensure_top_most_z_index(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
        app.framework_win.add_widget = lambda child: app.framework_win.children.insert(0, child)

        wid = MagicMock()
        app.framework_win.add_widget(wid)
        assert app.framework_win.children[0] == wid
        app.ensure_top_most_z_index(wid)
        assert app.framework_win.children[0] == wid

        wid.activate_modal = None
        wid2 = MagicMock()
        app.framework_win.add_widget(wid2)
        assert app.framework_win.children[0] != wid
        app.ensure_top_most_z_index(wid)
        assert app.framework_win.children[0] == wid

        wid.activate_modal = lambda: setattr(wid, '_activate_modal_called', True)
        wid3 = MagicMock()
        app.framework_win.add_widget(wid3)
        app.ensure_top_most_z_index(wid)
        assert getattr(wid, '_activate_modal_called', False) is True

    def test_main_kv_load(self, restore_app_env):
        try:
            write_file(MAIN_KV_FILE_NAME, MAIN_KV_LAYOUT)
            app = KivyMainApp()
            assert app.framework_app.kv_file == MAIN_KV_FILE_NAME
        finally:
            if os.path.exists(MAIN_KV_FILE_NAME):
                os.remove(MAIN_KV_FILE_NAME)

    def test_mix_background_ink(self, restore_app_env):
        app = KivyMainApp()
        app.mix_background_ink()
        assert app.framework_app.mixed_back_ink[0] \
            == (app.flow_id_ink[0] + app.flow_path_ink[0] + app.selected_ink[0]) / 3.0
        assert app.framework_app.mixed_back_ink[1] \
            == (app.flow_id_ink[1] + app.flow_path_ink[1] + app.selected_ink[1]) / 3.0
        assert app.framework_app.mixed_back_ink[2] \
            == (app.flow_id_ink[2] + app.flow_path_ink[2] + app.selected_ink[2]) / 3.0
        assert app.framework_app.mixed_back_ink[3] \
            == (app.flow_id_ink[3] + app.flow_path_ink[3] + app.selected_ink[3]) / 3.0

    def test_play_beep(self, restore_app_env):
        app = KivyMainApp()
        app.play_beep()

    def test_play_sound_missing(self, restore_app_env):
        app = KivyMainApp()
        app.play_sound('tst')

    def test_play_sound_wav(self, restore_app_env):
        sound_dir = 'snd'
        sound_file = 'tst_snd_file'
        try:
            os.mkdir(sound_dir)
            shutil.copy(os.path.join(TESTS_FOLDER, 'tst.wav'), os.path.join(sound_dir, sound_file + '.wav'))
            app = KivyMainApp()
            app.load_sounds()
            app.play_sound(sound_file)
        finally:
            shutil.rmtree(sound_dir)

    def test_play_sound_invalid_wav(self, restore_app_env):
        sound_dir = 'snd'
        sound_file = 'tst_snd_file'
        try:
            os.mkdir(sound_dir)
            write_file(os.path.join(sound_dir, sound_file + '.mp3'), 'invalid sound file content')
            app = KivyMainApp()
            app.load_sounds()
            app.play_sound(sound_file)
        finally:
            shutil.rmtree(sound_dir)

    def test_play_vibrate(self, restore_app_env):
        app = KivyMainApp()
        app.play_vibrate()

    def test_play_vibrate_invalid_pattern(self, restore_app_env):
        app = KivyMainApp()
        app.play_vibrate(('invalid pattern', ))

    def test_popups_opened(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
        app.framework_root = MagicMock()
        app.framework_root.children = []

        class _Popup:
            """ dummy popup """
            def open(self, _parent):
                """ popup open method """
                app.framework_win.children.append(self)

        # noinspection PyTypeChecker
        app.open_popup(_Popup)

        popups = app.popups_opened()
        assert popups
        assert isinstance(popups[0], _Popup)

    def test_text_size_guess(self, restore_app_env):
        app = KivyMainApp()

        assert app.text_size_guess("") == (0.0, 0.0)
        assert app.text_size_guess("tst") == (3 * app.font_size / 1.77, app.font_size * 1.29)
        assert app.text_size_guess("tst\nWWW") == (3 * app.font_size / 1.77, app.font_size * 2 * 1.29)

        font_size = 99
        assert app.text_size_guess("", font_size=font_size) == (0.0, 0.0)
        assert app.text_size_guess("tst", font_size=font_size) == (3 * font_size / 1.77, font_size * 1.29)
        assert app.text_size_guess("tst\nWWW", font_size=font_size) == (3 * font_size / 1.77, font_size * 2 * 1.29)

    def test_widget_children(self, restore_app_env):
        app = KivyMainApp()

        class _Widget:
            """ dummy widget """
            children = []
            width = 99
            height = 99
        parent = _Widget()
        app.framework_win = parent
        wid = _Widget()
        app.framework_win.children.append(wid)
        assert app.widget_children(app.framework_win) == [wid]

        assert app.widget_children(app.framework_win, only_visible=True) == [wid]
        wid.width = 0
        assert app.widget_children(app.framework_win, only_visible=True) == []

    def test_widget_pos(self, restore_app_env):
        app = KivyMainApp()
        tst_pos = (36, 99)

        class Widget:
            """ dummy widget """
            pos = tst_pos

            @staticmethod
            def to_window(*pos_args):
                """ dummy win coordinate convert to absolute """
                return pos_args

        assert app.widget_pos(Widget()) == tst_pos


@skip_gitlab_ci
class TestFlow:
    def test_flow_enter(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
        assert len(app.flow_path) == 0
        flow1 = id_of_flow('enter', 'first_flow')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1

    def test_flow_enter_next_id(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        flow1 = id_of_flow('enter', 'first_flow')
        flow2 = id_of_flow('action', '2nd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == flow2

    def test_flow_leave(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
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
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = []
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        flow2 = id_of_flow('action', '2nd_flow', 'tst_key2')
        flow3 = id_of_flow('leave', '3rd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert app.flow_id == flow2

        app.change_flow(flow3, flow_id=flow3)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow3

    def test_set_flow_with_send_event(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.on_flow_id_called

        flow1 = 'first_flow'
        app.change_app_state('flow_id', flow1)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert app.on_flow_id_called

    def test_set_flow_without_send_event(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.on_flow_id_called

        flow1 = 'first_flow'
        app.change_app_state('flow_id', flow1, send_event=False)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert not app.on_flow_id_called


@skip_gitlab_ci
class TestEvents:
    def test_flow_id(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_flow_id_called
        app.change_app_state('flow_id', id_of_flow('tst', 'flow'))
        assert app.on_flow_id_called

    def test_init(self, restore_app_env):
        app = KivyAppTest()
        assert app.on_init_called

    def test_key_press_text(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        key_text = 'y'
        modifiers = ["alt"]
        app.framework_app.key_press_from_kivy(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == (modifiers[0].capitalize(), key_text)

    def test_key_press_code(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 369
        key_text = ''
        modifiers = ["meta", "ctrl"]
        app.framework_app.key_press_from_kivy(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == ("CtrlMeta", str(key_code))

    def test_key_release(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        app.framework_app.key_release_from_kivy(kbd, key_code, None)
        assert app.last_keys == (str(key_code), )

    def test_on_clipboard_file_save(self, restore_app_env):
        old_content = Clipboard.paste()
        file_path = '.any_tst_file_name'
        counter = 0

        def inc_counter(*_args, **_kwargs):
            """ increment call counter """
            nonlocal counter
            counter += 1

        assert not os.path.isfile(file_path)
        app = KivyAppTest()
        content = "credentials content\nwith multiple lines\nfor äÛß tests not has to be in any 'special' format!"

        try:
            app.show_message = inc_counter
            assert app.on_clipboard_file_save("", {}) is False
            assert counter == 1

            app.show_confirmation = inc_counter
            assert app.on_clipboard_file_save("test_kivy.py", {}) is True
            assert counter == 2

            Clipboard.copy(content)
            app.on_clipboard_file_save(file_path, {})
            assert counter == 3
            assert os.path.isfile(file_path)
            assert read_file(file_path) == content

        finally:
            Clipboard.copy(old_content)
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_on_flow_widget_focused(self, restore_app_env):
        app = KivyAppTest()

        class Wid:
            """ test dummy """
            focus = False
            is_focusable = True

        wid = Wid()
        app.widget_by_flow_id = lambda flow_id: wid
        app.on_flow_widget_focused()
        assert wid.focus is True

    def test_on_kbd_input_mode_change(self, restore_app_env):
        app = KivyAppTest()
        old_mode = app.kbd_input_mode

        app.on_kbd_input_mode_change('', {})
        assert app.kbd_input_mode == ''

        app.on_kbd_input_mode_change('below_target', {})
        assert app.kbd_input_mode == 'below_target'

        # app.kbd_input_mode = old_mode
        assert app.on_kbd_input_mode_change(old_mode, {})

    def test_on_light_theme_change(self, restore_app_env):
        app = KivyAppTest()

        app.on_light_theme_change('any', dict(light_theme=True))
        assert app.light_theme

        app.on_light_theme_change('any', dict(light_theme=False))
        assert not app.light_theme

    def test_on_pause(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_pause_called
        # Clock.schedule_once(lambda dt: Window.do_pause())
        app.framework_app.dispatch('on_pause')
        # Clock.schedule_once(app.framework_app.stop)
        # Clock.schedule_once(lambda dt: stopTouchApp(), 0.9)
        # app.run_app()
        assert app.on_pause_called

    def test_on_resume(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_resume_called
        app.framework_app.dispatch('on_resume')
        Clock.schedule_once(app.framework_app.stop, 0.6)
        app.run_app()
        assert app.on_resume_called

    def test_on_stop(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_stop_called
        # Clock.schedule_once(app.stop_app)
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        Clock.tick()
        assert app.on_stop_called

    def test_on_stop_with_stop_touch_app(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_stop_called
        Clock.schedule_once(lambda dt: stopTouchApp())
        app.run_app()
        Clock.tick()
        assert app.on_stop_called

    def test_on_user_preferences_open_enabling_debug(self, restore_app_env):
        app = KivyAppTest()

        app.debug_level = DEBUG_LEVEL_ENABLED
        assert app._debug_enable_clicks == 0
        assert not app.on_user_preferences_open('', {})

        app.debug_level = DEBUG_LEVEL_DISABLED
        assert not app.on_user_preferences_open('', {})
        assert not app.on_user_preferences_open('', {})
        assert not app.on_user_preferences_open('', {})
        assert app.debug_level == DEBUG_LEVEL_ENABLED

        app.debug_level = DEBUG_LEVEL_DISABLED
        assert not app.on_user_preferences_open('', {})
        assert app._debug_enable_clicks == 1
        # using Clock.schedule_once(_delayed_test, 6.9) and the commented subfunction underneath -> get never executed:
        # def _delayed_test(dt: float):
        #     print("delayed test_on_user_preferences_open_enabling_debug after:", dt)
        #     assert app.debug_level == DEBUG_LEVEL_DISABLED
        #     assert app._debug_enable_clicks == 0
        started = Clock.time()
        while Clock.time() - started < 6.9:
            Clock.tick()
        assert app.debug_level == DEBUG_LEVEL_DISABLED
        assert app._debug_enable_clicks == 0

    def test_open_popup_basic(self, restore_app_env):
        app = KivyAppTest()
        called = False
        passed_pa = None

        class TestPopUp(Popup):
            """ popup test class """
            test_attr = BooleanProperty(False)

            @staticmethod
            def open(parent):
                """ open popup method """
                nonlocal called, passed_pa
                called = True
                passed_pa = parent

        # noinspection PyTypeChecker
        popup = app.open_popup(TestPopUp, test_attr=True)
        assert called
        assert hasattr(popup, 'test_attr')
        assert popup.test_attr is True

        # noinspection PyTypeChecker
        app.open_popup(TestPopUp, opener=popup, test_attr=True)
        assert passed_pa == popup

    def test_open_popup_like_android(self, restore_app_env):
        app = KivyAppTest()
        called = False
        passed_pa = None

        class TestPopUp(Popup):
            """ popup test class """
            test_attr = BooleanProperty(False)

            @staticmethod
            def open(parent):
                """ open popup method """
                nonlocal called, passed_pa
                called = True
                passed_pa = parent

        with patch('ae.kivy.apps.os_platform', return_value='android'):
            # noinspection PyTypeChecker
            popup = app.open_popup(TestPopUp, test_attr=True)
            assert called
            assert hasattr(popup, 'test_attr')
            assert popup.test_attr is True

            # noinspection PyTypeChecker
            app.open_popup(TestPopUp, opener=popup, test_attr=True)
            assert passed_pa == popup

    def test_retrieve_app_states(self, restore_app_env):
        app = KivyMainApp()
        assert app.retrieve_app_states() == {}

    def test_run(self, ini_file, restore_app_env):
        app = KivyAppTest()
        assert app.framework_app
        assert not app.on_run_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_run_called
        # assert app.framework_app.app_states == def_app_states
        assert app.on_start_called
        assert app.on_start_called > app.on_run_called

    def test_start(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_run_called
        assert not app.on_start_called
        assert not app.on_started_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_start_called
        assert app.on_started_called
        assert app.on_run_called < app.on_start_called < app.on_started_called


called_bound = False


def bound(*_args, **_kwargs):
    """ bound test func """
    global called_bound
    called_bound = True


@skip_gitlab_ci
class TestI18N:
    def test_get_txt_instance(self):
        assert callable(get_txt)
        assert hasattr(get_txt, 'switch_lang')
        assert isinstance(get_txt, Observable)

    def test_binding(self):
        assert not get_txt.observers
        get_txt.fbind('_', bound)
        assert len(get_txt.observers) == 1

        get_txt.fbind('any', bound)
        assert len(get_txt.observers) == 1

    def test_unbinding(self):
        assert len(get_txt.observers) == 1      # from the last test method
        get_txt.funbind('_', bound)
        assert not get_txt.observers

        get_txt.funbind('any', bound)
        assert not get_txt.observers

    def test_switch_lang(self, restore_app_env):
        KivyAppTest()  # switch_lang() needs framework app instance
        old_lang = default_language()
        get_txt.switch_lang('xx')
        assert default_language() == 'xx'
        default_language(old_lang)

    def test_translate(self):
        assert get_txt("text to translate") == "text to translate"

    def test_translate_with_count(self):
        assert get_txt("text with {count} to translate", count=69) == "text with 69 to translate"

    def test_update(self, restore_app_env):
        KivyAppTest()  # switch_lang() needs framework app instance
        get_txt.fbind('_', bound, ('arg0', ))
        assert not called_bound
        get_txt.switch_lang('yy')
        assert called_bound

    def test_on_lang_code_change(self, restore_app_env):
        app = KivyAppTest()

        app.on_lang_code_change('zz', {})
        assert default_language() == 'zz'
