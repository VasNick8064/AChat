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


chat_router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='app/templates')

active_connections: Dict[int, WebSocket] = {}


# Страница чата
@chat_router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    try:
        users_all = await UsersDAO.find_all()
        return templates.TemplateResponse("chat.html", {"request": request, "user": user_data, 'users_all': users_all})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessageDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []


@chat_router.post("/messages", response_model=MessageCreate)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
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
    print(f"Current user name: {current_user.name}")

    return {'recipient_id': message.recipient_id,
            'content': message.content,
            'name_user': current_user.name,
            'status': 'ok',
            'msg': 'Message saved!'}


async def notify_user(user_id: int, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)


@chat_router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket

    try:
        while True:
            partner_id = await find_random_online_user(user_id)
            if partner_id:
                await websocket.send_json({"partner_id": partner_id})
                await active_connections[partner_id].send_json({"partner_id": user_id})
                break  # Exit loop after pairing
            else:
                await websocket.send_json({"message": "Ожидание собеседника..."})
                await asyncio.sleep(5)  # Wait before checking again

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)


async def find_random_online_user(exclude_user_id: int):
    online_users = [user_id for user_id in active_connections.keys() if user_id != exclude_user_id]
    return random.choice(online_users) if online_users else None
