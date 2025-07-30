# SPDX-FileCopyrightText: 2020-2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Generator

import bpy
from bl_ui import space_statusbar
from bpy.types import Context, PropertyGroup, STATUSBAR_HT_header, UILayout, WindowManager
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty, CollectionProperty

from . _unique_name import eval_unique_name

__all__ = (
    "progress",
)


class progress:
    """
    Displays progressbar in statusbar.

    :cvar int PROGRESS_BAR_UI_UNITS: UI units [4...12] for each progressbar (label and icon size does not count). 6 by default (readonly).
    """

    _is_drawn = False
    _attrname = ""

    @staticmethod
    def _update_statusbar():
        if bpy.context.workspace:
            bpy.context.workspace.status_text_set(text=None)

    class ProgressPropertyItem(PropertyGroup):
        "Single progressbar indicator."

        identifier: StringProperty(
            maxlen=64,
            options={'HIDDEN'},
        )
        "Progressbar identifier name."

        def _common_value_update(self, context: Context) -> None:
            progress._update_statusbar()

        subtype: EnumProperty(
            items=(
                ('PERCENTAGE', "Percentage", ""),
                ('STEP', "Step", ""),
                ('CONTINUOUS', "Continuous", "")
            ),
            default='PERCENTAGE',
            options={'HIDDEN'},
            update=_common_value_update,  # type: ignore
        )
        "Progressbar subtype."

        valid: BoolProperty(
            default=True,
            update=_common_value_update,  # type: ignore
        )
        "If progressbar is still valid."

        label: StringProperty(
            default="Progress",
            options={'HIDDEN'},
            update=_common_value_update,  # type: ignore
        )
        "Progressbar label."

        num_steps: IntProperty(
            min=1,
            default=1,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,  # type: ignore
        )
        "Number of steps."

        step: IntProperty(
            min=0,
            default=0,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,  # type: ignore
        )
        "Current step."

    def _func_draw_progress(self, context: Context):
        layout: UILayout = self.layout  # type: ignore

        if hasattr(WindowManager, progress._attrname):
            for item in progress.valid_progress_items():
                row = layout.row(align=True)

                factor = item.step / item.num_steps

                match item.subtype:
                    case 'PERCENTAGE':
                        row.label(text=item.label)
                        row.progress(type='BAR', text=f"{factor * 100} %", factor=factor)
                    case 'STEP':
                        row.label(text=item.label)
                        row.progress(type='BAR', text=f"{item.step} / {item.num_steps}", factor=factor)
                    case 'CONTINUOUS':
                        row.progress(type='RING', text=item.label, factor=factor)
                        item.num_steps = 25
                        item.step += 1
                        if item.step >= 25:
                            item.step = 0

    @classmethod
    def progress_items(cls) -> tuple[ProgressPropertyItem]:
        return tuple(getattr(bpy.context.window_manager, cls._attrname, tuple()))

    @classmethod
    def valid_progress_items(cls) -> Generator[ProgressPropertyItem]:
        """
        Unfinished progressbar items generator.

        :yield: Unfinished progressbar.
        :rtype: Generator[:class:`ProgressPropertyItem`]
        """

        return (_ for _ in cls.progress_items() if _.valid)

    @classmethod
    def _get(cls, *, identifier: str) -> None | ProgressPropertyItem:
        for item in cls.progress_items():
            if item.identifier == identifier:
                return item

    @classmethod
    def get(cls, *, identifier: str = "") -> ProgressPropertyItem:
        item = cls._get(identifier=identifier)
        if item is None:
            if not cls._is_drawn:
                bpy.utils.register_class(progress.ProgressPropertyItem)
                cls._attrname = eval_unique_name(arr=WindowManager, prefix="bhq_", suffix="_progress")

                setattr(
                    WindowManager,
                    cls._attrname,
                    CollectionProperty(type=progress.ProgressPropertyItem, options={'HIDDEN'})
                )
                STATUSBAR_HT_header.append(cls._func_draw_progress)
                cls._update_statusbar()

            cls._is_drawn = True
            ret: progress.ProgressPropertyItem = getattr(bpy.context.window_manager, cls._attrname).add()
            ret.identifier = identifier
            return ret
        else:
            ret = item
            ret.valid = True
            return ret

    @classmethod
    def complete(cls, *, identifier: str):
        item = cls._get(identifier=identifier)
        if item:
            item.valid = False

            for _ in cls.valid_progress_items():
                return
            cls.release_all()

    @classmethod
    def release_all(cls):
        """
        Removes all progressbars and restores statusbar to original state.
        """

        if not cls._is_drawn:
            return

        assert (cls._attrname)
        delattr(WindowManager, cls._attrname)
        bpy.utils.unregister_class(progress.ProgressPropertyItem)

        STATUSBAR_HT_header.remove(cls._func_draw_progress)
        cls._update_statusbar()

        cls._is_drawn = False
