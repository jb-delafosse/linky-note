from linky_note.adapters.references_db.query_builders import (
    SQLiteReferenceDatabase,
)
from linky_note.dto.dto import Note, Reference
from linky_note.interfaces.references_db import (
    GetNoteByTitleQuery,
    GetReferencesThatTarget,
    UpsertNoteQuery,
    UpsertReferenceQuery,
)
from tests.unit_tests.adapters.references_db.conftest import NoteFactory


def test_upsert_note(test_db: SQLiteReferenceDatabase, note: Note):
    # Given
    query = UpsertNoteQuery(note=note)

    # WHEN
    db_response = test_db.upsert_note(query)

    # THEN
    assert db_response.note == note
    assert isinstance(db_response.note_id, int)


def test_upsert_reference(test_db: SQLiteReferenceDatabase):
    # Given
    note_1, note_2 = NoteFactory.create_batch(size=2)
    reference = Reference(
        source_note=Note(
            note_title=note_1.note_title, note_path=note_1.note_path
        ),
        target_note=Note(
            note_title=note_2.note_title, note_path=note_2.note_path
        ),
        context=f"A nice reference to {note_2.note_title}",
    )

    query = UpsertReferenceQuery(
        source_note_id=note_1.id, target_note_id=note_2.id, reference=reference
    )

    # WHEN
    db_response = test_db.upsert_reference(query)

    # THEN
    assert db_response.source_note_id == note_1.id
    assert db_response.target_note_id == note_2.id
    assert db_response.reference == reference


def test_get_note_by_title(test_db: SQLiteReferenceDatabase):
    # GIVEN
    note_1, note_2 = NoteFactory.create_batch(size=2)

    query = GetNoteByTitleQuery(note_title=note_2.note_title)

    # WHEN
    db_response = test_db.get_note_by_title(query)

    # THEN
    assert db_response.note_id == note_2.id


def test_get_references_by_title(test_db: SQLiteReferenceDatabase):
    # GIVEN
    note_1 = NoteFactory.create(higher_edges=2)
    query = GetReferencesThatTarget(reference=note_1.note_title)

    # WHEN
    db_response = test_db.get_references_that_targets(query)

    # THEN
    # - I find the 2 references
    # - The references are returned sorted by source_note_title
    assert len(db_response.references) == 2
    assert (
        db_response.references[0].source_note.note_title
        <= db_response.references[1].source_note.note_title
    )
