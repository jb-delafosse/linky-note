import pytest
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.dto.dto import Note
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db():

    return factory()


@pytest.fixture
def note():
    return Note(note_title="Entity", note_path="Entity.md")
