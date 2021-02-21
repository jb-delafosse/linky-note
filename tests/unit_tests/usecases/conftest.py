from unittest.mock import MagicMock

import pytest
from linky_note.interfaces import parser


@pytest.fixture(scope="function")
def note_parser():
    parser.PARSER = MagicMock()
    parser.PARSER.parse_filename = MagicMock()
    return parser.PARSER.parse_filename
