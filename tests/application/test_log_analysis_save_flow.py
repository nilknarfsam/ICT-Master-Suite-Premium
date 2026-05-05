from src.application.services import log_analysis_service as las
from src.application.services.log_analysis_service import LogAnalysisService


def test_save_analysis_flow_calls_repository_with_expected_parameters(monkeypatch):
    service = LogAnalysisService()
    captured = {}

    def fake_salvar_observacao(file_name, text, tecnico=None):
        captured["file_name"] = file_name
        captured["text"] = text
        captured["tecnico"] = tecnico
        return True

    monkeypatch.setattr(las, "salvar_observacao", fake_salvar_observacao)

    result = service.save_analysis("log_a.txt", "texto de analise", "Tecnico A")

    assert result is True
    assert captured == {
        "file_name": "log_a.txt",
        "text": "texto de analise",
        "tecnico": "Tecnico A",
    }
