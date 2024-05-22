from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import models
from database import db_dependency
from schemas import User
from utils.support_functions import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create/")
async def create_user(user: Annotated[User, Depends()], db: db_dependency):
    """создание пользователя"""

    db_user = models.User(username=user.username, email=user.email, mobile=user.mobile,
                          password=hash_password(user.password), password2=hash_password(user.password))
    db_user.is_active = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return user


@router.get("/read/{id}")
async def read_user(user_id: int, db: db_dependency):
    """просмотр пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    return result


@router.delete("/delete/{id}")
async def delete_user(user_id: int, db: db_dependency):
    """удаление пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    db.delete(result)
    db.commit()

    return result


@router.put("/put/{id}")
async def update_user(user_id: int, user: Annotated[User, Depends()], db: db_dependency):
    """редактирование пользователя"""

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
