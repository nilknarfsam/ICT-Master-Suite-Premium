from src.application.services import log_analysis_service as las
from src.application.services.log_analysis_service import LogAnalysisService


def test_parse_log_metadata_with_mock(monkeypatch):
    service = LogAnalysisService()

    def fake_parse(path, file_name, content):
        return {"tipo": "TRI", "status": "FAIL", "serial": "S1", "modelo": "M1", "data": "N/A", "cor": "red"}

    monkeypatch.setattr(las, "parse_metadata_inteligente", fake_parse)
    result = service.parse_log_metadata("virtual.log", "file.csv", "content")

    assert result["tipo"] == "TRI"
    assert result["status"] == "FAIL"


def test_save_analysis_with_mock(monkeypatch):
    service = LogAnalysisService()
    captured = {}

    def fake_save_observacao(file_name, text, tecnico=None):
        captured["file_name"] = file_name
        captured["text"] = text
        captured["tecnico"] = tecnico
        return True

    monkeypatch.setattr(las, "salvar_observacao", fake_save_observacao)
    ok = service.save_analysis("x.log", "analise", technician="Tec1")

    assert ok is True
    assert captured == {"file_name": "x.log", "text": "analise", "tecnico": "Tec1"}


def test_read_analysis_with_mock(monkeypatch):
    service = LogAnalysisService()
    monkeypatch.setattr(las, "ler_observacao", lambda file_name: "historico mockado")

    result = service.read_analysis("x.log")
    assert result == "historico mockado"
