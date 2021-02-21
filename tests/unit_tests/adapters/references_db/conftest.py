import pytest
from linky_note.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from linky_note.dto.dto import ModifyConfig, Note, NotePath, NoteTitle
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db():

    return factory(modify_config=ModifyConfig())


@pytest.fixture
def note():
    return Note(note_title=NoteTitle("Entity"), note_path=NotePath("Entity.md"))
