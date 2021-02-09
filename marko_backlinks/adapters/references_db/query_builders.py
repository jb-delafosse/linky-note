from typing import Optional

from marko_backlinks.adapters.references_db import tables
from marko_backlinks.dto.dto import Note, Reference
from marko_backlinks.interfaces.references_db import (
    GetNoteByTitleQuery,
    GetNoteResponse,
    GetReferencesResponse,
    GetReferencesThatTarget,
    IReferenceDB,
    UpsertNoteQuery,
    UpsertNoteResponse,
    UpsertReferenceQuery,
    UpsertReferenceResponse,
)
from sqlalchemy import insert, join, select
from sqlalchemy.engine import Connectable
from sqlalchemy.orm import aliased


class SQLiteReferenceDatabase(IReferenceDB):
    def __init__(self, db_connection: Connectable):
        self._db_connection = db_connection

    def upsert_reference(
        self, query: UpsertReferenceQuery
    ) -> UpsertReferenceResponse:
        insert_stmt = insert(tables.Reference).values(
            {
                "source_note_id": query.source_note_id,
                "target_note_id": query.target_note_id,
                "context": query.reference.context,
            }
        )
        res = self._db_connection.execute(insert_stmt)
        return UpsertReferenceResponse(
            reference=query.reference,
            target_note_id=query.target_note_id,
            source_note_id=query.source_note_id,
            reference_id=res.inserted_primary_key[0],
        )

    def upsert_note(self, query: UpsertNoteQuery) -> UpsertNoteResponse:
        insert_stmt = insert(tables.Note).values(
            {
                "note_title": query.note.note_title,
                "note_path": query.note.note_path,
            }
        )
        res = self._db_connection.execute(insert_stmt)
        return UpsertNoteResponse(
            note=query.note, note_id=res.inserted_primary_key[0]
        )

    def get_note_by_title(
        self, query: GetNoteByTitleQuery
    ) -> Optional[GetNoteResponse]:
        select_stmt = select([tables.Note]).where(
            tables.Note.note_title == query.note_title
        )
        res = self._db_connection.execute(select_stmt).fetchone()
        if res:
            return GetNoteResponse(
                note_id=res[0], note=Note(note_title=res[1], note_path=res[2])
            )
        else:
            return None

    def get_references_that_target(
        self, query: GetReferencesThatTarget
    ) -> GetReferencesResponse:
        TargetNotes = aliased(tables.Note, name="target_notes")
        SourceNotes = aliased(tables.Note, name="source_notes")
        stmt = (
            join(
                SourceNotes,
                tables.Reference,
                onclause=SourceNotes.id == tables.Reference.source_note_id,
            )
            .join(
                TargetNotes,
                onclause=TargetNotes.id == tables.Reference.target_note_id,
            )
            .select()
            .where(TargetNotes.note_title == query.note_title)
            .order_by(SourceNotes.note_title)
        )
        res = self._db_connection.execute(stmt).fetchall()
        return GetReferencesResponse(
            references=tuple(
                Reference(
                    source_note=Note(note_title=row[1], note_path=row[2]),
                    target_note=Note(note_title=row[8], note_path=row[9]),
                    context=row[4],
                )
                for row in res
            )
        )
