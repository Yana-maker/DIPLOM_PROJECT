from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_create_user():
    """Тест на создание пользователя"""
    response = client.post("/users/create/", json={
          "is_active": True,
          "username": "testuser",
          "email": "userexample@dsfs.com",
          "mobile": "+7 (920) 031-99-99",
          "password": "stringD123%",
          "password2": "stringD123%"
    })
    assert response.status_code == 200, response.text
    assert response.json()["username"] == "testuser"


def test_read_user():
    """Тест на чтение пользователя"""
    response = client.get("/users/read/1")
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"


def test_update_user():
    """Тест на редактирование пользователя"""
    data = {
        "username": "updateduser",
        "email": "updateduser@example.com",
        "mobile": "9876543210",
        "password": "updatedpassword",
        "password2": "updatedpassword"
    }
    response = client.put("/users/put/1", json=data)
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"


def test_delete_user():
    """Тест на удаление пользователя"""
    response = client.delete("/users/delete/1")
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"
