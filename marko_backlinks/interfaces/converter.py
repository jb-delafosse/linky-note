from typing import List

from abc import ABC, abstractmethod
from dataclasses import dataclass

from marko_backlinks.dto.dto import Note, ParsedReference
from marko_backlinks.usecases.marko_ext.elements import Document


@dataclass(frozen=True)
class ParseFilenameResult:
    ast: Document
    references: List[ParsedReference]
    note: Note


class IConverter(ABC):
    @abstractmethod
    def parse_filename(self, filename: str) -> ParseFilenameResult:
        pass

    @abstractmethod
    def render(self, ast: Document) -> str:
        pass


CONVERTER: IConverter
