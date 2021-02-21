from sqlalchemy import Column, ForeignKey, UniqueConstraint, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()  # pylint: disable=invalid-name


# mypy don't support Base as base class.
class Note(Base):  # type: ignore
    __tablename__ = "notes"

    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    note_title = Column(
        types.String, nullable=False, sqlite_on_conflict_unique="IGNORE"
    )
    note_path = Column(types.String, nullable=False)
    UniqueConstraint("note_title")

    def source_notes(self):
        return [x.source_note for x in self.lower_edges]

    def target_notes(self):
        return [x.target_note for x in self.higher_edges]


# mypy don't support Base as base class.
class Reference(Base):  # type: ignore
    __tablename__ = "references"

    id = Column(types.INTEGER, primary_key=True, autoincrement=True)
    context = Column(types.String, nullable=False)
    source_note_id = Column(types.INTEGER, ForeignKey("notes.id"))
    target_note_id = Column(types.INTEGER, ForeignKey("notes.id"))
    source_note = relationship(
        Note, primaryjoin=source_note_id == Note.id, backref="lower_edges"
    )
    target_note = relationship(
        Note, primaryjoin=target_note_id == Note.id, backref="higher_edges"
    )
