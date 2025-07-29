from .multicolumn import MultiColumnFormatter

class ColumnBuilder:
    def __init__(self, text: str):
        self.text = text
        self.config = {
            "width": 30,
            "align": "left",
            "indent": 0,
            "border": False,
        }

    def width(self, value: int): self.config["width"] = value; return self
    def align(self, value: str): self.config["align"] = value; return self
    def indent(self, value: int): self.config["indent"] = value; return self
    def border(self, value: bool = True): self.config["border"] = value; return self

class ColumnLayout:
    @classmethod
    def from_builders(cls, *builders: ColumnBuilder) -> MultiColumnFormatter:
        configs = [b.config for b in builders]
        texts = [b.text for b in builders]
        return MultiColumnFormatter(configs)._with_texts(texts)
