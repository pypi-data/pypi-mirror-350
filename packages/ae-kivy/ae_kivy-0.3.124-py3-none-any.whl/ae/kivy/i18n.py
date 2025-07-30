"""
ae.kivy.i18n module
-------------------

this module is adding translatable f-strings to the python and kv code of your app,
via the helper function :func:`~ae.kivy.i18n.get_txt` and the :class:`~ae.kivy.i18n._GetTextBinder` class.

"""
from typing import Any, Callable, Optional

from kivy.app import App                                                                                # type: ignore
from kivy.event import Observable                                                                       # type: ignore
from kivy.lang import global_idmap                                                                      # type: ignore

from ae.i18n import default_language, get_f_string                                                      # type: ignore


class _GetTextBinder(Observable):
    """ redirect :func:`ae.i18n.get_f_string` to an instance of this class.

    kivy currently only support a single one automatic binding in kv files for all function names ending with `_`
    (see `watched_keys` extension in kivy/lang/parser.py line 201; e.g. `f_` would get recognized by the lang_tr
    re pattern, but kivy will only add the `_` symbol to watched_keys and therefore `f_` not gets bound.)
    to allow both - f-strings and simple get_text messages - this module binds :func:`ae.i18n.get_f_string`
    to the `get_txt` symbol (instead of :func:`ae.i18n.get_text`).

    :data:`get_txt` can be used as the translation callable, but also to switch the current default language.
    additionally, :data:`get_txt` is implemented as an observer that automatically updates any translations
    messages of all active/visible kv rules on switch of the language at app run-time.

    inspired by (see also discussion at https://github.com/kivy/kivy/issues/1664):

    - https://github.com/tito/kivy-gettext-example
    - https://github.com/Kovak/kivy_i18n_test
    - https://git.bluedynamics.net/phil/woodmaster-trainer/-/blob/master/src/ui/kivy/i18n.py

    """
    observers: list[tuple[Callable, tuple, dict]] = []  #: list of bound observer tuples (func, args, kwargs)
    _bound_uid = -1

    def fbind(self, name: str, func: Callable, *args, **kwargs) -> int:
        """ override fbind (fast bind) from :class:`Observable` to collect and separate `_` bindings.

        :param name:            attribute name to be bound.
        :param func:            observer notification function (to be called if the attribute changes).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        :return:                unique id of this binding.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            self.observers.append((func.__call__, args, kwargs))  # type: ignore # __call__ to prevent weakly-ref-err
            # Observable.bound_uid - initialized in _event.pyx/Observable.cinit() - is not available in python:
            # uid = self.bound_uid # also not available via getattr(self, 'bound_uid')
            # self.bound_uid += 1
            # return uid
            uid = self._bound_uid
            self._bound_uid -= 1
            return uid  # alternative ugly hack: return -len(self.observers)

        return super().fbind(name, func, *args, **kwargs)

    def funbind(self, name: str, func: Callable, *args, **kwargs):
        """ override fast unbind.

        :param name:            bound attribute name.
        :param func:            observer notification function (called if attribute changed).
        :param args:            args to be passed to the observer.
        :param kwargs:          kwargs to be passed to the observer.
        """
        if name == "_":
            # noinspection PyUnresolvedReferences
            key = (func.__call__, args, kwargs)  # type: ignore # __call__ to prevent ReferenceError: weakly-ref
            if key in self.observers:
                self.observers.remove(key)
        else:
            super().funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang_code: str):
        """ change language and update kv rules properties.

        :param lang_code:       language code to switch this app to.
        """
        default_language(lang_code)

        app = App.get_running_app()

        for func, args, _kwargs in self.observers:
            app.main_app.vpo(f"_GetTextBinder.switch_lang({lang_code}) calling observer {str(args[0])[:45]}")
            try:
                func(args[0], None, None)
            except ReferenceError as ex:  # pragma: no cover # ReferenceError: a weakly-ref object no longer exists
                app.main_app.dpo(f"_GetTextBinder.switch_lang({lang_code}) exception {ex}")

        app.title = get_txt(app.main_app.app_title)

    def __call__(self, text: str, count: Optional[int] = None, language: str = '',
                 loc_vars: Optional[dict[str, Any]] = None, **kwargs) -> str:
        """ translate text into the current-default or the passed language.

        :param text:            text to translate.
        :param count:           optional count for pluralization.
        :param language:        language code to translate the passed text to (def=current default language).
        :param loc_vars:        local variables used in the conversion of the f-string expression to a string.
                                the `count` item of this dict will be overwritten by the value of the
                                :paramref:`~_GetTextBinder.__call__.count` parameter (if this argument got specified).
        :param kwargs:          extra kwargs (for example, :paramref:`~ae.i18n.get_f_string.glo_vars` or
                                :paramref:`~ae.i18n.get_f_string.key_suffix` - see :func:`~ae.i18n.get_f_string`).
        :return:                translated text.
        """
        if count is not None:
            if loc_vars is None:
                loc_vars = {}
            loc_vars['count'] = count
        return get_f_string(text, language=language, loc_vars=loc_vars, **kwargs)


get_txt = _GetTextBinder()              #: instantiate global i18n translation callable and language switcher helper
get_txt.__qualname__ = 'GetTextBinder'  # hide sphinx build warning (build crashes if the get_txt var gets documented)
global_idmap['_'] = get_txt             # bind as function/callable with the name `_` to be used in kv files
