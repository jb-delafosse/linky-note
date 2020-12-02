from typing import AnyStr, List, Optional, Union

from marko import Parser, block
from marko.helpers import Source
from marko_backlinks.dto.dto import Note, ParsedReference, Reference
from marko_backlinks.interfaces import references_db
from marko_backlinks.usecases.marko_ext.exceptions import TitleNotFoundException


class ReferenceParser(Parser):
    def __init__(self):
        super().__init__()
        self._reference_db = references_db.REFERENCE_DB_FACTORY()

    def parse(
        self, source_or_text
    ):  # type: (Union[Source, AnyStr]) -> Union[List[block.BlockElement], block.BlockElement]
        ast = super().parse(source_or_text=source_or_text)
        if not isinstance(source_or_text, Source):
            self._update_db_from_ast(ast)
        return ast

    def _update_db_from_ast(self, ast):
        note: Optional[Note] = ast.source_note
        if not note:
            raise TitleNotFoundException()
        db_response = self._reference_db.upsert_note(
            references_db.UpsertNoteQuery(note=note)
        )
        parsed_references: List[ParsedReference] = ast.references
        references = [
            Reference(
                source_note=note,
                target_note=p_ref.target_note,
                context=p_ref.context,
            )
            for p_ref in parsed_references
        ]
        for reference in references:
            target_note = reference.target_note
            reference_db_response = self._reference_db.upsert_note(
                references_db.UpsertNoteQuery(note=target_note)
            )
            if reference_db_response and db_response:
                self._reference_db.upsert_reference(
                    references_db.UpsertReferenceQuery(
                        reference=reference,
                        target_note_id=reference_db_response.note_id,
                        source_note_id=db_response.note_id,
                    )
                )
