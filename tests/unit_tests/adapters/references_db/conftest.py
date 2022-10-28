import factory
import pytest
from factory import SubFactory
from linky_note.adapters.references_db import tables
from linky_note.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from linky_note.adapters.references_db.query_builders import (
    SQLiteReferenceDatabase,
)
from linky_note.dto.dto import ModifyConfig, Note, NotePath, NoteTitle
from linky_note.interfaces.references_db import IReferenceDB
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

ENGINE = create_engine("sqlite://")
session = scoped_session(sessionmaker(bind=ENGINE))
sql_db_factory = SqlReferenceDatabaseFactory(ENGINE)


@pytest.fixture
def test_db() -> IReferenceDB:
    yield SQLiteReferenceDatabase(
        session(), reference_by=ModifyConfig().reference_by
    )
    session.remove()


@pytest.fixture
def note():
    return Note(note_title=NoteTitle("Entity"), note_path=NotePath("Entity.md"))


class NoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tables.Note
        sqlalchemy_session = session

    note_title = factory.Faker("word")
    note_path = factory.LazyAttribute(lambda obj: "%s.md" % obj.note_title)

    @factory.post_generation
    def higher_edges(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            assert isinstance(extracted, int)
            refs = ReferenceFactory.create_batch(
                size=extracted,
                target_note=self,
                target_note_id=self.id,
                **kwargs,
            )
            self.higher_edges = refs

    @factory.post_generation
    def lower_edges(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            assert isinstance(extracted, int)
            ReferenceFactory.create_batch(
                size=extracted,
                source_note=self,
                source_note_id=self.id,
                **kwargs,
            )


class ReferenceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tables.Reference
        sqlalchemy_session = session
        sqlalchemy_get_or_create = (
            "target_note_id",
            "source_note_id",
        )

    source_note = SubFactory(NoteFactory)
    target_note = SubFactory(NoteFactory)
    source_note_id = factory.LazyAttribute(lambda obj: obj.source_note.id)
    target_note_id = factory.LazyAttribute(lambda obj: obj.target_note.id)
    context = factory.Faker("sentence")
