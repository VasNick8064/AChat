from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
import logging



templates = Jinja2Templates(directory='templates')

app_router = APIRouter()

"""
Главная страница чата
"""


@app_router.get("/chat", status_code=200)
async def get_chat(request: Request):
    try:
        logging.info("Переход на страницу /chat")
        return templates.TemplateResponse("chat.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Функции загрузки файлов в чат
"""


@app_router.post("/files", tags=["File Work"])
async def create_file(file: Annotated[bytes, File()]):
    logging.info("Вызов метода создания файла")
    if len(file) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"file_size": len(file)}


@app_router.post("/uploadfile", tags=["File Work"])
async def create_upload_file(file: UploadFile):
    logging.info("Вызов метода загрузки файла")
    if len(file.filename) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"filename": file.filename}