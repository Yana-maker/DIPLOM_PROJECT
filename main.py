import datetime
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, Union, List, Annotated
from fastapi.responses import JSONResponse

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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: bool
    owner: Optional[int] = None

    class Config:
        exclude = "owner"


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


@app.get("/login/")
async def login():
    """вход"""
    pass


@app.get("/logout/")
async def logout():
    """выход"""
    pass


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
async def update_user(user_id: int, user: Annotated[User, Depends()], db: db_dependency):
    """редактирование пользователя"""

    result = db.query(models.User).filter(models.User.id == user_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="такой пользователь не найден")

    else:
        result.username = user.username
        result.email = user.email
        result.mobile = validate_mobile(user.mobile)
        result.password = user.password
        result.password2 = user.password2

        db.commit()

        return user


@app.post("/product/")
async def create_product(product: Annotated[Product, Depends()], db: db_dependency):
    """создание продукта, нужно доработать"""

    db_product = models.Product(title=product.title, description=product.description, price=product.price,
                                created_at=datetime.datetime.now(), is_active=product.is_active, owner=product.owner)
    db_product.update_at = None
    db.add(db_product)
    db.commit()
    db.refresh(db_product)


    return product

