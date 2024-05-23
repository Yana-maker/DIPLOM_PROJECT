from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from database.db import db_dependency
from database.models import User
from database.schemas import Cart
from database import models
from utils.auth import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/create/")
async def create_cart(cart: Annotated[Cart, Depends()], db: db_dependency,
                      current_user: User = Depends(get_current_user)):
    """создание корзины"""
    for product in cart.product:
        db_cart = models.Cart(product=product)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)

    return cart


@router.get("/read/{id}")
async def read_cart(cart_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    """просмотр корзины"""

    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if db_cart is None:
        raise HTTPException(status_code=404, detail="такой корзины нет")

    return sum(db_cart.product.price)


@router.delete("/delete/{id}")
async def delete_cart(cart_id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    """удаление корзины"""

    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if db_cart is None:
        raise HTTPException(status_code=404, detail="такой корзины нет")

    db.delete(db_cart)
    db.commit()

    return db_cart
