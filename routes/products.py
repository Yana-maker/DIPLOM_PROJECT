from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import models
from database import db_dependency
from schemas import Product
import datetime


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/create/")
async def create_product(product: Annotated[Product, Depends()], db: db_dependency):
    """создание продукта, нужно доработать"""

    db_product = models.Product(title=product.title, description=product.description, price=product.price,
                                created_at=datetime.datetime.now(), is_active=product.is_active, owner=product.owner)
    db_product.update_at = None
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return product


@router.get("/read/{id}")
async def read_product(product_id: int, db: db_dependency):
    """просмотр продукта"""

    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="такой продукт не найден")

    return db_product


@router.delete("/delete/{id}")
async def delete_product(product_id: int, db: db_dependency):
    """удаление продукта"""

    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="такой продукт не найден")

    db.delete(db_product)
    db.commit()

    return db_product


@router.put("/update/{id}")
async def update_product(product_id: int, product: Annotated[Product, Depends()], db: db_dependency):
    """редактирование продукта"""

    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if db_product is None:
        raise HTTPException(status_code=404, detail="такой продукт не найден")

    db_product.title = product.title
    db_product.description = product.description
    db_product.price = product.price
    db_product.created_at = product.created_at
    db_product.updated_at = datetime.datetime.now()
    db_product.is_active = product.is_active
    db_product.owner = product.owner
    db.commit()

    return db_product
