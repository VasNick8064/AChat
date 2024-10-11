# import psycopg2
#
# conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="127.0.0.1")
# cursor = conn.cursor()
#
# conn.autocommit = True
# # команда для создания базы данных AChat
# sql = "CREATE DATABASE AChat"
# cursor.execute("CREATE TABLE users (id_user SERIAL PRIMARY KEY, name_user VARCHAR(50),  password VARCHAR(50))")
# cursor.execute("CREATE TABLE users_message (id_user SERIAL PRIMARY KEY, name_user VARCHAR(50),  message VARCHAR(50))")
# # выполняем код sql
# cursor.execute(sql)
# print("База данных успешно создана")
#
# cursor.close()
# conn.close()