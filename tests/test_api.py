import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from database import models
from database.models import User
from main import app


# Конфигурация базы данных для тестов
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:432502@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture(scope="function")
def client():
    """Тестовый клиент FastAPI"""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def session():
    """Тестовая сессия базы данных"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user_success(client: TestClient, session: SessionLocal):
    """Тест успешной регистрации пользователя"""
    new_user = {
        "is_active": "true",
        "username": "api test",
        "email": "api@e.com",
        "mobile": "+7 (005) 996-90-07",
        "password": "PassworD123%",
        "password2": "PassworD123%",
    }


    response = client.post("/auth/register/", json=new_user)
    print(f'{response.json()}')

    # Проверка, что пользователь был создан в базе данных
    user = session.query(models.User).filter(models.User.email == new_user["email"]).first()
    assert user is not None
    assert user.username == new_user["username"]
    assert user.email == new_user["email"]
    assert user.mobile == new_user["mobile"]


def test_create_user_existing_email(client: TestClient, session: SessionLocal):
    """Тест регистрации с уже существующей почтой"""
    create_user_data = {
        'username': 'api проверка почты',
        'email': 'apitest@e.com',
        'mobile': '+7 (025) 994-90-07',
        'password': 'PassworD123%',
        'password2': 'PassworD123%'

    }

    # Создаем пользователя с этой почтой
    user = User(
        username=create_user_data["username"],
        email=create_user_data["email"],
        mobile=create_user_data["mobile"],
        password=create_user_data["password"],
        password2=create_user_data["password2"],
        is_active=True,
    )
    session.add(user)
    session.commit()

    response = client.post("/auth/register/", json=create_user_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "такая почта уже существует"


def test_create_user_existing_mobile(client: TestClient, session: SessionLocal):
    """Тест регистрации с уже существующим номером телефона"""
    create_user_data = {
        'username': 'api проверка номера',
        'email': 'tes323t@e.com',
        'mobile': '+7 (025) 996-90-07',
        'password': 'PassworD123%',
        'password2': 'PassworD123%',
    }

    # Создаем пользователя с этим номером телефона
    user = User(
        username=create_user_data["username"],
        email=create_user_data["email"],
        mobile=create_user_data["mobile"],
        password=create_user_data["password"],
        password2=create_user_data["password2"],
        is_active=True,
    )
    session.add(user)
    session.commit()

    response = client.post("/auth/register/", json=create_user_data)

    assert response.status_code == 422
    assert response.json()["detail"] == "такой телефон уже существует"
