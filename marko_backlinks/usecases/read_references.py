from typing import Dict

from marko.block import Document
from marko_backlinks.dto.dto import Note, NotePath
from marko_backlinks.interfaces import reference_extractor, references_db


def read_references(
    parsed_files: Dict[NotePath, Document]
) -> Dict[Note, Document]:
    _reference_db = references_db.REFERENCE_DB_FACTORY()
    rv = {}
    for filename, ast in parsed_files.items():
        note, references = reference_extractor.EXTRACTOR_FACTORY(
            filename
        ).extract_references(ast)
        rv[note] = ast
        db_response = _reference_db.upsert_note(
            references_db.UpsertNoteQuery(note=note)
        )
        for reference in references:
            _insert_target_note_and_reference(
                _reference_db, db_response, reference
            )
    return rv


def _insert_target_note_and_reference(_reference_db, db_response, reference):
    reference_db_response = _reference_db.upsert_note(
        references_db.UpsertNoteQuery(note=reference.target_note)
    )
    if reference_db_response and db_response:
        _reference_db.upsert_reference(
            references_db.UpsertReferenceQuery(
                reference=reference,
                target_note_id=reference_db_response.note_id,
                source_note_id=db_response.note_id,
            )
        )
