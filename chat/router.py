from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from chat.dao import MessageDAO
from chat.schemas import MessageRead, MessageCreate
from user.dao import UsersDAO
from user.dependencies import get_current_user
from db.models import User
import asyncio
import logging

chat_router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory='templates')


# Активные WebSocket-подключения: {user_id: websocket}
active_connections: Dict[int, WebSocket] = {}


# Функция для отправки сообщения пользователю, если он подключен
async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        # Отправляем сообщение в формате JSON
        await websocket.send_json(message)


# WebSocket эндпоинт для соединений
@chat_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Принимаем WebSocket-соединение
    await websocket.accept()
    # Сохраняем активное соединение для пользователя
    active_connections[user_id] = websocket
    try:
        while True:
            # Просто поддерживаем соединение активным (1 секунда паузы)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)

@chat_router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    users_all = await UsersDAO.find_all()
    return templates.TemplateResponse("chat.html",
                                      {"request": request, "user": user_data, 'users_all': users_all})


@chat_router.get("message/{user_id}", response_model=List[MessageRead])
async def get_message(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessageDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


@chat_router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    # Добавляем новое сообщение в базу данных
    await MessagesDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id
    )
    # Подготавливаем данные для отправки сообщения
    message_data = {
        'sender_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
    }
    # Уведомляем получателя и отправителя через WebSocket
    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)

    # Возвращаем подтверждение сохранения сообщения
    return {'recipient_id': message.recipient_id, 'content': message.content, 'status': 'ok', 'msg': 'Message saved!'}


