from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import logging
from database import async_session_maker

"""
Класс с общими методами для работы CRUD
"""


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        logging.info("db/dao.py - find_one_or_none_by_id [Работа с БД]: Поиск и возврат одного экземпляра модели по data_id: " + str(
            data_id) + " или None")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
              Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

              Аргументы:
                  **filter_by: Критерии фильтрации в виде именованных параметров.

              Возвращает:
                  Экземпляр модели или None, если ничего не найдено.
        """
        logging.info("db/dao.py - find_one_or_none [Работа с БД]: Поиск и возврат одного экземпляра модели по переданному "
                     "параметру "+ str(filter_by) + " или None")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
              Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

              Аргументы:
                  **filter_by: Критерии фильтрации в виде именованных параметров.

              Возвращает:
                  Список экземпляров модели.
        """
        logging.info(
            "db/dao.py - find_all [Работа с БД]: Поиск и возврат всех экземпляров модели по переданному"
            "параметруу")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        """
                Асинхронно создает новый экземпляр модели с указанными значениями.

                Аргументы:
                    **values: Именованные параметры для создания нового экземпляра модели.

                Возвращает:
                    Созданный экземпляр модели.
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                    logging.info("db/dao.py - add[Работа с БД]: Запись " + str(values) + " была добавлена в БД")
                except SQLAlchemyError as e:
                    logging.info("db/dao.py - add[Работа с БД]: Ошибка при записи " + str(values) + "  в БД")
                    await session.rollback()
                    raise e
                return new_instance
