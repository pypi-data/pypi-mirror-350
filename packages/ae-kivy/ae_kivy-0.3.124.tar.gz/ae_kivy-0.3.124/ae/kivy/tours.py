"""
ae.kivy.tours module
--------------------

this module provides the following classes to augment the user interface of your apps with animated product tours,
tutorials, walkthroughs and user onboarding/welcome features:

    * :class:`~ae.kivy.tours.AnimatedTourMixin`
    * :class:`~ae.kivy.tours.AnimatedOnboardingTour`
    * :class:`~ae.kivy.tours.TourOverlay`


the class :class:`~ae.kivy.tours.TourOverlay` is implementing an overlay layout widget to display the animations,
shaders, tour page texts, tooltip text and the navigation buttons of an active/running app tour.

the :class:`~ae.kivy.tours.AnimatedTourMixin` can be mixed-into a tour class that inherits from
:class:`~ae.gui.tours.TourBase` to extend it with animation and glsl shader features.

the class :class:`~ae.kivy.tours.AnimatedOnboardingTour` is based on :class:`~ae.gui.tours.OnboardingTour` and
:class:`~ae.kivy.tours.AnimatedTourMixin` to extend the generic app onboarding tour
class with animations. it provides a generic app onboarding tour that covers the core features that can be easily
extended with app-specific tour pages.

to integrate a more app-specific onboarding tour into your app, declare a class with a name composed by the name
of your app (:attr:`~ae.gui.app.MainAppBase.app_name`) in camel-case, followed by the suffix `'OnboardingTour'`.
"""
import traceback
from copy import deepcopy
from typing import Any, Callable, Optional, Type, Union

# noinspection PyProtectedMember
from kivy.animation import Animation, CompoundAnimation                                                 # type: ignore
from kivy.clock import Clock                                                                            # type: ignore
from kivy.core.window import Window                                                                     # type: ignore
from kivy.metrics import sp                                                                             # type: ignore
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty              # type: ignore
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior                                     # type: ignore
from kivy.uix.floatlayout import FloatLayout                                                            # type: ignore
from kivy.uix.textinput import TextInput                                                                # type: ignore
from kivy.uix.widget import Widget                                                                      # type: ignore

from ae.base import snake_to_camel                                                                      # type: ignore
from ae.dynamicod import try_eval                                                                       # type: ignore
from ae.gui.utils import REGISTERED_TOURS, help_id_tour_class                                           # type: ignore
from ae.gui.app import MainAppBase                                                                      # type: ignore
from ae.gui.tours import OnboardingTour, TourBase                                                       # type: ignore
from ae.kivy_glsl import ShaderIdType, ShadersMixin                                                     # type: ignore

from .behaviors import ModalBehavior
from .widgets import AbsolutePosSizeBinder


PageAnimationType = tuple[str, Union[Animation, str]]
""" tuple of a widget id string and an :class:`~kivy.animation.Animation` instance/evaluation-expression.

    if the first character of the widget id is a `@` then the :attr:`~kivy.animation.Animation.repeat` attribute of
    the :class:`~kivy.animation.Animation` instance will be set to True. the rest of the widget id string specifies
    the widget to be animated which is either:

    * one of the widgets of the :class:`TourOverlay` layout class, identified by the on of the following strings:
      `'next_but'`, `'page_lbl'`, `'tap_pointer'`, `'prev_but'`, `'title_lbl'`, `'tooltip'`, `'tour_page_texts'`.
    * the explained widget if an empty string is given.
    * the :class:`TourOverlay` layout class instance for any other string (e.g. `'layout'` or `'overlay'`).

    alternative to an animation instance, a evaluation string can be specified. these evaluations allow to use the
    following globals: :class:`~kivy.animation.Animation` (also abbreviated as `A`), :class:`~kivy.clock.Clock`,
    :attr:`~ae.gui.tours.TourBase.layout`, :attr:`~kivy.metrics.sp`, :class:`~kivy.core.window.Window` and a
    reference to the instance of this app tour via `tour`.
"""

PageAnimationsType = tuple[PageAnimationType, ...]  #: tuple of :data:`PageAnimationType` items

WidgetValues = dict[str, Union[list, tuple, dict, float]]
""" a key of this dict specifies the name, the dict value the value of a widget property/attribute. """


DEF_FADE_OUT_APP = 0.39                                             #: default of tour layout fade out app screen factor


