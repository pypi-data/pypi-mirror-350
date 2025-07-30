# Printly
[![PyPI - Version](https://img.shields.io/pypi/v/printly)](https://pypi.org/project/printly/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/printly)](https://pypi.org/project/printly/)
[![License](https://img.shields.io/pypi/l/printly)](https://github.com/haripowesleyt/printly/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/printly)](https://pypi.org/project/printly/)

Printly is a Python library that enhances the built-in print function with direct text styling: foreground color (`fg`), background color (`bg`), and font styles (`fs`).

## Features
- **Colors:**
  - Supports over 140 color names ([from HTML](https://htmlcolorcodes.com/color-names/))
  - Supports all RGB values (e.g., `"128,0,128"`)
  - Supports all HEX color codes (e.g., `"#ff00ff"`)
- **Font Styles:**
  - Supports 7 font styles: `bold`, `italic`, `strikethrough`, `underline`, `overline`, `double-underline`, `hidden`.
  - Supports combining multiple font styles (e.g., `"bold+italic"`)
- **Compatibility:**
  - Supports all standard `print()` parameters: `sep`, `end`, `file`, `flush`.

## Installation
```bash
pip install printly
```

## Usage

### 1. `print()` Function
An enhanced version of the built-in `print()` function.

#### Example 1 (Recommended)
```python
import printly
printly.print("Hello, world!", fg="red", bg="white", fs="bold")
```
![usage-print-recommended](https://raw.githubusercontent.com/haripowesleyt/printly/main/assets/images/usage-print-recommended.png)

#### Example 2 (Override Built-in `print()`)
```python
from printly import print
print("I am a hacker!", fg="lime", bg="black", fs="bold+italic")
```
![usage-print-override](https://raw.githubusercontent.com/haripowesleyt/printly/main/assets/images/usage-print-override.png)

### 2. `style()` Function
Apply foreground color, background color, and font style to text.

#### Example
```python
from printly import style
print(style("I love you! 💓", fg="deeppink", bg="hotpink", fs="bold"))
```
![usage-style](https://raw.githubusercontent.com/haripowesleyt/printly/main/assets/images/usage-style.png)

## License
This project is licensed under the **MIT License** – see the [LICENSE](https://raw.githubusercontent.com/haripowesleyt/printly/main/LICENSE) file for details.
