from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse, Response

from user.auth import get_password_hash, authenticate_user, create_access_token
from user.dao import UsersDAO
from user.schemas import UserReg, UserAuth

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

"""
Принимаем данные от пользователя после регистрации, затем делаем проверку на то существует ли он в базе данных. 
Если не существует и никаких ошибок валидации нет, то мы записываем пользователя в базу дынных.
"""


@auth_router.post("/register")
async def register_user(user_data: UserReg) -> JSONResponse:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_data.hashed_password)
    await UsersDAO.add(**user_dict)
    return JSONResponse(content={"message": "Вы успешно зарегистрированы!", "redirect_url": "/chat"})


"""
Проверяем учётные данные пользователя (электронную почту и пароль) и после успешной аутентификации 
генерируем токен доступа, который отправляется обратно клиенту
"""


@auth_router.post("/login")
async def login_user(response: Response, user_data: UserAuth) -> JSONResponse:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True) # httponly - куки доступны только через HTTP или HTTPS
    return JSONResponse({"message": "Вы успешно зашли на сайт!", "access_token": access_token, "refresh_token": None, "redirect_url": "/chat"})
