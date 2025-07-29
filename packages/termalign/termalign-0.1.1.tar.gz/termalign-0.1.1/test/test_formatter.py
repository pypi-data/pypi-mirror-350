
from termalign.formatter import TextFormatter

def test_textformatter_left():
    fmt = TextFormatter(width=20, align="left", indent=2, border=False)
    result = fmt.format("hello")
    lines = result.splitlines()
    assert all(line.startswith("  ") for line in lines)
    assert "hello" in result

def test_textformatter_center_with_border():
    fmt = TextFormatter(width=30, align="center", indent=0, border=True)
    result = fmt.format("centered text")
    lines = result.splitlines()
    assert lines[0].startswith("+")  # top border
    assert "centered text" in result

def test_textformatter_justify():
    text = "this is a long line that should be justified nicely"
    fmt = TextFormatter(width=40, align="justify", indent=0, border=False)
    formatted = fmt.format(text)
    for line in formatted.splitlines():
        assert len(line) == 40