def ani_start_check(ani: Animation, wid: Widget):                                                   # pragma: no cover
    """ start animation if needed, else skip animation start.

    :param ani:                 :class:`~kivy.animation.Animation` instance.
    :param wid:                 widget to start/skip the animation for.
    """
    for attr, value in ani.animated_properties.items():
        if getattr(wid, attr) != value:
            ani.start(wid)
            break


def animated_widget_values(wid: Widget, ani: Union[Animation, CompoundAnimation]) -> WidgetValues:  # pragma: no cover
    """ determine from a widget the attribute/property values animated/changed by an animation.

    :param wid:                 widget of which the animation property values will get retrieved.
    :param ani:                 :class:`~kivy.animation.Animation`/:class:`kivy.animation.CompoundAnimation` instance.
    :return:                    dict with widget property names and values.
    """
    wid_values = {}
    for key in ani.animated_properties.keys():
        wid_values[key] = getattr(wid, key)
    return wid_values


def restore_widget_values(wid: Widget, values: WidgetValues):                                       # pragma: no cover
    """ restore property values of a widget.

    :param wid:                 widget of which the animation property values will get restored.
    :param values:              attribute/property values to restore on the widget.
    """
    for attr, value in values.items():
        setattr(wid, attr, value)


class AnimatedTourMixin:                                                                            # pragma: no cover
    """ tour class mixin to add individual shaders to the tour layout and their child widgets. """
    # abstracts
    layout: Widget
    main_app: Any
    page_ids: list[str]
    page_idx: int
    setup_texts: Callable

    def __init__(self, main_app: MainAppBase) -> None:
        super().__init__(main_app)                                          # type: ignore

        self._added_animations: list[tuple[Widget, Animation, WidgetValues]] = []
        self._added_shaders: list[tuple[Widget, ShaderIdType]] = []
        self._explained_binder = AbsolutePosSizeBinder()

        self.pages_animations: dict[Optional[str], PageAnimationsType] = {}
        """ dict of compound animation instances of the pages of this tour.

        the key of this dict is the page id or None (for animations available in all pages of this tour).
        each value of this dict is of the type :data:`PageAnimationsType`.
        """

        self.pages_shaders: dict[Optional[str], tuple[tuple[str, ShaderIdType], ...]] = {}
        """ dict of widget shaders for the pages of this tour.

        the key of this dict is the page id or None (for shaders available in all pages of this tour).
        each value of this dict is a tuple of tuples of widget id and add_shader()-kwargs.

        the widget id string specifies the widget to which a shader will be added, which is either:

        * one of the widgets of the :class:`TourOverlay` layout class, identified by the on of the following strings:
          `'next_but'`, `'page_lbl'`, `'tap_pointer'`, `'prev_but'`, `'title_lbl'`, `'tooltip'`, `'tour_page_texts'`.
        * the explained widget if an empty string is given.
        * the :class:`TourOverlay` layout class instance for any other string (e.g. `'layout'` or `'overlay'`).

        before the add_shader()-kwargs dict will be passed to the :meth:`~ae.kivy_glsl.ShadersMixin.add_shader` method,
        all their non-string values, specifying as strings, will be evaluated/converted automatically. the evaluation
        provides the following globals: :attr:`~ae.gui.tours.TourBase.layout`, :attr:`~kivy.metrics.sp`,
        :class:`~kivy.clock.Clock`, :class:`~kivy.core.window.Window` and the `tour` instance.
        """

        self.switch_next_animations: dict[Optional[str], PageAnimationsType] = {}
        """ dict of compound animation instances for the next page switch transition of the pages of this tour.

        the key of this dict is the page id or None (for animations available in all pages of this tour).
        each value of this dict is of the type :data:`PageAnimationsType`.
        """

    def _add_animations(self, animations: PageAnimationsType):
        """ add animations to the tour page currently displayed in the tour layout/overlay.

        :param animations:      tuple of 2-element-tuples having widget id and animation instance/evaluation-string.
        :return:                length of the longest animation added (in seconds).
        """
        max_len = 0.0
        layout = self.layout
        added = []
        for wid_id, anim in animations:
            if isinstance(anim, str):
                glo_vars = self.main_app.global_variables(layout=layout, sp=sp, tour=self,
                                                          A=Animation, Animation=Animation, Clock=Clock, Window=Window)
                anim = try_eval(anim, glo_vars=glo_vars)

            if wid_id[0:1] == '@':
                wid_id = wid_id[1:]
                anim.repeat = True
            wid = layout.ids.get(wid_id, layout) if wid_id else layout.explained_widget
            start_values = animated_widget_values(wid, anim)
            anim.start(wid)
            added.append((wid, anim, start_values))

            max_len = max(max_len, anim.duration)

        self._added_animations.extend(added)

        return max_len

    def next_page(self):
        """ overridden to add demo animations before/on switch to the next tour page. """
        page_id = self.page_ids[self.page_idx]
        next_animations = self.switch_next_animations.get(None, ()) + self.switch_next_animations.get(page_id, ())
        anim_length = self._add_animations(next_animations)
        if anim_length:
            # noinspection PyUnresolvedReferences
            self.main_app.call_method_delayed(anim_length + 0.123, super().next_page)
        else:
            # noinspection PyUnresolvedReferences
            super().next_page()

    def setup_explained_widget(self) -> list:
        """ overridden to bind pos/size of explained widget(s) to the tour layout/overlay placeholder.

        :return:                list of explained widget instances.
        """
        self._explained_binder.unbind()

        # noinspection PyUnresolvedReferences
        widgets = super().setup_explained_widget()                          # type: ignore

        layout = self.layout
        exp_wid = layout.explained_widget
        self._explained_binder = ebi = AbsolutePosSizeBinder(*widgets, bind_window_size=True)
        ebi.size_to_attribute(layout, 'explained_size')
        ebi.pos_to_attribute(layout, 'explained_pos')
        if exp_wid is layout.ids.explained_placeholder:
            ebi.size_to_attribute(exp_wid, 'size')
            ebi.pos_to_attribute(exp_wid, 'pos')

        return widgets

    def setup_page_shaders_and_animations(self):
        """ set up shaders and animations of the current page.

        specified in :attr:`~AnimatedTourMixin.pages_shaders` and :attr:`~AnimatedTourMixin.pages_animations`.
        """
        def _evaluated_shader_kwargs() -> dict:
            tour_shader_kwargs = deepcopy(shader_kwargs)    # pylint: disable=undefined-loop-variable
            glo_vars = self.main_app.global_variables(layout=layout, sp=sp, tour=self, Clock=Clock, Window=Window)
            for key, arg in tour_shader_kwargs.items():
                if isinstance(arg, str) and key not in ('add_to', 'render_shape', 'shader_code', 'shader_file'):
                    tour_shader_kwargs[key] = try_eval(arg, glo_vars=glo_vars)
            return tour_shader_kwargs

        page_id = self.page_ids[self.page_idx]
        page_shaders = self.pages_shaders.get(None, ()) + self.pages_shaders.get(page_id, ())
        layout = self.layout
        added = []
        for wid_id, shader_kwargs in page_shaders:
            wid = layout.ids.get(wid_id, layout) if wid_id else layout.explained_widget
            added.append((wid, wid.add_shader(**_evaluated_shader_kwargs())))
        self._added_shaders = added

        self._add_animations(self.pages_animations.get(None, ()) + self.pages_animations.get(page_id, ()))

    def setup_layout(self):
        """ overridden to set up animations and shaders of the current tour page. """
        # noinspection PyUnresolvedReferences
        super().setup_layout()
        Clock.tick()                # update position of the explained widget
        self.setup_page_shaders_and_animations()

    def simulate_text_input(self, text_input: TextInput, text_to_delay: str,
                            text_to_insert: str = "", deltas: tuple[float, ...] = (1.8, 0.6, 0.3)):
        """ simulate the typing of texts by a user entered into an explained TextInput widget of a tour page.

        :param text_input:      text input widget, either of type :class:`~kivy.textinput.TextInput` or
                                :class:`~ae.kivy.widgets.FlowInput`.
        :param text_to_delay:   text string to be inserted delayed by the seconds specified in deltas[0].
        :param text_to_insert:  text string to be inserted directly into the passed text input widget.
        :param deltas:          delay deltas in seconds between each character to simulate text inputted by a user.
                                the first delta default is a bit higher to finish navigation button y-pos-animation.
        """
        if text_input.get_root_window():
            for char_to_insert in text_to_insert:
                if text_input.interesting_keys.get(ord(char_to_insert), None) == 'backspace':   # chr(8)
                    text_input.do_backspace()
                else:
                    text_input.insert_text(char_to_insert)

            if text_to_delay:
                next_delay = deltas[0]
                self.main_app.call_method_delayed(next_delay, self.simulate_text_input, text_input, text_to_delay[1:],
                                                  text_to_insert=text_to_delay[0], deltas=deltas[1:] + (next_delay, ))

    def tap_animation(self, wid_id: str = '', pos_delay: float = 2.34,
                      press_delay: float = 0.69, release_delay: float = 0.39) -> PageAnimationType:
        """ create a compound animation instance simulating a user touch/tap on the specified widget.

        :param wid_id:          specifies the widget to be tap simulated: either a widget id string (first item of the
                                :data:`PageAnimationType` tuple), or (if prefixed with a column character) tap/focus/
                                state id of a widget, or an empty string (specifies the currently explained widget).
        :param pos_delay:       time in seconds to position/move the pointer from the next button to the widget.
        :param press_delay:     time in seconds of the button press simulation animation.
        :param release_delay:   time in seconds of the button release simulation animation.
        :return:                compound animation instance simulating a tap.

        .. note:: use as animation evaluation expression to get the widget values on setup-time of the page (not tour).
        """
        layout = self.layout
        if wid_id[0:1] == ':':
            tap_wid = self.main_app.widget_by_flow_id(wid_id[1:])
        else:
            tap_wid = layout.ids.get(wid_id, layout) if wid_id else layout.explained_widget
        tap_wid_x, tap_wid_y = tap_wid.to_window(*tap_wid.center)
        nxt_wid = layout.ids.next_but
        poi_wid = layout.ids.tap_pointer
        poi_w, poi_h = poi_wid.size
        poi_x = tap_wid_x - poi_w * 13.0 / 30.0    # - tap_pointer.png index finger x position offset
        poi_y = tap_wid_y - poi_h * 29.0 / 30.0

        poi_wid.center = nxt_wid.center
        ani = Animation(x=poi_x, y=poi_y, width=poi_w, height=poi_h, opacity=1.0, d=pos_delay, t='in_sine') \
            + Animation(x=poi_x + poi_w * 0.156, y=poi_y + poi_h * 0.153,
                        width=poi_w * 0.69, height=poi_h * 0.69, d=press_delay, t='out_sine')
        poi_values = animated_widget_values(poi_wid, ani)

        if isinstance(tap_wid, ButtonBehavior):
            release_ani = Animation(x=poi_x, y=poi_y, width=poi_w, height=poi_h, opacity=0.39, d=release_delay - 0.03)

            def _touched_anim():
                wid_state = tap_wid.state
                tap_wid.state = 'normal' if wid_state == 'down' else 'down'
                if not isinstance(tap_wid, ToggleButtonBehavior):
                    release_ani.start(poi_wid)
                    self.main_app.call_method_delayed(
                        release_delay, lambda *_args: (setattr(tap_wid, 'state', wid_state), self.setup_texts()))

            ani.bind(on_complete=lambda *_args: (_touched_anim(), self.setup_texts()))
            release_ani.bind(on_complete=lambda *_args: restore_widget_values(poi_wid, poi_values))

        return ani

    def teardown_shaders_and_animations(self):
        """ tear down all added shaders and animations of the current tour page (including switch next page ani). """
        for wid, anim, start_values in reversed(self._added_animations):
            anim.stop(wid)
            restore_widget_values(wid, start_values)
        self._added_animations = []

        for wid, shader_id in reversed(self._added_shaders):
            wid.del_shader(shader_id)
        self._added_shaders = []

    def teardown_app_flow(self):
        """ overridden to tear down the animations of the current/last-shown tour page. """
        self.teardown_shaders_and_animations()
        # noinspection PyUnresolvedReferences
        super().teardown_app_flow()


