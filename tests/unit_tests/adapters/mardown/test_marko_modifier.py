from marko_backlinks.adapters.markdown.marko_modifier import MarkoModifierImpl
from marko_backlinks.dto.dto import (
    Note,
    NotePath,
    NoteTitle,
    Reference,
    ReferenceContext,
)
from marko_backlinks.interfaces.references_db import GetReferencesResponse


def test_marko_modifier_nominal(build_ast, mocked_db):
    # Given
    source_note = Note(
        note_title=NoteTitle("Marketing"), note_path=NotePath("Marketing.md")
    )
    url = f"[{source_note.note_title}]({source_note.note_path})"
    ast = build_ast(source_note)
    returned_value = GetReferencesResponse(
        (
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath("digital-marketing.md"),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath("digital-marketing.md"),
                ),
                target_note=source_note,
                context=ReferenceContext(f"Another reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("No Marketing"),
                    note_path=NotePath("No-marketing.md"),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
        )
    )
    modifier = MarkoModifierImpl(mocked_db(returned_value))

    # When
    modified_ast = modifier.modify_ast(ast, source_note)

    # Then
    assert len(modified_ast.children[7].children[0].children) == 4
