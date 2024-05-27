from database.models import User, Product
import pytest, pytest_asyncio
import datetime


def test_user():
    user = User(id=1, username='test_user', email='test@example.com', mobile='+7 (925) 000-00-07',
                password='passworD123%', password2='passworD123%', is_active=True)

    assert user.id == 1
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.mobile == '+7 (925) 000-00-07'
    assert user.password == 'passworD123%'
    assert user.password2 == 'passworD123%'
    assert user.is_active == True



def test_product():
    product = Product(id=1, title='test_product', price=150, created_at=datetime.datetime.now(),
                      is_active=True, owner=1)

    assert product.id == 1
    assert product.title == 'test_product'
    assert product.price == 150
    assert product.created_at == datetime.datetime.now()
    assert product.is_active == True
    assert product.owner == 1
