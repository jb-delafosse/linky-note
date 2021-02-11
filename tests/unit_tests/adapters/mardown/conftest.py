import pytest
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.interfaces import references_db
from sqlalchemy import create_engine

ENGINE = create_engine("sqlite://")
factory = SqlReferenceDatabaseFactory(ENGINE)

references_db.REFERENCE_DB_FACTORY = SqlReferenceDatabaseFactory(ENGINE)
