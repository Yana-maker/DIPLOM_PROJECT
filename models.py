from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from database import Base


class User(Base):
    """таблица в БД пользователь"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    mobile = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    password2 = Column(String, index=True)
    is_active = Column(Boolean, index=True, default=False)


class Product(Base):
    """таблица в БД продукт"""
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True, default=None)
    price = Column(Integer, index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    is_active = Column(Boolean, index=True)
    owner = Column(Integer, ForeignKey('users.id'))


class Cart(Base):
    """таблица в БД корзина"""
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, index=True)
    product = Column(Integer, ForeignKey('product.id'))
