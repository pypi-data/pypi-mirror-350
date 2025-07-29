
import pytest
from termalign.core import align_line, format_block, wrap_and_indent, format_columns

def test_align_line_left():
    assert align_line("hi", 5, "left") == "hi   "

def test_align_line_right():
    assert align_line("hi", 5, "right") == "   hi"

def test_align_line_center():
    assert align_line("hi", 5, "center") == "  hi "


def test_align_line_justify():
    result = align_line("a b", 5, "justify")
    assert result == "a   b"  # 3 spaces to justify

def test_align_line_invalid():
    with pytest.raises(ValueError):
        align_line("text", 10, "diagonal")

def test_format_block_left():
    text = "Python is great"
    result = format_block(text, width=10, align="left").splitlines()
    assert all(len(line) == 10 for line in result)
    assert result[0].startswith("Python")

def test_format_block_justify():
    text = "Justify this line evenly"
    lines = format_block(text, width=24, align="justify").splitlines()
    assert all(len(line) == 24 for line in lines)

def test_wrap_and_indent():
    text = "Indent this block of text properly across multiple lines."
    wrapped = wrap_and_indent(text, width=40, indent=4).splitlines()
    assert all(line.startswith("    ") for line in wrapped)

def test_format_columns_alignment():
    col1 = "left\ncolumn"
    col2 = "right\ntext"
    col3 = "center\nblock"
    result = format_columns([col1, col2, col3], [10, 10, 10], align="left").splitlines()
    assert len(result) == 2
    assert result[0].startswith("left") and result[1].startswith("column")
