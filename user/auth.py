import logging

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr
from config import get_auth_data
from user.dao import UsersDAO

"""
Создание контекста для хэширования паролей
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
Функция шифрования пароля
"""


def get_password_hash(password: str) -> str:
    logging.info("user/auth.py - get_password_hash[Работа с БД]: Вызов функции")
    return pwd_context.hash(password)


"""
Функция для проверки пароля
"""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    logging.info("user/auth.py - verify_password[Работа с БД]: Вызов функции, проверка на валидность пароля")
    return pwd_context.verify(plain_password, hashed_password) # метод verify проверяет, совпадает ли введенный пароль
    # с хешированным паролем.


"""
Функция для генерации JWT токена

Функция create_access_token создает JSON Web Token (JWT) для аутентификации пользователей. 
Она принимает словарь с данными, добавляет время истечения токена (по умолчанию 30 дней), 
и затем кодирует эти данные в JWT с использованием секретного ключа и алгоритма шифрования, 
заданных в конфигурации приложения.
"""


def create_access_token(data: dict) -> str:
    logging.info("user/auth.py - create_access_token: Генерация токена: " + str(data))
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30) # устанавливаем срок действия токена (наст.время + 30дней)
    to_encode.update({"exp": expire}) # добавляем срок действия "exp" к полехной нагрузке токена
    auth_data = get_auth_data()  #get_auth_data() вызывается из модуля config
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    # Метод jwt.encode()
    # из библиотеки PyJWT, используется для создания JWT. Он принимает три аргумента:
    # - Полезная нагрузка (to_encode), которая включает данные пользователя и срок действия.
    # - Секретный ключ , используемый для подписи токена (auth_data["secret_key"]).
    # - Алгоритм, используемый для подписи (auth_data["algorithm"])
    logging.info("user/auth.py - create_access_token: Возврат токена: " + str(encode_jwt))
    return encode_jwt # сгенерированный JWT возвращается в виде строки


"""
authenticate_user - функция, которая принимает Email и пароль, и проверяет есть ли такой пользователь в базе данных.
"""


async def authenticate_user(email: EmailStr, password: str):
    logging.info("user/auth.py - authenticate_user[Работа с БД]: Вызов функции")
    user = await UsersDAO.find_one_or_none(email=email) # ищем емейл в БД, через общий метод find_one_or_none
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        logging.info("user/auth.py - authenticate_user[Работа с БД]: Проверка на наличие пользователя " + str(
            email) + " в БД - НЕ ПРОЙДЕНА")
        return None # если емейл не найден или введенный пароль не соответствует зашифрованному паролю в БД
    logging.info("user/auth.py - authenticate_user[Работа с БД]: Успешная проверка на наличие пользователя " + str(email) + " в БД")
    return user
