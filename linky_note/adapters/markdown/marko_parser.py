from pathlib import Path

from linky_note.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    FrontMatter,
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
        if parse_config.parse_frontmatter:
            self.marko_parser.add_element(FrontMatter)
        self.marko_parser.add_element(Wikiimage)
        self.marko_parser.add_element(BacklinkSection)

    def parse_file(self, filepath: Path) -> Document:
        with open(filepath) as file:
            text = file.read()
            ast: Document = self.marko_parser.parse(text)
            return ast
