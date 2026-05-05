import sqlite3
from datetime import datetime

from src.infrastructure.sqlite.sqlite_paths import DB_LOCAL_PATH


class LogIndexRepository:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_LOCAL_PATH
        self._memory_conn = sqlite3.connect(":memory:") if self.db_path == ":memory:" else None

    def _connect(self):
        if self._memory_conn is not None:
            return self._memory_conn
        return sqlite3.connect(self.db_path)

    def init_index_db(self):
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS log_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    modified_time REAL NOT NULL
                )
                """
            )
            self._ensure_compatible_columns(cursor)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_log_index_file_name ON log_index (file_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_log_index_modified_time ON log_index (modified_time)")
            conn.commit()

    def _ensure_compatible_columns(self, cursor):
        cursor.execute("PRAGMA table_info(log_index)")
        existing = {row[1] for row in cursor.fetchall()}
        if "extension" not in existing:
            cursor.execute("ALTER TABLE log_index ADD COLUMN extension TEXT")
        if "size_bytes" not in existing:
            cursor.execute("ALTER TABLE log_index ADD COLUMN size_bytes INTEGER")
        if "indexed_at" not in existing:
            cursor.execute("ALTER TABLE log_index ADD COLUMN indexed_at TIMESTAMP")

    def insert_log_entry(self, file_name, path, modified_time):
        self.init_index_db()
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO log_index (file_name, path, modified_time)
                VALUES (?, ?, ?)
                """,
                (file_name, path, modified_time),
            )
            conn.commit()

    def upsert_log_entry(self, file_name, path, modified_time, extension=None, size_bytes=None):
        self.init_index_db()
        indexed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        existing = self.get_entry_by_path(path)
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            if existing:
                cursor.execute(
                    """
                    UPDATE log_index
                    SET file_name = ?, modified_time = ?, extension = ?, size_bytes = ?, indexed_at = ?
                    WHERE path = ?
                    """,
                    (file_name, modified_time, extension, size_bytes, indexed_at, path),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO log_index (file_name, path, modified_time, extension, size_bytes, indexed_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (file_name, path, modified_time, extension, size_bytes, indexed_at),
                )
            conn.commit()

    def get_entry_by_path(self, path):
        self.init_index_db()
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, path, modified_time, extension, size_bytes, indexed_at
                FROM log_index
                WHERE path = ?
                LIMIT 1
                """,
                (path,),
            )
            return cursor.fetchone()

    def count_entries(self):
        self.init_index_db()
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM log_index")
            return cursor.fetchone()[0]

    def search_by_term(self, term):
        self.init_index_db()
        needle = f"%{(term or '').lower()}%"
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT file_name, path, modified_time
                FROM log_index
                WHERE lower(file_name) LIKE ?
                ORDER BY modified_time DESC
                """,
                (needle,),
            )
            return cursor.fetchall()

    def clear_index(self):
        self.init_index_db()
        conn = self._connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM log_index")
            conn.commit()
