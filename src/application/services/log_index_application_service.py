from src.core.indexing.log_index_service import LogIndexService


class LogIndexApplicationService:
    """Servico de aplicacao para indexacao local de logs."""

    def __init__(self, service=None):
        self.service = service or LogIndexService()

    def build_incremental_index(self, base_path, allowed_extensions=None):
        return self.service.build_incremental_index(base_path, allowed_extensions)

    def index_file(self, path):
        return self.service.index_file(path)

    def search(self, term):
        return self.service.search(term)

    def is_index_available(self):
        return self.service.is_index_available()

    def count_entries(self):
        return self.service.count_entries()
