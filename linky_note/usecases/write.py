from typing import Dict

import os
from pathlib import Path

from linky_note.dto.dto import Note
from linky_note.interfaces import renderer
from marko.block import Document


def write(files: Dict[Note, Document], directory: Path) -> None:
    for note, ast in files.items():
        dir_ = os.path.join(directory, note.note_path)
        Path(os.path.dirname(dir_)).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(directory, note.note_path), "w+") as file:
            with renderer.RENDERER as _renderer:
                text = _renderer.render(ast)
                file.write(text)
