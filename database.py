from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
