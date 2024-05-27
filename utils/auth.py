from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from jose import JWTError
from datetime import datetime, timedelta
from starlette import status
from database import models
from settings import SECRET_KEY, ALGORITHM
from database.db import db_dependency
from settings import bcrypt_context, oauth2_bearer


def create_access_token(username: any, user_id: int, expires_delta: timedelta):
    """Функция для создания токена JWT"""
    to_encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: any, password: str, db):
    """проверка авторизации пользователя"""
    user_db1 = get_by_email_or_mobile_user(db, username)
    if not user_db1:
        return False
    if not bcrypt_context.verify(password, user_db1.password):
        return False
    return user_db1


def get_by_email_or_mobile_user(db: db_dependency, username):
    """функция для проверки username при авторизации"""
    db_users = db.query(models.User).all()
    for db_user in db_users:
        if username in db_user.mobile or username in db_user.email:
            return db_user


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """функция для проверки авторизированного пользователя"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Нет авторизированного пользователя',
            )
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Нет авторизированного пользователя',
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
