# SPDX-FileCopyrightText: 2020-2024 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os

import bpy
import bpy.utils.previews
from bpy.types import ImagePreview

__all__ = (
    "IconsCache",
)


class IconsCache:
    """
    Abstract icons cache class.
    """

    __slots__ = (
        "_directory",
        "_data_identifiers",
        "_image_names",
        "_cache",
        "_pcoll_cache",
    )

    _directory: str
    "Icons source directory."

    _data_identifiers: tuple[str, ...]
    "Icons data identifiers."

    _image_names: tuple[str, ...]
    "Icons image identifiers."

    _cache: dict[str, int]
    "Icons map: `identifier: icon_value`"

    _pcoll_cache: None | bpy.utils.previews.ImagePreviewCollection
    "Image icons cache"

    def _intern_initialize_from_data_files(self):
        for identifier in self._data_identifiers:
            try:
                icon_value = bpy.app.icons.new_triangles_from_file(os.path.join(self._directory, f"{identifier}.dat"))
            except ValueError:
                # log.warning(f"Unable to load icon \"{identifier}\"")
                icon_value = 0

            self._cache[identifier] = icon_value

    def _intern_initialize_from_image_files(self):
        if self._image_names:
            pcoll = bpy.utils.previews.new()
            for name in self._image_names:
                prv: ImagePreview = pcoll.load(name, os.path.join(self._directory, name), 'IMAGE')
                self._cache[os.path.splitext(name)[0]] = prv.icon_id
            self._pcoll_cache = pcoll

    def __init__(self, *, directory: str = "", data_identifiers: tuple[str, ...] = (), image_names: tuple[str, ...] = ()):
        self._directory = directory
        self._data_identifiers = data_identifiers
        self._image_names = image_names
        self._cache = dict()
        self._pcoll_cache = None

        self._intern_initialize_from_data_files()
        self._intern_initialize_from_image_files()

    def release(self):
        if self._pcoll_cache is not None:
            bpy.utils.previews.remove(self._pcoll_cache)
            self._pcoll_cache = None

        self._cache.clear()

    def get_id(self, identifier: str) -> int:
        return self._cache.get(identifier, 0)
