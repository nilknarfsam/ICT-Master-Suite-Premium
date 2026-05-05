from src.application.dtos.search_options import SearchOptions
from src.application.services.log_search_service import LogSearchService


class DummyIndexService:
    def __init__(self, available=True, results=None):
        self.available = available
        self.results = results or []
        self.calls = []

    def is_index_available(self):
        self.calls.append(("is_index_available",))
        return self.available

    def search(self, term):
        self.calls.append(("search", term))
        return self.results


def test_search_with_index_uses_index_when_available():
    dummy = DummyIndexService(
        available=True,
        results=[("abc123_fail.csv", "/tmp/a.csv", 10.0)],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions()

    result = service.search_with_index("abc123", options)

    assert result == [("abc123_fail.csv", "/tmp/a.csv", 10.0)]
    assert ("search", "abc123") in dummy.calls


def test_search_with_index_returns_none_when_unavailable():
    dummy = DummyIndexService(available=False, results=[("abc123_fail.csv", "/tmp/a.csv", 10.0)])
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions()

    result = service.search_with_index("abc123", options)

    assert result is None
    assert ("search", "abc123") not in dummy.calls


def test_search_with_index_applies_filter_correctly():
    dummy = DummyIndexService(
        available=True,
        results=[
            ("abc123_fail.csv", "/tmp/a.csv", 10.0),
            ("abc123_pass.csv", "/tmp/b.csv", 9.0),
            ("abc123_fail.bin", "/tmp/c.bin", 8.0),
            ("zzz999_fail.csv", "/tmp/d.csv", 7.0),
        ],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions()

    result = service.search_with_index("abc123", options)

    assert result == [("abc123_fail.csv", "/tmp/a.csv", 10.0)]


def test_search_with_index_applies_limit():
    dummy = DummyIndexService(
        available=True,
        results=[
            ("abc123_fail_1.csv", "/tmp/a1.csv", 10.0),
            ("abc123_fail_2.csv", "/tmp/a2.csv", 9.0),
            ("abc123_fail_3.csv", "/tmp/a3.csv", 8.0),
        ],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions(max_results=2)

    result = service.search_with_index("abc123", options)

    assert len(result) == 2
    assert result[0][0] == "abc123_fail_1.csv"
    assert result[1][0] == "abc123_fail_2.csv"
