from typing import Any
from typing_extensions import Self

from pydantic import BaseModel, Field, EmailStr, field_validator


class User(BaseModel):
    email: EmailStr = Field(default=..., description="E-mail пользователя")
    name: str = Field(default=..., min_length=4, max_length=20, description="Имя пользователя")
    password: str = Field(default=..., description="Пароль пользователя")


    @field_validator("password")
    @classmethod
    def password_validate(cls, password):
        if len(password) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов")
        if not any(char.isdigit() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.isupper() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        return password
