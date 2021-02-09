from typing import AnyStr, List, Union

from marko import Parser, block
from marko.helpers import Source


class ReferenceParser(Parser):
    def parse(
        self, source_or_text
    ):  # type: (Union[Source, AnyStr]) -> Union[List[block.BlockElement], block.BlockElement]
        ast = super().parse(source_or_text=source_or_text)
        return ast
