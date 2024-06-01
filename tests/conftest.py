import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import app
from fastapi.testclient import TestClient

# Конфигурация базы данных для тестов

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:432502@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
def client():
    """Тестовый клиент FastAPI"""
    with TestClient(app) as client:
        yield client
