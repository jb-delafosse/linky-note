from typing import Optional

from collections import defaultdict
from copy import deepcopy

from marko import Renderer
from marko.block import Document
from marko.inline import Link
from marko_backlinks.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    Wikilink,
)
from marko_backlinks.adapters.markdown.marko_ext.marko_builder import (
    MarkoBuilder,
)
from marko_backlinks.dto.dto import LinkSystem, ModifyConfig, Note
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
    def __init__(self, reference_db: IReferenceDB, modify_config: ModifyConfig):
        super().__init__()
        self._reference_db = reference_db
        self.config = modify_config

    def render_wikilink(self, element: Wikilink):
        return self.build_link_or_wikilink(element.label, element.dest, None)

    def render_link(self, element: Link):
        return self.build_link_or_wikilink(
            element.children[0].children, element.dest, None
        )

    def build_link_or_wikilink(
        self, label: str, dest: str, title: Optional[str] = None
    ):
        if self.config.link_system == LinkSystem.LINK:
            link = object.__new__(Link)
            link.label = label
            link.title = title
            link.dest = dest
            link.children = [MarkoBuilder.build_raw_element(label)]
            link.override = True
            return link
        elif self.config.link_system == LinkSystem.WIKILINK:
            return MarkoBuilder.build_raw_element(f"[[{label}]]")

    def render_backlink_section(self, element: BacklinkSection):
        return MarkoBuilder.build_raw_element("")

    def render_document(self, element: Document, note: Note):
        element = self.render_children(element)
        element.children.append(
            MarkoBuilder.build_heading(2, LINKED_REFERENCE_SECTION_HEADER)
        )
        element.children.append(MarkoBuilder.build_blank_line())
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
                MarkoBuilder.build_paragraph(
                    [
                        self.build_link_or_wikilink(
                            source_note.note_title, source_note.note_path
                        )
                    ]
                )
            )
            list_references = []
            for context in contexts:
                list_references.append(
                    MarkoBuilder.build_paragraph(
                        [MarkoBuilder.build_raw_element(context)]
                    )
                )
            items_in_backlink_section.append(
                MarkoBuilder.build_list(
                    [MarkoBuilder.build_list_item(list_references)]
                )
            )
        return MarkoBuilder.build_list(
            [MarkoBuilder.build_list_item(items_in_backlink_section)]
        )

    def render_wikiimage(self, element):
        raise NotImplementedError()


class MarkoModifierImpl(IModifier):
    def modify_ast(self, ast: Document, note: Note) -> Document:
        return ModifyAst(self.reference_db, self.modify_config).render_document(
            ast, note
        )
