import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import host, port, dbname, user, password

DB_HOST = host
DB_PORT = port
DB_NAME = dbname
DB_USER = user
DB_PASSWORD = password

# print(f"Host: {DB_HOST}")
# print(f"Port: {DB_PORT}")
# print(f"Database Name: {DB_NAME}")
# print(f"User: {DB_USER}")
# print(f"Password: {DB_PASSWORD}")


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)  # асинхронное подключение к базе данных PostgreSQL
async_session_maker = async_sessionmaker(engine, expire_on_commit=True)  # фабрика асинхронных сессий

"""
Base: абстрактный класс, от которого наследуются все модели. 
Он используется для миграций и аккумулирует информацию обо всех моделях, 
чтобы Alembic мог создавать миграции для синхронизации структуры базы данных с моделями на бекенде.·
"""


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


"""
create_tables функция создания таблиц в БД
"""


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
