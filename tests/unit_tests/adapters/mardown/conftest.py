from unittest.mock import MagicMock

import pytest
from linky_note.adapters.markdown.marko_ext.elements import Wikilink
from linky_note.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from linky_note.dto.dto import Note
from linky_note.interfaces import references_db
from linky_note.interfaces.references_db import (
    GetReferencesResponse,
    IReferenceDB,
)
from marko import Parser
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db():
    return factory()


@pytest.fixture
def build_ast():
    from linky_note.adapters.markdown.marko_modifier import (
        LINKED_REFERENCE_SECTION_HEADER,
    )

    def _build(note: Note):
        text = (
            f"# {note.note_title}\n"
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
            "\n"
            "Just adding a [[Wikilink]] in here"
            "\n"
            f"## {LINKED_REFERENCE_SECTION_HEADER}\n"
            "\n"
            "  * [Note A](Note A.md)\n"
            f"    * a reference to [{note.note_title}]({note.note_path})\n"
            f"    * another reference to [{note.note_title}]({note.note_path})\n"
        )
        parser = Parser()
        parser.add_element(Wikilink)
        document = parser.parse(text)
        document.source_note = note
        return document

    return _build


@pytest.fixture
def mocked_db():
    def mock_db(returned_value: GetReferencesResponse):
        factory_mock = MagicMock(spec_set=SqlReferenceDatabaseFactory)
        mock = MagicMock(spec_set=IReferenceDB)
        mock.get_references_that_targets.return_value = returned_value
        factory_mock.return_value = mock
        references_db.REFERENCE_DB_FACTORY = factory_mock
        return factory_mock

    return mock_db
