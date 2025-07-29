import re

# --- Generic Padding ---
def pad_line(text: str, width: int, char: str = " ") -> str:
    """Generic padding helper."""
    return text + char * max(0, width - len(text))


# --- Indentation ---
def indent_lines(text: str, indent: int = 4, char: str = " ") -> str:
    prefix = char * indent
    return "\n".join(prefix + line for line in text.splitlines())


# --- Borders ---
def add_border(text: str, style: str = "ascii") -> str:
    lines = text.splitlines()
    width = max(len(strip_ansi(line)) for line in lines)

    if style == "ascii":
        tl, tr, bl, br, h, v = "+", "+", "+", "+", "-", "|"
    elif style == "double":
        tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
    elif style == "unicode":
        tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"
    elif style == "dashed":
        tl, tr, bl, br, h, v = "+", "+", "+", "+", ".", "|"
    elif style == "doubledashed":
        tl, tr, bl, br, h, v = "+ ", " +", "+ ", " +", ":", "||"
    else:
        raise ValueError(f"Unsupported border style: {style}")

    top_line = f"{tl}{h * (width + 2)}{tr}"
    bottom_line = f"{bl}{h * (width + 2)}{br}"
    middle = [f"{v} {ansi_ljust(line, width)} {v}" for line in lines]

    return "\n".join([top_line] + middle + [bottom_line])


## Regex para detectar secuencias ANSI
_ansi_escape = re.compile(r"\x1b\[[0-9;]*m")

def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text."""
    return _ansi_escape.sub("", text)

def ansi_len(text: str) -> int:
    """Length of text without ANSI codes (visual length)."""
    return len(strip_ansi(text))

def ansi_ljust(text: str, width: int, fillchar: str = " ") -> str:
    """Left-justify while keeping ANSI codes in place."""
    return text + fillchar * max(0, width - ansi_len(text))

def ansi_rjust(text: str, width: int, fillchar: str = " ") -> str:
    """Right-justify while keeping ANSI codes in place."""
    return fillchar * max(0, width - ansi_len(text)) + text

def ansi_center(text: str, width: int, fillchar: str = " ") -> str:
    """Center text while preserving ANSI codes."""
    pad = max(0, width - ansi_len(text))
    left = pad // 2
    right = pad - left
    return fillchar * left + text + fillchar * right

def colorize(text: str, color: str = "white", bold: bool = False, width: int = None, align: str = "left") -> str:
    """Apply ANSI color and bold style, with optional width-based alignment."""
    COLORS = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37", "reset": "0"
    }
    code = COLORS.get(color.lower(), "37")
    ansi = f"\033[1;{code}m{text}\033[0m" if bold else f"\033[{code}m{text}\033[0m"

    if width is None:
        return ansi

    # Alineación visual si se da width
    if align == "center":
        return ansi_center(ansi, width)
    elif align == "right":
        return ansi_rjust(ansi, width)
    else:
        return ansi_ljust(ansi, width)
