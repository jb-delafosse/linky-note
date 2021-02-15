from typing import List, Optional, Tuple, Union

from marko.block import BlockElement, Document, Heading
from marko.inline import InlineElement, Link
from marko.md_renderer import MarkdownRenderer
from marko_backlinks.adapters.markdown.marko_ext.elements import Wikilink
from marko_backlinks.common.exceptions import InvalidNoteError
from marko_backlinks.dto.dto import Note, NotePath, NoteTitle, Reference
from marko_backlinks.interfaces.reference_extractor import IExtractor

Element = Union[BlockElement, InlineElement]


class MarkoExtractor(IExtractor):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.md_renderer = MarkdownRenderer()
        self.note_title = None

    def extract_references(self, ast: Document) -> Tuple[Note, List[Reference]]:
        return self._extract(element=ast, references=[], parent=None)

    def _extract(
        self,
        element: Union[List, Element, str],
        references: List[Reference],
        parent: Optional[Element],
    ) -> Tuple[Note, List[Reference]]:
        """Renders the given element to string.

        :param element: a element to be rendered.
        :returns: the output string or any values.
        """

        if isinstance(element, Heading):
            self._extract_note_title(element)
        if isinstance(element, Link):
            references.append(self._extract_link(element, parent))
        if isinstance(element, Wikilink):
            references.append(self._extract_wikilink(element, parent))
        if isinstance(element, list):
            for child in element:
                self._extract(
                    element=child, references=references, parent=element
                )
        if hasattr(element, "children"):
            self._extract_deeper(element, self.note_title, references)
        return (
            Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(self.filename),
            ),
            references,
        )

    def _extract_deeper(self, element, note_title, references):

        if isinstance(element, str):
            pass
        else:
            self._extract(
                element.children, references=references, parent=element
            )

    def _extract_link(self, element: Link, parent: Element) -> Reference:
        if not self.note_title:
            raise InvalidNoteError(
                message=f"No title found in {self.filename}."
            )
        if not parent:
            raise InvalidNoteError(
                message=f"Found title at root level in {self.filename}."
            )
        return Reference(
            source_note=Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(self.filename),
            ),
            target_note=Note(
                note_title=NoteTitle(
                    element.title or element.children[0].children
                ),
                note_path=NotePath(element.dest),
            ),
            context="".join(self.md_renderer.render(item) for item in parent),
        )

    def _extract_wikilink(self, element: Wikilink, parent) -> Reference:
        if not self.note_title:
            raise InvalidNoteError(
                message=f"No title found in {self.filename}."
            )
        if not parent:
            raise InvalidNoteError(
                message=f"Found title at root level in {self.filename}."
            )
        return Reference(
            source_note=Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(self.filename),
            ),
            target_note=Note(
                note_title=NoteTitle(element.label),
                note_path=NotePath(element.dest),
            ),
            context="".join(self.md_renderer.render(item) for item in parent),
        )

    def _extract_note_title(self, element):
        if element.level == 1:
            if self.note_title:
                raise InvalidNoteError(
                    message=f"Two titles found in {self.filename}."
                )
            self.note_title = element.children[0].children
