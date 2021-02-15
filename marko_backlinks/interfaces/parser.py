from abc import ABC, abstractmethod

from marko.block import Document


class IParser(ABC):
    @abstractmethod
    def parse_filename(self, filename: str) -> Document:
        pass


PARSER: IParser
