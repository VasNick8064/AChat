from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

router = APIRouter()

"""
Главная страница чата
"""


@router.get("/chat", status_code=200)
async def get_chat(request: Request):
    try:
        return templates.TemplateResponse("chat.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Метод отправки сообщений
"""


@router.post("/sm", status_code=200)
async def send_message(request: Request, message: str):
    return templates.TemplateResponse("chat.html", {"request": request, "message": message})


"""
Методы загрузки файлов в чат
"""


@router.post("/files")
async def create_file(file: Annotated[bytes, File()]):
    if len(file) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"file_size": len(file)}


@router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    if len(file.filename) > 41943040:
        raise HTTPException(status_code=400, detail="Большой размер файла")
    return {"filename": file.filename}