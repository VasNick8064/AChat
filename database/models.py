from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, Integer, Text, ForeignKey

Base = declarative_base()

"""
(SQLAlchemy) Модель таблицы users 
Таблица пользователей: эта модель представляет пользователей в базе данных, 
сохраняя их информацию, такую как адрес электронной почты, имя и хешированный пароль.
"""


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    # Связь между User и Message
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")


"""
(SQLAlchemy) Модель таблицы messages
Таблица сообщений: эта модель хранит сообщения, отправленные пользователями,
включая содержание сообщения и ссылку на отправившего его пользователя.
"""


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'),
                                         nullable=False)  # Внешний ключ на id пользователя в User
    content: Mapped[str] = mapped_column(Text)

    # Связь между Message и User
    user: Mapped[User] = relationship("User", back_populates="messages")
