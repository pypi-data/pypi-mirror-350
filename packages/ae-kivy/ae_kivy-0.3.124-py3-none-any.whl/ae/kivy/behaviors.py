"""
ae.kivy.behaviors module
------------------------

this module provides the following behavior classes:

    * :class:`~ae.kivy.behaviors.HelpBehavior` extends and prepares any Kivy widget to show an
      individual help text for it.
    * :class:`~ae.kivy.behaviors.ModalBehavior` is a generic mix-in class that provides modal behavior to any container
      widget.
    * :class:`~ae.kivy.behaviors.SlideSelectBehavior`: quickly navigate in elliptically shaped sub-/menus, alternatively
      starting with a long touch, then slide to the menu item to select and release.
    * :class:`~ae.kivy.behaviors.TouchableBehavior`: extends toggle-/touch-behavior of
      :class:`~kivy.uix.behaviors.ButtonBehavior`.


help behavior mixin
^^^^^^^^^^^^^^^^^^^

to show an i18n translatable help text for a Kivy widget, create a subclass of the widget and add the
mixin-/behavior-class :class:`~ae.kivy.behavior.HelpBehavior`. the following example is attaching a help text to the
Kivy :class:`~kivy.uix.button.Button` widget::

    from kivy.uix.button import Button
    from ae.kivy.widgets import HelpBehavior

    class ButtonWithHelpText(HelpBehavior, Button):
        ...

alternatively, you can archive this via the definition of a new kv-lang rule, like shown underneath::

    <ButtonWithHelpText@HelpBehavior+Button>

.. note::
    to automatically lock and mark the widget you want to add help texts for, this mixin class has to be specified
    as the first inheriting class in the class or rule declaration.


modal behavior mixin
^^^^^^^^^^^^^^^^^^^^

to convert a container widget into a modal dialog, add the :class:`~ae.kivy.behaviors.ModalBehavior` mix-in class,
provided by this ae namespace portion.

the following code snippet demonstrates a typical implementation::

    class MyContainer(ModalBehavior, BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def open(self):
            self.activate_esc_key_close()
            self.activate_modal()

        def close(self):
            self.deactivate_esc_key_close()
            self.deactivate_modal()


calling the method :meth:`~ae.kivy.behaviors.ModalBehavior.activate_esc_key_close` in the `open` method of a container
class allows the user to close the popup by pressing the Escape key (or Back on Android). this optional feature can
be reverted by calling the :meth:`~ae.kivy.behaviors.ModalBehavior.deactivate_esc_key_close` method in your
`close` method.

to additionally activate the modal mode, call the method :meth:`~ae.kivy.behaviors.ModalBehavior.activate_modal`.
the modal mode can be deactivated by calling the :meth:`~ae.kivy.behaviors.ModalBehavior.deactivate_modal` method.

after activating the modal mode, most of the user interactions (like touches, or mouse and keyboard events) will be
consumed or filtered. therefore, it is recommended to also visually change the GUI while in the modal mode, which
has to be implemented by the mixing-in container widget.

.. hint::
    usage examples of the :class:`~ae.kivy.behaviors.ModalBehavior` mix-in are e.g., the classes
    :class:`~ae.kivy.tours.TourOverlay` and :class:`~ae.kivy.widgets.FlowPopup`.

"""
from functools import partial
from typing import Any, Callable, Optional, Union

from kivy.animation import Animation                                                                    # type: ignore
from kivy.app import App                                                                                # type: ignore
from kivy.clock import Clock                                                                            # type: ignore
from kivy.core.window import Window                                                                     # type: ignore
from kivy.graphics import Ellipse                                                                       # type: ignore
from kivy.input import MotionEvent                                                                      # type: ignore
from kivy.properties import (                                                                           # type: ignore
    BooleanProperty, DictProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.dropdown import DropDown                                                                  # type: ignore
from kivy.uix.widget import Widget                                                                      # type: ignore

from ae.base import stack_var                                                                           # type: ignore
from ae.gui.app import MainAppBase                                                                      # type: ignore
from ae.gui.utils import flow_action                                                                    # type: ignore
from ae.kivy_glsl import ShaderIdType                                                                   # type: ignore


TOUCH_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.06, 0.03, 0.03)
""" very short/~0.3s vibrate pattern for button and toggler touch. """


