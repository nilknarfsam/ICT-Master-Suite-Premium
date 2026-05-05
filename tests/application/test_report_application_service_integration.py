from src.application.services import report_application_service as ras
from src.application.services.report_application_service import ReportApplicationService


def test_gerar_relatorio_excel_com_caminho_valido_retorna_true(monkeypatch):
    service = ReportApplicationService()
    captured = {"path": None}

    def fake_gerar_relatorio_excel(caminho_destino):
        captured["path"] = caminho_destino
        return True

    monkeypatch.setattr(ras, "gerar_relatorio_excel", fake_gerar_relatorio_excel)
    result = service.gerar_relatorio_excel("C:/tmp/relatorio.xlsx")

    assert result is True
    assert captured["path"] == "C:/tmp/relatorio.xlsx"


def test_gerar_relatorio_excel_retorna_true(monkeypatch):
    service = ReportApplicationService()
    monkeypatch.setattr(ras, "gerar_relatorio_excel", lambda caminho_destino: True)
    assert service.gerar_relatorio_excel("C:/tmp/ok.xlsx") is True


def test_gerar_relatorio_excel_retorna_false(monkeypatch):
    service = ReportApplicationService()
    monkeypatch.setattr(ras, "gerar_relatorio_excel", lambda caminho_destino: False)
    assert service.gerar_relatorio_excel("C:/tmp/fail.xlsx") is False
