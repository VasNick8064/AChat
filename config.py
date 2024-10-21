import os
from dotenv import load_dotenv

load_dotenv()

dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
secret_key = os.getenv("secret_key")
algorithm = os.getenv("algorithm")

"""
Функция get_auth_data() предназначена для получения информации, связанной с аутентификацией, в структурированном формате
"""


def get_auth_data():
    return {"secret_key": secret_key, "algorithm": algorithm}
