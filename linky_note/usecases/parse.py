from typing import Dict

import glob
import os
from pathlib import Path

from linky_note.dto.dto import NotePath
from linky_note.interfaces import parser
from marko.block import Document


def parse(directory: Path) -> Dict[NotePath, Document]:
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        ast = parser.PARSER.parse_filename(filename)
        files[NotePath(filename)] = ast
    return files
