from settings import bcrypt_context


def hash_password(password: str):
    """Функция для хэширования пароля"""
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Функция для проверки пароля при авторизации"""
    return bcrypt_context.verify(plain_password, hashed_password)
