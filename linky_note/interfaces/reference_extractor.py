from typing import Callable, List, Tuple

from abc import ABC, abstractmethod

from linky_note.dto.dto import Note, Reference
from marko.block import Document


class IExtractor(ABC):
    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def extract_references(self, ast: Document) -> Tuple[Note, List[Reference]]:
        pass


ReferenceExtractorFactory = Callable[[str], IExtractor]
EXTRACTOR_FACTORY: ReferenceExtractorFactory
