from src.application.services.log_search_service import LogSearchService


def test_default_max_results_is_500():
    service = LogSearchService()
    options = service.build_default_options()
    assert options.max_results == 500


def test_limit_results_keeps_first_500_items():
    service = LogSearchService()
    options = service.build_default_options()
    results = list(range(700))

    limited = service.limit_results(results, options)

    assert len(limited) == 500
    assert limited == list(range(500))
