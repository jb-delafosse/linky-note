from abc import ABC, abstractmethod

from linky_note.dto.dto import ModifyConfig, Note
from linky_note.interfaces import references_db
from marko.block import Document


class IModifier(ABC):
    def __init__(self, modify_config: ModifyConfig):
        self.reference_db = references_db.REFERENCE_DB_FACTORY(modify_config)
        self.modify_config = modify_config

    @abstractmethod
    def modify_ast(self, ast: Document, note: Note) -> Document:
        pass


MODIFIER: IModifier