def grab_touch(touch: MotionEvent, widget: Widget, exclusive: bool = False, main_app: Optional[MainAppBase] = None
               ) -> bool:
    """ temporal helper function to debug occasionally happening exclusive grab conflicts """
    if not main_app:
        main_app = App.get_running_app().main_app

    wid_info = repr(widget)
    if widget != (caller := stack_var('self')):
        wid_info += f" via {caller=}"

    try:
        main_app.vpo(f"grab_touch: {exclusive=} {wid_info=} {touch=}")
        touch.grab(widget, exclusive=exclusive)
        return True

    except Exception as exception:
        main_app.po(f"grab_touch FAILED with {exception=} for {exclusive=} {wid_info=} {touch=}")

    return False


class HelpBehavior:
    """ behavior mixin class for widgets providing help texts. """
    help_id = StringProperty()
    """ unique help id of the widget.

    The correct identification of each help-aware widget presuppose that the attribute :attr:`~HelpBehavior.help_id` has
    a unique value for each widget instance. This is done automatically for the widgets provided by the module
    :mod:`ae.kivy.widgets` by converting the app flow or app state of these widgets into a help id (see e.g. the
    implementation of the class :class:`~ae.kivy.widgets.FlowButton`).

    :attr:`help_id` is a :class:`~kivy.properties.StringProperty` and defaults to an empty string.
    """

    help_lock = BooleanProperty(False)
    """ this property is True if the help mode is active and this widget is not the help target.

    :attr:`help_lock` is a :class:`~kivy.properties.BooleanProperty` and defaults to the value `False`.
    """

    help_vars = DictProperty()
    """ dict of extra data to displayed/render the help text of this widget.

    The :attr:`~HelpBehavior.help_vars` is a dict which can be used to provide extra context data to dynamically
    generate, translate and display individual help texts.

    :attr:`help_vars` is a :class:`~kivy.properties.DictProperty` and defaults to an empty dict.
    """

    _shader_args = ObjectProperty()     #: shader internal data / id

    # abstract attributes and methods provided by the class to be mixed into
    collide_point: Callable

    def on_touch_down(self, touch: MotionEvent) -> bool:                                    # pragma: no cover
        """ prevent any processing if touch is done on the help activator widget or in active help mode.

        :param touch:           motion/touch event data.
        :return:                a boolean True value if the event got processed/used, else False.
        """
        main_app = App.get_running_app().main_app

        if main_app.help_activator.collide_point(*touch.pos):
            return False        # allow the help activator button to process this touch-down event

        if self.help_lock and self.collide_point(*touch.pos) and main_app.help_display(self.help_id, self.help_vars):
            return True         # main_app.help_layout is not None

        return super().on_touch_down(touch)                 # type: ignore # pylint: disable=no-member


