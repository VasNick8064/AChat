from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator

"""
schemas - здесь представлены модели, которые мы используем
"""

"""
(Pydantic) 
Модель UserReg: эта модель используется для проверки и сериализации пользовательского ввода, 
особенно во время регистрации или входа в систему.
"""


class UserReg(BaseModel):
    email: EmailStr = Field(default=..., description="E-mail пользователя")
    name: str = Field(default=..., min_length=4, max_length=20, description="Имя пользователя")
    hashed_password: str = Field(default=..., description="Пароль пользователя")

    @field_validator("hashed_password")
    @classmethod
    def password_validate(cls, hashed_password):
        if len(hashed_password) < 8:
            raise ValueError("Пароль должен содержать не менее 8 символов")
        if not any(char.isdigit() for char in hashed_password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not any(char.isupper() for char in hashed_password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        return hashed_password


"""
Test
"""
# data = {
#     "email": "afwf@mail.ru",
#     "name": "Test",
#     "password": "Password1"
# }
#
#
# def test_val(data: dict):
#     try:
#         users = User(**data)
#         print(users)
#     except ValidationError as e:
#         print(f"Ошибка валидации: {e}")
#
#
# test_val(data)

"""
(Pydantic) Модель message для отправки сообщений <<<нужна ли она вообще?>>>
"""


class Message(BaseModel):
    name: str  # Как подставить имя пользователя который сейчас в сессии?
    message: str = Field(default=..., max_length=140, description="Сообщение пользователя")
    message_time: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M"),
                              description="Время сообщения в формате HH:MM")
