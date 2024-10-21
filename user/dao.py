from db.dao import BaseDAO
from db.models import User

"""
UserDAO - класс для взаимодействия с таблицей пользователей.
"""


class UsersDAO(BaseDAO):
    model = User
