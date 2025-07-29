
from .columns import ColumnBuilder, ColumnLayout

def format_table(
    texts: list[str],
    widths: list[int],
    aligns: list[str] = None,
    borders: bool = False,
    indents: list[int] = None
) -> str:
    """
    Formats multiple blocks of text as aligned columns in a table.

    Args:
        texts: List of text blocks for each column.
        widths: Width of each column.
        aligns: Alignment for each column ('left', 'center', 'right', 'justify').
        borders: Whether to use ASCII borders around each column.
        indents: Left indentation for each column.

    Returns:
        A string with the text formatted into aligned columns.
    """

    if aligns is None:
        aligns = ["left"] * len(texts)
    if indents is None:
        indents = [0] * len(texts)

    builders = [
        ColumnBuilder(text)
        .width(widths[i])
        .align(aligns[i])
        .indent(indents[i])
        .border(borders)
        for i, text in enumerate(texts)
    ]

    return ColumnLayout.from_builders(*builders).format()
