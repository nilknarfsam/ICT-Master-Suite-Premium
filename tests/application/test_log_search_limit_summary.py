from src.application.services.log_search_service import LogSearchService


def test_was_limited_true_when_original_greater():
    service = LogSearchService()
    assert service.was_limited(600, 500) is True


def test_was_limited_false_when_original_smaller():
    service = LogSearchService()
    assert service.was_limited(400, 500) is False


def test_was_limited_false_when_counts_equal():
    service = LogSearchService()
    assert service.was_limited(500, 500) is False


def test_was_limited_false_for_empty_list_counts():
    service = LogSearchService()
    assert service.was_limited(0, 0) is False
