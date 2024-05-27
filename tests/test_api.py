import pytest
from fastapi.testclient import TestClient
from starlette import status
from main import app

client = TestClient(app)


@pytest.fixture()
def client():
    return TestClient(app)


def test_create_user_register(client):
    # Создаем тестовые данные
    test_user = {
        "username": "test_user",
        "email": "test@example.com",
        "mobile": "+7 (925) 000-00-07",
        "password": "passworD123%",
        "password2": "passworD123%"
    }

    # Отправляем POST-запрос на регистрацию пользователя
    response = client.post("/register/", json=test_user)

    # Проверяем статус-код
    assert response.status_code == 201

    # Проверяем, что в ответе есть access_token и token_type
    assert "access_token" in response.json()
    assert "token_type" in response.json()



def test_login_for_access_token(client):
    data = {
            "username": "test_user",
            "password": "passworD123%"
    }

    response = client.post("/token/", json=data)

    print(response.json())

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
