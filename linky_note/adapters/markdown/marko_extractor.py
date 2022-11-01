from typing import List, Optional, Tuple, Union

import os.path
from pathlib import Path

from linky_note.adapters.markdown.marko_ext.elements import Wikilink
from linky_note.common.exceptions import InvalidNoteError
from linky_note.dto.dto import (
    Note,
    NotePath,
    NoteTitle,
    Reference,
    ReferenceContext,
)
from linky_note.interfaces.reference_extractor import IExtractor
from marko.block import BlockElement, Document, Heading
from marko.inline import InlineElement, Link
from marko.md_renderer import MarkdownRenderer

Element = Union[BlockElement, InlineElement]


class MarkoExtractor(IExtractor):
    def __init__(self, filepath: NotePath):
        super().__init__(filepath)
        self.md_renderer = MarkdownRenderer()
        self.note_title: Optional[str] = None

    def extract_references(self, ast: Document) -> Tuple[Note, List[Reference]]:
        return self._extract(element=ast, references=[], parent=None)

    def _extract(
        self,
        element: Union[List[Element], Element, str],
        references: List[Reference],
        parent: Optional[Union[Element, List[Element]]],
    ) -> Tuple[Note, List[Reference]]:
        if isinstance(element, Heading):
            self._extract_note_title(element)
        if isinstance(element, Link):
            if not isinstance(parent, List):
                raise InvalidNoteError(
                    f"Expected a list as parent for the link and got {parent}."
                )
            else:
                references.append(self._extract_link(element, parent))
        if isinstance(element, Wikilink):
            references.append(self._extract_wikilink(element, parent))
        if isinstance(element, list):
            for child in element:
                self._extract(
                    element=child, references=references, parent=element
                )
        if hasattr(element, "children"):
            self._extract_deeper(element, references)
        if not self.note_title:
            raise InvalidNoteError(
                message=f"No title found in {self.filepath}."
            )
        return (
            Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(Path(self.filepath)),
            ),
            references,
        )

    def _extract_deeper(self, element, references):

        if isinstance(element, str):
            pass
        else:
            self._extract(
                element.children, references=references, parent=element
            )

    def _extract_link(self, element: Link, parent: List[Element]) -> Reference:
        if not self.note_title:
            raise InvalidNoteError(
                message=f"No title found in {self.filepath}."
            )
        root = Path("/")
        file_dir = (root / self.filepath).parent
        abs_target_path = Path(os.path.abspath(file_dir / Path(element.dest)))
        rel_target_path = Path(os.path.relpath(abs_target_path, start=root))
        context = self._build_context(parent)
        return Reference(
            source_note=Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(self.filepath),
            ),
            target_note=Note(
                note_title=NoteTitle(
                    element.title or element.children[0].children
                ),
                note_path=NotePath(rel_target_path),
            ),
            context=ReferenceContext(context),
        )

    def _build_context(self, parent):
        context = ""
        for item in parent:
            if isinstance(item, Wikilink):
                context += f"**{item.label}**"
            elif isinstance(item, Link):
                context += f"**{item.title or item.children[0].children}**"
            else:
                context += self.md_renderer.render(item)
        return context

    def _extract_wikilink(self, element: Wikilink, parent) -> Reference:
        if not self.note_title:
            raise InvalidNoteError(
                message=f"No title found in {self.filepath}."
            )
        context = self._build_context(parent)
        return Reference(
            source_note=Note(
                note_title=NoteTitle(self.note_title),
                note_path=NotePath(self.filepath),
            ),
            target_note=Note(
                note_title=NoteTitle(element.label),
                note_path=NotePath(Path(element.dest)),
            ),
            context=ReferenceContext(context),
        )

    def _extract_note_title(self, element):
        if element.level == 1:
            if self.note_title:
                raise InvalidNoteError(
                    message=f"Two titles found in {self.filepath}."
                )
            self.note_title = element.children[0].children
