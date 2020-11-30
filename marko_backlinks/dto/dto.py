from typing import Any, NewType

from dataclasses import dataclass

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
