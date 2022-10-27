from typing import Tuple

import os
from pathlib import Path

from linky_note.adapters.markdown.factories import MarkoExtractorFactory
from linky_note.adapters.markdown.marko_modifier import MarkoModifierImpl
from linky_note.adapters.markdown.marko_parser import MarkoParserImpl
from linky_note.dto.dto import LinkyNoteConfig
from linky_note.interfaces.modifier import IModifier
from linky_note.interfaces.parser import IParser
from linky_note.interfaces.reference_extractor import ReferenceExtractorFactory
from linky_note.interfaces.renderer import IRenderer
from marko.md_renderer import MarkdownRenderer


def setup_markdown(
    config: LinkyNoteConfig,
) -> Tuple[IParser, ReferenceExtractorFactory, IModifier, IRenderer]:
    return (
        MarkoParserImpl(config.parse_config),
        MarkoExtractorFactory(),
        MarkoModifierImpl(config.modify_config),
        MarkdownRenderer(),
    )
