from typing import Dict

from marko.block import Document
from marko_backlinks.dto.dto import Note
from marko_backlinks.interfaces import renderer


def write(files: Dict[Note, Document]) -> None:
    for note, ast in files.items():
        with open(note.note_path, "w") as file:
            with renderer.RENDERER as _renderer:
                text = _renderer.render(ast)
                file.write(text)
