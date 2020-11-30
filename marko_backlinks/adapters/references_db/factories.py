from marko_backlinks.adapters.references_db.query_builders import (
    SQLiteReferenceDatabase,
)
from marko_backlinks.adapters.references_db.tables import Base
from sqlalchemy.engine import Connectable
from sqlalchemy.orm import sessionmaker


class SqlReferenceDatabaseFactory:
    _engine = None
    _session = None

    def __new__(cls, db_connection: Connectable):
        cls._engine = db_connection
        Base.metadata.create_all(cls._engine)
        Session = sessionmaker(bind=cls._engine)  # pylint: disable=invalid-name
        cls._session = Session()
        return super().__new__(cls)

    @classmethod
    def __call__(cls) -> SQLiteReferenceDatabase:
        #  SQLAlchemy engine does not allow variable permutation in the string
        # But a Session does
        return SQLiteReferenceDatabase(cls._session)
