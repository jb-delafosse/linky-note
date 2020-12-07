import factory
from factory import SubFactory
from marko_backlinks.adapters.references_db import tables
from marko_backlinks.adapters.references_db.query_builders import (
    SQLiteReferenceDatabase,
)
from marko_backlinks.dto.dto import Note, Reference
from marko_backlinks.interfaces.references_db import (
    GetNoteByTitleQuery,
    GetReferencesThatTarget,
    UpsertNoteQuery,
    UpsertReferenceQuery,
)
from tests.unit_tests.adapters.references_db.conftest import (
    factory as sql_db_factory,
)


class NoteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = tables.Note
        sqlalchemy_session = sql_db_factory._session
        sqlalchemy_session_persistence = "commit"

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
        sqlalchemy_session = sql_db_factory._session
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_get_or_create = (
            "target_note_id",
            "source_note_id",
        )

    source_note = SubFactory(NoteFactory)
    target_note = SubFactory(NoteFactory)
    source_note_id = factory.LazyAttribute(lambda obj: obj.source_note.id)
    target_note_id = factory.LazyAttribute(lambda obj: obj.target_note.id)
    context = factory.Faker("sentence")


def test_upsert_note(test_db: SQLiteReferenceDatabase, note: Note):
    # Given
    query = UpsertNoteQuery(note=note)

    # WHEN
    db_response = test_db.upsert_note(query)

    # THEN
    assert db_response.note == note
    assert isinstance(db_response.note_id, int)


def test_upsert_reference(test_db: SQLiteReferenceDatabase):
    # Given
    note_1, note_2 = NoteFactory.create_batch(size=2)
    reference = Reference(
        source_note=Note(
            note_title=note_1.note_title, note_path=note_1.note_path
        ),
        target_note=Note(
            note_title=note_2.note_title, note_path=note_2.note_path
        ),
        context=f"A nice reference to {note_2.note_title}",
    )

    query = UpsertReferenceQuery(
        source_note_id=note_1.id, target_note_id=note_2.id, reference=reference
    )

    # WHEN
    db_response = test_db.upsert_reference(query)

    # THEN
    assert db_response.source_note_id == note_1.id
    assert db_response.target_note_id == note_2.id
    assert db_response.reference == reference


def test_get_note_by_title(test_db: SQLiteReferenceDatabase):
    # GIVEN
    note_1, note_2 = NoteFactory.create_batch(size=2)

    query = GetNoteByTitleQuery(note_title=note_2.note_title)

    # WHEN
    db_response = test_db.get_note_by_title(query)

    # THEN
    assert db_response.note_id == note_2.id


def test_get_references_by_tatitle(test_db: SQLiteReferenceDatabase):
    # GIVEN
    note_1 = NoteFactory.create(higher_edges=2)
    query = GetReferencesThatTarget(note_title=note_1.note_title)

    # WHEN
    db_response = test_db.get_references_that_target(query)

    # THEN
    # - I find the 2 references
    # - The references are returned sorted by source_note_title
    assert len(db_response.references) == 2
    assert (
        db_response.references[0].source_note.note_title
        <= db_response.references[1].source_note.note_title
    )
