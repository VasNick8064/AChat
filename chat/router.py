from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from chat.dao import MessageDAO
from chat.schemas import MessageRead, MessageCreate
from user.dao import UsersDAO
from user.dependencies import get_current_user
from db.models import User
import asyncio
import random
import logging

chat_router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='app/templates')

active_connections: Dict[int, WebSocket] = {}  # Пользователи, которые находятся на сайте в данный момент


# Страница чата
@chat_router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    try:
        users_all = await UsersDAO.find_all()  # нужно ли нам получать всех юзеров?
        return templates.TemplateResponse("chat.html", {"request": request, "user": user_data, 'users_all': users_all})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""
Маршрут: GET /messages/{user_id}
Описание: Этот маршрут позволяет пользователю получить список сообщений между ним и другим пользователем, идентифицированным по user_id.
Параметры:
user_id: ID пользователя, чьи сообщения нужно получить.
current_user: текущий аутентифицированный пользователь, получаемый через зависимость get_current_user.
Возвращаемое значение: список сообщений (или пустой список, если сообщений нет).
"""


@chat_router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessageDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


"""
Маршрут: POST /messages
Описание: Этот маршрут позволяет пользователю отправить сообщение другому пользователю.
Параметры:
message: объект сообщения, содержащий информацию о содержимом и получателе.
current_user: текущий аутентифицированный пользователь.
Процесс:
Сообщение сохраняется в базе данных.
Уведомления отправляются как отправителю, так и получателю с помощью функции notify_user.
Возвращаемое значение: подтверждение успешной отправки сообщения с информацией о получателе и статусе.
"""


@chat_router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    logging.info("chat/router.py - /messages [POST]: Отправка сообщения пользователем: " + current_user.name)
    await MessageDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id,
    )
    message_data = {
        'current_user_id': current_user.id,
        'recipient_id': message.recipient_id,
        'content': message.content,
        'name_user': current_user.name
    }

    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)
    logging.info("chat/router.py - /messages [POST]: Cообщение отправлено пользователем: " + current_user.name + ", ID: " + str(current_user.id) + ", и добавлено в БД")

    return {'recipient_id': message.recipient_id,
            'content': message.content,
            'name_user': current_user.name,
            'status': 'ok',
            'msg': 'Message saved!'}


"""
Описание: notify_user отправляет уведомление пользователю через веб-сокет, если он в данный момент подключен.
"""


async def notify_user(user_id: int, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


"""
Маршрут: ws /ws/{user_id}
Описание: Этот маршрут устанавливает веб-сокет-соединение для пользователя, позволяя ему общаться в режиме реального времени.
Процесс:
Пользователь принимает соединение и добавляется в список активных подключений.
В бесконечном цикле происходит поиск случайного онлайн-партнера для общения.
Если партнер найден, пользователи уведомляются о друг друге.
Если партнер не найден, пользователю отправляется сообщение об ожидании.
"""


@chat_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    logging.info("chat/router.py - //ws/{user_id} [WEBSOCKET]: Вызов функции  websocket_endpoint")

    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            logging.info("chat/router.py - //ws/{user_id} [WEBSOCKET]: Поиск рандомного онлайн собеседника")
            partner_id = await find_random_online_user(user_id)
            if partner_id:
                logging.info("chat/router.py - //ws/{user_id} [WEBSOCKET]: Собеседник найден")
                await websocket.send_json({"partner_id": partner_id})
                await active_connections[partner_id].send_json({"partner_id": user_id})
                break  # Exit loop after pairing
            else:
                await websocket.send_json({"message": "Ожидание собеседника..."})
                await asyncio.sleep(5)  # Wait before checking again

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)


"""
find_random_online_user ищет случайного пользователя из списка онлайн-пользователей, исключая текущего пользователя.
"""


async def find_random_online_user(exclude_user_id: int):
    online_users = [user_id for user_id in active_connections.keys() if user_id != exclude_user_id]
    logging.info("chat/router.py - find_random_online_user: Вызов функции")
    return random.choice(online_users) if online_users else None
