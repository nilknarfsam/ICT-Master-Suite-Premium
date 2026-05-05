class LogSearchService:
    """Serviço de aplicação para futuras orquestrações de busca de logs."""

    def normalize_search_term(self, term: str) -> str:
        return (term or "").strip().lower()

    def validate_search_term(self, term: str, min_length: int = 5) -> bool:
        normalized = self.normalize_search_term(term)
        return len(normalized) >= min_length
