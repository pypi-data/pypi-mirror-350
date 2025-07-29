# SPDX-FileCopyrightText: 2020-2024 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import blf
from bpy.types import UILayout, Context
from bpy.app.translations import pgettext
from mathutils import Vector

__all__ = (
    "eval_text_pixel_dimensions",
    "draw_wrapped_text",
)


def eval_text_pixel_dimensions(*, fontid: int = 0, text: str = "") -> Vector:
    """
    Evaluates text dimensions in pixels as it would be desplayed in the UI.

    :param fontid: Font identifier, default ``0``.
    :type fontid: int, optional
    :param text: Text to be evaluated, default - empty string.
    :type text: str, optional
    :return: Width and height in pixels.
    :rtype: `mathutils.Vector`_
    """

    ret = Vector((0.0, 0.0))
    if not text:
        return ret

    is_single_char = bool(len(text) == 1)
    SINGLE_CHARACTER_SAMPLES = 100
    if is_single_char:
        text *= SINGLE_CHARACTER_SAMPLES

    ret.x, ret.y = blf.dimensions(fontid, text)

    if is_single_char:
        ret.x /= SINGLE_CHARACTER_SAMPLES

    return ret


def draw_wrapped_text(
    context: Context,
    layout: UILayout,
    *,
    text: str,
    text_ctxt: None | str = None,
    fixed_width: int = -1
) -> None:
    """
    Wrapped text in the UI. Text block would be wrapped to width of contextual region. 

    :param context: Current context.
    :type context: `Context`_
    :param layout: Current UI layout.
    :type layout: `UILayout`_
    :param text: Text block to be displayed.
    :type text: str
    :param fixed_width: Fixed width of text block in pixels. Any positive value would ignore region width.
    """

    if context.region.type == 'WINDOW':
        win_padding = 30
    elif context.region.type == 'UI':
        win_padding = 52
    else:
        win_padding = 52

    if fixed_width > 0:
        wrap_width = fixed_width
    else:
        wrap_width = context.region.width

    wrap_width = max(0, wrap_width - win_padding)
    space_width = eval_text_pixel_dimensions(text=' ').x

    text = pgettext(text, text_ctxt)

    for line in text.split('\n'):
        num_characters = len(line)

        if not num_characters:
            layout.separator()
            continue

        line_words = list((_, eval_text_pixel_dimensions(text=_).x) for _ in line.split(' '))
        num_line_words = len(line_words)
        line_words_last = num_line_words - 1

        sublines = [""]
        subline_width = 0.0

        for i in range(num_line_words):
            word, word_width = line_words[i]

            sublines[-1] += word
            subline_width += word_width

            next_word_width = 0.0
            if i < line_words_last:
                next_word_width = line_words[i + 1][1]

                sublines[-1] += ' '
                subline_width += space_width

            if subline_width + next_word_width > wrap_width:
                subline_width = 0.0
                if i < line_words_last:
                    sublines.append("")  # Add new sub-line.

        for subline in sublines:
            layout.label(text=subline)
