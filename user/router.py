from fastapi import APIRouter, HTTPException, status
from user.auth import get_password_hash
from user.dao import UsersDAO
from db.schemas import UserReg

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

"""
Принимаем данные от пользователя после регистрации, затем делаем проверку на то существует ли он в базе данных. 
Если не существует и никаких ошибок валидации нет, то мы записываем пользователя в базу дынных.
"""


@auth_router.post("/register")
async def register_user(user_data: UserReg) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже существует"
        )
    user_dict = user_data.dict()
    user_dict["hashed_password"] = get_password_hash(user_data.hashed_password)
    await UsersDAO.add(**user_dict)
    return {"message": "Вы успешно зарегистрированы!"}
