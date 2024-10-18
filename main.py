from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from chat.app import router

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


achat.include_router(router) # Подключаем маршруты из app
