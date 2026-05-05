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

    def count_entries(self):
        return self.repository.count_entries()

    def clear_index(self):
        self.repository.clear_index()

    def index_file(self, path):
        if not path or not os.path.isfile(path):
            return False
        try:
            file_name = os.path.basename(path)
            modified_time = os.path.getmtime(path)
            extension = os.path.splitext(file_name)[1].lower()
            size_bytes = os.path.getsize(path)
            self.repository.upsert_log_entry(
                file_name=file_name,
                path=path,
                modified_time=modified_time,
                extension=extension,
                size_bytes=size_bytes,
            )
            return True
        except OSError:
            return False

    def build_incremental_index(self, base_path, allowed_extensions=None):
        if not base_path or not os.path.exists(base_path):
            return {"indexed": 0, "errors": 0}

        allowed = None
        if allowed_extensions:
            allowed = {ext.lower() for ext in allowed_extensions}

        indexed = 0
        errors = 0
        for root, _, files in os.walk(base_path):
            for file_name in files:
                extension = os.path.splitext(file_name)[1].lower()
                if allowed is not None and extension not in allowed:
                    continue
                full_path = os.path.join(root, file_name)
                try:
                    if self.index_file(full_path):
                        indexed += 1
                    else:
                        errors += 1
                except (PermissionError, OSError):
                    errors += 1
                    continue
        return {"indexed": indexed, "errors": errors}
