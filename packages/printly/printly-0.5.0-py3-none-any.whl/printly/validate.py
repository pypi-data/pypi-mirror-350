"""Defines `validate_color()`, `validate_font_style()`."""

import re
from difflib import get_close_matches
from .types import Color, FontStyle
from .const import FS_CODES, HEX_PREFIX, RGB_DELIMITER, RGB_VALUES


def validate_color(color: Color) -> Color:
    """Validates a color to check if it is supported."""
    color = re.sub(r"(\s+|-+)", "", f"{color}").lower()
    if HEX_PREFIX in color:
        if not re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color):
            raise ValueError(f"Invalid HEX color '{color!r}'. Must be '#rgb' or '#rrggbb'.")
        if len(hex_digits := color[1:]) == 3:
            color = f"#{"".join(d * 2 for d in hex_digits)}"
    elif RGB_DELIMITER in color:
        if not re.match(r"^\d{,3},\d{,3},\d{,3}$", color):
            raise ValueError(f"Invalid RGB color {color!r}. Must be in the format 'r,g,b'.")
        if not all((0 <= int(v) <= 255 for v in color.split(RGB_DELIMITER))):
            raise ValueError(f"Invalid RGB color '{color}'. RGB values must be in range 0-255.")
    else:
        if color not in (valid_colors := tuple(RGB_VALUES)):
            if closest := ", ".join(get_close_matches(color, RGB_VALUES, n=1)):
                raise ValueError(f"Invalid color name {color!r}. Did you mean {closest!r}?")
            raise ValueError(f"Invalid color name '{color}'. Expected one of {tuple(valid_colors)}")
    return color


def validate_font_style(font_style: FontStyle) -> FontStyle:
    """Validates a font style to check if it is supported."""
    font_style = re.sub(r"\s+", "", f"{font_style}").lower()
    if font_style not in (font_styles := FS_CODES):
        if closest := ", ".join(get_close_matches(font_style, FS_CODES, n=1)):
            raise ValueError(f"Invalid font style {font_style!r}. Did you mean {closest!r}?")
        raise ValueError(f"Invalid font style {font_style!r}. Expected one of {tuple(font_styles)}")
    return font_style
