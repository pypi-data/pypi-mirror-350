
# Termalign

**Termalign** is a lightweight Python module for advanced text formatting and alignment in terminals, logs, CLI output, and simple plain-text reports.

It provides intuitive functions and classes to align, format, wrap, colorize, and decorate text with optional borders and multi-column layouts.

---

## Features

- Align text: left, right, center, justify
- Wrap and indent multiline text
- Add decorative or structural ASCII/Unicode borders
- Apply color and bold styling (ANSI-compatible)
- Define reusable formatting styles
- Easily create multi-column text layouts
- Simple API (`format_table`) for quick use
- Advanced API (`TextFormatter`, `ColumnBuilder`) for full control

---

## Installation

```bash
# Clone or copy this module into your project
# or install manually via pip (in development)
pip install -e .
```

---

## Usage Examples

### Align a single line

```python
from termalign import align_line

print(align_line("Hello", width=20, align="center"))
# --> "       Hello        "
```

### Format a block of text

```python
from termalign import format_block

text = "Python is a powerful, readable, and versatile programming language."
print(format_block(text, width=40, align="justify"))
#Python  is  a  powerful,  readable,  and
#versatile      programming     language.

```

### Use a reusable formatter

```python
from termalign import TextFormatter

fmt = TextFormatter(width=50, align="center", indent=4, border=True)
print(fmt.format("Centered and bordered text"))
#    +------------------------------------------------+
#    |           Centered and bordered text           |
#    +------------------------------------------------+

```

### Add a border (ASCII, Unicode, Double, Dashed, DoubleDashed)

```python
from termalign.utils import add_border

print(add_border("Hello World", style="unicode"))
#┌─────────────┐
#│ Hello World │
#└─────────────┘

```

### Apply color

```python
from termalign.utils import colorize

print(colorize("Success!", "green", bold=True))
print(colorize("Warning!", "yellow"))
print(colorize("Error!", "red"))
```

---

## Format a Table (the easiest way!)

```python
from termalign import format_table

print(format_table(
    texts=[
        "Full name of the participant",
        "Subject age",
        "Current city of residence"
    ],
    widths=[30, 20, 40],
    aligns=["left", "center", "right"],
    borders=True
))
#+--------------------------------+  +----------------------+  +------------------------------------------+
#| Full name of the participant   |  |     Subject age      |  |                Current city of residence |
#+--------------------------------+  +----------------------+  +------------------------------------------+
```

---

## Advanced Usage with `ColumnBuilder`

```python
from termalign import ColumnBuilder, ColumnLayout

layout = ColumnLayout.from_builders(
    ColumnBuilder("Left Column").width(30).align("left").border(),
    ColumnBuilder("Center Column").width(20).align("center").border(),
    ColumnBuilder("Right Column").width(40).align("right").indent(2).border()
)

print(layout.format())
#+--------------------------------+  +----------------------+    +----------------------------------------+
#| Left Column                    |  |    Center Column     |    |                           Right Column |
#+--------------------------------+  +----------------------+    +----------------------------------------+

```

---

## Tools Reference

### Core Functions
- `align_line(text, width, align)`: Align a single line.
- `format_block(text, width, align)`: Wrap and align multiple lines.
- `wrap_and_indent(text, width, indent)`: Wrap text with paragraph-style indentation.
- `format_columns(blocks, widths, align)`: Combine pre-formatted blocks into columns.

### Formatting Utilities
- `pad_line(text, width)`: Manually pad a string.
- `indent_lines(text, indent)`: Add indentation to each line.
- `add_border(text, style)`: Wrap text with a border (`ascii`, `unicode`, `double`, `dashed`, `DoubleDashed`).
- `colorize(text, color, bold=False)`: Apply terminal ANSI color and bold style.

### High-Level Interfaces
- `TextFormatter(width, align, indent, border)`: Object for reusable formatting config.
- `format_table(...)`: Quick function to build table with one-liners.
- `ColumnBuilder(text)`: Fluent builder for defining a column.
- `ColumnLayout.from_builders(...)`: Combine columns with full control.

---

## License

MIT License
