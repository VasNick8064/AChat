import psycopg2
from shemas import cursor, conn

try:
    cursor.execute("""
    CREATE TABLE messages (
        id SERIAL PRIMARY KEY,
        from_user_id INT,
        message_text TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Таблица 'messages' успешно создана.")

except Exception as e:
    print(f"Ошибка подключения: {e}")
finally:
    if conn:
        conn.close()