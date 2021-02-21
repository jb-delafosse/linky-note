from linky_note.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    Wikiimage,
    Wikilink,
)
from linky_note.dto.dto import ParseConfig
from linky_note.interfaces.parser import IParser
from marko import Parser
from marko.block import Document


class MarkoParserImpl(IParser):
    def __init__(self, parse_config: ParseConfig):
        self.marko_parser = Parser()
        if parse_config.parse_wikilinks:
            self.marko_parser.add_element(Wikilink)
        self.marko_parser.add_element(Wikiimage)
        self.marko_parser.add_element(BacklinkSection)

    def parse_filename(self, filename: str) -> Document:
        with open(filename) as file:
            text = file.read()
            ast: Document = self.marko_parser.parse(text)
            return ast
