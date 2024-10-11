from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, validator


Base = declarative_base()


class Message(BaseModel):  # Определяем модель структуры данных для /sm, а так же валидируем данные
    message: str

    @validator('message')
    def message_length(cls, v):
        if len(v) > 140:
            raise ValueError("Введите не более 140 символов")
        return v