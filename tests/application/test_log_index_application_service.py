from src.application.services.log_index_application_service import LogIndexApplicationService


class DummyLogIndexService:
    def __init__(self):
        self.calls = []

    def build_incremental_index(self, base_path, allowed_extensions=None):
        self.calls.append(("build_incremental_index", base_path, allowed_extensions))
        return {"indexed": 10, "errors": 1}

    def index_file(self, path):
        self.calls.append(("index_file", path))
        return True

    def search(self, term):
        self.calls.append(("search", term))
        return [("abc123_fail.csv", "/tmp/abc123_fail.csv", 123.0)]

    def is_index_available(self):
        self.calls.append(("is_index_available",))
        return True

    def count_entries(self):
        self.calls.append(("count_entries",))
        return 42


def test_build_incremental_index_with_mock():
    dummy = DummyLogIndexService()
    service = LogIndexApplicationService(service=dummy)

    result = service.build_incremental_index("/tmp/logs", {".csv"})

    assert result == {"indexed": 10, "errors": 1}
    assert dummy.calls[0] == ("build_incremental_index", "/tmp/logs", {".csv"})


def test_index_file_with_mock():
    dummy = DummyLogIndexService()
    service = LogIndexApplicationService(service=dummy)

    result = service.index_file("/tmp/a.csv")

    assert result is True
    assert dummy.calls[0] == ("index_file", "/tmp/a.csv")


def test_search_with_mock():
    dummy = DummyLogIndexService()
    service = LogIndexApplicationService(service=dummy)

    result = service.search("abc123")

    assert len(result) == 1
    assert result[0][0] == "abc123_fail.csv"
    assert dummy.calls[0] == ("search", "abc123")


def test_is_index_available_with_mock():
    dummy = DummyLogIndexService()
    service = LogIndexApplicationService(service=dummy)

    result = service.is_index_available()

    assert result is True
    assert dummy.calls[0] == ("is_index_available",)


def test_count_entries_with_mock():
    dummy = DummyLogIndexService()
    service = LogIndexApplicationService(service=dummy)

    result = service.count_entries()

    assert result == 42
    assert dummy.calls[0] == ("count_entries",)
