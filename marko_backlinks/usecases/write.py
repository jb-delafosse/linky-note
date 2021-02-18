from typing import Dict

import os
from pathlib import Path

from marko.block import Document
from marko_backlinks.dto.dto import Note
from marko_backlinks.interfaces import renderer


def write(files: Dict[Note, Document], directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for note, ast in files.items():
        with open(os.path.join(directory, note.note_path), "w+") as file:
            with renderer.RENDERER as _renderer:
                text = _renderer.render(ast)
                file.write(text)
