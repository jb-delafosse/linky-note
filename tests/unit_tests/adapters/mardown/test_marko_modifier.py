from linky_note.adapters.markdown.marko_modifier import (
    MarkoModifierImpl,
    _is_internal_destination,
)
from linky_note.dto.dto import (
    LinkSystem,
    ModifyConfig,
    Note,
    NotePath,
    NoteTitle,
    Reference,
    ReferenceContext,
)
from linky_note.interfaces.references_db import GetReferencesResponse
from marko.inline import RawText


def test_marko_modifier_nominal_link_system(build_ast, mocked_db):
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
    modifier = MarkoModifierImpl(mocked_db(returned_value), ModifyConfig())

    # When
    modified_ast = modifier.modify_ast(ast, source_note)

    # Then
    assert len(modified_ast.children[9].children[0].children) == 2


def test_marko_modifier_nominal_wikilink_system(build_ast, mocked_db):
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
    modifier = MarkoModifierImpl(
        mocked_db(returned_value), ModifyConfig(link_system=LinkSystem.WIKILINK)
    )

    # When
    modified_ast = modifier.modify_ast(ast, source_note)

    # Then
    assert isinstance(modified_ast.children[3].children[1], RawText)


def test__is_internal_destination():
    # Given
    internal_dest = "note.md"
    external_dest = "www.google.com"

    # When / Then
    assert _is_internal_destination(internal_dest)
    assert not _is_internal_destination(external_dest)
