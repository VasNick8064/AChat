import logging

from sqlalchemy import select, and_, or_
from db.dao import BaseDAO
from db.models import Message
from database import async_session_maker


class MessageDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int):
        logging.info("Вызов функции get_messages_between_users")
        """
        Асинхронно находит и возвращает все сообщения между двумя пользователями.

        Аргументы:
            user_id_1: ID первого пользователя.
            user_id_2: ID второго пользователя.

        Возвращает:
            Список сообщений между двумя пользователями.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter(
                or_(
                    and_(cls.model.sender_id == user_id_1, cls.model.recipient_id == user_id_2),
                    and_(cls.model.sender_id == user_id_2, cls.model.recipient_id == user_id_1)
                )
            ).order_by(cls.model.id)
            result = await session.execute(query)
            return result.scalars().all()

"""
Этот метод отличается от стандартных методов в базовом классе DAO тем, что использует метод filter и
логические операторы для создания более сложных SQL-запросов.
Метод принимает ID двух пользователей и возвращает все сообщения между ними, независимо от того, кто является отправителем или получателем.
На выходе, данный метод получает id двух пользователей.
"""