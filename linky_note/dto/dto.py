from typing import NewType

from dataclasses import dataclass
from enum import Enum

NoteTitle = NewType("NoteTitle", str)
NotePath = NewType("NotePath", str)
ReferenceContext = NewType("ReferenceContext", str)


@dataclass(frozen=True)
class Note:
    note_title: NoteTitle
    note_path: NotePath


@dataclass(frozen=True)
class Reference:
    source_note: Note
    target_note: Note
    context: ReferenceContext


@dataclass(frozen=True)
class ParsedReference:
    target_note: Note
    context: ReferenceContext


@dataclass(frozen=True)
class ParseConfig:
    parse_wikilinks: bool = True


class LinkSystem(str, Enum):
    WIKILINK = "wikilink"
    LINK = "link"


class ReferenceBy(str, Enum):
    TITLE = "title"
    FILENAME = "filename"


@dataclass(frozen=True)
class ModifyConfig:
    link_system: LinkSystem = LinkSystem.LINK
    reference_by: ReferenceBy = ReferenceBy.TITLE


@dataclass(frozen=True)
class LinkyNoteConfig:
    parse_config: ParseConfig = ParseConfig()
    modify_config: ModifyConfig = ModifyConfig()
