from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from chat.app import router
import asyncio
from database import create_tables
from db.models import User, Message

achat = FastAPI(
    title="AChat",
    version="0.0.1")

achat.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

"""
Начальная страница чата
"""


@achat.get("/", status_code=200)
async def get_started(request: Request):
    return templates.TemplateResponse("start_page.html", {"request": request})


achat.include_router(router)  # Подключаем маршруты из app


async def main():
    try:
        await create_tables()  # Вызов функции для создания таблиц
    except FastAPI:
        print("Таблицы не были созданы")


if __name__ == "__main__":
    asyncio.run(main())