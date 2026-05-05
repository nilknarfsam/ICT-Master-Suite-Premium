from src.application.services.log_search_service import LogSearchService


def test_normalize_search_term_with_spaces():
    service = LogSearchService()
    assert service.normalize_search_term("   ABCDE   ") == "abcde"


def test_normalize_search_term_lowercase_input():
    service = LogSearchService()
    assert service.normalize_search_term("serialxyz") == "serialxyz"


def test_validate_search_term_empty_input():
    service = LogSearchService()
    assert service.validate_search_term("") is False


def test_validate_search_term_four_characters():
    service = LogSearchService()
    assert service.validate_search_term("abcd") is False


def test_validate_search_term_five_characters():
    service = LogSearchService()
    assert service.validate_search_term("abcde") is True
