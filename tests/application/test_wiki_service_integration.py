from src.application.services import wiki_service as ws
from src.application.services.wiki_service import WikiService


def test_wiki_service_listar_modelos_mock(monkeypatch):
    service = WikiService()
    esperado = [{"id": 1, "nome": "MODEL_A"}]
    monkeypatch.setattr(ws, "listar_modelos", lambda: esperado)

    assert service.listar_modelos() == esperado


def test_wiki_service_adicionar_modelo_mock(monkeypatch):
    service = WikiService()
    captured = {"nome": None}

    def fake_add(nome_modelo):
        captured["nome"] = nome_modelo
        return 42

    monkeypatch.setattr(ws, "adicionar_modelo", fake_add)
    result = service.adicionar_modelo("MODEL_X")

    assert result == 42
    assert captured["nome"] == "MODEL_X"


def test_wiki_service_buscar_solucoes_mock(monkeypatch):
    service = WikiService()
    expected = [{"id": 5, "fase": "ICT", "sintoma": "falha", "solucao": "troca", "tecnico": "T1", "data": "2026-05-05"}]
    captured = {"args": None}

    def fake_search(modelo_id, fase, busca_texto):
        captured["args"] = (modelo_id, fase, busca_texto)
        return expected

    monkeypatch.setattr(ws, "buscar_solucoes_wiki", fake_search)
    result = service.buscar_solucoes(10, "ICT", "falha")

    assert result == expected
    assert captured["args"] == (10, "ICT", "falha")


def test_wiki_service_adicionar_solucao_mock(monkeypatch):
    service = WikiService()
    captured = {"args": None}

    def fake_add_solution(modelo_id, fase, sintoma, solucao, tecnico_id):
        captured["args"] = (modelo_id, fase, sintoma, solucao, tecnico_id)
        return True

    monkeypatch.setattr(ws, "adicionar_solucao_wiki", fake_add_solution)
    result = service.adicionar_solucao(11, "FCT", "sem boot", "troca componente", "Tecnico A")

    assert result is True
    assert captured["args"] == (11, "FCT", "sem boot", "troca componente", "Tecnico A")
