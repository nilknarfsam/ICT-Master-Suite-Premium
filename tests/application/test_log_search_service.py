from src.application.services.log_search_service import LogSearchService


def test_normalize_search_term_lower_and_trim():
    service = LogSearchService()
    assert service.normalize_search_term("  SeRiAl123  ") == "serial123"


def test_validate_search_term_short_and_long():
    service = LogSearchService()
    assert service.validate_search_term("abc", min_length=5) is False
    assert service.validate_search_term("abcde", min_length=5) is True
