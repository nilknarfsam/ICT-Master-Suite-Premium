from src.core.failures import failure_repository


class DummyCursor:
    def __init__(self):
        self.executed = []

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        return None


class DummyConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self):
        return self._cursor

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_salvar_falha_db_mockado_salva_estrutura_basica(monkeypatch):
    cursor = DummyCursor()
    conn = DummyConnection(cursor)

    monkeypatch.setattr(failure_repository, "conectar_banco", lambda timeout=20: conn)

    falha = {
        "id": "f01",
        "data_registro": "2026-05-05 10:00:00",
        "data_falha": "2026-05-05 09:59:59",
        "arquivo": "arquivo.log",
        "serial": "SERIAL0001",
        "modelo": "MODEL_A",
        "componente": "COMP1",
        "step": "STEP1",
    }

    ok = failure_repository.salvar_falha_db(falha)

    assert ok is True
    assert conn.committed is True
    assert len(cursor.executed) == 1
    _, params = cursor.executed[0]
    assert params["id"] == "f01"
    assert params["serial"] == "SERIAL0001"
    assert params["modelo"] == "MODEL_A"
    assert params["status_tratativa"] == "ABERTO"


def test_salvar_falha_db_campos_obrigatorios_basicos_presentes():
    falha = {
        "id": "f02",
        "data_registro": "2026-05-05 10:00:00",
        "data_falha": "2026-05-05 09:59:59",
        "arquivo": "arquivo2.log",
        "serial": "SERIAL0002",
        "modelo": "MODEL_B",
        "componente": "COMP2",
        "step": "STEP2",
    }

    obrigatorios = {"id", "data_registro", "data_falha", "arquivo", "serial", "modelo", "componente", "step"}
    assert obrigatorios.issubset(set(falha.keys()))
