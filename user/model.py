from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError

"""
(Pydantic) Модель user для регистрации пользователей
Модель пользователя: эта модель используется для проверки и сериализации пользовательского ввода, 
особенно во время регистрации или входа в систему.
"""


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


"""
Test
"""
# data = {
#     "email": "afwf@mail.ru",
#     "name": "Test",
#     "password": "Password1"
#
# }
#
#
# def test_val(data: dict) -> None:
#     try:
#         users = User(**data)
#         print(users)
#     except ValidationError as e:
#         print(f"Ошибка валидации: {e}")
#
#
# test_val(data)
