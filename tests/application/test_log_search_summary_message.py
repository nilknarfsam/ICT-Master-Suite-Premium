from src.application.services.log_search_service import LogSearchService


def test_build_summary_message_limited():
    service = LogSearchService()
    summary = {
        "total_original": 1200,
        "total_exibido": 500,
        "limitado": True,
        "max_results": 500,
    }
    assert (
        service.build_summary_message(summary)
        == "Exibindo 500 de 1200 arquivos encontrados. Refine a busca para ver menos resultados."
    )


def test_build_summary_message_not_limited():
    service = LogSearchService()
    summary = {
        "total_original": 43,
        "total_exibido": 43,
        "limitado": False,
        "max_results": 500,
    }
    assert service.build_summary_message(summary) == "43 arquivos encontrados."
