from typing import Dict

import glob
import os
from pathlib import Path

from marko.block import Document
from marko_backlinks.dto.dto import NotePath
from marko_backlinks.interfaces import parser


def parse(directory: Path) -> Dict[NotePath, Document]:
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        ast = parser.PARSER.parse_filename(filename)
        files[NotePath(filename)] = ast
    return files
