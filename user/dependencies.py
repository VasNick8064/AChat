import logging
from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from user.exceptions import TokenNoFoundException, TokenExpiredException, NoJwtException, NoUserIdException
from config import get_auth_data
from user.dao import UsersDAO

"""
Достаем значение ключа users_access_token из куки
"""


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token


"""
Аутентификация текущего пользователя
"""


async def get_current_user(token: str = Depends(get_token)): # получаем из токена данные с которыми можно будет
    # работать (exp и sub)
    try:
        logging.info("user/dependencies.py - get_current_user: Получаем данные из токена: " + str(token))
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except JWTError:
        logging.info(
            "user/dependencies.py - get_current_user[Аутентификация]: Не удалось получить данные из токена")
        raise NoJwtException
    # Проверяем истекло ли время токена
    expire = payload.get("exp")  # извлекаем время истечения срока действия из декодированной полезной нагрузки токена
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc) # преобразуем expire в "datetime" объект
    if (not expire) or (expire_time < datetime.now(timezone.utc)): # проверяем есть ли параметр срока истечения
        # жизни токена и не является ли эта дата больше текущей
        logging.info("user/dependencies.py - get_current_user[Аутентификация]: Истекло время токена")
        raise TokenExpiredException
    # Проверяем есть ли параметр ID пользователя
    user_id = payload.get("sub")
    if not user_id:
        logging.info("user/dependencies.py - get_current_user[Аутентификация]: Не найден параметр ID пользователя")
        raise NoUserIdException
    # Пытаемся получить данные о пользователе
    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        logging.info("user/dependencies.py - get_current_user[Аутентификация]: Пользователь не найден")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    logging.info("user/dependencies.py - get_current_user[Аутентификация]: Получаем данные о пользователе с ID: " + str(user_id))
    return user
