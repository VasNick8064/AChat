from pydantic import BaseModel, Field

"""
Pydantic модель для представления сообщения
"""


class MessageRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор сообщения")
    sender_id: int = Field(..., description="ID отправителя сообщения")
    recipient_id: int = Field(..., description="ID получателя сообщения")
    content: str = Field(..., description="Содержимое сообщения")


"""
Pydantic модель для создания сообщения
"""


class MessageCreate(BaseModel):
    recipient_id: int = Field(..., description="ID получателя сообщения")
    content: str = Field(..., description="Содержимое сообщения")
    name_user: str = Field(..., description="Имя пользователя")
