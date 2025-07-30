# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:11:50
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Time methods.
"""


from typing import Any, Dict, TypedDict, Literal, Callable, Optional, Union, overload, NoReturn
from pandas import (
    DataFrame,
    Timestamp as pd_timestamp,
    Timedelta as pd_timedelta
)
from time import (
    struct_time as time_struct_time,
    strftime as time_strftime,
    time as time_time,
    sleep as time_sleep
)
from datetime import (
    datetime as datetime_datetime,
    date as datetime_date,
    time as datetime_time,
    timedelta as datetime_timedelta
)

from .rexception import throw
from .rnumber import digits
from .rrandom import randn
from .rregex import search
from .rstdout import echo


__all__ = (
    "now",
    "time_to",
    "text_to_time",
    "to_time",
    "sleep",
    "wait",
    "RTimeMark"
)


RecordData = TypedDict("RecordData", {"timestamp": int, "datetime": datetime_datetime, "timedelta": Optional[datetime_timedelta], "note": Optional[str]})


@overload
def now(format_: Literal["datetime"] = "datetime") -> datetime_datetime: ...

@overload
def now(format_: Literal["date"] = "datetime") -> datetime_date: ...

@overload
def now(format_: Literal["time"] = "datetime") -> datetime_time: ...

@overload
def now(format_: Literal["datetime_str", "date_str", "time_str"] = "datetime") -> str: ...

@overload
def now(format_: Literal["timestamp"] = "datetime") -> int: ...

@overload
def now(format_: Any) -> NoReturn: ...

def now(
    format_: Literal[
        "datetime",
        "date",
        "time",
        "datetime_str",
        "date_str",
        "time_str",
        "timestamp"
    ] = "datetime"
) -> Union[
    datetime_datetime,
    datetime_date,
    datetime_time,
    str,
    int
]:
    """
    Get the now time.

    Parameters
    ----------
    format_ : Format type.
        - `Literal['datetime']` : Return datetime object of datetime package.
        - `Literal['date']` : Return date object of datetime package.
        - `Literal['time']` : Return time object of datetime package.
        - `Literal['datetime_str']` : Return string in format `'%Y-%m-%d %H:%M:%S'`.
        - `Literal['date_str']` : Return string in format `'%Y-%m-%d'`.
        - `Literal['time_str']` : Return string in foramt `'%H:%M:%S'`.
        - `Literal['timestamp']` : Return time stamp in milliseconds.

    Returns
    -------
    The now time.
    """

    # Return.
    if format_ == "datetime":
        return datetime_datetime.now()
    elif format_ == "date":
        return datetime_datetime.now().date()
    elif format_ == "time":
        return datetime_datetime.now().time()
    elif format_ == "datetime_str":
        return datetime_datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif format_ == "date_str":
        return datetime_datetime.now().strftime("%Y-%m-%d")
    elif format_ == "time_str":
        return datetime_datetime.now().strftime("%H:%M:%S")
    elif format_ == "timestamp":
        return int(time_time() * 1000)
    else:
        throw(ValueError, format_)


@overload
def time_to(
    obj: Union[
        datetime_datetime,
        datetime_date,
        datetime_time,
        datetime_timedelta,
        time_struct_time,
        pd_timestamp,
        pd_timedelta
    ],
    decimal: bool = False,
    raising: bool = True
) -> str: ...

@overload
def time_to(
    obj: Any,
    decimal: bool = False,
    raising: Literal[True] = True
) -> NoReturn: ...

@overload
def time_to(
    obj: Any,
    decimal: bool = False,
    raising: Literal[False] = True
) -> Any: ...

def time_to(
    obj: Any,
    decimal: bool = False,
    raising: bool = True
) -> Any:
    """
    Convert time object to text.

    Parameters
    ----------
    obj : Time object.
        - `datetime` : Text format is `'%Y-%m-%d %H:%M:%S'`.
        - `date` : Text format is `'%Y-%m-%d'`.
        - `time` : Text format is `'%H:%M:%S'`.
        - `struct_time` : Text format is `'%Y-%m-%d %H:%M:%S'`.

    decimal : Whether with decimal, precision to microseconds.
    raising : When parameter `obj` value error, whether throw exception, otherwise return original value.

    Returns
    -------
    Converted text.
    """

    # Type "datetime".
    if obj.__class__ in (datetime_datetime, pd_timestamp):
        if decimal:
            format_ = "%Y-%m-%d %H:%M:%S.%f"
        else:
            format_ = "%Y-%m-%d %H:%M:%S"
        text = obj.strftime(format_)

    # Type "date".
    elif obj.__class__ == datetime_date:
        text = obj.strftime("%Y-%m-%d")

    # Type "time".
    elif obj.__class__ == datetime_time:
        if decimal:
            format_ = "%H:%M:%S.%f"
        else:
            format_ = "%H:%M:%S"
        text = obj.strftime(format_)

    # Type "timedelta".
    elif obj.__class__ in (datetime_timedelta, pd_timedelta):
        timestamp = obj.seconds + obj.microseconds / 1000_000
        if timestamp >= 0:
            timestamp += 57600
            time = datetime_datetime.fromtimestamp(timestamp).time()
            if decimal:
                format_ = "%H:%M:%S.%f"
            else:
                format_ = "%H:%M:%S"
            text = time.strftime(format_)
            if obj.days != 0:
                text = f"{obj.days}day " + text

        ## Throw exception.
        elif raising:
            throw(ValueError, obj)

        ## Not raise.
        else:
            return obj

    # Type "struct_time".
    elif obj.__class__ == time_struct_time:
        if decimal:
            format_ = "%Y-%m-%d %H:%M:%S.%f"
        else:
            format_ = "%Y-%m-%d %H:%M:%S"
        text = time_strftime(format_, obj)

    # Throw exception.
    elif raising:
        throw(TypeError, obj)

    # Not raise.
    else:
        return obj

    return text


def text_to_time(
    string: str
) -> Optional[
    Union[
        datetime_datetime,
        datetime_date,
        datetime_time
    ]
]:
    """
    Convert text to time object.

    Parameters
    ----------
    string : String.

    Returns
    -------
    Object or null.
    """

    # Get parameter.
    time_obj = None
    str_len = len(string)

    # Extract.

    ## Standard.
    if 14 <= str_len <= 19:
        try:
            time_obj = datetime_datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass
        else:
            return time_obj
    if 8 <= str_len <= 10:
        try:
            time_obj = datetime_datetime.strptime(string, "%Y-%m-%d").date()
        except ValueError:
            pass
        else:
            return time_obj
    if 5 <= str_len <= 8:
        try:
            time_obj = datetime_datetime.strptime(string, "%H:%M:%S").time()
        except ValueError:
            pass
        else:
            return time_obj

    ## Regular.

    ### Type "datetime".
    if 14 <= str_len <= 21:
        pattern = r"^(\d{4})\S(\d{1,2})\S(\d{1,2})\S?.(\d{1,2})\S(\d{1,2})\S(\d{1,2})\S?$"
        result = search(pattern, string)
        if result is not None:
            year, month, day, hour, minute, second = [
                int(value)
                for value in result
            ]
            time_obj = datetime_datetime(year, month, day, hour, minute, second)
            return time_obj

    ### Type "date".
    if 8 <= str_len <= 11:
        pattern = r"^(\d{4})\S(\d{1,2})\S(\d{1,2})\S?$"
        result = search(pattern, string)
        if result is not None:
            year, month, day = [
                int(value)
                for value in result
            ]
            time_obj = datetime_date(year, month, day)
            return time_obj

    ### Type "time".
    if 5 <= str_len <= 9:
        pattern = r"^(\d{1,2})\S(\d{1,2})\S(\d{1,2})\S?$"
        result = search(pattern, string)
        if result is not None:
            hour, minute, second = [
                int(value)
                for value in result
            ]
            time_obj = datetime_time(hour, minute, second)
            return time_obj


@overload
def to_time(
    obj: str,
    raising: bool = True
) -> Union[datetime_datetime, datetime_date, datetime_time]: ...

@overload
def to_time(
    obj: Union[time_struct_time, float],
    raising: bool = True
) -> datetime_datetime: ...

@overload
def to_time(
    obj: Any,
    raising: Literal[True] = True
) -> NoReturn: ...

@overload
def to_time(
    obj: Any,
    raising: Literal[False] = True
) -> Any: ...

def to_time(
    obj: Any,
    raising: bool = True
) -> Any:
    """
    Convert object to time object.

    Parameters
    ----------
    obj : Object.
    raising : When parameter `obj` value error, whether throw exception, otherwise return original value.

    Returns
    -------
    Time object.
    """

    # Type "str".
    if obj.__class__ == str:
        time_obj = text_to_time(obj)

    # Type "struct_time".
    elif obj.__class__ == time_struct_time:
        time_obj = datetime_datetime(
            obj.tm_year,
            obj.tm_mon,
            obj.tm_mday,
            obj.tm_hour,
            obj.tm_min,
            obj.tm_sec
        )

    # Type "float".
    elif obj.__class__ in (int, float):
        int_len, _ = digits(obj)
        if int_len == 10:
            time_obj = datetime_datetime.fromtimestamp(obj)
        elif int_len == 13:
            time_obj = datetime_datetime.fromtimestamp(obj / 1000)
        else:
            time_obj = None

    # No time object.
    if time_obj is None:

        ## Throw exception.
        if raising:
            throw(ValueError, obj)

        ## Not raise.
        else:
            return obj

    return time_obj


def sleep(
    *thresholds: float,
    precision: Optional[int] = None
) -> float:
    """
    Sleep random seconds.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When `length is 0`, then low and high thresholds is `0` and `10`.
        - When `length is 1`, then sleep this value.
        - When `length is 2`, then low and high thresholds is `thresholds[0]` and `thresholds[1]`.
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - `None` : Set to Maximum decimal digits of element of parameter `thresholds`.
        - `int` : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters `precision` is `0`, then return int.
        - When parameters `precision` is `greater than 0`, then return float.
    """

    # Handle parameter.
    if len(thresholds) == 1:
        second = float(thresholds[0])
    else:
        second = randn(*thresholds, precision=precision)

    # Sleep.
    time_sleep(second)

    return second


def wait(
    func: Callable[..., bool],
    *args: Any,
    _interval: float = 1,
    _timeout: Optional[float] = None,
    **kwargs: Any
) -> float:
    """
    Wait success, timeout throw exception.

    Parameters
    ----------
    func : Function to be decorated, must return `bool` value.
    args : Position arguments of decorated function.
    _interval : Interval seconds.
    _timeout : Timeout seconds, timeout throw exception.
        - `None` : Infinite time.
        - `float` : Use this time.

    kwargs : Keyword arguments of decorated function.

    Returns
    -------
    Total spend seconds.
    """

    # Set parameter.
    rtm = RTimeMark()
    rtm()

    # Not set timeout.
    if _timeout is None:

        ## Wait.
        while True:
            success = func(*args, **kwargs)
            if success: break
            sleep(_interval)

    # Set timeout.
    else:

        ## Wait.
        while True:
            success = func(*args, **kwargs)
            if success: break

            ## Timeout.
            rtm()
            if rtm.total_spend > _timeout:
                throw(TimeoutError, _timeout)

            ## Sleep.
            sleep(_interval)

    ## Return.
    rtm()
    return rtm.total_spend


class RTimeMark():
    """
    Rey`s `time mark` type.
    """


    def __init__(self) -> None:
        """
        Build `time mark` instance.
        """

        # Record table.
        self.record: Dict[int, RecordData] = {}


    def mark(self, note: Optional[str] = None) -> int:
        """
        Marking now time.

        Parameters
        ----------
        note : Mark note.

        Returns
        -------
        Mark index.
        """

        # Get parametes.

        # Mark.
        index = len(self.record)
        now_timestamp = now("timestamp")
        now_datetime = now("datetime")
        record = {
            "timestamp": now_timestamp,
            "datetime": now_datetime,
            "timedelta": None,
            "note": note
        }

        ## Not first.
        if index != 0:
            last_index = index - 1
            last_datetime = self.record[last_index]["datetime"]
            record["timedelta"] = now_datetime - last_datetime

        ## Record.
        self.record[index] = record

        return index


    def report(self, title: Optional[str] = None) -> DataFrame:
        """
        Print and return time mark information table.

        Parameters
        ----------
        title : Print title.
            - `None` : Not print.
            - `str` : Print and use this title.

        Returns
        -------
        Time mark information table
        """

        # Get parameter.
        record_len = len(self.record)
        data = [
            info.copy()
            for info in self.record.values()
        ]
        indexes = [
            index
            for index in self.record
        ]

        # Generate report.

        ## No record.
        if record_len == 0:
            row = dict.fromkeys(("timestamp", "datetime", "timedelta", "note"))
            data = [row]
            indexes = [0]

        ## Add total row.
        if record_len > 2:
            row = dict.fromkeys(("timestamp", "datetime", "timedelta", "note"))
            max_index = record_len - 1
            total_timedelta = self.record[max_index]["datetime"] - self.record[0]["datetime"]
            row["timedelta"] = total_timedelta
            data.append(row)
            indexes.append("total")

        ## Convert.
        for row in data:
            if row["timestamp"] is not None:
                row["timestamp"] = str(row["timestamp"])
            if row["datetime"] is not None:
                row["datetime"] = str(row["datetime"])[:-3]
            if row["timedelta"] is not None:
                if row["timedelta"].total_seconds() == 0:
                    timedelta_str = "00:00:00.000"
                else:
                    timedelta_str = str(row["timedelta"])[:-3]
                    timedelta_str = timedelta_str.rsplit(" ", 1)[-1]
                    if timedelta_str[1] == ":":
                        timedelta_str = "0" + timedelta_str
                    if row["timedelta"].days != 0:
                        timedelta_str = "%sday %s" % (
                            row["timedelta"].days,
                            timedelta_str
                        )
                row["timedelta"] = timedelta_str
        df_info = DataFrame(data, index=indexes)
        df_info.fillna("-", inplace=True)

        # Print.
        if title is not None:
            echo(df_info, title=title)

        return df_info


    @property
    def total_spend(self) -> float:
        """
        Get total spend seconds.

        Returns
        -------
        Total spend seconds.
        """

        # Break.
        if len(self.record) <= 1: return 0.0

        # Get parameter.
        first_timestamp = self.record[0]["timestamp"]
        max_index = max(self.record)
        last_timestamp = self.record[max_index]["timestamp"]

        # Calculate.
        seconds = round((last_timestamp - first_timestamp) / 1000, 3)

        return seconds


    def __str__(self) -> str:
        """
        Convert to string.

        Returns
        -------
        Converted string.
        """

        # Get.
        report = self.report()

        # Convert.
        string = str(report)

        return string


    __call__ = mark