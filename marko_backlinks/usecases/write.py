from typing import Dict

from marko_backlinks.interfaces import converter
from marko_backlinks.usecases.marko_ext.elements import Document


def write(files: Dict[str, Document]) -> None:
    for filename, ast in files.items():
        with open(filename, "w") as file:
            text = converter.CONVERTER.render(ast)
            file.write(text)
