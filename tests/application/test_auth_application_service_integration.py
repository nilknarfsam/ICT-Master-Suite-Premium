from src.application.services import auth_application_service as aas
from src.application.services.auth_application_service import AuthApplicationService


def test_validar_login_with_mock(monkeypatch):
    service = AuthApplicationService()
    esperado = {"id": 1, "nome": "Admin", "login": "admin", "is_admin": True}
    monkeypatch.setattr(aas, "validar_login", lambda login, senha: esperado)
    assert service.validar_login("admin", "admin123") == esperado


def test_obter_usuario_por_login_with_mock(monkeypatch):
    service = AuthApplicationService()
    esperado = {"id": 2, "nome": "Tec", "login": "tec", "is_admin": False}
    monkeypatch.setattr(aas, "obter_usuario_por_login", lambda login: esperado)
    assert service.obter_usuario_por_login("tec") == esperado


def test_listar_usuarios_with_mock(monkeypatch):
    service = AuthApplicationService()
    esperado = [{"id": 1, "nome": "Admin", "login": "admin", "is_admin": True}]
    monkeypatch.setattr(aas, "listar_usuarios", lambda: esperado)
    assert service.listar_usuarios() == esperado


def test_cadastrar_usuario_with_mock(monkeypatch):
    service = AuthApplicationService()
    captured = {"args": None}

    def fake_cadastrar(nome, login, senha, is_admin):
        captured["args"] = (nome, login, senha, is_admin)
        return True

    monkeypatch.setattr(aas, "cadastrar_usuario", fake_cadastrar)
    assert service.cadastrar_usuario("Novo", "novo", "123", False) is True
    assert captured["args"] == ("Novo", "novo", "123", False)


def test_deletar_usuario_with_mock(monkeypatch):
    service = AuthApplicationService()
    captured = {"id": None}

    def fake_deletar(id_usuario):
        captured["id"] = id_usuario
        return True

    monkeypatch.setattr(aas, "deletar_usuario", fake_deletar)
    assert service.deletar_usuario(10) is True
    assert captured["id"] == 10


def test_atualizar_usuario_with_mock(monkeypatch):
    service = AuthApplicationService()
    captured = {"args": None}

    def fake_atualizar(id_usuario, novo_nome, novo_login, nova_senha=None):
        captured["args"] = (id_usuario, novo_nome, novo_login, nova_senha)
        return True

    monkeypatch.setattr(aas, "atualizar_usuario", fake_atualizar)
    assert service.atualizar_usuario(2, "Nome 2", "login2", "senha2") is True
    assert captured["args"] == (2, "Nome 2", "login2", "senha2")
