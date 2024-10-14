import asyncio
from typing import Annotated
from fastapi import FastAPI, HTTPException, Form, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from app.models import Message

achat = FastAPI(
    title="AChat",
    version="0.0.1")
achat.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

"""
Главная страница чата
"""


@achat.get("/chat", response_class=HTMLResponse, status_code=200)
async def get_started(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


"""
Метод отправки сообщений
"""


@achat.post("/sm", status_code=200)
async def send_message(request: Request, message: Message = Form(...)):
    return templates.TemplateResponse("chat.html", {"request": request, "message": message})


"""
Приветственная страница чата (регистрация/вход)
"""


@achat.get("/", response_class=HTMLResponse, status_code=200)
async def get_started(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


"""
Методы загрузки файлов в чат
"""


@achat.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    await asyncio.sleep(1)
    if len(file) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"file_size": len(file)}


@achat.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    if len(file.filename) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"filename": file.filename}
