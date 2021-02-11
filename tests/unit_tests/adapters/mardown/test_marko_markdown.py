from unittest.mock import mock_open, patch

import pytest
from marko import Markdown
from marko.md_renderer import MarkdownRenderer
from marko_backlinks.adapters.markdown.marko_markdown import MarkoMarkdownImpl
from marko_backlinks.common.exceptions import InvalidNoteError
from marko_backlinks.dto.dto import (
    Note,
    NotePath,
    NoteTitle,
    ParsedReference,
    ReferenceContext,
)
from marko_backlinks.usecases.extension import ReferencesExtension

content = """
# Meeting Note ABC

Wikilinks should work [[Meeting Note]]

Standard [URL](URL.md) aswell
"""


@patch("builtins.open", mock_open(read_data=content))
def test_parse_filename_nominal():
    # Given: a filename and
    markdown = MarkoMarkdownImpl(
        marko=Markdown(
            renderer=MarkdownRenderer, extensions=[ReferencesExtension]
        )
    )
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_filename(filename)

    # Then
    assert result.note == Note(
        note_title=NoteTitle("Meeting Note ABC"),
        note_path=NotePath("Meeting Note ABC.md"),
    )
    expected_notes = [
        ParsedReference(
            context=ReferenceContext("Wikilinks should work [[Meeting Note]]"),
            target_note=Note(
                note_title=NoteTitle("Meeting Note"),
                note_path=NotePath("Meeting Note.md"),
            ),
        ),
        ParsedReference(
            context=ReferenceContext("Standard [URL](URL.md) aswell"),
            target_note=Note(
                note_title=NoteTitle("URL"), note_path=NotePath("URL.md")
            ),
        ),
    ]

    assert result.references == expected_notes


content_no_title = """
No Title
"""


@patch("builtins.open", mock_open(read_data=content_no_title))
def test_parse_filename_no_title():
    # Given: a filename and
    markdown = MarkoMarkdownImpl(
        marko=Markdown(
            renderer=MarkdownRenderer, extensions=[ReferencesExtension]
        )
    )
    filename = "meeting-note.md"

    # When/Then:
    with pytest.raises(InvalidNoteError):
        markdown.parse_filename(filename)
