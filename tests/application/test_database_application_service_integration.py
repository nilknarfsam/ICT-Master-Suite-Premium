from src.application.services import database_application_service as das
from src.application.services.database_application_service import DatabaseApplicationService


def test_verificar_conexao_db_with_mock(monkeypatch):
    service = DatabaseApplicationService()
    monkeypatch.setattr(das, "verificar_conexao_db", lambda: True)
    assert service.verificar_conexao_db() is True


def test_init_db_with_mock(monkeypatch):
    service = DatabaseApplicationService()
    captured = {"called": False}

    def fake_init_db():
        captured["called"] = True
        return "ok_init_db"

    monkeypatch.setattr(das, "init_db", fake_init_db)
    result = service.init_db()

    assert captured["called"] is True
    assert result == "ok_init_db"


def test_bootstrap_database_with_mock(monkeypatch):
    service = DatabaseApplicationService()
    captured = {"called": False}

    def fake_bootstrap_database():
        captured["called"] = True
        return "ok_bootstrap"

    monkeypatch.setattr(das, "bootstrap_database", fake_bootstrap_database)
    result = service.bootstrap_database()

    assert captured["called"] is True
    assert result == "ok_bootstrap"
