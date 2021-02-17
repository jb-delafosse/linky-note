from typing import List, Optional, Union

from collections import defaultdict
from copy import deepcopy

from marko import Renderer
from marko.block import BlankLine, Document, Heading
from marko.block import List as MdList
from marko.block import ListItem, Paragraph
from marko.inline import Link, RawText
from marko_backlinks.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    Wikilink,
)
from marko_backlinks.dto.dto import Note
from marko_backlinks.interfaces import references_db
from marko_backlinks.interfaces.modifier import IModifier
from marko_backlinks.interfaces.references_db import IReferenceDB

LINKED_REFERENCE_SECTION_HEADER = "Linked References"


class NoOpRenderer(Renderer):
    def render_children(self, element):
        if isinstance(element, list):
            return [self.render(e) for e in element]
        if isinstance(element, str):
            return element
        rv = deepcopy(element)
        if hasattr(rv, "children"):
            rv.children = self.render(rv.children)
        return rv


class ModifyAst(NoOpRenderer):
    def __init__(self, reference_db: IReferenceDB):
        super().__init__()
        self._reference_db = reference_db

    def render_wikilink(self, element: Wikilink):
        link = self.build_link(element.label, element.dest, None)
        return link

    def build_link(
        self, label: str, dest: str, title: Optional[str] = None
    ) -> Link:
        link = object.__new__(Link)
        link.label = label
        link.title = title
        link.dest = dest
        link.children = [self.build_raw_element(label)]
        link.override = True
        return link

    def build_raw_element(self, label: str) -> RawText:
        raw_text = object.__new__(RawText)
        raw_text.children = label
        return raw_text

    def build_blank_line(self):
        blank_line = object.__new__(BlankLine)
        blank_line.inline_children = False
        blank_line.override = False
        blank_line.priority = 5
        blank_line.virtual = False
        return blank_line

    def build_heading(self, level: int, label: str):
        raw_text = self.build_raw_element(label)
        heading = object.__new__(Heading)
        heading.inline_children = True
        heading.level = level
        heading.override = True
        heading.priority = 6
        heading.virtual = False
        heading.children = [raw_text]
        return heading

    def render_backlink_section(self, element: BacklinkSection):
        return self.build_raw_element("")

    def render_document(self, element: Document, note: Note):
        element = self.render_children(element)
        element.children.append(
            self.build_heading(2, LINKED_REFERENCE_SECTION_HEADER)
        )
        element.children.append(self.build_blank_line())
        element.children.append(self.build_backlinks(element, note))
        return element

    def build_backlinks(self, element: Document, note: Note):
        db_response = self._reference_db.get_references_that_target(
            references_db.GetReferencesThatTarget(note_title=note.note_title)
        )
        ref_dict = defaultdict(list)
        items_in_backlink_section = []
        for ref in db_response.references:
            ref_dict[ref.source_note].append(ref.context)
        for source_note, contexts in ref_dict.items():
            items_in_backlink_section.append(
                self.build_paragraph(
                    [
                        self.build_link(
                            source_note.note_title, source_note.note_path
                        )
                    ]
                )
            )
            list_references = []
            for context in contexts:
                list_references.append(
                    self.build_paragraph([self.build_raw_element(context)])
                )
            items_in_backlink_section.append(
                self.build_list([self.build_list_item(list_references)])
            )
        return self.build_list(
            [self.build_list_item(items_in_backlink_section)]
        )

    def build_list(self, items: List[ListItem], bullet: str = "*") -> MdList:
        md_list = object.__new__(MdList)
        md_list.bullet = bullet
        md_list.inline_children = False
        md_list.ordered = False
        md_list.override = False
        md_list.priority = 6
        md_list.start = 1
        md_list.children = items
        return md_list

    def build_list_item(
        self, children: List[Union[Paragraph, MdList]]
    ) -> ListItem:
        item = object.__new__(ListItem)
        item.inline_children = False
        item.override = False
        item.priority = 5
        item.virtual = True
        item.children = children
        return item

    def build_paragraph(self, children: List[Union[Link, RawText]]):
        paragraph = object.__new__(Paragraph)
        paragraph.inline_children = True
        paragraph.override = False
        paragraph.priority = 1
        paragraph.virtual = False
        paragraph.children = children
        return paragraph

    def render_wikiimage(self, element):
        raise NotImplementedError()


class MarkoModifierImpl(IModifier):
    def modify_ast(self, ast: Document, note: Note) -> Document:
        return ModifyAst(self.reference_db).render_document(ast, note)
