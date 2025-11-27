import pytest
import sqlite3
from db import init_db, add_user, get_users

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    return conn


def test_add_user(conn):
    # TODO: Добавьте пользователя и проверьте, что он появился в базе
    pass


def test_empty_db(conn):
    # TODO: В только что созданной базе список пользователей должен быть пустым
    pass
