from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from database import db_dependency
from schemas import Cart
import models


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/create/")
async def create_cart(cart: Annotated[Cart, Depends()], db: db_dependency):
    """создание корзины"""

    db_cart = models.Cart(product=cart.product)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return cart


@router.get("/read/{id}")
async def read_cart(cart_id: int, db: db_dependency):
    """просмотр корзины"""

    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if db_cart is None:
        raise HTTPException(status_code=404, detail="такой корзины нет")

    return db_cart


@router.delete("/delete/{id}")
async def delete_cart(cart_id: int, db: db_dependency):
    """удаление корзины"""

    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if db_cart is None:
        raise HTTPException(status_code=404, detail="такой корзины нет")

    db.delete(db_cart)
    db.commit()

    return db_cart
