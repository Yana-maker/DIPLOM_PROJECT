from typing import Annotated
import models
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from database import db_dependency
from utils.support_functions import verify_password


# Создание объекта OAuth2PasswordBearer для JWT авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBasic()


@router.get('/basic-auth/')
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """авторизация пользователя"""
    return {
        'massage': f'Hi! {credentials.username}',
        'username': credentials.username,
        'password': credentials.password
    }


@router.get('/check_basic-auth/')
async def check_auth_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)], db: db_dependency):
    """проверка пользователя есть он ли в БД"""
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль",
        headers={"WWW-Authenticate": "Basic"}

    )

    db_user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if db_user is None:
        return unauthed_exc

    if not verify_password(credentials.password.encode('utf-8'), db_user.password):
        return unauthed_exc

    return {
        "massage": "авторизация прошла успешно",
        "user": db_user
    }
