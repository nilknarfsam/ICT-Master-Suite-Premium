import os

from src.core.indexing.log_index_repository import LogIndexRepository


class LogIndexService:
    def __init__(self, repository=None):
        self.repository = repository or LogIndexRepository()

    def build_index_from_directory(self, base_path):
        if not base_path or not os.path.exists(base_path):
            return 0

        self.repository.init_index_db()
        self.repository.clear_index()

        indexed = 0
        for root, _, files in os.walk(base_path):
            for file_name in files:
                full_path = os.path.join(root, file_name)
                try:
                    modified_time = os.path.getmtime(full_path)
                except OSError:
                    continue
                self.repository.insert_log_entry(file_name, full_path, modified_time)
                indexed += 1
        return indexed

    def search(self, term):
        return self.repository.search_by_term(term)

    def is_index_available(self):
        try:
            self.repository.init_index_db()
            return True
        except Exception:
            return False
