from termalign.table import format_table

def test_format_table_basic():
    output = format_table(
        texts=["one", "two"],
        widths=[10, 10],
        aligns=["left", "right"],
        borders=True
    )
    assert "+" in output  # ascii border
    assert "one" in output
    assert "two" in output

def test_format_table_with_indent():
    output = format_table(
        texts=["column1", "column2"],
        widths=[15, 15],
        aligns=["left", "right"],
        borders=False,
        indents=[2, 4]
    )
    lines = output.splitlines()
    assert all(line.startswith("  ") or line.startswith("    ") for line in lines)
