import datetime
import phonenumbers
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, Union, List, Annotated

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from validators import validate_mobile

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class User(BaseModel):
    """модель пользователя"""
    username: str
    email: EmailStr = Field(unique=True)
    mobile: str = Field(unique=True)
    password: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    is_active: Optional[bool] = True

    '''class Config:
        orm_mode = True'''


class Product(BaseModel):
    """модель продукта"""
    title: str
    description: Optional[str] = None
    price: int
    created_at: str
    updated_at: str
    is_active: bool
    owner: Optional[int] = None


class Cart(BaseModel):
    """модель корзины"""
    product: List[Product]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/user/")
async def create_user(user: Annotated[User, Depends()], db: db_dependency):
    """создание пользователя"""

    db_user = models.User(username=user.username, email=user.email, mobile=validate_mobile(user.mobile),
                          password=user.password, password2=user.password2)
    db_user.is_active = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        'username': user.username
    }


@app.get("/user/read/{id}")
async def read_user(user_id: int, db: db_dependency):
    """просмотр пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    return result


@app.delete("/user/delete/{id}")
async def delete_user(user_id: int, db: db_dependency):
    """удаление пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    db.delete(result)
    db.commit()


@app.put("/user/put/{id}")
async def update_user(user_id: int, db: db_dependency):
    """редактирование пользователя"""

    pass
