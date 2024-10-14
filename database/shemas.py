import psycopg2

try:
    conn = psycopg2.connect(
        dbname="achat",
        user="postgres",
        password="8064",
        host="127.0.0.1",
        port="5432"
    )

    print("Подключение успешно!")

    conn.autocommit = True

    # Создание курсора
    cursor = conn.cursor()

except Exception as e:
    print(f"Ошибка подключения: {e}")
