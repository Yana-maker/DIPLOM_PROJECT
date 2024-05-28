from datetime import datetime

from typer import models
from database.models import User, Product
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Конфигурация базы данных для тестов
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:432502@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture(scope="function")
def session():
    """Тестовая сессия базы данных"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user(session):
    """Тестирование создания пользователя"""
    user = User(
        username="testuser",
        email="test@extuyam6ple.com",
        mobile="+7 (925) 996-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(user)
    session.commit()
    session.refresh(user)



    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@extuyam6ple.com"
    assert user.mobile == "+7 (925) 996-90-07"
    assert user.password == 'PassworD123%'
    assert user.password2 == 'PassworD123%'
    assert user.is_active is True



def test_read_user(session):
    """Тестирование чтения пользователя"""
    user = User(
        username="testuser",
        email="test@extuya7mple.com",
        mobile="+7 (925) 997-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(user)
    session.commit()

    read_user = session.query(User).filter(User.id == user.id).first()

    assert read_user.username == "testuser"
    assert read_user.email == "test@extuya7mple.com"
    assert read_user.mobile == "+7 (925) 997-90-07"
    assert read_user.password == "PassworD123%"
    assert read_user.password2 == "PassworD123%"
    assert read_user.is_active is True


def test_update_user(session):
    """Тестирование обновления пользователя"""
    user = User(
        username="testuser",
        email="test@extuyamuple.com",
        mobile="+7 (925) 998-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(user)
    session.commit()

    user.username = "updated_testuser"
    user.email = "updated_test@extuyamuple.com"
    user.mobile = "+7 (923) 998-90-07"
    user.password = "updated_testpassDord23%"
    user.password2 = "updated_testpassDord23%"
    user.is_active = False

    session.commit()

    updated_user = session.query(User).filter(User.id == user.id).first()

    assert updated_user.username == "updated_testuser"
    assert updated_user.email == "updated_test@extuyamuple.com"
    assert updated_user.mobile == "+7 (923) 998-90-07"
    assert updated_user.password == "updated_testpassDord23%"
    assert updated_user.password2 == "updated_testpassDord23%"
    assert updated_user.is_active is False


def test_delete_user(session):
    """Тестирование удаления пользователя"""
    user = User(
        username="testuser",
        email="test@extuyampile.com",
        mobile="+7 (925) 999-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(user)
    session.commit()
    session.delete(user)
    session.commit()

    deleted_user = session.query(User).filter(User.id == user.id).first()
    assert deleted_user is None



def test_create_product(session):
    """Тестирование создания продукта"""

    owner = User(
        username="testuser",
        email="test@ex3533tuyampile.com",
        mobile="+7 (925) 889-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )
    session.add(owner)
    session.commit()

    product = Product(
        title="Test Product",
        description="This is a test product",
        price=100,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        owner=owner.id
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    assert product.id is not None
    assert product.title == "Test Product"
    assert product.description == "This is a test product"
    assert product.price == 100
    assert product.owner == owner.id


def test_read_product(session):
    """Тестирование чтения продукта"""

    owner = User(
        username="testuser",
        email="test@ex3dfs33tuyampile.com",
        mobile="+7 (923) 889-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(owner)
    session.commit()

    product = Product(
        title="Test Product",
        description="This is a test product",
        price=100,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        owner=owner.id
    )

    session.add(product)
    session.commit()

    read_product = session.query(Product).filter(Product.id == product.id).first()

    assert read_product.title == "Test Product"
    assert read_product.description == "This is a test product"
    assert read_product.price == 100
    assert read_product.owner == owner.id


def test_update_product(session):
    """Тестирование обновления продукта"""

    owner = User(
        username="testuser",
        email="test@ex3dffsds33tuyampile.com",
        mobile="+7 (912) 889-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(owner)
    session.commit()

    product = Product(
        title="Test Product",
        description="This is a test product",
        price=100,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        owner=owner.id
    )

    session.add(product)
    session.commit()

    product.title = "Updated Test Product"
    product.description = "This is an updated test product"
    product.price = 200
    product.is_active = False

    session.commit()

    updated_product = session.query(Product).filter(Product.id == product.id).first()

    assert updated_product.title == "Updated Test Product"
    assert updated_product.description == "This is an updated test product"
    assert updated_product.price == 200
    assert updated_product.is_active is False


def test_delete_product(session):
    """Тестирование удаления продукта"""

    owner = User(
        username="testuser",
        email="test@le.com",
        mobile="+7 (991) 889-90-07",
        password='PassworD123%',
        password2='PassworD123%',
        is_active=True,
    )

    session.add(owner)
    session.commit()

    product = Product(
        title="Test Product",
        description="This is a test product",
        price=100,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        owner=owner.id
    )

    session.add(product)
    session.commit()

    session.delete(product)
    session.commit()

    deleted_product = session.query(Product).filter(Product.id == product.id).first()

    assert deleted_product is None
