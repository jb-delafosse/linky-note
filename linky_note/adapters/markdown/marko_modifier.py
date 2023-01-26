from typing import Optional

import os.path
import urllib.parse
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import yaml
from linky_note.adapters.markdown.marko_ext.elements import (
    BacklinkSection,
    FrontMatter,
    Wikilink,
)
from linky_note.adapters.markdown.marko_ext.marko_builder import MarkoBuilder
from linky_note.dto.dto import (
    BacklinksLocation,
    LinkSystem,
    ModifyConfig,
    Note,
    ReferenceBy,
)
from linky_note.interfaces import references_db
from linky_note.interfaces.modifier import IModifier
from linky_note.interfaces.references_db import IReferenceDB
from marko import Renderer
from marko.block import Document
from marko.inline import Link

LINKED_REFERENCE_SECTION_HEADER = "Linked References"


class ModifierVisitor(Renderer):
    def __init__(
        self,
        reference_db: IReferenceDB,
        modify_config: ModifyConfig,
        note: Note,
    ):
        super().__init__()
        self._reference_db = reference_db
        self.config = modify_config
        self.root = Path("/root")
        self.note = note

    @staticmethod
    def _encode_once(dest: str) -> str:
        decoded = urllib.parse.unquote(dest)
        return urllib.parse.quote(decoded)

    def build_link_or_wikilink(
        self, label: str, dest: str, title: Optional[str] = None
    ):
        if self.config.link_system == LinkSystem.LINK:
            if _is_internal_destination(dest):
                return MarkoBuilder.build_link(
                    self._encode_once(dest), label, title
                )
            else:
                return MarkoBuilder.build_link(dest, label, title)
        elif self.config.link_system == LinkSystem.WIKILINK:
            if _is_internal_destination(dest):
                return MarkoBuilder.build_raw_element(f"[[{label}]]")
            else:
                return MarkoBuilder.build_link(dest, label, title)

    def render_wikilink(self, element: Wikilink):
        return self.build_link_or_wikilink(element.label, element.dest, None)

    def render_link(self, element: Link):
        return self.build_link_or_wikilink(
            element.children[0].children, element.dest, None
        )

    def _build_frontmatter(self, db_response):
        ref_dict = defaultdict(list)
        for ref in db_response.references:
            ref_dict[ref.source_note].append(ref.context)

        sub_item = []
        for source_note, contexts in ref_dict.items():
            rel_path = os.path.relpath(
                self.root / source_note.note_path,
                self.root / self.note.note_path.parent,
            )
            sub_item.append(
                {
                    "note_title": source_note.note_title,
                    "note_path": str(rel_path),
                    "references": [context for context in contexts],
                }
            )
        return {"backlinks": sub_item}

    def _build_backlinks(self, db_response):
        ref_dict = defaultdict(list)
        items_in_backlink_section = []
        for ref in db_response.references:
            ref_dict[ref.source_note].append(ref.context)

        for source_note, contexts in ref_dict.items():
            sub_item = []
            rel_path = os.path.relpath(
                self.root / source_note.note_path,
                self.root / self.note.note_path.parent,
            )
            sub_item.append(
                MarkoBuilder.build_paragraph(
                    [
                        self.build_link_or_wikilink(
                            source_note.note_title, str(rel_path)
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
            sub_item.append(
                MarkoBuilder.build_list(
                    [MarkoBuilder.build_list_item(list_references)]
                )
            )
            items_in_backlink_section.append(
                MarkoBuilder.build_list_item(sub_item)
            )
        return MarkoBuilder.build_list(items_in_backlink_section)

    def render_backlinksection(self):
        element = BacklinkSection("")
        element.children.append(
            MarkoBuilder.build_heading(2, LINKED_REFERENCE_SECTION_HEADER)
        )
        db_response = self._reference_db.get_references_that_targets(
            references_db.GetReferencesThatTarget(
                reference=self.note.note_title
                if self.config.reference_by == ReferenceBy.TITLE
                else self.note.note_path
            )
        )
        if len(db_response.references) > 0:
            element.children.append(MarkoBuilder.build_blank_line())
            element.children.append(self._build_backlinks(db_response))
        return element

    def render_list(self, element: list) -> list:
        return [self.render_children(e) for e in element]

    def render_document(self, element: Document):
        element.children = self.render_list(element.children)

        first_child_is_frontmatter = isinstance(
            element.children[0], FrontMatter
        )
        if (
            self.config.backlinks_location == BacklinksLocation.FRONTMATTER
            and not first_child_is_frontmatter
        ):
            raise Exception(
                f"Expected a frontmatter, found none in {self.note.note_title}"
            )

        last_child_is_a_backlink_section = isinstance(
            element.children[-1], BacklinkSection
        )
        if (
            self.config.backlinks_location == BacklinksLocation.BACKLINK_SECTION
            and not last_child_is_a_backlink_section
        ):
            element.children.append(self.render_backlinksection())
        return element

    def render_frontmatter(self, element: FrontMatter):
        db_response = self._reference_db.get_references_that_targets(
            references_db.GetReferencesThatTarget(
                reference=self.note.note_title
                if self.config.reference_by == ReferenceBy.TITLE
                else self.note.note_path
            )
        )
        element.dict.update(self._build_frontmatter(db_response))
        yaml_text = yaml.dump(element.dict)
        element.children = [
            MarkoBuilder.build_raw_element(f"---\n{yaml_text}---")
        ]
        return element

    def render_children(self, element):
        if isinstance(element, Document):
            return self.render_document(element)
        if isinstance(element, FrontMatter):
            return self.render_frontmatter(element)
        if isinstance(element, BacklinkSection):
            return self.render_backlinksection()
        if isinstance(element, list):
            return self.render_list(element)
        if isinstance(element, Wikilink):
            return self.render_wikilink(element)
        if isinstance(element, Link):
            return self.render_link(element)
        if isinstance(element, str):
            return element
        rv = deepcopy(element)
        if hasattr(rv, "children"):
            rv.children = self.render(rv.children)
        return rv


class ModifierVisitorFactory:
    def __init__(self, reference_db: IReferenceDB, modify_config: ModifyConfig):
        self._reference_db = reference_db
        self.config = modify_config
        self.root = Path("/root")

    def __call__(self, note: Note) -> ModifierVisitor:
        return ModifierVisitor(self._reference_db, self.config, note)


def _is_internal_destination(dest: str):
    return dest.endswith(".md")


class ModifyAst:
    def __init__(self, reference_db: IReferenceDB, modify_config: ModifyConfig):
        super().__init__()
        self.visitor_factory = ModifierVisitorFactory(
            reference_db, modify_config
        )

    def modify_document(self, element: Document, note: Note):
        visitor = self.visitor_factory(note)
        element = visitor.render_children(element)
        return element


class MarkoModifierImpl(IModifier):
    def modify_ast(self, ast: Document, note: Note) -> Document:
        return ModifyAst(self.reference_db, self.modify_config).modify_document(
            ast, note
        )
