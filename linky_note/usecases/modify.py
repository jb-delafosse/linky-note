from typing import Dict

from linky_note.dto.dto import Note
from linky_note.interfaces import modifier
from marko.block import Document


def modify(files: Dict[Note, Document]) -> Dict[Note, Document]:
    return {
        key: modifier.MODIFIER.modify_ast(ast, key)
        for key, ast in files.items()
    }