class AnimatedOnboardingTour(AnimatedTourMixin, OnboardingTour):                                    # pragma: no cover
    """ onboarding tour, extended with animations and glsl shaders. """
    def __init__(self, main_app: MainAppBase) -> None:
        super().__init__(main_app)

        self._bound = None

        self.pages_animations.update({
            None: (
                ('@root',
                 Animation(ani_value=0.999, t='in_out_sine', d=30) + Animation(ani_value=0.0, t='in_out_sine', d=9)),
            ),
            '': (
                ('next_but',
                 "A(font_size=layout.font_height, t='in_out_sine', d=24) + "
                 "A(font_size=layout.main_app.framework_app.min_font_size, t='in_out_sine', d=3) + "
                 "A(font_size=layout.main_app.framework_app.max_font_size, t='in_out_sine', d=6) + "
                 "A(font_size=layout.font_height, t='in_out_sine', d=3)"),
            ),
            'layout_font_size': (
                ('@',
                 "A(value=min(layout.main_app.font_size * 1.5, layout.main_app.framework_app.max_font_size),"
                 "  t='in_out_sine', d=12.9) + "
                 "A(value=max(layout.main_app.font_size * 0.6, layout.main_app.framework_app.min_font_size),"
                 "  t='in_out_sine', d=4.2)"),
            )
        })

        self.pages_shaders.update({
            '': (
                ('layout', {'alpha': "lambda: 0.39 * layout.ani_value",
                            'center_pos': "lambda: list(map(float, layout.ids.next_but.center))",
                            'shader_code': "=plunge_waves", 'time': "lambda: -Clock.get_boottime()",
                            'tint_ink': [0.21, 0.39, 0.09, 0.9]}),
                ('tour_page_texts', {'add_to': 'before'}),
                ('next_but',
                 {'add_to': 'before', 'alpha': "lambda: 0.3 + layout.ani_value / 3", 'render_shape': 'Ellipse',
                  'shader_code': '=plunge_waves'}),
            ),
            'page_switching': (
                ('layout', {'alpha': "lambda: 0.39 * layout.ani_value",
                            'center_pos': "lambda: list(map(float, layout.ids.prev_but.center))",
                            'shader_code': "=plunge_waves", 'time': "lambda: -Clock.get_boottime()",
                            'tint_ink': [0.21, 0.39, 0.09, 0.9]}),
                ('tour_page_texts', {'add_to': 'before'}),
                ('prev_but',
                 {'add_to': 'before', 'alpha': "lambda: 0.12 + layout.ani_value / 3", 'render_shape': 'Ellipse',
                  'shader_code': '=plunge_waves', 'time': "lambda: -Clock.get_boottime()"}),
            ),
            'tip_help_intro': (
                ('tour_page_texts', {'add_to': 'before', 'alpha': "lambda: 0.12 + layout.ani_value / 3",
                                     'render_shape': 'RoundedRectangle', 'shader_code': '=worm_whole',
                                     'tint_ink': [0.021, 0.039, 0.009, 0.9]}),
                ('prev_but',
                 {'add_to': 'before', 'alpha': "lambda: 0.12 + layout.ani_value / 3", 'render_shape': 'Ellipse',
                  'shader_code': '=worm_whole', 'time': "lambda: -Clock.get_boottime()"}),
                ('next_but',
                 {'add_to': 'before', 'alpha': "lambda: 0.12 + layout.ani_value / 3", 'render_shape': 'Ellipse',
                  'shader_code': '=worm_whole'}),
            ),
            'tip_help_tooltip': (
                ('prev_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=fire_storm',
                              'tint_ink': [0.81, 0.39, 0.09, 0.39], 'time': "lambda: -Clock.get_boottime()"}),
                ('next_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=fire_storm',
                              'tint_ink': [0.03, 0.03, 0.9, 0.39]}),
            ),
            'responsible_layout': (
                ('prev_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=colored_smoke',
                              'time': "lambda: -Clock.get_boottime()"}),
                ('next_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=colored_smoke'}),
            ),
            'layout_font_size': (
                ('prev_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=circled_alpha',
                              'tint_ink': [0.51, 0.39, 0.9, 0.999]}),
                ('next_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'shader_code': '=circled_alpha',
                              'tint_ink': [0.81, 0.39, 0.9, 0.999]}),
            ),
            'tour_end': (
                ('tour_page_texts', {'add_to': 'before'}),
                ('prev_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'tint_ink': [0.51, 0.39, 0.9, 0.999],
                              'time': "lambda: -Clock.get_boottime()"}),
                ('next_but', {'add_to': 'before', 'render_shape': 'Ellipse', 'tint_ink': [0.81, 0.39, 0.9, 0.999]}),
            ),
        })

    def next_page(self):
        """ overriding to remove the next button size animation only visible in the first tour after app re/start. """
        layout = self.layout
        layout.ani_value = 0.0
        super().next_page()
        if self.last_page_id == '' and self.pages_animations.pop('', False):
            Animation(font_size=layout.font_height).start(layout.ids.next_but)  # set font size back to the original val

    def setup_layout(self):
        """ overridden to update layout texts if app window/screen orientation (app.landscape) changes. """
        super().setup_layout()
        page_id = self.page_ids[self.page_idx]
        if page_id == 'responsible_layout':
            self._bound = self.main_app.framework_app.fbind('landscape', lambda *_args: self.setup_texts())
        elif page_id == 'layout_font_size':
            self._bound = self._added_animations[-1][1].fbind('on_progress', lambda *_args: self.setup_texts())

    def teardown_shaders_and_animations(self):
        """ overridden to unbind setup_texts() on leaving the responsible_layout tour page. """
        if self._bound:
            page_id = self.page_ids[self.page_idx]
            if page_id == 'responsible_layout':
                self.main_app.framework_app.unbind_uid('landscape', self._bound)
            elif page_id == 'layout_font_size':
                # noinspection PyUnresolvedReferences
                self._added_animations[-1][1].unbind_uid('on_progress', self._bound)
            self._bound = None

        super().teardown_shaders_and_animations()


