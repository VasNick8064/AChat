import psycopg2
from shemas import cursor, conn

try:
    cursor.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        password  VARCHAR(20),
        email VARCHAR(30)
    );
    """)
    print("Таблица 'users' успешно создана.")

except Exception as e:
    print(f"Ошибка подключения: {e}")
finally:
    if conn:
        conn.close()