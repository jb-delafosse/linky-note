from unittest.mock import mock_open, patch

from linky_note.adapters.markdown.marko_ext.elements import Wikiimage, Wikilink
from linky_note.adapters.markdown.marko_parser import MarkoParserImpl
from linky_note.dto.dto import ParseConfig

content_links = """# Meeting Note ABC

Wikilinks should work [[Meeting Note]]
Wikiimage should work ![[image.png]]
"""


@patch("builtins.open", mock_open(read_data=content_links))
def test_parse_filename_nominal():
    # Given: a filename and
    markdown = MarkoParserImpl(ParseConfig(parse_wikilinks=True))
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_filename(filename)

    # Then
    assert isinstance(result.children[2].children[1], Wikilink)
    assert isinstance(result.children[2].children[4], Wikiimage)


@patch("builtins.open", mock_open(read_data=content_links))
def test_parse_filename_nominal_deactivate_wikilinks():
    # Given: a filename and
    markdown = MarkoParserImpl(ParseConfig(parse_wikilinks=False))
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_filename(filename)

    # Then
    assert (
        result.children[2].children[0].children
        == "Wikilinks should work [[Meeting Note]]"
    )
    assert isinstance(result.children[2].children[3], Wikiimage)
