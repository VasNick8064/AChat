
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated

Base = declarative_base()


class Message(BaseModel):  # Определяем модель структуры данных для /sm, а так же валидируем данные
    message: Annotated[str, StringConstraints(max_length=140)]

    # @validator('message')
    # def message_length(cls, v):
    #     if len(v) > 140:
    #         raise ValueError("Введите не более 140 символов")
    #     return