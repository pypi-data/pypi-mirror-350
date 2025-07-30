# SPDX-FileCopyrightText: 2020-2024 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os

import bpy
from bpy.types import UILayout, Menu

__all__ = (
    "copy_default_presets_from",
    "template_preset",
)


def copy_default_presets_from(*, src_root: str):
    """
    Copies preset files from extension directory to Blender preset directory.

    :param src_root: Preset directory.
    :type src_root: str
    """

    for root, _dir, files in os.walk(src_root):
        for filename in files:
            rel_dir = os.path.relpath(root, src_root)
            src_fp = os.path.join(root, filename)

            tar_dir = bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", rel_dir), create=True)
            if not tar_dir:
                print("Failed to create presets path")
                return

            tar_fp = os.path.join(tar_dir, filename)

            with open(src_fp, 'r', encoding="utf-8") as src_file, open(tar_fp, 'w', encoding="utf-8") as tar_file:
                tar_file.write(src_file.read())


def template_preset(layout: UILayout, *, menu: Menu, operator: str) -> None:
    """
    Template for displaying presets in the UI.

    :param layout: Current UI layout.
    :type layout: `UILayout`_
    :param menu: Menu class to be used for displaying list of presets.
    :type menu: 'Menu'_
    :param operator: Operator's ``bl_idname`` identifier to be used for adding and removing presets.
    :type operator: str
    """

    row = layout.row(align=True)
    row.use_property_split = False

    row.menu(menu=menu.__name__, text=menu.bl_label)
    row.operator(operator=operator, text="", icon='ADD')
    row.operator(operator=operator, text="", icon='REMOVE').remove_active = True
