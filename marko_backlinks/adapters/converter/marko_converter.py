from marko import Markdown
from marko_backlinks.common.exceptions import InvalidNoteError
from marko_backlinks.interfaces.converter import IConverter, ParseFilenameResult
from marko_backlinks.usecases.marko_ext.elements import Document


class MarkoConverterImpl(IConverter):
    def __init__(self, marko: Markdown):
        self.marko = marko

    def parse_filename(self, filename: str) -> ParseFilenameResult:
        with open(filename) as file:
            text = file.read()
            ast: Document = self.marko.parse(text)
            if not ast.source_note:
                raise InvalidNoteError(
                    message=f"could not find title in {filename}"
                )
            return ParseFilenameResult(
                ast=ast, references=ast.references, note=ast.source_note
            )

    def render(self, ast: Document) -> str:
        text: str = self.marko.render(ast)
        return text
