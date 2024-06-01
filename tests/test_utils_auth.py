from unittest.mock import Mock
from settings import bcrypt_context
from utils.auth import authenticate_user, get_by_email_or_mobile_user


def test_authenticate_user():
    """Тестирование функции авторизации пользователя"""
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = [
        Mock(email="test_create_user_register_success@example.com", mobile="+7 (999) 999-99-99",
             password=bcrypt_context.hash("Passwor123%"))
    ]
    assert authenticate_user("test_create_user_register_success@example.com", "Passwor123%", mock_db) is not False


def test_get_by_email_or_mobile_user():
    """Тестирование функции проверки почты/телефона пользователя"""
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = [
        Mock(email="test@test.com", mobile="1234567890")
    ]
    assert get_by_email_or_mobile_user(mock_db, "test@test.com") is not None


