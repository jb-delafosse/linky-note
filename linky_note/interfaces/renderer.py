from abc import ABC, abstractmethod

from marko.block import Document


class IRenderer(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def render(self, ast: Document) -> str:
        pass


RENDERER: IRenderer
