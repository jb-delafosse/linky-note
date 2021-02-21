from abc import ABC, abstractmethod

from marko.block import Document
from marko_backlinks.dto.dto import ModifyConfig, Note
from marko_backlinks.interfaces.references_db import ReferenceDbFactory


class IModifier(ABC):
    def __init__(
        self, db_factory: ReferenceDbFactory, modify_config: ModifyConfig
    ):
        self.reference_db = db_factory(modify_config)
        self.modify_config = modify_config

    @abstractmethod
    def modify_ast(self, ast: Document, note: Note) -> Document:
        pass


MODIFIER: IModifier
