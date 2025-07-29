# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2025-05-23 11:47:17
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Type methods.
"""


__all__ = (
    "RError",
    "RActiveError",
    "RNull"
)


class RError(Exception):
    """
    Rey `error` type.
    """


class RActiveError(RError):
    """
    Rey's `active error` type.
    """


class RNull():
    "Rey `null` type."
