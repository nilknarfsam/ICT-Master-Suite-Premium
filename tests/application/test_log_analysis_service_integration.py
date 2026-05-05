from src.application.services import log_analysis_service as las
from src.application.services.log_analysis_service import LogAnalysisService


def test_parse_metadata_integration_uses_parser_function(monkeypatch):
    service = LogAnalysisService()
    calls = {"count": 0, "args": None}

    def fake_parse_metadata(path, file_name, content):
        calls["count"] += 1
        calls["args"] = (path, file_name, content)
        return {"tipo": "TRI", "status": "FAIL", "serial": "SERIALX", "modelo": "MODELX", "data": "N/A", "cor": "red"}

    monkeypatch.setattr(las, "parse_metadata_inteligente", fake_parse_metadata)

    result = service.parse_log_metadata("virtual/path.log", "file.csv", "log-content")

    assert calls["count"] == 1
    assert calls["args"] == ("virtual/path.log", "file.csv", "log-content")
    assert result["tipo"] == "TRI"
    assert result["status"] == "FAIL"


def test_get_serial_history_with_mock(monkeypatch):
    service = LogAnalysisService()
    esperado = {"data": "2026-05-05", "texto": "historico", "tecnico": "T1"}
    monkeypatch.setattr(las, "buscar_historico_serial", lambda serial: esperado)
    assert service.get_serial_history("SERIAL123") == esperado


def test_get_ict_statistics_with_mock(monkeypatch):
    service = LogAnalysisService()
    esperado = {"total_hoje": 5, "top_componente": "R1", "top_5_componentes": [], "db_online": True}
    monkeypatch.setattr(las, "obter_estatisticas_ict", lambda: esperado)
    assert service.get_ict_statistics() == esperado


def test_get_latest_analyses_with_mock(monkeypatch):
    service = LogAnalysisService()
    esperado = [("2026-05-05", "SERIAL123", "COMP", "TRATADO")]
    monkeypatch.setattr(las, "obter_ultimas_analises", lambda limite=10: esperado)
    assert service.get_latest_analyses(15) == esperado


def test_get_progress_statistics_with_mock(monkeypatch):
    service = LogAnalysisService()
    esperado = {"abertos": 2, "tratados": 7}
    monkeypatch.setattr(las, "obter_estatisticas_progresso", lambda: esperado)
    assert service.get_progress_statistics() == esperado


def test_clear_analyses_with_mock(monkeypatch):
    service = LogAnalysisService()
    monkeypatch.setattr(las, "limpar_analises_db", lambda: True)
    assert service.clear_analyses() is True
