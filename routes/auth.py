from datetime import timedelta
from typing import Annotated
from database import models
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from database.db import db_dependency
from database.schemas import CreateUserRequest, Token, LoginUser
from utils.auth import create_access_token, \
    authenticate_user, bcrypt_context, user_dependency, get_by_email_or_mobile_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/register/', status_code=status.HTTP_201_CREATED)
async def create_user_register(db: db_dependency, create_user_request: Annotated[CreateUserRequest, Depends()]):
    """регистарация пользователя"""

    db_user_email = db.query(models.User).filter(models.User.email == create_user_request.email).first()
    db_user_mobile = db.query(models.User).filter(models.User.mobile == create_user_request.mobile).first()

    if db_user_email:
        raise HTTPException(
            status_code=400,
            detail="такая почта уже существует"
        )
    if db_user_mobile:
        raise HTTPException(
            status_code=400,
            detail="такой телефон уже существует"
        )

    created_user_model = models.User(
        username=create_user_request.username,
        email=create_user_request.email,
        mobile=create_user_request.mobile,
        password=bcrypt_context.hash(create_user_request.password),
        password2=bcrypt_context.hash(create_user_request.password),
        is_active=True

    )

    db.add(created_user_model)
    db.commit()
    db.refresh(created_user_model)

    return create_user_request


@router.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
):
    """создание токена"""
    authed_user = authenticate_user(form_data.username, form_data.password, db)
    if not authed_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="нет такого пользователя",
                            )

    token = create_access_token(authed_user.username, authed_user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


@router.post("/login")
async def login_user(db: db_dependency, form_data: LoginUser = Depends()):
    """вход по телефону или почте"""

    user_db = get_by_email_or_mobile_user(db, form_data.login)
    if not user_db:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='неверные почта или телефон',
            )

    if not bcrypt_context.verify(form_data.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="неверный пароль",
        )

    token = create_access_token(user_db.username, user_db.id, timedelta(minutes=20))

    return {
        'access_token': token,
        'token_type': 'bearer',
    }


@router.get("/me", status_code=status.HTTP_200_OK)
async def user(user_db: user_dependency, db: db_dependency):
    """проверка авторизированного пользователя"""
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Нет авторизированного пользователя")
    return {'user_db': user_db}
