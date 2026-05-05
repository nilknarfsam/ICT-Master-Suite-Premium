from scripts import build_log_index as bli


def test_resolve_directories_uses_config_when_args_empty():
    config = {
        "caminho_logs_tri": "tri_path",
        "caminho_logs_agilent": "agilent_path",
        "backup_local_dir": "backup_path",
    }
    result = bli.resolve_directories([], config)
    assert result == ["tri_path", "agilent_path", "backup_path"]


def test_resolve_directories_uses_args_when_provided():
    config = {
        "caminho_logs_tri": "tri_path",
        "caminho_logs_agilent": "agilent_path",
        "backup_local_dir": "backup_path",
    }
    result = bli.resolve_directories(["arg1", "arg2"], config)
    assert result == ["arg1", "arg2"]


def test_main_uses_config_when_no_args(monkeypatch):
    calls = []

    class DummyService:
        def build_incremental_index(self, base_path, allowed_extensions=None):
            calls.append(("build", base_path, allowed_extensions))
            return {"indexed": 1, "errors": 0}

        def count_entries(self):
            calls.append(("count",))
            return 3

    monkeypatch.setattr(
        bli,
        "carregar_config",
        lambda: {
            "caminho_logs_tri": "tri_path",
            "caminho_logs_agilent": "agilent_path",
            "backup_local_dir": "backup_path",
        },
    )
    monkeypatch.setattr(bli, "LogIndexApplicationService", lambda: DummyService())

    exit_code = bli.main([])

    assert exit_code == 0
    assert calls[0][0] == "build"
    assert calls[0][1] == "tri_path"
    assert calls[1][1] == "agilent_path"
    assert calls[2][1] == "backup_path"
    assert calls[3] == ("count",)


def test_main_uses_args_when_provided(monkeypatch):
    calls = []

    class DummyService:
        def build_incremental_index(self, base_path, allowed_extensions=None):
            calls.append(("build", base_path))
            return {"indexed": 2, "errors": 1}

        def count_entries(self):
            calls.append(("count",))
            return 2

    monkeypatch.setattr(
        bli,
        "carregar_config",
        lambda: {
            "caminho_logs_tri": "tri_path",
            "caminho_logs_agilent": "agilent_path",
            "backup_local_dir": "backup_path",
        },
    )
    monkeypatch.setattr(bli, "LogIndexApplicationService", lambda: DummyService())

    exit_code = bli.main(["x", "y"])

    assert exit_code == 0
    assert calls[0] == ("build", "x")
    assert calls[1] == ("build", "y")
    assert calls[2] == ("count",)
