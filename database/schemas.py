from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
import re


class User(BaseModel):
    """модель пользователя"""

    is_active: Optional[bool] = True
    username: str
    email: EmailStr
    mobile: str
    password: str
    password2: str


class LoginUser(BaseModel):
    login: str
    password: str


class CreateUserRequest(User):

    username: str
    email: EmailStr
    mobile: str
    password: str
    password2: str

    @field_validator("mobile")
    def phone_number_validation(cls, value):
        """валидация телефоного номера"""

        # Шаблон для валидации телефонного номера (например, +7 (999) 999-99-99)
        regex = r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$"
        if not re.match(regex, value):
            raise HTTPException(status_code=400,
                                detail="Неверный формат телефонного номера.",
                                )
        return value

    @field_validator("password")
    def password_validation(cls, value):
        # проверка длины пароля
        if len(value) < 8:
            raise HTTPException(status_code=400,
                                detail="Пароль должен быть не менее 8 символов.",
                                )

        # Проверка на латиницу и спецсимволы
        if not re.match(r"^[a-zA-Z0-9$%&!]*$", value):
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать только латинские буквы, цифры и символы $%&!",
                                )

        # Проверка на наличие хотя бы одного символа верхнего регистра
        if not any(c.isupper() for c in value):
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать хотя бы один символ верхнего регистра.",
                                )

        # Проверка на наличие хотя бы одного спецсимвола
        if not any(c in "$%&!" for c in value):
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать хотя бы один спецсимвол из $%&!",
                                )
        return value

    @field_validator("password2")
    def confirm_password_validation(cls, value, values):
        if value != values.get("password"):
            raise HTTPException(status_code=400,
                                detail="Пароли не совпадают",
                                )
        return value


class Product(BaseModel):
    """модель продукта"""
    title: str
    description: Optional[str] = None
    price: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: bool
    owner: Optional[int] = None


class Cart(BaseModel):
    """модель корзины"""

    product: List[Product]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str = None
