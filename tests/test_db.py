import pytest
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from database.db import get_db, db_dependency


def test_get_db():
    db = next(get_db())
    assert isinstance(db, Session)

