from pathlib import Path

from linky_note.adapters.markdown.marko_extractor import MarkoExtractor
from linky_note.dto.dto import Note, NotePath, NoteTitle


def test_marko_extractor_nominal(build_ast):
    # Given
    source_note = Note(
        note_title=NoteTitle("Marketing"),
        note_path=NotePath(Path("Marketing.md")),
    )
    ast = build_ast(source_note)

    # When
    note, references = MarkoExtractor(
        filepath=NotePath(Path("Marketing.md"))
    ).extract_references(ast)

    # Then
    assert note == source_note
    assert references[0].source_note == source_note
    assert references[0].target_note == Note(
        NoteTitle("Wikilink"), NotePath(Path("Wikilink.md"))
    )
    assert references[0].context == "Just adding a **Wikilink** in here"
    assert note == source_note
    assert references[1].source_note == source_note
    assert references[1].target_note == source_note
    assert (
        references[1].context == f"a reference to **{source_note.note_title}**"
    )
    assert references[2].source_note == source_note
    assert references[2].target_note == source_note
    assert (
        references[2].context
        == f"another reference to **{source_note.note_title}**"
    )
