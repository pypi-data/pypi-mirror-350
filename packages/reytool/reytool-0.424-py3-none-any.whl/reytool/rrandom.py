# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-04-22 22:32:34
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Random methods.
"""


from typing import Any, Union, Optional, Literal, Sequence, overload
from math import ceil as math_ceil
from secrets import randbelow as secrets_randbelow

from .rexception import throw
from .rnumber import digits


__all__ = (
    "randn",
    "randb",
    "randi"
)


@overload
def randn(*thresholds: int, precision: None = None) -> int: ...

@overload
def randn(*thresholds: float, precision: None = None) -> float: ...

@overload
def randn(*thresholds: float, precision: Literal[0] = None) -> int: ...

@overload
def randn(*thresholds: float, precision: int = None) -> float: ...

def randn(*thresholds: float, precision: Optional[int] = None) -> Union[int, float]:
    """
    Random number.
    True random based on secrets package.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When `length is 0`, then low and high thresholds is `0` and `10`.
        - When `length is 1`, then low and high thresholds is `0` and `thresholds[0]`.
        - When `length is 2`, then low and high thresholds is `thresholds[0]` and `thresholds[1]`.

    precision : Precision of random range, that is maximum decimal digits of return value.
        - `None` : Set to Maximum decimal digits of element of parameter `thresholds`.
        - `int` : Set to this value.

    Returns
    -------
    Random number.
        - When parameters `precision` is 0, then return int.
        - When parameters `precision` is greater than 0, then return float.
    """

    # Handle parameter.
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        threshold_low = 0
        threshold_high = 10
    elif thresholds_len == 1:
        threshold_low = 0
        threshold_high = thresholds[0]
    elif thresholds_len == 2:
        threshold_low = thresholds[0]
        threshold_high = thresholds[1]
    else:
        raise ValueError("number of parameter 'thresholds' must is 0 or 1 or 2")
    if precision is None:
        threshold_low_desimal_digits = digits(threshold_low)[1]
        threshold_high_desimal_digits = digits(threshold_high)[1]
        desimal_digits_max = max(threshold_low_desimal_digits, threshold_high_desimal_digits)
        precision = desimal_digits_max

    # Get random number.
    magnifier = 10 ** precision
    threshold_low = int(threshold_low * magnifier)
    threshold_high = int(threshold_high * magnifier)
    range_ = threshold_high - threshold_low + 1
    number = secrets_randbelow(range_)
    number += threshold_low
    number = number / magnifier

    # Convert Integer.
    if precision == 0:
        number = int(number)

    return number


def randb(pr: float = 0.5) -> bool:
    """
    Random bool.
    True random based on secrets package.

    Parameters
    ----------
    pr : Probability setting.
        - `∈(0, 1)` : Random probability, formula is `randn(1, int(1 / pr * 100)) <= 100`.
        - `∈(1, +∞)` : Random range, formula is `randn(1, ceil(pr)) == 1`.

    Returns
    -------
    Random bool.
    """

    # Random probability.
    if 0 < pr < 1:
        high = int(1 / pr * 100)
        result = randn(1, high) <= 100

    # Random range.
    elif 1 < pr:
        high = math_ceil(pr)
        result = randn(1, high) == 1

    # Throw exception.
    else:
        throw(ValueError, pr)

    return result


def randi(data: Sequence) -> Any:
    """
    Random index data.
    True random based on secrets package.

    Parameters
    ----------
    data : Sequence data.

    Returns
    -------
    Element.
    """

    # Get parameter.
    data_len = len(data)

    # Random.
    index = randn(data_len - 1)
    element = data[index]

    return element