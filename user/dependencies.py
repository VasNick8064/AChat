from datetime import datetime, timezone

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from config import get_auth_data
from user.dao import UsersDAO

"""
Достаем значение ключа users_access_token из куки
"""


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")
    return token


"""
В этом месте мы создали свой декодер. 
Его смысл в том, чтоб получить из токена данные с которыми можно будет работать (exp и sub)
"""


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валиден")
    # Проверяем истекло ли время токена
    expire = payload.get("exp")  # извлекаем время истечения срока действия из декодированной полезной нагрузки токена
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc) # преобразуем expire в "datetime" объект
    if (not expire) or (expire_time < datetime.now(timezone.utc)): # проверяем есть ли параметр срока истечения
        # жизни токена и не является ли эта дата больше текущей
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")
    # Проверяем есть ли параметр ID пользователя
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя")
    # Пытаемся получить данные о пользователе
    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    return user
