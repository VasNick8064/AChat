from typing import Any
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from models import Message


achat = FastAPI(
    title="AChat",
    version="0.0.1")
achat.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


@achat.get("/", response_class=HTMLResponse)
async def get_started(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@achat.post("/sm")
async def send_message(request: Request, message: Message = Form(...)):
    return templates.TemplateResponse("chat.html", {"request": request})
