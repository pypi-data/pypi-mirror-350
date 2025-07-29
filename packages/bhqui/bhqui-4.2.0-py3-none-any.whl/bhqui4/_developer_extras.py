# SPDX-FileCopyrightText: 2020-2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Context, UILayout

from . _wrapped_text import draw_wrapped_text

__all__ = (
    "developer_extras_poll",
    "template_developer_extras_warning",
)


def developer_extras_poll(context: Context) -> bool:
    """
    Check if developer extras should be displayed in user interface.

    :param context: Current context.
    :type context: `Context`_
    :return: True if developer extras should be shown.
    :rtype: bool
    """

    assert context.preferences

    return context.preferences.view.show_developer_ui


def template_developer_extras_warning(context: Context, layout: UILayout, text_ctxt: str = 'bqhui') -> None:
    """
    Template UI text which warns user about section which is intended for development purposes and also
    allows to disable developer extras.

    .. note::

        `bqhui` used as message context in localization, so message can be translated.

    :param context: Current context.
    :type context: `Context`_
    :param layout: UI layout where warning should be displayed.
    :type layout: `UILayout`_
    :param text_ctxt: Text translation context.
    :type text_ctxt: str
    """

    if developer_extras_poll(context):
        assert context.preferences

        col = layout.column(align=True)
        scol = col.column(align=True)
        scol.alert = True
        scol.label(text="Warning", icon='INFO')
        text = "This section is intended for developers. You see it because " \
            "you have an active \"Developers Extras\" option in the Blender " \
            "user preferences."
        draw_wrapped_text(context, scol, text=text, text_ctxt=text_ctxt)

        col.prop(context.preferences.view, "show_developer_ui")
