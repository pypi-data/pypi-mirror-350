from .core import format_columns
from .formatter import TextFormatter

class MultiColumnFormatter:
    def __init__(self, configs: list[dict]):
        self.formatters = [TextFormatter(**cfg) for cfg in configs]

    def _with_texts(self, texts: list[str]):
        self._texts = texts
        return self

    def format(self) -> str:
        return self._format_with_texts(self._texts)

    def _format_with_texts(self, texts: list[str]) -> str:
        if len(texts) != len(self.formatters):
            raise ValueError("Number of texts must match number of column configurations.")
        blocks = [fmt.format(text) for fmt, text in zip(self.formatters, texts)]
        widths = [
            fmt.width + (2 if fmt.border else 0) + fmt.indent
            for fmt in self.formatters
        ]
        return format_columns(blocks, widths=widths, align='left')
