from unittest.mock import mock_open, patch

from linky_note.adapters.markdown.marko_ext.elements import (
    FrontMatter,
    Wikiimage,
    Wikilink,
)
from linky_note.adapters.markdown.marko_parser import MarkoParserImpl
from linky_note.dto.dto import ParseConfig

content_wikilinks = """# Meeting Note ABC

Wikilinks should work [[Meeting Note]]
Wikiimage should work ![[image.png]]
"""

content_frontmatter = """---
layout: post
title: Meeting Note ABC
---

# Meeting Note ABC

Wikilinks should work [[Meeting Note]]
Wikiimage should work ![[image.png]]
"""


@patch("builtins.open", mock_open(read_data=content_wikilinks))
def test_parse_filename_nominal():
    # Given: a filename and
    markdown = MarkoParserImpl(ParseConfig(parse_wikilinks=True))
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_file(filename)

    # Then
    assert isinstance(result.children[2].children[1], Wikilink)
    assert isinstance(result.children[2].children[4], Wikiimage)


@patch("builtins.open", mock_open(read_data=content_wikilinks))
def test_parse_filename_nominal_deactivate_wikilinks():
    # Given: a filename and
    markdown = MarkoParserImpl(ParseConfig(parse_wikilinks=False))
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_file(filename)

    # Then
    assert (
        result.children[2].children[0].children
        == "Wikilinks should work [[Meeting Note]]"
    )
    assert isinstance(result.children[2].children[3], Wikiimage)


@patch("builtins.open", mock_open(read_data=content_frontmatter))
def test_parse_filename_nominal_frontmatter():
    # Given: a filename
    markdown = MarkoParserImpl(ParseConfig(parse_frontmatter=True))
    filename = "meeting-note.md"

    # When:
    result = markdown.parse_file(filename)

    # Then
    frontmatter = result.children[0]
    assert isinstance(frontmatter, FrontMatter)
    assert (
        frontmatter.children[0].children
        == "layout: post\ntitle: Meeting Note ABC\n"
    )
