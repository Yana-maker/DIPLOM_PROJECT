from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# to get a string like this run:
# openssl rand -hex 32

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


# Функция для хэширования пароля
def hash_password(password: str):
    return bcrypt_context.hash(password)


# Функция для проверки пароля при авторизации
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)
