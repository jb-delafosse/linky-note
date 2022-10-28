from typing import Dict

import os
from pathlib import Path

from linky_note.dto.dto import NotePath
from linky_note.interfaces import parser
from marko.block import Document


def parse(directory: Path) -> Dict[NotePath, Document]:
    files = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".md"):
                if dirpath != "":
                    rel_dir = Path(os.path.relpath(dirpath, directory))
                else:
                    rel_dir = Path()
                abs_path = Path(os.path.join(dirpath, filename))
                rel_path = Path(os.path.join(rel_dir, filename))
                ast = parser.PARSER.parse_file(abs_path)
                files[NotePath(rel_path)] = ast
    return files
