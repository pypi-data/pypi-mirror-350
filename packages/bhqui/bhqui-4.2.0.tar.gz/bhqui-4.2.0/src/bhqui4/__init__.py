# SPDX-FileCopyrightText: 2020-2024 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

if __debug__:
    def __reload_submodules(lc):
        import importlib

        if "_unique_name" in lc:
            importlib.reload(_unique_name)
        if "_wrapped_text" in lc:
            importlib.reload(_wrapped_text)
        if "_developer_extras" in lc:
            importlib.reload(_developer_extras)
        if "_progress" in lc:
            importlib.reload(_progress)
        if "_icons_cache" in lc:
            importlib.reload(_icons_cache)
        if "_preset" in lc:
            importlib.reload(_preset)

    __reload_submodules(locals())
    del __reload_submodules

from . import _unique_name
from . import _wrapped_text
from . import _developer_extras
from . import _progress
from . import _icons_cache
from . import _preset

from . _unique_name import *
from . _wrapped_text import *
from . _developer_extras import *
from . _progress import *
from . _icons_cache import *
from . _preset import *


__all__ = (
    # file://./_unique_name.py
    "eval_unique_name",

    # file://./_wrapped_text.py
    "eval_text_pixel_dimensions",
    "draw_wrapped_text",

    # file://./_developer_extras.py
    "developer_extras_poll",
    "template_developer_extras_warning",

    # file://./_progress.py
    "progress",

    # file://./_icons_cache.py
    "IconsCache",

    # file://./_preset.py
    "copy_default_presets_from",
    "template_preset",
)
