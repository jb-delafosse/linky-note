from typing import Callable, List, Tuple

from abc import ABC, abstractmethod

from marko.block import Document
from marko_backlinks.dto.dto import Note, Reference


class IExtractor(ABC):
    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def extract_references(self, ast: Document) -> Tuple[Note, List[Reference]]:
        pass


ReferenceExtractorFactory = Callable[[str], IExtractor]
EXTRACTOR_FACTORY: ReferenceExtractorFactory
