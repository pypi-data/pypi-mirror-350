# SPDX-FileCopyrightText: 2020-2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import random
import string
from typing import Iterable

import bpy


__all__ = (
    "eval_unique_name",
)


def eval_unique_name(*, arr: Iterable, prefix: str = "", suffix: str = "") -> str:
    """
    Evaluates random unique name for new array items with pre-defined prefix and suffix. Might be used for ``bpy.data``
    and ``bpy.ops`` to register temporary data blocks.

    :param arr: Existing array.
    :type arr: Iterable
    :param prefix: Name prefix. In case of `bpy.ops` as an array prefix:
        ``bpy.ops.[prefix][unique name][suffix]`` - this might be used as temporary operator's `bl_idname` field.
    :type prefix: str, optional
    :param suffix: Name suffix, default to "".
    :type suffix: str, optional
    :return: Unique name.
    :rtype: str
    """

    if arr is bpy.ops:
        ret = prefix + '.' + str().join(random.sample(string.ascii_lowercase, k=10)) + suffix
        if isinstance(getattr(getattr(arr, ret, None), "bl_idname", None), str):
            return eval_unique_name(arr=arr, prefix=prefix, suffix=suffix)
        return ret
    else:
        ret = prefix + str().join(random.sample(string.ascii_letters, k=5)) + suffix
        if hasattr(arr, ret) or (isinstance(arr, Iterable) and ret in arr):
            return eval_unique_name(arr=arr, prefix=prefix, suffix=suffix)
        return ret
