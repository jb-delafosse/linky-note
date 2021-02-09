from typing import Dict

import glob
import os
from pathlib import Path

from marko_backlinks.dto.dto import Reference
from marko_backlinks.interfaces import converter, references_db
from marko_backlinks.usecases.marko_ext.elements import Document


def parse(directory: Path) -> Dict[str, Document]:
    _reference_db = references_db.REFERENCE_DB_FACTORY()
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        parse_result = converter.CONVERTER.parse_filename(filename)
        db_response = _reference_db.upsert_note(
            references_db.UpsertNoteQuery(note=parse_result.note)
        )
        references = [
            Reference(
                source_note=parse_result.note,
                target_note=p_ref.target_note,
                context=p_ref.context,
            )
            for p_ref in parse_result.references
        ]

        for reference in references:
            target_note = reference.target_note
            reference_db_response = _reference_db.upsert_note(
                references_db.UpsertNoteQuery(note=target_note)
            )
            if reference_db_response and db_response:
                _reference_db.upsert_reference(
                    references_db.UpsertReferenceQuery(
                        reference=reference,
                        target_note_id=reference_db_response.note_id,
                        source_note_id=db_response.note_id,
                    )
                )
        files[filename] = parse_result.ast
    return files
