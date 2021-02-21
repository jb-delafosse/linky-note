import pytest
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.dto.dto import ModifyConfig, Note, NotePath, NoteTitle
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db():

    return factory(modify_config=ModifyConfig())


@pytest.fixture
def note():
    return Note(note_title=NoteTitle("Entity"), note_path=NotePath("Entity.md"))
