import time

from src.application.dtos.search_options import SearchOptions
from src.application.services.log_index_application_service import LogIndexApplicationService


class LogSearchService:
    """Serviço de aplicação para futuras orquestrações de busca de logs."""
    def __init__(self, log_index_application_service=None):
        self.log_index_application_service = log_index_application_service or LogIndexApplicationService()


    def normalize_search_term(self, term: str) -> str:
        return (term or "").strip().lower()

    def validate_search_term(self, term: str, min_length: int = 5) -> bool:
        normalized = self.normalize_search_term(term)
        return len(normalized) >= min_length

    def build_default_options(self) -> SearchOptions:
        return SearchOptions()

    def should_include_file(self, file_name: str, term: str, options: SearchOptions) -> bool:
        name = (file_name or "").lower()
        search_term = self.normalize_search_term(term)
        if not search_term or search_term not in name:
            return False

        if not name.endswith(tuple(ext.lower() for ext in options.allowed_extensions)):
            return False

        if not options.include_pass_logs:
            if "pass" in name or name.startswith("p_"):
                return False

        return True

    def limit_results(self, results, options: SearchOptions):
        max_results = max(0, int(options.max_results))
        return results[:max_results]

    def was_limited(self, original_count: int, limited_count: int) -> bool:
        return original_count > limited_count

    def build_summary_message(self, summary: dict) -> str:
        total_original = summary.get("total_original", 0)
        total_exibido = summary.get("total_exibido", 0)
        limitado = summary.get("limitado", False)
        source = summary.get("source")
        if limitado:
            base_message = (
                f"Exibindo {total_exibido} de {total_original} arquivos encontrados. "
                "Refine a busca para ver menos resultados."
            )
        else:
            base_message = f"{total_exibido} arquivos encontrados."

        if source == "index":
            return f"Busca rápida: {base_message}"
        if source == "scanner":
            return f"Busca em rede: {base_message}"
        return base_message

    def is_index_ready(self) -> bool:
        return self.log_index_application_service.is_index_available()

    def search_with_index(self, term: str, options: SearchOptions):
        if not self.is_index_ready():
            return None

        indexed_results = self.log_index_application_service.search(term)
        filtered = [
            item
            for item in indexed_results
            if self.should_include_file(item[0], term, options)
        ]
        return self.limit_results(filtered, options)

    def timed_search_with_index(self, term: str, options: SearchOptions):
        """Wrapper de medicao para diagnostico de performance.

        Mede o tempo total da execucao de `search_with_index` e devolve um par
        `(resultado, tempo_ms)`, sem alterar o contrato de `search_with_index`.

        Util para `scripts/benchmark_search.py` e para registro de baseline em
        `docs/BASELINE_BUSCA.md`. Nao e consumido pela UI.
        """
        start = time.perf_counter()
        try:
            results = self.search_with_index(term, options)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
        return results, elapsed_ms
