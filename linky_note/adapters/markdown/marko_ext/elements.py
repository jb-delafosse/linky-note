from typing import Any, Iterator, List, Match, Optional, Tuple

import re
from pathlib import Path

import yaml
from linky_note.adapters.markdown.marko_ext.marko_builder import MarkoBuilder
from linky_note.dto.dto import (
    Note,
    NotePath,
    NoteTitle,
    ParsedReference,
    ReferenceContext,
)
from marko import block, inline, inline_parser
from marko.helpers import Source
from marko.inline import Link as MarkoLink


class Wikilink(inline.InlineElement):

    pattern = r"(?<!\!)\[\[([\s\S]*?)\]\]"
    priority = 5

    def __init__(self, match):
        super().__init__(match)
        self.label = match.group(1)
        self.dest = f"{self.label}.md"

    @classmethod
    def find(cls, text):  # type: (str) -> List[Match[Any]]
        """This method should return an iterable containing matches of this element."""
        if isinstance(cls.pattern, str):
            cls.pattern = re.compile(cls.pattern)  # type: ignore
        match_list = [match for match in cls.pattern.finditer(text)]  # type: ignore
        return match_list


class FrontMatter(block.BlockElement):
    pattern = r"^---\n([\s\S]+?)---"
    priority = 9

    def __init__(self, match):
        super().__init__()
        if match:
            self.children = [MarkoBuilder.build_raw_element(match.group(1))]
            self.dict = yaml.load(match.group(1), Loader=yaml.SafeLoader)
        else:
            self.children = None

    @classmethod
    def match(cls, source):  # type: (Source) -> bool
        m = source.expect_re(cls.pattern)
        if not m:
            return False
        return True

    @classmethod
    def parse(cls, source):  # type: (Source) -> FrontMatter
        instance = cls(source.match)
        source.consume()
        return instance


class Wikiimage(inline.InlineElement):
    pattern = r"\!\[\[([\s\S]*?)\]\]"
    priority = 5

    def __init__(self, match):
        super().__init__(match)
        self.image_path = match.group(1)


class Link(MarkoLink):
    """Link: [text](/link/destination)"""

    virtual = True
    parse_children = True
    override = False

    def __init__(self, match):  # type: (Match[Any]) -> None
        super().__init__(match)
        self.label, self.title, self.dest = Link.extract_label_title_and_dest(
            match
        )

    @staticmethod
    def extract_label_title_and_dest(match) -> Tuple[str, str, Optional[str]]:
        label = match.group(1)
        if (
            match.group(2)
            and match.group(2)[0] == "<"
            and match.group(2)[-1] == ">"
        ):
            dest = match.group(2)[1:-1]
        else:
            dest = match.group(2) or ""
        dest = inline.Literal.strip_backslash(dest)
        title = (
            inline.Literal.strip_backslash(match.group(3)[1:-1])
            if match.group(3)
            else None
        )
        return label, title, dest


class LinkOrEmph(inline.InlineElement):
    """This is a special element, whose parsing is done specially.
    And it produces Link or Emphasis elements.
    """

    parse_children = True
    override = False

    def __new__(cls, match):  # type: (Match[Any]) -> LinkOrEmph
        return inline.parser.inline_elements[match.etype](match)  # type: ignore

    @classmethod
    def find(cls, text):  # type: (str) -> Iterator[Match[Any]]
        match_list = inline_parser.find_links_or_emphs(text, inline._root_node)
        for match in match_list:
            if match.etype == "Link":
                link = Link(match)
                if link.dest:
                    ref = ParsedReference(
                        target_note=Note(
                            note_title=NoteTitle(link.title)
                            or NoteTitle(link.label),
                            note_path=NotePath(Path(link.dest)),
                        ),
                        context=ReferenceContext(text),
                    )
                    inline._root_node.references.append(ref)
            yield match


class BacklinkSection(block.BlockElement):
    priority = 7
    pattern = re.compile(
        r"( {0,3}#{2} Linked References\n)(^[\s\S]*$)(?=(?:^ {0,3}(#{1,6})([^\n]*?|[^\n\S]*)[^\n\S]*$\n?)|$)",
        flags=re.M,
    )
    inline_children = False

    def __init__(self, match):
        self.level = 2
        self.children = []

    @classmethod
    def match(cls, source):
        return source.expect_re(cls.pattern)

    @classmethod
    def parse(cls, source):  # type: (Source) -> Any
        state = cls(source.match)
        source.consume()
        return state
