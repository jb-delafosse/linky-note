from typing import Callable, Optional, Tuple, Type

from abc import ABC, abstractmethod
from dataclasses import dataclass

from marko_backlinks.dto.dto import Note, Reference

NoteId = Type[int]
ReferenceId = Type[int]


@dataclass(frozen=True)
class UpsertNoteQuery:
    note: Note


@dataclass(frozen=True)
class UpsertNoteResponse:
    note: Note
    note_id: NoteId


@dataclass(frozen=True)
class UpsertReferenceQuery:
    reference: Reference
    target_note_id: NoteId
    source_note_id: NoteId


@dataclass(frozen=True)
class UpsertReferenceResponse:
    reference: Reference
    target_note_id: NoteId
    source_note_id: NoteId
    reference_id: ReferenceId


@dataclass(frozen=True)
class GetNoteByTitleQuery:
    note_title: str


@dataclass(frozen=True)
class GetNoteResponse:
    note: Note
    note_id: NoteId


@dataclass(frozen=True)
class GetReferencesThatTarget:
    note_title: str


@dataclass(frozen=True)
class GetReferencesResponse:
    references: Tuple[Reference, ...]


class IReferenceDB(ABC):
    @abstractmethod
    def upsert_note(self, query: UpsertNoteQuery) -> UpsertNoteResponse:
        pass

    @abstractmethod
    def upsert_reference(
        self, query: UpsertReferenceQuery
    ) -> UpsertReferenceResponse:
        pass

    @abstractmethod
    def get_note_by_title(
        self, query: GetNoteByTitleQuery
    ) -> Optional[GetNoteResponse]:
        pass

    @abstractmethod
    def get_references_that_target(
        self, query: GetReferencesThatTarget
    ) -> GetReferencesResponse:
        pass


ReferenceDbFactory = Callable[[], IReferenceDB]
REFERENCE_DB_FACTORY: ReferenceDbFactory
