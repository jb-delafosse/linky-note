from abc import ABC, abstractmethod
from pathlib import Path

from marko.block import Document


class IParser(ABC):
    @abstractmethod
    def parse_file(self, filepath: Path) -> Document:
        pass


PARSER: IParser
