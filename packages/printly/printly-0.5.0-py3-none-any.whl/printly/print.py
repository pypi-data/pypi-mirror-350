"""Defines `print()` function."""

import sys
from typing import Any, Optional, TextIO
from .style import style
from .types import Color, FontStyle

builtin_print = print  # pylint: disable=used-before-assignment


def print(  # pylint: disable=redefined-builtin, too-many-arguments
    *objects: Any,
    sep: Optional[str] = " ",
    end: Optional[str] = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
    fg: Optional[Color] = None,
    bg: Optional[Color] = None,
    fs: Optional[FontStyle] = None,
) -> None:
    """Prints values to a stream (defaults to sys.stdout) with optional text styling (color, font).

    Args:
        *objects (Any): The objects to print.
        sep (str | None): The string used to separate the objects. Defaults to " ".
        end (str | None): The string printed after the last object. Defaults to "\\n".
        file (TextIO | None): A file-like object (stream) to which the objects are printed. \
            Defaults to `sys.stdout`.
        flush (bool): Whether to forcibly flush the stream. Defaults to `False`.
        fg (Color | None): Foreground color for the text. Defaults to `None`.
        bg (Color | None): Background color for the text. Defaults to `None`.
        fs (FontStyle | None): Font style for the text. Defaults to `None`.
    """
    if (fg or bg or fs) and (file is None or file in sys.stdout, sys.stderr):
        objects = tuple(style(f"{object}", fg=fg, bg=bg, fs=fs) for object in objects)
        sep = style(f"{sep}", fg=fg, bg=bg, fs=fs) if sep else sep
        end = style(f"{end}", fg=fg, bg=bg, fs=fs) if end else end
    builtin_print(*objects, sep=sep, end=end, file=file, flush=flush)