class ModalBehavior:                                                                                # pragma: no cover
    """ mix-in to allow close on press of the Escape/Back key, to optionally provide a modal mode to a container widget.

    to make the container widget's modal state more obvious, add in your container widget an overlay color with an
    alpha between 0.3 and 0.9, together with the following canvas instructions:

        canvas:
            Color:
                rgba: root.my_overlay_color[:3] + [root.my_overlay_color[3] if self.is_modal else 0]
            Rectangle:
                size: Window.size if self.is_modal else (0, 0)

    two rectangles will be needed to not overlay/fade-out the help activator button::

        canvas:
            Color:
                rgba: self.my_overlay_color[:3] + [self.my_overlay_color[-1] if self.is_modal else 0]
            Rectangle:
                size:
                    Window.width if self.is_modal else 0, \
                    Window.height - app.main_app.help_activator.height if self.is_modal else 0
            Rectangle:
                pos: app.main_app.help_activator.right, app.main_app.help_activator.y
                size:
                    Window.width - app.main_app.help_activator.width if self.is_modal else 0, \
                    app.main_app.help_activator.height

    """
    # abstracts provided by Kivy's :class:`~kivy.uix.widget.Widget` class or by the mixing-in container widget class.
    center: list                #: center position of :class:`~kivy.uix.widget.Widget`
    close: Callable             #: method to dismiss the container widget (provided by self/container-widget)
    collide_point: Callable     #: method to detect collisions with other widgets of :class:`~kivy.uix.widget.Widget`
    disabled: bool              #: disabled property of :class:`~kivy.uix.widget.Widget`
    fbind: Callable             #: fast binding method of :class:`~kivy.uix.widget.Widget`
    funbind: Callable           #: fast unbinding method of :class:`~kivy.uix.widget.Widget`
    unbind_uid: Callable        #: the faster unbinding method of :class:`~kivy.uix.widget.Widget`

    auto_dismiss = BooleanProperty()
    """ determines if the container is automatically dismissed when the user hits the Esc/Back key or clicks outside it.

    :attr:`auto_dismiss` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    """

    is_modal = BooleanProperty(defaultvalue=False)
    """ flag if modal mode is active. use :meth:`.activate_modal` and :meth:`.deactivate_modal` to change this value.

    :attr:`is_modal` is a :class:`~kivy.properties.BooleanProperty` and defaults to False.
    """

    _center_aligned: bool = False                           #: True if self will be repositioned to the Window center
    _fast_bound_center_uid: int = 0                         #: fbind/unbind_uid of the center property (pos and size)
    _touch_started_inside: Optional[bool] = None            #: flag if touch started inside this widget or group

    def _align_center(self, *_args):
        """ reposition the container to the center of the app window.

        :param _args:           unused (passed only on bound window resize events)
        """
        if self._center_aligned and self.is_modal:
            self.center = Window.center

    def _on_key_down(self, _window, key, _scancode, _codepoint, _modifiers) -> Optional[bool]:
        """ close/dismiss this popup if back/Esc key get pressed - allowing stacking with DropDown/FlowDropDown. """
        if key == 27 and self.auto_dismiss and self.is_modal:
            if not App.get_running_app().tour_layout:   # prevent close/dismiss by the Esc key if an app tour is active
                self.close()
            return True
        return None

    def activate_esc_key_close(self):
        """ activate the key press handler, calling self.close() if Escape/Back key get pressed. """
        Window.bind(on_key_down=self._on_key_down)

    def activate_modal(self, align_center: bool = True):
        """ activate or renew modal mode for the mixing-in container widget.

        :param align_center:    pass False to prevent the automatic alignment of :attr:`~kivy.uix.widget.Widget.center`
                                to :attr:`~kivy.core.window.Window.center` on reposition or resize of self
                                or on resize of :class:`~kivy.core.window.Window`.
        """
        self.deactivate_modal()

        Window.add_widget(self)

        if align_center:
            Window.bind(on_resize=self._align_center)
            self._center_aligned = align_center
            # binding center includes a notification event on change of :attr:`~kivy.uix.widget.Widget.pos` and `size`
            self._fast_bound_center_uid = self.fbind('center', self._align_center)

        self.is_modal = True

    def deactivate_esc_key_close(self):
        """ deactivate the keyboard event handler, activated via :meth:`.activate_esc_key_close`. """
        Window.unbind(on_key_down=self._on_key_down)

    def deactivate_modal(self):
        """ deactivate modal mode for the mixing-in container. """
        if self._fast_bound_center_uid:
            self.unbind_uid('center', self._fast_bound_center_uid)
            Window.unbind(on_resize=self._align_center)
            self._fast_bound_center_uid = 0

        if self._center_aligned:
            Window.unbind(on_resize=self._align_center)
            self._center_aligned = False

        if self.is_modal:
            Window.remove_widget(self)
        self.is_modal = False

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ a touch-down event handler prevents the processing of a touch on the help activator widget by this popup.

        :param touch:           motion/touch event data.
        :return:                a boolean True value if the event got processed/used, else False.
        """
        self._touch_started_inside = self.touch_pos_is_inside(touch.pos)

        if App.get_running_app().main_app.help_activator.collide_point(*touch.pos):
            return False  # allow the help activator button to process this touch-down event
            # .. and leave self._touch_started_inside == None to not initiate popup.close/dismiss in on_touch_up

        if self.disabled if self._touch_started_inside else self.auto_dismiss:
            return self.is_modal

        return super().on_touch_down(touch)    # type: ignore # pylint: disable=no-member

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ touch move event handler. """
        if self.disabled if self._touch_started_inside else self.auto_dismiss:
            return self.is_modal

        # noinspection PyUnresolvedReferences
        return super().on_touch_move(touch)    # type: ignore # pylint: disable=no-member

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ touch up event handler. """
        if self.auto_dismiss and self._touch_started_inside is False:
            self.close(touch)
            ret = True
        else:
            # noinspection PyUnresolvedReferences
            ret = super().on_touch_up(touch)      # type: ignore # pylint: disable=no-member
        self._touch_started_inside = None
        return ret

    def touch_pos_is_inside(self, pos: list[float]) -> bool:
        """ check if the touch pos is inside this widget or a group of sub-widgets.

        :param pos:             touch position (x, y) in window coordinates.
        :return:                a boolean value True if this widget or group processes a touch event at the touch
                                position specified in the :paramref:`~touch_pos_is_inside.pos` argument.
        """
        return self.collide_point(*pos)


class SlideSelectBehavior:                                                                        # pragma: no cover
    """ quickly navigate in sub-/menus, starting with a long touch, then slide to the menu item to select and release.

    the slide-select feature of this class allows quicker selections of any menu item, by opening any popup via the
    :meth:`~ae.kivy.behaviors.TouchableBehavior.on_long_tap` event, then move the pointer/finger onto the menu item to
    select to finally release the touch. to enable this feature, specify the touch event in the `touch_event` key of the
    `popup_kwargs` dict in the :meth:`~ae.gui.app.MainAppBase.change_flow` call, e.g., by adding the following lines in
    your kv code onto the :class:`~ae.kivy.widgets.FlowButton`/:class:`~ae.kivy.widgets.FlowToggler` that is opening
    the popup::

        on_long_tap:
            app.main_app.change_flow(id_of_flow('open', 'my_menu'),
            **update_tap_kwargs(self, popup_kwargs=dict(touch_event=args[1])))

    .. note::
        has to be inherited (to be in the MRO) before :class:`~kivy.uix.behaviors.ButtonBehavior`, respectively
        :class:`~kivy.uix.behaviors.ToggleButtonBehavior`, for the touch event gets grabbed properly.
    """
    # abstracts of mixing-in class; e.g., from :class:`~kivy.widget.Widget`, :class:`~ae.kivy_glsl.ShadersMixin`,
    # :class:`~kivy.uix.dropdown.DropDown` and :class:`~kivy.uix.behaviors.ButtonBehavior`.
    attach_to: Optional[Widget]
    close: Callable
    collide_point: Callable
    dispatch: Callable
    to_widget: Callable

    def __init__(self, **kwargs):
        """ set normal pressed state shader on widget initialization. """
        self._layout_finished: bool = True
        self._opened_item: Optional[Widget] = None
        self._touch_moved_outside: bool = False
        self.main_app = App.get_running_app().main_app

        # noinspection PyUnresolvedReferences
        super().__init__(**kwargs)

    @staticmethod
    def _cancel_slide_select_closer(touch):
        slide_select_closer = touch.ud.pop('slide_select_closer', None)
        if slide_select_closer:
            Clock.unschedule(slide_select_closer)  # alternatively: slide_select_closer.cancel()

    @staticmethod
    def _cancel_slide_select_opener(touch):
        slide_select_opener = touch.ud.pop('slide_select_opener', None)
        if slide_select_opener:
            Clock.unschedule(slide_select_opener)  # alternatively: slide_select_opener.cancel()

    def _grab_and_open(self, touch: MotionEvent, item: Widget, first_close: Widget, *_args):
        if first_close:  # moved over another menu item of the parent menu then close
            touch.ungrab(first_close)
            first_close.close()  # the foremost submenu and open the sibling submenu instead

        if not self.main_app.change_flow(item.tap_flow_id, **item.tap_kwargs):
            return

        self._opened_item = item
        sub_menu = Window.children[0]           # the submenu just opened above via change_flow
        # touch.grab(sub_menu)
        grab_touch(touch, sub_menu, main_app=self.main_app)
        # allow dispatching of :meth:`ModalBehavior.on_touch_move` events for slide_select
        sub_menu._touch_started_inside = True   # pylint: disable=W0212

    @staticmethod
    def _ungrab_and_close(touch: MotionEvent, popup: Union[Widget, 'SlideSelectBehavior'], *_args):
        touch.ungrab(popup)
        # noinspection PyProtectedMember
        Window.children[1]._opened_item = None                  # pylint: disable=W0212
        popup.close()

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger moves.

        :param touch:           motion/touch event data.
        :return:                a boolean True value if the event got processed/used.
        """
        is_dropdown = isinstance(self, DropDown)
        opener: Optional[Widget] = self.attach_to if is_dropdown else self
        in_opener = opener and opener.collide_point(*touch.pos)
        if opener and not in_opener:
            opener._touch_moved_outside = True                  # pylint: disable=W0212

        # slide_select of menu-items/children of :class:`FlowDropDown`, :class:`FlowSelector` and :class:`FlowPopup`
        self._cancel_slide_select_closer(touch)
        self._cancel_slide_select_opener(touch)
        mnu_items = getattr(self, 'menu_items', None)
        if mnu_items and self._layout_finished:
            win_chi = Window.children[:2]
            foremost_popup = self is win_chi[0]

            if foremost_popup and in_opener and opener._touch_moved_outside:    # type: ignore # pylint: disable=W0212
                touch.ud['slide_select_closer'] = slide_select_closer = partial(self._ungrab_and_close, touch, self)
                Clock.schedule_once(slide_select_closer, 0.69)

            if self in win_chi:
                wid_pos = self.to_widget(*touch.pos)
                col_items = [item for item in mnu_items                 # pylint: disable=E1133
                             if item != self._opened_item
                             and item.collide_point(*wid_pos)
                             and flow_action(getattr(item, 'tap_flow_id', "")) == 'open']
                if len(col_items) == 1:  # single non-overlapping item found
                    touch.ud['slide_select_opener'] = slide_select_opener = partial(
                        self._grab_and_open, touch, col_items[0], None if foremost_popup else win_chi[0])
                    Clock.schedule_once(slide_select_opener, 0.39)
                    # return True # returning True prevents touch-initiated scrolls, e.g., in UserPrefs Colors dropdown

                elif foremost_popup:
                    widgets = mnu_items + [self.attach_to if is_dropdown else self]
                    min_x, min_y, width, height = self.main_app.widgets_enclosing_rectangle(widgets)
                    if not (min_x <= touch.x <= min_x + width and min_y <= touch.y <= min_y + height):
                        self._ungrab_and_close(touch, self)
                        return True

        # noinspection PyUnresolvedReferences
        return super().on_touch_move(touch)     # type: ignore # pylint: disable=no-member

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger up.

        :param touch:           motion/touch event data.
        :return:                boolean True value if the event got processed/used.
        """
        self._cancel_slide_select_closer(touch)
        self._cancel_slide_select_opener(touch)
        self._opened_item = None

        if touch.ud.pop('is_long_tap', False):
            items = getattr(self, 'menu_items', None)
            if items and self._layout_finished and self == Window.children[0]:
                for item in items:                                          # pylint: disable=E1133
                    if item.collide_point(*item.to_widget(*touch.pos)):     # slide_select touch released on a menu item
                        if hasattr(item, 'on_release'):
                            if item not in touch.ud:                        # prevent multiple dispatch of on_release
                                item.dispatch('on_release')
                                return True
                        elif hasattr(item, 'focus'):
                            item.unfocus_on_touch = False
                            item.focus = True
                            return True
                        elif hasattr(item, 'value_pos'):
                            item.value_pos = touch.pos
                            return True
                        else:
                            break

        # noinspection PyUnresolvedReferences
        return super().on_touch_up(touch)   # type: ignore # pylint: disable=no-member # does touch.ungrab(self)


class TouchableBehavior:                                                                        # pragma: no cover
    """ touch-/toggle-button mix-in class with shaders, animations and additional events for double/triple/long touches.

    :Events:
        `on_double_tap`:
           fired with the touch-down MotionEvent instance arg when a button gets tapped twice within a short time.
        `on_triple_tap`:
           fired with the touch-down MotionEvent instance arg when a button gets tapped three times within a short time.
        `on_long_tap`:
           fired with the touch-down MotionEvent instance arg when a button gets tapped more than 2.4 seconds.
        `on_alt_tap`:
           fired with the touch-down MotionEvent instance arg when a button gets either double, triple or long tapped.

    .. note::
        has to be inherited (to be in the MRO) before the class :class:`~kivy.uix.behaviors.ButtonBehavior`,
        respectively :class:`~kivy.uix.behaviors.ToggleButtonBehavior`, for the touch event gets grabbed properly.
    """
    # abstracts of mixing-in class; e.g., from :class:`~kivy.widget.Widget`, :class:`~ae.kivy_glsl.ShadersMixin`,
    # :class:`~ae.kivy.behaviors.SlideSelectBehavior`, and :class:`~kivy.uix.behaviors.ButtonBehavior`
    add_shader: Callable
    center_x: float
    center_y: float
    collide_point: Callable
    del_shader: Callable
    disabled: bool
    dispatch: Callable
    state: str

    # Kivy properties and events
    down_shader = DictProperty(allownone=True)
    """ shader running if button is in pressed state `'down'`.

    :attr:`down_shader` is a :class:`~kivy.properties.DictProperty` and defaults to the :data:`firestorm shader
    <ae.kivy_glsl.FIRE_STORM_SHADER_CODE>`. set to `None` to not render the default shader on button press/down.
    """

    normal_shader = DictProperty(allownone=True)
    """ shader running if button is in pressed state `'normal'`.

    :attr:`normal_shader` is a :class:`~kivy.properties.DictProperty` and defaults to the :data:`plunge wave shader
    <ae.kivy_glsl.PLUNGE_WAVES_SHADER_CODE>`. set to `None` to not render a shader on button release/up.
    """

    _touch_anim = NumericProperty(1.0)  #: widget-got-touched-animation
    _touch_x = NumericProperty()        #: x pos moving in touch animation from initial touch to center pos
    _touch_y = NumericProperty()        #: y pos moving in touch animation from initial touch to center pos

    __events__ = ('on_alt_tap', 'on_double_tap', 'on_long_tap', 'on_triple_tap')

    def __init__(self, **kwargs):
        """ set normal pressed state shader on widget initialization. """
        self._state_shader_id: ShaderIdType = {}

        # noinspection PyUnresolvedReferences
        super().__init__(**kwargs)

        main_app = App.get_running_app().main_app
        if self.down_shader is not None:
            self.down_shader = {'shader_code': '=fire_storm', 'render_shape': Ellipse,
                                'tint_ink': main_app.flow_path_ink}
        if self.normal_shader is not None:
            self.normal_shader = {'shader_code': '=plunge_waves', 'render_shape': Ellipse, 'add_to': 'before',
                                  'alpha': 0.36, 'contrast': 0.09, 'tex_col_mix': 0.87,
                                  'time': lambda: -Clock.get_boottime(), 'tint_ink': main_app.flow_id_ink}

    @staticmethod
    def _cancel_long_touch_clock(touch: MotionEvent) -> bool:
        long_touch_handler = touch.ud.pop('long_touch_handler', None)
        if long_touch_handler:
            Clock.unschedule(long_touch_handler)  # alternatively: long_touch_handler.cancel()
        return bool(long_touch_handler)

    def on_alt_tap(self, touch: MotionEvent):
        """ default handler for alternative tap (double, triple or long tap/click).

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_double_tap(self, touch: MotionEvent):
        """ default event handler for double tap/click events.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def on_down_shader(self, *_args):
        """ event handler called when button down state shader changed. """
        self._update_shader()

    def on_long_tap(self, touch: MotionEvent):
        """ long tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """
        # remove 'long_touch_handler' key from touch.ud dict although just fired to signalize that
        # the long tap event got handled in self.on_touch_up (to return True)
        self._cancel_long_touch_clock(touch)
        touch.ud['is_long_tap'] = True

        # reset the button state to normal - if the state is still down (to replace down_shader with normal_shader)
        if self.state == 'down':
            self.state = 'normal'

        # to prevent dismiss via super().on_touch_up: exclusive receive of this touch-up event in self.on_touch_up
        # later uncommented again, because long tap dropdowns did not stay open and selected menu item on slide to it
        # touch.grab(self)   # without exclusive submenu gets selected on long touch release of dropdown-opening button
        # if touch.grab_exclusive_class is None:  # check if already grabbed, to prevent exception in touch.grab() call
        #    touch.grab(self, exclusive=True)  # was commented because already grabbed/exclusive prevents slide_select
        if not grab_touch(touch, self, exclusive=True):
            grab_touch(touch, self)

        # also dispatch as an alternative tap
        self.dispatch('on_alt_tap', touch)

    def on_normal_shader(self, *_args):
        """ button normal state shader changed event handler. """
        self._update_shader()

    def on_state(self, _widget: Any, _value: str):
        """ the button press-state-changed event handler, switching between `'normal'` and `'down'` state shader.

        :param _widget:         button widget (is self).
        :param _value:          new state value (either 'normal' or 'down').
        """
        self._update_shader()

    def on_touch_down(self, touch: MotionEvent) -> bool:
        """ add sound, vibration and animation, check for a running tour and additional double/triple/alt touch events.

        :param touch:           motion/touch event data.
        :return:                a boolean True if the event got processed/used.
        """
        if not self.disabled and self.collide_point(touch.x, touch.y):
            main_app = App.get_running_app().main_app
            if main_app.tour_layout and self is not main_app.help_activator:
                return True  # suppress on_release event if the app tour is running (except for the activator button)

            self._touch_anim = 0.0
            self._touch_x, self._touch_y = touch.pos
            Animation(_touch_anim=1.0, _touch_x=self.center_x, _touch_y=self.center_y, t='out_quad', d=0.69).start(self)
            is_triple = touch.is_triple_tap
            if is_triple or touch.is_double_tap:
                # pylint: disable=maybe-no-member
                self.dispatch('on_triple_tap' if is_triple else 'on_double_tap', touch)
                self.dispatch('on_alt_tap', touch)
                return True
            # pylint: disable=maybe-no-member
            touch.ud['long_touch_handler'] = long_touch_handler = lambda dt: self.dispatch('on_long_tap', touch)
            Clock.schedule_once(long_touch_handler, 0.99)
            main_app.play_vibrate(TOUCH_VIBRATE_PATTERN)
            main_app.play_sound('touched')

        # noinspection PyUnresolvedReferences
        return super().on_touch_down(touch)  # type: ignore # pylint: disable=no-member # does touch.grab(self)

    def on_touch_move(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger moves.

        :param touch:           motion/touch event data.
        :return:                a boolean True if the event got processed/used.
        """
        # if moved, then cancel long touch detection, an alternative method to calc touch.pos distances is:
        # Vector.distance(Vector(ref.sx, ref.sy), Vector(touch.osx, touch.osy)) > 0.009
        if abs(touch.ox - touch.x) > 9 and abs(touch.oy - touch.y) > 9:
            self._cancel_long_touch_clock(touch)

        # noinspection PyUnresolvedReferences
        return super().on_touch_move(touch)                         # type: ignore # pylint: disable=no-member

    def on_touch_up(self, touch: MotionEvent) -> bool:
        """ disable long touch on mouse/finger up.

        :param touch:           motion/touch event data.
        :return:                True if the event got processed/used.
        """
        if touch.grab_current is self:
            touch.ungrab(self)
            # cancel the long touch clock callback (if still running respectively if not on_long_tap)
            if not self._cancel_long_touch_clock(touch):
                return True                 # prevent popup/dropdown dismiss

        # noinspection PyUnresolvedReferences
        return super().on_touch_up(touch)   # type: ignore # pylint: disable=no-member # does touch.ungrab(self)

    def on_triple_tap(self, touch: MotionEvent):
        """ the triple tap/click default handler.

        :param touch:           motion/touch event data with the touched widget in `touch.grab_current`.
        """

    def _update_shader(self):
        """ update shader on changed shader or button state. """
        if self._state_shader_id:
            self.del_shader(self._state_shader_id)
            self._state_shader_id = {}

        add_shader_kwargs = self.down_shader if self.state == 'down' else self.normal_shader
        if add_shader_kwargs:
            self._state_shader_id = self.add_shader(**add_shader_kwargs)
