from unittest.mock import mock_open, patch

from marko_backlinks.adapters.markdown.marko_ext.elements import (
    Wikiimage,
    Wikilink,
)
from marko_backlinks.adapters.markdown.marko_parser import MarkoParserImpl

content_links = """# Meeting Note ABC

Wikilinks should work [[Meeting Note]]
Wikiimage should work ![[image.png]]
"""


@patch("builtins.open", mock_open(read_data=content_links))
def test_parse_filename_nominal():
    # Given: a filename and
    markdown = MarkoParserImpl()
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_filename(filename)

    # Then
    assert isinstance(result.children[2].children[1], Wikilink)
    assert isinstance(result.children[2].children[4], Wikiimage)
