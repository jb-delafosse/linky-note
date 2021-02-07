from abc import ABC, abstractmethod

from marko_backlinks.usecases.marko_ext.elements import Document


class IConverter(ABC):
    @abstractmethod
    def parse_filename(self, filename: str) -> Document:
        pass

    @abstractmethod
    def render(self, ast: Document) -> str:
        pass


CONVERTER: IConverter
