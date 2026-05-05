from src.application.services.log_search_service import LogSearchService


def test_build_summary_message_with_source_index():
    service = LogSearchService()
    summary = {
        "total_original": 1200,
        "total_exibido": 500,
        "limitado": True,
        "max_results": 500,
        "source": "index",
    }
    assert (
        service.build_summary_message(summary)
        == "Busca rápida: Exibindo 500 de 1200 arquivos encontrados. Refine a busca para ver menos resultados."
    )


def test_build_summary_message_with_source_scanner():
    service = LogSearchService()
    summary = {
        "total_original": 43,
        "total_exibido": 43,
        "limitado": False,
        "max_results": 500,
        "source": "scanner",
    }
    assert service.build_summary_message(summary) == "Busca em rede: 43 arquivos encontrados."


def test_build_summary_message_without_source_keeps_compatibility():
    service = LogSearchService()
    summary = {
        "total_original": 43,
        "total_exibido": 43,
        "limitado": False,
        "max_results": 500,
    }
    assert service.build_summary_message(summary) == "43 arquivos encontrados."
