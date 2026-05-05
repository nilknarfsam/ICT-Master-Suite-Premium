from src.application.dtos.search_options import SearchOptions


class LogSearchService:
    """Serviço de aplicação para futuras orquestrações de busca de logs."""

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
