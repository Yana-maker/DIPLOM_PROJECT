from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# to get a string like this run:
# openssl rand -hex 32

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2PasswordBearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def hash_password(password: str):
    """Функция для хэширования пароля"""
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Функция для проверки пароля при авторизации"""
    return bcrypt_context.verify(plain_password, hashed_password)
