from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy_utils import database_exists

from apb.database.utils import (
    create_db,
    engine_from_path,
    engine_from_session,
    path_to_uri,
)

# Define a test base and a simple model for testing
TestBase = declarative_base()


class User(TestBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)


@pytest.fixture
def temp_db_path(tmp_path: Path):
    return tmp_path / "test.db"


@pytest.fixture
def engine(temp_db_path):
    """Create an SQLAlchemy engine connected to the temporary database."""
    return engine_from_path(temp_db_path)


def test_path_to_uri(temp_db_path):
    uri = path_to_uri(temp_db_path)
    assert uri.startswith("sqlite:///")
    assert uri.endswith(str(temp_db_path))


def test_engine_from_path(temp_db_path):
    engine = engine_from_path(temp_db_path)
    assert isinstance(engine, Engine)
    assert str(engine.url).startswith("sqlite:///")


def test_engine_from_session(engine):
    with Session(engine) as session:
        assert engine_from_session(session) == engine


def test_create_db(engine):
    assert not database_exists(engine.url)
    create_db(engine, TestBase)
    assert database_exists(engine.url)


def test_create_db_already_exists(engine):
    create_db(engine, TestBase)
    assert database_exists(engine.url)

    with pytest.raises(ValueError, match="Database already exists."):
        create_db(engine, TestBase, exist_ok=False)