class TourOverlay(ModalBehavior, ShadersMixin, FloatLayout):                                        # pragma: no cover
    """ tour layout/view overlay singleton class to display an active/running modal app tour with optional glsl shaders.
    """
    ani_value = NumericProperty()
    """ animated float value between 0.0 and 1.0, used e.g. by :attr:`AnimatedTourMixin.pages_animations`.

    :attr:`ani_value` is a :class:`~kivy.properties.NumericProperty` and is read-only.
    """

    explained_pos = ListProperty([-9, -9])
    """ window position (absolute x, y window coordinates) of the targeted/explained/highlighted widget.

    :attr:`explained_pos` is a :class:`~kivy.properties.ListProperty` and is read-only.
    """

    explained_size = ListProperty([0, 0])
    """ widget size (width, height) of the targeted/explained/highlighted widget.

    :attr:`explained_size` is a :class:`~kivy.properties.ListProperty` and is read-only.
    """

    explained_widget = ObjectProperty()
    """ explained widget instance on actual tour (page).

    :attr:`explained_widget` is a :class:`~kivy.properties.ObjectProperty` and is read-only.
    """

    fade_out_app = NumericProperty(DEF_FADE_OUT_APP)
    """ fade out app screen factor: 0.0 prevents fade out of the areas around TourPageTexts and the explained widget.

    1.0 results in maximum app screen fade out. configurable for individual tour page via `page_data['fade_out_app']`.

    :attr:`fade_out_app` is a :class:`~kivy.properties.NumericProperty` and defaults to 0.39.
    """

    label_height = NumericProperty()
    """ height in pixels of the page text labels and text lines.

    :attr:`label_height` is a :class:`~kivy.properties.NumericProperty` and is read-only.
    """

    navigation_disabled = BooleanProperty()
    """ if this flag is True then the back/next buttons in the tour layout/overlay are disabled.

    :attr:`navigation_disabled` is a :class:`~kivy.properties.BooleanProperty` and is read-only.
    """

    tour_instance = ObjectProperty()
    """ holding the :class:`~ae.gui.tours.TourBase` instance of the current tour, initialized by :meth:`.start_tour`.

    :attr:`tour_instance` is a :class:`~kivy.properties.ObjectProperty` and is read-only.
    """

    def __init__(self, main_app: MainAppBase, tour_class: Optional[Type[TourBase]] = None, **kwargs):
        """ prepare app and tour overlay (singleton instance of this class) to start tour.

        :param main_app:        main app instance.
        :param tour_class:      optional tour (pages) class, default: tour class of current help id or OnboardingTour.
        """
        self.main_app = main_app
        main_app.vpo("TourOverlay.__init__")

        self._tooltip_animation = None
        self.auto_dismiss = False
        self.explained_widget = main_app.help_activator             # assign a fake init widget to prevent None errors

        super().__init__(**kwargs)

        if main_app.help_layout:
            main_app.help_activation_toggle()                       # deactivate help mode if activated

        self.start_tour(tour_class)

    def next_page(self):
        """ switch to the next tour page. """
        self.main_app.vpo("TourOverlay.next_page")
        self.navigation_disabled = True
        self.tour_instance.cancel_auto_page_switch_request()
        self.tour_instance.next_page()

    def on_navigation_disabled(self, *_args):
        """ handle the navigation button disable change event to hide page texts (blend-in-anim in page_updated()). """
        if self.navigation_disabled:
            ani = Animation(opacity=0.123, d=0.6)
            ids = self.ids
            ani_start_check(ani, ids.tour_page_texts)
            ani_start_check(ani, ids.prev_but)
            ani_start_check(ani, ids.next_but)
            ani_start_check(ani, ids.stop_but)

    def page_updated(self):
        """ callback from :meth:`~TourBase.setup_layout` for UI-specific patches, after tour layout/overlay setup. """
        tooltip = self.ids.tooltip
        win_height = Window.height
        nav_y = self.label_height * 1.29    # default pos_y of navigation bar with prev/next buttons
        if self.main_app.widget_visible(tooltip):
            exp_y = self.explained_pos[1]
            pos1 = min(exp_y, tooltip.y)
            pos2 = max(exp_y + self.explained_size[1], tooltip.top)
            if pos1 < win_height - pos2:
                nav_y = max(nav_y + pos2, win_height - self.ids.tour_page_texts.height)

        ani_kwargs = {'t': 'in_out_sine', 'd': 2.1}
        ani_start_check(Animation(fade_out_app=self.tour_instance.page_data.get('fade_out_app', DEF_FADE_OUT_APP),
                                  navigation_pos_hint_y=nav_y / win_height,
                                  **ani_kwargs),
                        self)
        ani = Animation(opacity=1.0, **ani_kwargs)
        ani_start_check(ani, self.ids.tour_page_texts)
        ani_start_check(ani, self.ids.prev_but)
        ani_start_check(ani, self.ids.next_but)
        ani_start_check(ani, self.ids.stop_but)

        self.navigation_disabled = False

    def prev_page(self):
        """ switch to the previous tour page. """
        self.main_app.vpo("TourOverlay.prev_page")
        self.navigation_disabled = True
        self.tour_instance.cancel_auto_page_switch_request()
        self.tour_instance.prev_page()

    def start_tour(self, tour_cls: Optional[Type[TourBase]] = None) -> bool:
        """ reset app state and prepare tour to start.

        :param tour_cls:        optional tour (pages) class, default: tour of currently shown help id or OnboardingTour.
        :return:                a boolean True value if tour exists and got started, else False.
        """
        main_app = self.main_app
        if not tour_cls:
            tour_cls = help_id_tour_class(main_app.displayed_help_id) \
                or REGISTERED_TOURS.get(snake_to_camel(main_app.app_name) + 'OnboardingTour') \
                or AnimatedOnboardingTour
        main_app.vpo(f"TourOverlay.start_tour tour_cls={tour_cls.__name__}")

        try:
            main_app.change_observable('tour_layout', self)             # set tour layout
            # noinspection PyArgumentList
            self.tour_instance = tour_instance = tour_cls(main_app)     # initialize tour instance
            tour_instance.start()                                       # start tour
            main_app.help_activator.ani_start()
        except Exception as ex:                                         # pylint: disable=broad-exception-caught
            main_app.po(f"TourOverlay.start_tour exception {ex}")
            traceback.print_exc()
            main_app.help_activator.ani_stop()
            main_app.change_observable('tour_layout', None)             # reset tour layout
            return False

        ani = Animation(ani_value=0.3, t='in_out_sine', d=6) + Animation(ani_value=0.999, t='in_out_sine', d=3)
        ani.repeat = True
        ani.start(self.ids.tooltip)
        self._tooltip_animation = ani

        self.activate_esc_key_close()
        self.activate_modal()

        return True

    def stop_tour(self):
        """ stop tour and restore the initially backed-up app state. """
        main_app = self.main_app
        main_app.vpo("TourOverlay.stop_tour")

        self.navigation_disabled = True

        if self._tooltip_animation:
            self._tooltip_animation.stop(self.ids.tooltip)

        if self.tour_instance:
            self.tour_instance.stop()
        else:
            main_app.po("TourOverlay.stop_tour error: called without tour instance")

        main_app.help_activator.ani_stop()
        main_app.change_observable('tour_layout', None)    # set app./main_app.tour_layout to None

        self.deactivate_esc_key_close()
        self.deactivate_modal()
