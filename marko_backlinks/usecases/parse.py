from typing import Dict

import glob
import os
from pathlib import Path

from marko_backlinks.interfaces import converter
from marko_backlinks.usecases.marko_ext.elements import Document


def parse(directory: Path) -> Dict[str, Document]:
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        parse_result = converter.CONVERTER.parse_filename(filename)
        files[filename] = parse_result.ast
    return files
