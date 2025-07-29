from __future__ import annotations

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy_utils import database_exists

from apb.types import Pathish

# For now, this is a strictly SQLite3 library
DB_SCHEME = "sqlite:///"


def path_to_uri(path: Pathish) -> str:
    return f"{DB_SCHEME}{path}"


def engine_from_path(path: Pathish) -> Engine:
    uri = str(path)
    if not uri.startswith(DB_SCHEME):
        uri = path_to_uri(uri)

    return create_engine(uri)


def engine_from_session(session: Session) -> Engine:
    connection = session.get_bind()

    if not isinstance(connection, Engine):
        raise ValueError(f"Connection to {session} is not an engine")

    return connection


def create_db(engine: Engine, model: DeclarativeMeta, exist_ok: bool = False) -> None:
    """Create the database.

    Args:
        exist_ok:
            If False, raises an error if the database already exists. If True and the DB
            exists, no operation takes place.

    Raises:
        ValueError: If the database exists and `exist_ok` is False.
    """
    if database_exists(engine.url) and not exist_ok:
        raise ValueError("Database already exists.")

    model.metadata.create_all(engine)
