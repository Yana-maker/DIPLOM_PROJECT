import jwt
import pytest
from datetime import timedelta
from unittest.mock import Mock, patch
from settings import SECRET_KEY, ALGORITHM, bcrypt_context
from utils.auth import create_access_token, authenticate_user, get_by_email_or_mobile_user, get_current_user


'''
@pytest.mark.parametrize("username, user_id, expires_delta, expected", [
    ("test_user", 1, timedelta(hours=1), True),
    ("invalid_user", 2, timedelta(hours=1), False),
])

def test_create_access_token(username, user_id, expires_delta, expected):
    token = create_access_token(username, user_id, expires_delta)
    assert (jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('sub') == username) == expected
'''


def test_authenticate_user():
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = [
        Mock(email="test@test.com", mobile="1234567890", password=bcrypt_context.hash("password123"))
    ]
    assert authenticate_user("test@test.com", "password123", mock_db) is not False


def test_get_by_email_or_mobile_user():
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = [
        Mock(email="test@test.com", mobile="1234567890")
    ]
    assert get_by_email_or_mobile_user(mock_db, "test@test.com") is not None


class MockRequest:
    def __init__(self, token):
        self.headers = {'Authorization': f'Bearer {token}'}


'''async def test_get_current_user():
    mock_token = create_access_token("test_user", 1, timedelta(hours=1))
    request = MockRequest(mock_token)
    with patch("settings.oauth2_bearer", return_value=request):
        current_user = await get_current_user(request.headers['Authorization'])
        assert current_user['username'] == "test_user"'''
