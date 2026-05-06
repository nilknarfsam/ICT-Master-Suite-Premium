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


def test_timed_search_with_index_returns_pair_with_results():
    dummy = DummyIndexService(
        available=True,
        results=[("abc123_fail.csv", "/tmp/a.csv", 10.0)],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions()

    pair = service.timed_search_with_index("abc123", options)

    assert isinstance(pair, tuple)
    assert len(pair) == 2

    results, elapsed_ms = pair
    assert results == [("abc123_fail.csv", "/tmp/a.csv", 10.0)]
    assert isinstance(elapsed_ms, float)
    assert elapsed_ms >= 0.0


def test_timed_search_with_index_returns_none_when_index_unavailable():
    dummy = DummyIndexService(
        available=False,
        results=[("abc123_fail.csv", "/tmp/a.csv", 10.0)],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions()

    results, elapsed_ms = service.timed_search_with_index("abc123", options)

    assert results is None
    assert isinstance(elapsed_ms, float)
    assert elapsed_ms >= 0.0
    assert ("search", "abc123") not in dummy.calls


def test_timed_search_with_index_preserves_filter_and_limit():
    dummy = DummyIndexService(
        available=True,
        results=[
            ("abc123_fail_1.csv", "/tmp/a1.csv", 10.0),
            ("abc123_fail_2.csv", "/tmp/a2.csv", 9.0),
            ("abc123_pass.csv", "/tmp/p.csv", 8.0),
            ("zzz999_fail.csv", "/tmp/z.csv", 7.0),
        ],
    )
    service = LogSearchService(log_index_application_service=dummy)
    options = SearchOptions(max_results=1)

    results, elapsed_ms = service.timed_search_with_index("abc123", options)

    assert results == [("abc123_fail_1.csv", "/tmp/a1.csv", 10.0)]
    assert elapsed_ms >= 0.0


def test_timed_search_with_index_propagates_unexpected_exception():
    class ExplodingIndex(DummyIndexService):
        def search(self, term):
            raise RuntimeError("boom")

    service = LogSearchService(
        log_index_application_service=ExplodingIndex(available=True),
    )
    options = SearchOptions()

    raised = False
    try:
        service.timed_search_with_index("abc123", options)
    except RuntimeError:
        raised = True

    assert raised, "RuntimeError do indice deve ser propagado para o chamador"
