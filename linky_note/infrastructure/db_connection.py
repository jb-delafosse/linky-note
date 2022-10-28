from linky_note.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from linky_note.interfaces.references_db import ReferenceDbFactory
from sqlalchemy import create_engine


def setup_db() -> ReferenceDbFactory:
    ENGINE = create_engine("sqlite://")
    return SqlReferenceDatabaseFactory(ENGINE)
