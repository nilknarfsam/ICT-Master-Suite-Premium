from src.application.dtos.search_options import SearchOptions
from src.application.services.log_search_service import LogSearchService


def test_build_default_options():
    service = LogSearchService()
    options = service.build_default_options()

    assert options.max_results == 500
    assert options.include_backup is True
    assert options.include_pass_logs is False
    assert options.allowed_extensions == (".csv", ".dcl", ".txt", ".log")


def test_should_include_file_accepts_fail_log():
    service = LogSearchService()
    options = service.build_default_options()

    assert service.should_include_file("abc123_fail.csv", "abc123", options) is True


def test_should_include_file_rejects_pass_by_default():
    service = LogSearchService()
    options = service.build_default_options()

    assert service.should_include_file("abc123_pass.csv", "abc123", options) is False
    assert service.should_include_file("p_abc123.csv", "abc123", options) is False


def test_should_include_file_accepts_pass_when_enabled():
    service = LogSearchService()
    options = SearchOptions(include_pass_logs=True)

    assert service.should_include_file("abc123_pass.csv", "abc123", options) is True
    assert service.should_include_file("p_abc123.csv", "abc123", options) is True


def test_should_include_file_rejects_invalid_extension():
    service = LogSearchService()
    options = service.build_default_options()

    assert service.should_include_file("abc123_fail.xml", "abc123", options) is False


def test_should_include_file_rejects_missing_term():
    service = LogSearchService()
    options = service.build_default_options()

    assert service.should_include_file("xyz999_fail.csv", "abc123", options) is False
