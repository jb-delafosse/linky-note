from unittest.mock import MagicMock

import pytest
from marko import Markdown
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.dto.dto import Note
from marko_backlinks.interfaces import references_db
from marko_backlinks.interfaces.references_db import (
    GetReferencesResponse,
    IReferenceDB,
)
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db():
    return factory()


@pytest.fixture
def build_ast():
    from marko_backlinks.adapters.markdown.marko_modifier import (
        LINKED_REFERENCE_SECTION_HEADER,
    )

    def _build(note: Note):
        text = (
            f"# {note.note_title}\n"
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
            f"## {LINKED_REFERENCE_SECTION_HEADER}\n"
            "\n"
            "  * [Note A](Note A.md)\n"
            f"    * a reference to [{note.note_title}]({note.note_path})\n"
            f"    * another reference to [{note.note_title}]({note.note_path})\n"
        )
        document = Markdown().parse(text)
        document.source_note = note
        return document

    return _build


@pytest.fixture
def mocked_db():
    def mock_db(returned_value: GetReferencesResponse):
        factory_mock = MagicMock(spec_set=SqlReferenceDatabaseFactory)
        mock = MagicMock(spec_set=IReferenceDB)
        mock.get_references_that_target.return_value = returned_value
        factory_mock.return_value = mock
        return factory_mock

    return mock_db