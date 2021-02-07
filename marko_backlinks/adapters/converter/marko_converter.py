from marko import Markdown
from marko_backlinks.interfaces.converter import IConverter
from marko_backlinks.usecases.marko_ext.elements import Document


class MarkoConverterImpl(IConverter):
    def __init__(self, marko: Markdown):
        self.marko = marko

    def parse_filename(self, filename: str) -> Document:
        with open(filename) as file:
            text = file.read()
            ast: Document = self.marko.parse(text)
        return ast

    def render(self, ast: Document) -> str:
        text: str = self.marko.render(ast)
        return text
