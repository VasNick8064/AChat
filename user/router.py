import logging

from fastapi import APIRouter, HTTPException, status, Depends, Request
from starlette.responses import JSONResponse, Response, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.models import User
from user.auth import get_password_hash, authenticate_user, create_access_token
from user.dao import UsersDAO
from user.dependencies import get_current_user
from user.schemas import UserReg, UserAuth


templates = Jinja2Templates(directory='templates')

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

"""
Принимаем данные от пользователя после регистрации, затем делаем проверку на то существует ли он в базе данных. 
Если не существует и никаких ошибок валидации нет, то мы записываем пользователя в базу дынных.
"""


@auth_router.post("/register")
async def register_user(user_data: UserReg) -> JSONResponse:
    logging.info("user/router.py - register_user[Регистрация]: Попытка регистрации юзера")
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:  # проверка наличия пользовательских данных в бд
        logging.info("user/router.py - register_user[Регистрация]: ОШИБКА - пользщователь уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")
    user_dict = user_data.dict()  # преобразуем экземпляр модели UserReg в словарь
    user_dict["password"] = get_password_hash(user_data.password)  # хэшируем пароль перед добавлением в бд
    await UsersDAO.add(**user_dict)  # распаковываем и добавляем учетную запись в бд add(key:value,...)
    logging.info("user/router.py - register_user[Регистрация]: Пользователь: " + str(user_data) +" успешно зарегистрирован")

    return JSONResponse(content={"message": "Вы успешно зарегистрированы!", "redirect_url": "/chat"})


"""
Проверяем учётные данные пользователя (электронную почту и пароль) и после успешной аутентификации 
генерируем токен доступа, который отправляется обратно клиенту
"""


@auth_router.post("/login")
async def login_user(response: Response, user_data: UserAuth) -> dict[str, str | None]:
    logging.info("user/router.py - login_user[Авторизация]: Попытка авторизации юзера: " + str(user_data))
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:  # проверяем, существует ли пользователь в БД
        logging.info("user/router.py - login_user[Авторизация]: Ошибка авторизации юзера: " + str(user_data))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token,httponly=True)  # httponly - куки доступны только через HTTP или HTTPS
    logging.info("user/router.py - login_user[Авторизация]: Успешная авторизация юзера: " + str(user_data))
    return {"message": "Вы успешно вошли!", "redirect_url": "/chat"}

"""
Функция create_access_token вызывается для создания веб-токена JSON (JWT).
Содержимое полезной нагрузки:
Аргумент , передаваемый create_access_token , является словарем: {"sub": str(check.id)}.
Здесь "sub" означает «субъект». В контексте JWT это обычно пользователь, для которого выдан токен.
Идентификация пользователя:
check.id относится к уникальному идентификатору аутентифицированного пользователя, который извлекается из результата выполнения authenticate_user функции.

Метод set_cookie вызывается для response объекта, который позволяет установить HTTP-куки, отправляемые обратно клиенту (браузеру пользователя).
httponly=TrueЭтот флаг делает файл cookie доступным только через HTTP(S)-запросы, а не через JavaScript, работающий в браузере. 
Это важная мера безопасности, поскольку она помогает снизить риски, связанные с атаками с использованием межсайтового скриптинга (XSS), 
при которых вредоносные скрипты могут потенциально украсть файлы cookie.
"""

"""
get_me получаем информацию о пользователе
"""


@auth_router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)):
    logging.info("user/router.py - get_me[Информация]: Получить информацию о пользователе: " + str(user_data))
    return user_data


"""
logout_user удаляем JWT токен из куки
"""


@auth_router.post("/logout")
async def logout_user(response: Response, User = Depends(get_current_user)):
    response.delete_cookie(key="users_access_token")
    logging.info("user/router.py - logout_user[Выход из системы]: Куки пользователя: " + str(User.name) + ", ID: " + str(User.id) +" удалены")
    return {"message": "Пользователь вышел из системы", "redirect_url": "/auth"}


@auth_router.get("/", response_class=HTMLResponse, summary="Страница авторизации")
async def get_categories(request: Request):
    return templates.TemplateResponse("start_page.html", {"request": request})
