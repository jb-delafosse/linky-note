from pathlib import Path

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
        note_title=NoteTitle("Marketing"),
        note_path=NotePath(Path("Marketing.md")),
    )
    url = f"[{source_note.note_title}]({source_note.note_path})"
    ast = build_ast(source_note)
    returned_value = GetReferencesResponse(
        (
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath(Path("digital-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath(Path("digital-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"Another reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("No Marketing"),
                    note_path=NotePath(Path("No-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
        )
    )
    mocked_db(returned_value)
    modifier = MarkoModifierImpl(ModifyConfig())

    # When
    modified_ast = modifier.modify_ast(ast, source_note)

    # Then
    assert len(modified_ast.children[10].children[0].children) == 2


def test_marko_modifier_link_system_url_encode(build_ast, mocked_db):
    # Given
    # - a reference whose filename needs to be url encode
    # - a reference whose filename is already url endoded
    source_note = Note(
        note_title=NoteTitle("Marketing"),
        note_path=NotePath(Path("Marketing.md")),
    )
    url = f"[{source_note.note_title}]({source_note.note_path})"
    ast = build_ast(source_note)
    returned_value = GetReferencesResponse(
        (
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath(Path("digital marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Content Marketing"),
                    note_path=NotePath(Path("content%20marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
        )
    )
    mocked_db(returned_value)
    modifier = MarkoModifierImpl(ModifyConfig())

    # When
    # - Modifying the ast
    modified_ast = modifier.modify_ast(ast, source_note)

    # Then
    # - The link to the reference is URL encoded
    # - an already url encoded link is not re-encoded
    assert (
        modified_ast.children[10].children[0].children[0].children[0].dest
        == "digital%20marketing.md"
    )
    assert (
        modified_ast.children[10].children[1].children[0].children[0].dest
        == "content%20marketing.md"
    )


def test_marko_modifier_nominal_wikilink_system(build_ast, mocked_db):
    # Given
    source_note = Note(
        note_title=NoteTitle("Marketing"),
        note_path=NotePath(Path("Marketing.md")),
    )
    url = f"[{source_note.note_title}]({source_note.note_path})"
    ast = build_ast(source_note)
    returned_value = GetReferencesResponse(
        (
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath(Path("digital-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("Digital Marketing"),
                    note_path=NotePath(Path("digital-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"Another reference to {url}"),
            ),
            Reference(
                source_note=Note(
                    note_title=NoteTitle("No Marketing"),
                    note_path=NotePath(Path("No-marketing.md")),
                ),
                target_note=source_note,
                context=ReferenceContext(f"A reference to {url}"),
            ),
        )
    )
    mocked_db(returned_value)
    modifier = MarkoModifierImpl(ModifyConfig(link_system=LinkSystem.WIKILINK))

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
