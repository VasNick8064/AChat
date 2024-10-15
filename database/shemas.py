import psycopg2
from config import dbname, user, password, host, port


try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    print("Подключение успешно!")

    conn.autocommit = True

    # Создание курсора
    cursor = conn.cursor()

except Exception as e:
    print(f"Ошибка подключения: {e}")
