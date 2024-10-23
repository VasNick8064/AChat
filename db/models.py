from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, ForeignKey
from database import Base

"""
(SQLAlchemy) Модель таблицы users 
Таблица пользователей: эта модель представляет пользователей в базе данных, 
сохраняя их информацию, такую как адрес электронной почты, имя и хешированный пароль.
"""


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)


"""
(SQLAlchemy) Модель таблицы messages
Таблица сообщений: эта модель хранит сообщения, отправленные пользователями,
включая содержание сообщения и ссылку на отправившего его пользователя.
"""


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)