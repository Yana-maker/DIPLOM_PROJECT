from typing import Annotated, Dict, Optional
import jwt
from ecdsa.test_keys import data
from fastapi import Depends, HTTPException
from jose import JWTError
from datetime import datetime, timedelta
from starlette import status
from database import models
from settings import SECRET_KEY, ALGORITHM
from database.db import db_dependency
from utils.support_functions import bcrypt_context, oauth2_bearer, oauth2_scheme

ACCESS_TOKEN_EXPIRE_MINUTES = 20




def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT-токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

'''
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """Функция для создания токена JWT"""
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


'''
def authenticate_user(username: str, password: str, db):
    # user_db = db.query(models.User).filter(models.User.username == username).first()
    user_db1 = get_by_email_or_mobile_user(db, username)
    if not user_db1:
        return False
    if not bcrypt_context.verify(password, user_db1.password):
        return False
    return user_db1


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


def get_by_email_or_mobile_user(db: db_dependency, login):
    db_users = db.query(models.User).all()
    for db_user in db_users:
        if login in db_user.email or login in db_user.mobile:
            return db_user
