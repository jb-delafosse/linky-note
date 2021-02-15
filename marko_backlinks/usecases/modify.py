from typing import Dict

from marko.block import Document
from marko_backlinks.dto.dto import Note
from marko_backlinks.interfaces import modifier


def modify(files: Dict[Note, Document]) -> Dict[Note, Document]:
    return {
        key: modifier.MODIFIER.modify_ast(ast, key)
        for key, ast in files.items()
    }
