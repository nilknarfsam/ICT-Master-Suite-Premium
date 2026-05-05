from src.application.services.log_index_application_service import LogIndexApplicationService


class DummyCoreIndexService:
    def __init__(self):
        self.calls = []
        self.responses = {}

    def clear_index(self):
        self.calls.append(("clear_index",))

    def build_incremental_index(self, base_path, allowed_extensions=None):
        self.calls.append(("build_incremental_index", base_path, allowed_extensions))
        return self.responses.get(base_path, {"indexed": 0, "errors": 0})


def test_rebuild_clears_index_before_rebuilding():
    dummy = DummyCoreIndexService()
    dummy.responses = {"a": {"indexed": 2, "errors": 1}}
    app_service = LogIndexApplicationService(service=dummy)

    summary = app_service.rebuild_index(["a"], allowed_extensions={".csv"})

    assert summary["total_indexed"] == 2
    assert summary["total_errors"] == 1
    assert dummy.calls[0] == ("clear_index",)
    assert dummy.calls[1][0] == "build_incremental_index"


def test_rebuild_accumulates_multiple_paths():
    dummy = DummyCoreIndexService()
    dummy.responses = {
        "a": {"indexed": 2, "errors": 1},
        "b": {"indexed": 3, "errors": 0},
    }
    app_service = LogIndexApplicationService(service=dummy)

    summary = app_service.rebuild_index(["a", "b"], allowed_extensions={".csv", ".txt"})

    assert summary["paths"] == ["a", "b"]
    assert summary["total_indexed"] == 5
    assert summary["total_errors"] == 1
    assert len(summary["per_path"]) == 2


def test_rebuild_returns_expected_shape():
    dummy = DummyCoreIndexService()
    app_service = LogIndexApplicationService(service=dummy)

    summary = app_service.rebuild_index([], allowed_extensions={".csv"})

    assert summary == {
        "paths": [],
        "total_indexed": 0,
        "total_errors": 0,
        "per_path": [],
    }
