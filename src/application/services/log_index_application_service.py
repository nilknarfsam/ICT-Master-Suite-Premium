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

    def rebuild_index(self, base_paths: list[str], allowed_extensions=None):
        paths = [p for p in (base_paths or []) if p]
        self.service.clear_index()

        total_indexed = 0
        total_errors = 0
        per_path = []
        for path in paths:
            summary = self.service.build_incremental_index(path, allowed_extensions)
            total_indexed += summary.get("indexed", 0)
            total_errors += summary.get("errors", 0)
            per_path.append(
                {
                    "path": path,
                    "indexed": summary.get("indexed", 0),
                    "errors": summary.get("errors", 0),
                }
            )

        return {
            "paths": paths,
            "total_indexed": total_indexed,
            "total_errors": total_errors,
            "per_path": per_path,
        }
