from src.application.services.log_search_service import LogSearchService


def test_thread_filter_equivalence_term_and_extension_and_fail():
    service = LogSearchService()
    options = service.build_default_options()
    assert service.should_include_file("abc123_fail.csv", "abc123", options) is True


def test_thread_filter_equivalence_missing_term():
    service = LogSearchService()
    options = service.build_default_options()
    assert service.should_include_file("xyz999_fail.csv", "abc123", options) is False


def test_thread_filter_equivalence_invalid_extension():
    service = LogSearchService()
    options = service.build_default_options()
    assert service.should_include_file("abc123_fail.xml", "abc123", options) is False


def test_thread_filter_equivalence_reject_pass_name():
    service = LogSearchService()
    options = service.build_default_options()
    assert service.should_include_file("abc123_pass.csv", "abc123", options) is False


def test_thread_filter_equivalence_reject_p_prefix():
    service = LogSearchService()
    options = service.build_default_options()
    assert service.should_include_file("p_abc123.csv", "abc123", options) is False
