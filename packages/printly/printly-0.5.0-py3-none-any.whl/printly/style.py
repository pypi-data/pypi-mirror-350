"""Defines `style()` and `unstyle()`."""

import re
from typing import Iterator, Optional, Tuple
from .types import Color, FontStyle
from .validate import validate_color, validate_font_style
from .const import FS_CODES, FS_DELEMITER, HEX_PREFIX, RGB_DELIMITER, RGB_VALUES, RESET_CODE


def get_rgb_values(color: Color) -> Tuple[int, ...]:
    """Gets the RGB values of a given color."""
    color = validate_color(color)
    if color.startswith(HEX_PREFIX):
        return tuple(int(color[1:][i : i + 2], base=16) for i in range(0, 6, 2))
    if RGB_DELIMITER in color:
        return tuple(map(int, color.split(RGB_DELIMITER)))
    return RGB_VALUES[color]


def get_fs_codes(font_style: FontStyle) -> Iterator[int]:
    """Converts given font styles to font style codes."""
    for fs in font_style.split(FS_DELEMITER):
        yield FS_CODES[validate_font_style(fs)]


def style(
    text: str,
    fg: Optional[Color] = None,
    bg: Optional[Color] = None,
    fs: Optional[FontStyle] = None,
) -> str:
    """
    Applies foreground color, background color, and font style to text.

    Args:
        text (str): The text to be styled.
        fg (Color | None): Foreground color for the text. Defaults to `None`.
        bg (Color | None): Background color for the text. Defaults to `None`.
        fs (FontStyle | None): Font style(s) for the text. Defaults to `None`.

    Returns:
        str: Styled text.
    """
    if fg or bg or fs:
        fg_code = f"\033[38;2;{';'.join(map(str, get_rgb_values(fg)))}m" if fg else ""
        bg_code = f"\033[48;2;{';'.join(map(str, get_rgb_values(bg)))}m" if bg else ""
        fs_code = "".join((f"\033[{code}m" for code in get_fs_codes(fs))) if fs else ""
        styles = fg_code + bg_code + fs_code
        styled_text = styles + text.replace(RESET_CODE, f"{RESET_CODE}{styles}")
        styled_text = styled_text.replace("\n", f"{RESET_CODE}\n{styles}")
        return styled_text + (RESET_CODE if not styled_text.endswith(RESET_CODE) else "")
    return text


def unstyle(text: str) -> str:
    """Removes printly styles from text."""
    return re.sub(
        "(\033\\[(0|1|3|4|8|9|21|53)m|\033\\[(38|48);2;(\\d{,3};){2}\\d{,3}m)", "", f"{text}"
    )
