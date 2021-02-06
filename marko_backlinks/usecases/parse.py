from typing import Dict

import glob
import os
from pathlib import Path

from marko_backlinks.interfaces import converter
from marko_backlinks.usecases.marko_ext.elements import Document


def parse(directory: Path) -> Dict[str, Document]:
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        with open(filename) as file:
            ast = converter.CONVERTER.parse(file.read())
            files[filename] = ast
    return files
