import sqlite3

def init_db(conn):
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()

def add_user(conn, name):
    # TODO: Функция должна вставлять пользователя в таблицу users
    # Подсказка:
    # conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    # # conn.commit()
    pass

def get_users(conn):
    # TODO: Функция должна вернуть список всех пользователей
    # Подсказка:
    # return conn.execute("SELECT id, name FROM users").fetchall()
    pass
