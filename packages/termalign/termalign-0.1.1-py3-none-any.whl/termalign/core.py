from textwrap import wrap
from .utils import pad_line, indent_lines

def align_line(text: str, width: int, align: str = "left") -> str:
    if align == "left":
        return text.ljust(width)
    elif align == "right":
        return text.rjust(width)
    elif align == "center":
        return text.center(width)
    elif align == "justify":
        return justify_line(text, width)
    else:
        raise ValueError(f"Invalid alignment: {align}")

def format_block(text: str, width: int, align: str = "left") -> str:
    lines = wrap(text, width=width)
    return "\n".join(
        justify_line(line, width) if align == "justify" else align_line(line, width, align)
        for line in lines
    )

def justify_line(line: str, width: int) -> str:
    words = line.split()
    if len(words) == 1:
        return words[0].ljust(width)
    total_spaces = width - sum(len(w) for w in words)
    spaces_between = len(words) - 1
    base_space = total_spaces // spaces_between
    extras = total_spaces % spaces_between

    justified = ""
    for i, word in enumerate(words[:-1]):
        justified += word + " " * (base_space + (1 if i < extras else 0))
    justified += words[-1]
    return justified

def wrap_and_indent(text: str, width: int, indent: int = 4) -> str:
    wrapped_lines = wrap(text, width=width - indent)
    return indent_lines("\n".join(wrapped_lines), indent=indent)

def format_columns(blocks: list[str], widths: list[int], align: str = "left") -> str:
    # Split and align each block
    split_blocks = [
        [align_line(line, width, align) for line in block.splitlines()]
        for block, width in zip(blocks, widths)
    ]
    # Pad block heights
    max_lines = max(len(b) for b in split_blocks)
    padded_blocks = [
        b + [" " * widths[i]] * (max_lines - len(b))
        for i, b in enumerate(split_blocks)
    ]
    # Combine line by line
    return "\n".join("  ".join(parts) for parts in zip(*padded_blocks))
