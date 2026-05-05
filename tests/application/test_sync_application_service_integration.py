from src.application.services import sync_application_service as sas
from src.application.services.sync_application_service import SyncApplicationService


def test_sincronizar_fila_offline_with_mock(monkeypatch):
    service = SyncApplicationService()
    captured = {"called": False}

    def fake_sync_fila():
        captured["called"] = True
        return "ok_fila"

    monkeypatch.setattr(sas, "sincronizar_fila_offline", fake_sync_fila)
    result = service.sincronizar_fila_offline()

    assert captured["called"] is True
    assert result == "ok_fila"


def test_sincronizar_espelho_local_with_mock(monkeypatch):
    service = SyncApplicationService()
    captured = {"called": False}

    def fake_sync_espelho():
        captured["called"] = True
        return "ok_espelho"

    monkeypatch.setattr(sas, "sincronizar_espelho_local", fake_sync_espelho)
    result = service.sincronizar_espelho_local()

    assert captured["called"] is True
    assert result == "ok_espelho"


def test_init_db_local_with_mock(monkeypatch):
    service = SyncApplicationService()
    captured = {"called": False}

    def fake_init_db_local():
        captured["called"] = True
        return "ok_init"

    monkeypatch.setattr(sas, "init_db_local", fake_init_db_local)
    result = service.init_db_local()

    assert captured["called"] is True
    assert result == "ok_init"
