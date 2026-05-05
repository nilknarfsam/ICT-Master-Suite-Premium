from src.application.services import log_analysis_service as las
from src.application.services.log_analysis_service import LogAnalysisService


def test_read_analysis_calls_repository_and_returns_text(monkeypatch):
    service = LogAnalysisService()
    captured = {"file_name": None}

    def fake_ler_observacao(file_name):
        captured["file_name"] = file_name
        return "observacao teste"

    monkeypatch.setattr(las, "ler_observacao", fake_ler_observacao)
    result = service.read_analysis("arquivo.log")

    assert captured["file_name"] == "arquivo.log"
    assert result == "observacao teste"


def test_read_analysis_handles_empty_or_none(monkeypatch):
    service = LogAnalysisService()

    monkeypatch.setattr(las, "ler_observacao", lambda file_name: "")
    assert service.read_analysis("sem_obs.log") == ""

    monkeypatch.setattr(las, "ler_observacao", lambda file_name: None)
    assert service.read_analysis("sem_obs_none.log") is None
