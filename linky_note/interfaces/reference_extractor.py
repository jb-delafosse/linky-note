from typing import Callable, List, Tuple

from abc import ABC, abstractmethod
from pathlib import Path

from linky_note.dto.dto import Note, NotePath, Reference
from marko.block import Document


class IExtractor(ABC):
    def __init__(self, filepath: NotePath):
        self.filepath = filepath

    @abstractmethod
    def extract_references(self, ast: Document) -> Tuple[Note, List[Reference]]:
        pass


ReferenceExtractorFactory = Callable[[NotePath], IExtractor]
EXTRACTOR_FACTORY: ReferenceExtractorFactory
