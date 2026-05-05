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
