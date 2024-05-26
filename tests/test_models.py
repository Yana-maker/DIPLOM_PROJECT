from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from main import app
from database.models import User
from routes.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def test_user():
    """Создает тестового пользователя для использования в тестах."""
    user = User(
        username="test",
        email="yansdfsda@gmail.com",
        mobile="+7 (999) 999-99-99",
        password="Fdsdvsds324%",
        password2="Fdsdvsds324%"

    )

    yield user


@pytest.fixture
def authorized_client(test_user):
    """Создает клиент с токеном доступа для авторизованного пользователя."""
    token = create_access_token(data={'sub': test_user.username})
    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client


def test_unauthorized_endpoint(client):
    """Проверяет, что endpoint доступен только для авторизованных пользователей."""
    response = client.get("/protected_endpoint/")
    assert response.status_code == 401  # Ожидается ошибка 401 (Неавторизованный)


def test_authorized_endpoint(authorized_client):
    """Проверяет, что endpoint доступен для авторизованных пользователей."""
    response = authorized_client.get("/protected_endpoint/")
    assert response.status_code == 200  # Ожидается успешный ответ 200


def test_create_user(client):
    """Проверяет, что создание нового пользователя работает."""
    response = client.post("/users/", json={"username": "new_user", "email": "new_user@example.com", "password": "password123"})
    assert response.status_code == 201  # Ожидается код 201 (Создано)


def test_get_user_details(authorized_client, test_user):
    """Проверяет, что получение данных пользователя работает."""
    response = authorized_client.get(f"/users/{test_user.username}")
    assert response.status_code == 200  # Ожидается успешный ответ 200
    assert response.json()["username"] == test_user.username  # Проверяем, что верное имя пользователя


def test_update_user_details(authorized_client, test_user):
    """Проверяет, что обновление данных пользователя работает."""
    response = authorized_client.put(f"/users/{test_user.username}", json={"email": "new_email@example.com"})
    assert response.status_code == 200  # Ожидается успешный ответ 200
    assert response.json()["email"] == "new_email@example.com"  # Проверяем обновленное значение


def test_delete_user(authorized_client, test_user):
    """Проверяет, что удаление пользователя работает."""
    response = authorized_client.delete(f"/users/{test_user.username}")
    assert response.status_code == 204  # Ожидается код 204 (Нет контента)