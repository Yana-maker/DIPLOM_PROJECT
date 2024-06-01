import pytest
from utils.support_functions import hash_password, verify_password, bcrypt_context


@pytest.fixture
def mock_bcrypt_context(monkeypatch):
    def mock_hash(password):
        return f"hashed_{password}"

    def mock_verify(plain_password, hashed_password):
        return hashed_password == f"hashed_{plain_password}"

    monkeypatch.setattr(bcrypt_context, 'hash', mock_hash)
    monkeypatch.setattr(bcrypt_context, 'verify', mock_verify)


def test_hash_password(mock_bcrypt_context):
    """Тестирование функции хеширования пароля"""
    password = "mypassword"
    hashed_password = hash_password(password)
    assert hashed_password == "hashed_mypassword"


def test_verify_password(mock_bcrypt_context):
    """Тестирование проверки пароля"""
    plain_password = "mypassword"
    hashed_password = "hashed_mypassword"
    assert verify_password(plain_password, hashed_password) == True
