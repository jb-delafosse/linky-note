from abc import ABC, abstractmethod

from marko.block import Document


class IRenderer(ABC):
    @abstractmethod
    def render(self, ast: Document) -> str:
        pass


RENDERER: IRenderer
