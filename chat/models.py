import datetime
from pydantic import BaseModel, Field

"""
(Pydantic) Модель message для отправки сообщений <<<нужна ли она вообще?>>>
"""


class Message(BaseModel):
    name: str  # Как подставить имя пользователя который сейчас в сессии?
    message: str = Field(default=..., max_length=140, description="Сообщение пользователя")
    message_time: str = Field(default_factory=lambda: datetime.datetime.now().strftime("%H:%M"),
                              description="Время сообщения в формате HH:MM")


"""
Test
"""
# data = {
#     "name": "Test",
#     "message": "Password1"
# }
#
#
# def test_val(data: dict) -> None:
#     try:
#         users = Message(**data)
#         print(users)
#     except ValidationError as e:
#         print(f"Ошибка валидации: {e}")
#
#
# test_val(data)
