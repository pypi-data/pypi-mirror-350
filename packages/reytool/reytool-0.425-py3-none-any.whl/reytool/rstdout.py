# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-01 14:47:47
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Standard output methods.
"""


from typing import Any, Tuple, Literal, Optional, Callable, Union, Final
import sys
from io import TextIOWrapper
from os import devnull as os_devnull
from os.path import abspath as os_abspath

from .rsystem import get_first_notnull, get_name, get_stack_param
from .rtext import to_text, add_text_frame


__all__ = (
    "beautify_text",
    "echo",
    "rinput",
    "stop_print",
    "start_print",
    "modify_print",
    "reset_print",
    "add_print_position"
)


# Module path.
path_rprint: Final[str] = os_abspath(__file__)

# Status.
_stoped: bool = False
_modified: bool = False

# IO.
_io_null: TextIOWrapper = open(os_devnull, "w")
_io_stdout: TextIOWrapper = sys.stdout
_io_stdout_write: Callable[[str], int] = sys.stdout.write

# Is the print frame plain.
is_frame_plain: bool = False

# print default width.
default_width: int = 100


def beautify_text(
    data: Tuple[Any],
    title: Union[bool, str] = True,
    width: Optional[int] = None,
    frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full"
) -> str:
    """
    Beautify data to text.

    Parameters
    ----------
    data : Text data.
    title : Text title.
        - `Literal[True]` : Automatic get data variable name.
        - `Literal[False]` : No title.
        - `str` : Use this value as the title.

    width : Text width.
        - `None` : Use attribute `default_width`.
        - `int` : Use this value.

    frame : Text frame type.
        - `Literal[`full`]` : Add beautiful four side frame and limit length.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
            * When throw `exception`, then frame is `half` type.
        - `Literal[`half`]` : Add beautiful top and bottom side frame.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
        - `Literal[`top`]` : Add beautiful top side frame.
            * When attribute `is_frame_plain` is True, then frame is `top_plain` type.
        - `Literal[`half_plain`]` : Add plain top and bottom side frame.
        - `Literal[`top_plain`]` : Add plain top side frame.

    Returns
    -------
    Beautify text.
    """

    # Get parameter.

    ## Title.
    if title is True:
        titles = get_name(data, 3)
        if titles is not None:
            titles = [title if not title.startswith("`") else "" for title in titles]
            if set(titles) != {""}:
                title = " │ ".join(titles)
    if title.__class__ != str:
        title = None

    ## Width.
    global default_width
    width = get_first_notnull(width, default_width, default="exception")

    ## Frame.
    global is_frame_plain
    if is_frame_plain:
        if frame == "full":
            frame = "half_plain"
        elif frame == "half":
            frame = "half_plain"
        elif frame == "top":
            frame = "top_plain"

    # To text.
    text_list = [
        to_text(content, width=width)
        for content in data
    ]

    # Add frame.
    text = add_text_frame(*text_list, title=title, width=width, frame=frame)

    return text


def echo(
    *data: Any,
    title: Union[bool, str] = True,
    width: Optional[int] = None,
    frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full"
) -> str:
    """
    Beautify data to text, and print.

    Parameters
    ----------
    data : Text data.
    title : Text title.
        - `Literal[True]` : Automatic get data variable name.
        - `Literal[False]` : No title.
        - `str` : Use this value as the title.

    width : Text width.
        - `None` : Use attribute `default_width`.
        - `int` : Use this value.

    frame : Text frame type.
        - `Literal[`full`]` : Add beautiful four side frame and limit length.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
            * When throw `exception`, then frame is `half` type.
        - `Literal[`half`]` : Add beautiful top and bottom side frame.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
        - `Literal[`top`]` : Add beautiful top side frame.
            * When attribute `is_frame_plain` is True, then frame is `top_plain` type.
        - `Literal[`half_plain`]` : Add plain top and bottom side frame.
        - `Literal[`top_plain`]` : Add plain top side frame.

    Returns
    -------
    Beautify text.
    """

    # Beautify.
    text = beautify_text(data, title=title, width=width, frame=frame)

    # Print.
    print(text)

    return text


def rinput(
    *data: Any,
    title: Union[bool, str] = True,
    width: Optional[int] = None,
    frame: Optional[Literal["full", "half", "top", "half_plain", "top_plain"]] = "full",
    extra: Optional[str] = None
) -> str:
    """
    Beautify data to text, and print data, and read string from standard input.

    Parameters
    ----------
    data : Text data.
    title : Text title.
        - `Literal[True]` : Automatic get data variable name.
        - `Literal[False]` : No title.
        - `str` : Use this value as the title.

    width : Text width.
        - `None` : Use attribute `default_width`.
        - `int` : Use this value.

    frame : Text frame type.
        - `Literal[`full`]` : Add beautiful four side frame and limit length.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
            * When throw `exception`, then frame is `half` type.
        - `Literal[`half`]` : Add beautiful top and bottom side frame.
            * When attribute `is_frame_plain` is True, then frame is `half_plain` type.
        - `Literal[`top`]` : Add beautiful top side frame.
            * When attribute `is_frame_plain` is True, then frame is `top_plain` type.
        - `Literal[`half_plain`]` : Add plain top and bottom side frame.
        - `Literal[`top_plain`]` : Add plain top side frame.

    extra : Extra print text at the end.

    Returns
    -------
    Standard input string.
    """

    # Beautify.
    text = beautify_text(data, title=title, width=width, frame=frame)

    # Extra.
    if extra is not None:
        text += extra

    # Print.
    stdin = input(text)

    return stdin


def stop_print() -> None:
    """
    Stop standard output print.
    """

    # Stop.
    global _io_null
    sys.stdout = _io_null

    # Update status.
    global _stoped
    _stoped = True


def start_print() -> None:
    """
    Start standard output print.
    """

    # Check.
    global _stoped
    if not _stoped: return

    # Start.
    global _io_stdout
    sys.stdout = _io_stdout

    # Update status.
    _stoped = False


def modify_print(preprocess: Callable[[str], Optional[str]]) -> None:
    """
    Modify standard output print write method.

    Parameters
    ----------
    preprocess : Preprocess function.
        - `Callable[[str], str]` : Input old text, output new text, will trigger printing.
        - `Callable[[str], None]` : Input old text, no output, will not trigger printing.
    """


    # Define.
    def write(__s: str) -> Optional[int]:
        """
        Modified standard output write method.

        Parameters
        ----------
        __s : Write text.

        Returns
        -------
        Number of text characters.
        """

        # Preprocess.
        __s = preprocess(__s)

        # Write.
        if __s.__class__ == str:
            global _io_stdout_write
            write_len = _io_stdout_write(__s)
            return write_len


    # Modify.
    global _io_stdout
    _io_stdout.write = write

    # Update status.
    global _modified
    _modified = True


def reset_print() -> None:
    """
    Reset standard output print write method.
    """

    # Check.
    global _modified
    if not _modified: return

    # Reset.
    global _io_stdout
    global _io_stdout_write
    _io_stdout.write = _io_stdout_write

    # Update status.
    _modified = False


def add_print_position() -> None:
    """
    Add position text to standard output.
    """


    # Define.
    def preprocess(__s: str) -> str:
        """
        Preprocess function.

        Parameters
        ----------
        __s : Standard ouput text.

        Returns
        -------
        Preprocessed text.
        """

        # Break.
        if __s in ("\n", " ", "[0m"): return __s

        # Get parameter.
        stack_params = get_stack_param("full", 3)
        stack_floor = stack_params[-1]

        ## Compatible "echo".
        if (
            stack_floor["filename"] == path_rprint
            and stack_floor["name"] == "echo"
        ):
            stack_floor = stack_params[-2]

        # Add.
        __s = 'File "%s", line %s\n%s' % (
            stack_floor["filename"],
            stack_floor["lineno"],
            __s
        )

        return __s


    # Modify.
    modify_print(preprocess)