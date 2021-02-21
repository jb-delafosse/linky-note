from typing import List, Optional, Union

from marko.block import BlankLine, Heading
from marko.block import List as MdList
from marko.block import ListItem, Paragraph
from marko.inline import Link, RawText


class MarkoBuilder:
    @staticmethod
    def build_raw_element(label: str) -> RawText:
        raw_text = object.__new__(RawText)
        raw_text.children = label
        return raw_text

    @staticmethod
    def build_blank_line() -> BlankLine:
        blank_line = object.__new__(BlankLine)
        blank_line.inline_children = False
        blank_line.override = False
        blank_line.priority = 5
        blank_line.virtual = False
        return blank_line

    @staticmethod
    def build_heading(level: int, label: str) -> Heading:
        raw_text = MarkoBuilder.build_raw_element(label)
        heading = object.__new__(Heading)
        heading.inline_children = True
        heading.level = level
        heading.override = True
        heading.priority = 6
        heading.virtual = False
        heading.children = [raw_text]
        return heading

    @staticmethod
    def build_list(items: List[ListItem], bullet: str = "*") -> MdList:
        md_list = object.__new__(MdList)
        md_list.bullet = bullet
        md_list.inline_children = False
        md_list.ordered = False
        md_list.override = False
        md_list.priority = 6
        md_list.start = 1
        md_list.children = items
        return md_list

    @staticmethod
    def build_list_item(children: List[Union[Paragraph, MdList]]) -> ListItem:
        item = object.__new__(ListItem)
        item.inline_children = False
        item.override = False
        item.priority = 5
        item.virtual = True
        item.children = children
        return item

    @staticmethod
    def build_link(dest: str, label: str, title: Optional[str]) -> Link:
        link = object.__new__(Link)
        link.label = label
        link.title = title
        link.dest = dest
        link.children = [MarkoBuilder.build_raw_element(label)]
        link.override = True
        return link

    @staticmethod
    def build_paragraph(children: List[Union[Link, RawText]]) -> Paragraph:
        paragraph = object.__new__(Paragraph)
        paragraph.inline_children = True
        paragraph.override = False
        paragraph.priority = 1
        paragraph.virtual = False
        paragraph.children = children
        return paragraph
