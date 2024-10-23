from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from chat.app import app_router
import asyncio
from database import create_tables
from user.exceptions import TokenExpiredException, TokenNoFoundException
from user.router import auth_router
from chat.router import chat_router

achat = FastAPI(  # создание экземпляра приложения
    title="AChat",
    version="0.0.1")

achat.mount("/static", StaticFiles(directory="static"), name="static")  # обслуживание статических файлов

achat.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

templates = Jinja2Templates(directory='templates')

achat.include_router(app_router)  # Подключаем маршруты из app
achat.include_router(auth_router)  # Подключаем маршруты из User
achat.include_router(chat_router) # Подключаем маршруты из Chat
"""
Начальная страница чата
"""


@achat.get("/", status_code=200)  # редирект на страницу авторизации
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@achat.exception_handler(TokenExpiredException)  # Возвращаем редирект на страницу /auth если время токена истекло
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@achat.exception_handler(TokenNoFoundException)  # Возвращаем редирект на страницу /auth если токен не найден
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/")


async def main():
    try:
        await create_tables()  # Вызов функции для создания таблиц
    except FastAPI:
        print("Таблицы не были созданы")


if __name__ == "__main__":
    asyncio.run(main())
