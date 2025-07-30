# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Data methods.
"""


from typing import Any, List, Tuple, Dict, TypedDict, Iterable, Optional, NoReturn, Callable, Generator, overload

from .rexception import check_least_one, check_most_one
from .rsystem import is_iterable


__all__ = (
    "count",
    "flatten",
    "split",
    "unique",
    "in_arrs",
    "objs_in",
    "RGenerator"
)


CountResult = TypedDict("CountResult", {"value": Any, "count": int})


def count(
    data: Iterable,
    ascend: bool = False
) -> List[CountResult]:
    """
    Group count data element value.

    Parameters
    ----------
    data : Data.
    ascend : Whether ascending by count, otherwise descending order.

    Returns
    -------
    Count result.

    Examples
    --------
    >>> count([1, True, 1, '1', (2, 3)])
    [{'value': 1, 'count': 2}, {'value': True, 'count': 1}, {'value': '1', 'count': 1}, {'value': (2, 3), 'count': 1}]
    """

    # Set parameter.
    value_list = []
    count_list = []

    # Count.
    for element in data:
        value_list_exist = False
        for index, value in enumerate(value_list):
            element_str = str(element)
            value_str = str(value)
            if element_str == value_str:
                value_list_exist = True
                count_list[index] += 1
                break
        if not value_list_exist:
            value_list.append(element)
            count_list.append(1)

    # Convert.
    result = [
        {
            "value": value,
            "count": count
        }
        for value, count in zip(value_list, count_list)
    ]

    # Sort.
    result.sort(
        key=lambda info: info["count"],
        reverse=not ascend
    )

    return result


def flatten(data: Any, flattern_data: List = []) -> List:
    """
    Flatten data.

    Parameters
    ----------
    data : Data.
    flattern_data : Recursion cumulative data.

    Returns
    -------
    Data after flatten.
    """

    # Flatten.

    ## Recursion dict object.
    if data.__class__ == dict:
        for element in data.values():
            _ = flatten(element, flattern_data)

    ## Recursion iterator.
    elif is_iterable(data):
        for element in data:
            _ = flatten(element, flattern_data)

    ## Other.
    else:
        flattern_data.append(data)

    return flattern_data


@overload
def split(data: Iterable, share: None = None, bin_size: None = None) -> NoReturn: ...

@overload
def split(data: Iterable, share: int = None, bin_size: int = None) -> NoReturn: ...

@overload
def split(data: Iterable, share: Optional[int] = None, bin_size: Optional[int] = None) -> List[List]: ...

def split(data: Iterable, share: Optional[int] = None, bin_size: Optional[int] = None) -> List[List]:
    """
    Split data into multiple data.

    Parameters
    ----------
    data : Data.
    share : Number of splie share.
    bin_size : Size of each bin.

    Returns
    -------
    Split data.
    """

    # Check parameter.
    check_least_one(share, bin_size)
    check_most_one(share, bin_size)

    # Handle parameter.
    data = list(data)

    # Split.
    data_len = len(data)
    _data = []
    _data_len = 0

    ## by number of share.
    if share is not None:
        average = data_len / share
        for n in range(share):
            bin_size = int(average * (n + 1)) - int(average * n)
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size

    ## By size of bin.
    elif bin_size is not None:
        while True:
            _data = data[_data_len:_data_len + bin_size]
            _data.append(_data)
            _data_len += bin_size
            if _data_len > data_len:
                break

    return _data


def unique(data: Iterable) -> List:
    """
    De duplication of data.

    Parameters
    ----------
    data : Data.

    Returns
    -------
    List after de duplication.
    """

    # Handle parameter.
    data = tuple(data)

    # Delete duplicate.
    data_unique = list(set(data))
    data_unique.sort(key=data.index)
    return data_unique


def in_arrs(ojb: Any, *arrs: Iterable) -> bool:
    """
    Judge whether the one object is in multiple arrays.

    Parameters
    ----------
    obj : One object.
    arrs : Multiple arrays.

    Returns
    -------
    Judge result.
    """

    # Judge.
    for arr in arrs:
        if ojb in arr:
            return True
    return False


def objs_in(arr: Iterable, *objs: Any) -> bool:
    """
    Judge whether the multiple objects is in one array.

    Parameters
    ----------
    arr : One array.
    objs : Multiple objects.

    Returns
    -------
    Judge result.
    """

    # Judge.
    for obj in objs:
        if obj in arr:
            return True
    return False


class RGenerator(object):
    """
    Rey's `generator` type.
    """


    def __init__(
        self,
        func: Callable,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Build `generator` instance.

        Parameters
        ----------
        func : Generate function.
        args : Function default position arguments.
        kwargs : Function default keyword arguments.
        """

        # Set attribute.
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.params: List[Tuple[Tuple, Dict]] = []
        self.generator = self._generator()


    def _generator(self) -> Generator[Any, Any, None]:
        """
        Create generator.

        Parameters
        ----------
        Generator.
        """

        # Loop.
        while True:

            # Break.
            if self.params == []:
                break

            # Generate.
            args, kwargs = self.params.pop(0)
            result = self.func(*args, **kwargs)

            # Return.
            yield result


    def add(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """
        Add once generate.

        Parameters
        ----------
        args : Function position arguments.
        kwargs : Function keyword arguments.
        """

        # Set parameter.
        func_args = (
            *self.args,
            *args
        )
        func_kwargs = {
            **self.kwargs,
            **kwargs
        }

        # Add.
        item = (
            func_args,
            func_kwargs
        )
        self.params.append(item)


    __call__ = add


    def __next__(self) -> Any:
        """
        Generate once from generator.

        Returns
        -------
        Generate value.
        """

        # Generate.
        result = next(self.generator)

        return result


    def __iter__(self) -> Generator[Any, Any, None]:
        """
        Iterating generator.
        """

        # Iterating.
        return self.generator