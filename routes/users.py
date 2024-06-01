from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from database import models
from database.db import db_dependency
from database.schemas import User
from utils.auth import get_current_user
from utils.support_functions import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create/")
async def create_user(user: User, db: db_dependency):
    """Создание пользователя"""
    user_new = models.User(
        username=user.username,
        email=user.email,
        mobile=user.mobile,
        password=bcrypt_context.hash(user.password),
        password2=bcrypt_context.hash(user.password),
        is_active=True
    )
    db.add(user_new)
    db.commit()
    db.refresh(user_new)

    return user


@router.get("/read/{id}")
async def read_user(user_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    """Просмотр пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    return result


@router.delete("/delete/{id}")
async def delete_user(user_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    """Удаление пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    db.delete(result)
    db.commit()

    return result


@router.put("/put/{id}")
async def update_user(user_id: int, user: Annotated[User, Depends()], db: db_dependency,
                      current_user: User = Depends(get_current_user)):
    """Редактирование пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")
    else:
        result.username = user.username
        result.email = user.email
        result.mobile = user.mobile
        result.password = user.password
        result.password2 = user.password2

        db.commit()

        return user
