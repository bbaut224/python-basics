import pytest
import api_client

@pytest.fixture
def mock_get(monkeypatch):
    def fake_get(url):
        # всегда возвращаем одного и того же пользователя
        return type("Resp", (), {
            "json": lambda self=None: {"id": 1, "name": "TestUser"}
        })()

    monkeypatch.setattr("requests.get", fake_get)


def test_fetch_user(mock_get):
    # TODO: После реализации fetch_user должно вернуть структуру
    # {"id": 1, "name": "TestUser"}
    user = api_client.fetch_user(1)
    # TODO: Добавьте проверки
    pass
