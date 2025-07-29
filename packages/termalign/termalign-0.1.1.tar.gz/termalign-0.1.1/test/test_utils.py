
import pytest
from termalign.utils import pad_line, indent_lines, add_border, colorize

def test_pad_line_short():
    assert pad_line("abc", 6) == "abc   "

def test_pad_line_exact():
    assert pad_line("abcdef", 6) == "abcdef"

def test_indent_lines_basic():
    input_text = "line1\nline2"
    result = indent_lines(input_text, indent=2)
    assert result == "  line1\n  line2"

def test_add_border_ascii():
    input_text = "Hello"
    bordered = add_border(input_text, style="ascii").splitlines()
    assert bordered[0].startswith("+") and bordered[-1].startswith("+")

def test_add_border_unicode():
    input_text = "Hola"
    bordered = add_border(input_text, style="unicode").splitlines()
    assert bordered[0].startswith("┌") and bordered[-1].startswith("└")

def test_add_border_double():
    input_text = "Hola"
    bordered = add_border(input_text, style="double").splitlines()
    assert bordered[0].startswith("╔") and bordered[-1].startswith("╚")

def test_add_border_invalid():
    with pytest.raises(ValueError):
        add_border("text", style="fake")

def test_colorize_green():
    colored = colorize("ok", color="green")
    assert "\033[32m" in colored and colored.endswith("\033[0m")

def test_colorize_bold_red():
    colored = colorize("error", color="red", bold=True)
    assert "\033[1;31m" in colored
