from src.core.indexing.log_index_repository import LogIndexRepository


def test_init_index_db_creates_table():
    repo = LogIndexRepository(db_path=":memory:")
    repo.init_index_db()
    rows = repo.search_by_term("")
    assert rows == []


def test_insert_and_search_simple_term():
    repo = LogIndexRepository(db_path=":memory:")
    repo.init_index_db()
    repo.insert_log_entry("abc123_fail.csv", "/tmp/abc123_fail.csv", 200.0)
    repo.insert_log_entry("zzz999_fail.csv", "/tmp/zzz999_fail.csv", 100.0)

    rows = repo.search_by_term("abc123")
    assert len(rows) == 1
    assert rows[0][0] == "abc123_fail.csv"
    assert rows[0][1] == "/tmp/abc123_fail.csv"


def test_search_returns_newest_first():
    repo = LogIndexRepository(db_path=":memory:")
    repo.init_index_db()
    repo.insert_log_entry("same_a.csv", "/tmp/same_a.csv", 100.0)
    repo.insert_log_entry("same_b.csv", "/tmp/same_b.csv", 200.0)

    rows = repo.search_by_term("same")
    assert len(rows) == 2
    assert rows[0][0] == "same_b.csv"
    assert rows[1][0] == "same_a.csv"


def test_clear_index_removes_entries():
    repo = LogIndexRepository(db_path=":memory:")
    repo.init_index_db()
    repo.insert_log_entry("abc123_fail.csv", "/tmp/abc123_fail.csv", 200.0)
    assert len(repo.search_by_term("abc123")) == 1

    repo.clear_index()
    assert repo.search_by_term("abc123") == []
