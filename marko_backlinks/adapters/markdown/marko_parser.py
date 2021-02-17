from marko import Parser
from marko.block import Document
from marko_backlinks.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    Wikiimage,
    Wikilink,
)
from marko_backlinks.interfaces.parser import IParser


class MarkoParserImpl(IParser):
    def __init__(self):
        self.marko_parser = Parser()
        self.marko_parser.add_element(Wikilink)
        self.marko_parser.add_element(Wikiimage)
        self.marko_parser.add_element(BacklinkSection)

    def parse_filename(self, filename: str) -> Document:
        with open(filename) as file:
            text = file.read()
            ast: Document = self.marko_parser.parse(text)
            return ast
