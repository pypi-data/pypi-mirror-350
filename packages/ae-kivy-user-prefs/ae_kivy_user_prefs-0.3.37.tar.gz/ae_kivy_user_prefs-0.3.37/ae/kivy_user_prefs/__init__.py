"""
user preferences widgets for your kivy app
==========================================

this namespace portion is providing a set of widgets to allow the users of your app to change their personal
app states/settings/preferences, like the theme, the font size, the language and the used colors.

to use it in your app, import this module, which can be done either in one of the modules of your app via::

    import ae.kivy_user_prefs

alternatively, and when you use the `Kivy framework <https://kivy.org>`__ for your app, you can import it
within your main KV file, like this::

    #: import _any_dummy_name ae.kivy_user_prefs

.. note::
    the i18n translation texts of this namespace portion are provided mainly by the portion :mod:`ae.i18n`, registered
    on import of it, and the color names by :mod:`ae.gui.utils`. so when you import this portion from the main KV file
    of your app, and your app is overwriting a translation text of this portion, then you have to make sure
    that the translation texts of your main app get registered after the import of this portion. For that reason
    :class:`~ae.gui.app.MainAppBase` is using the `on_app_build` event to load the application resources,
    which gets fired after Kivy has imported the main KV file.


the user preferences are implemented as a :class:`~ae.kivy.widgets.FlowDropDown` via the widget `UserPreferencesPopup`.

to integrate it in your app, you simply add the `UserPreferencesButton` widget to the main KV file of your app.


user preferences debug mode
---------------------------

the user preferences are activating a debug mode when you click/touch the `UserPreferencesButton` button more than three
times within 6 seconds.

this debug mode activation is implemented in the :meth:`~ae.kivy.apps.KivyMainApp.on_user_preferences_open` event
handler method declared in the :mod:`ae.kivy.apps` module. it can be disabled for your app by simply overriding this
method with an empty method in your main app class.
"""
from typing import Any
from functools import partial

from kivy.app import App                                                            # type: ignore
from kivy.lang import Builder                                                       # type: ignore
from kivy.properties import StringProperty                                          # type: ignore

from ae.base import os_path_dirname, os_path_join                                   # type: ignore
from ae.gui.utils import id_of_flow, register_package_images                        # type: ignore
from ae.kivy.widgets import FlowButton, FlowDropDown                                # type: ignore
from ae.kivy.i18n import get_txt                                                    # type: ignore


__version__ = '0.3.37'


register_package_images()


Builder.load_file(os_path_join(os_path_dirname(__file__), "user_prefs.kv"))


class ChangeColorButton(FlowButton):        # pylint: disable=too-many-ancestors
    """ button widget created for each color. """
    color_name = StringProperty()           #: name of the color to change


class ThemesMenuPopup(FlowDropDown):        # pylint: disable=too-many-ancestors
    """ menu popup for the app themes with dynamic menu items for each theme. """
    @staticmethod
    def child_menu_items(theme_names: list[str]) -> list[dict[str, Any]]:       # pragma: no cover
        """ return child_data_maps list of menu item widget instantiation kwargs for the specified theme names.

        :param theme_names:     theme names (app state) bound to trigger/update child_data_maps.
        :return:                menu item widget instantiation kwargs list.
        """
        main_app = App.get_running_app().main_app
        show_confirmation = main_app.show_confirmation
        add_theme_text = get_txt("save as theme")

        def _confirm(*_args, theme_id: str):  # function needed to theme_name value from within (and not after) loop
            show_confirmation(
                message=get_txt("delete app theme {theme_id}"),
                title="delete theme",
                confirm_flow_id=id_of_flow('delete', 'theme', theme_id))

        max_text_len = len(add_theme_text)
        mnu_items: list[dict[str, Any]] = []

        for theme_name in theme_names:
            max_text_len = max(max_text_len, len(theme_name))
            mnu_items.append({'kwargs': {
                'text': theme_name,
                'tap_flow_id': id_of_flow('change', 'theme', theme_name),
                'tap_kwargs': {'popups_to_close': 1},
                'on_alt_tap': partial(_confirm, theme_id=theme_name)}})

        if mnu_items:
            mnu_items.append({'cls': 'ImageLabel', 'kwargs': {'text': "-" * max_text_len}})

        mnu_items.append({'kwargs': {
            'text': add_theme_text,
            'tap_flow_id': id_of_flow('show', 'input'),
            'tap_kwargs': {
                'popup_kwargs': {'message': get_txt("enter app theme name/id"),
                                 'title': add_theme_text,
                                 'confirm_flow_id': id_of_flow('save', 'theme'),
                                 'confirm_text': get_txt("save"),
                                 'input_default': main_app.theme_names[0] if main_app.theme_names else ""}}}})

        return mnu_items
