import sqlite3

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
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_log_index_file_name ON log_index (file_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_log_index_modified_time ON log_index (modified_time)")
            conn.commit()

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
