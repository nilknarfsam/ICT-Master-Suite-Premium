from src.core.indexing.log_index_repository import LogIndexRepository
from src.core.indexing.log_index_service import LogIndexService


def test_index_file_with_valid_file(tmp_path):
    db_path = tmp_path / "index.db"
    file_path = tmp_path / "abc123_fail.csv"
    file_path.write_text("content", encoding="utf-8")

    repo = LogIndexRepository(db_path=str(db_path))
    service = LogIndexService(repository=repo)

    ok = service.index_file(str(file_path))

    assert ok is True
    row = repo.get_entry_by_path(str(file_path))
    assert row is not None
    assert row[1] == "abc123_fail.csv"
    assert row[4] == ".csv"
    assert row[5] == len("content")


def test_index_file_with_missing_file(tmp_path):
    db_path = tmp_path / "index.db"
    repo = LogIndexRepository(db_path=str(db_path))
    service = LogIndexService(repository=repo)

    ok = service.index_file(str(tmp_path / "missing.csv"))

    assert ok is False
    assert repo.count_entries() == 0


def test_upsert_updates_existing_entry(tmp_path):
    db_path = tmp_path / "index.db"
    file_path = tmp_path / "same.csv"
    file_path.write_text("one", encoding="utf-8")

    repo = LogIndexRepository(db_path=str(db_path))
    service = LogIndexService(repository=repo)
    assert service.index_file(str(file_path)) is True
    first_count = repo.count_entries()

    file_path.write_text("updated-content", encoding="utf-8")
    assert service.index_file(str(file_path)) is True
    second_count = repo.count_entries()

    row = repo.get_entry_by_path(str(file_path))
    assert first_count == 1
    assert second_count == 1
    assert row[5] == len("updated-content")


def test_count_entries(tmp_path):
    db_path = tmp_path / "index.db"
    repo = LogIndexRepository(db_path=str(db_path))

    repo.upsert_log_entry("a.csv", "/tmp/a.csv", 1.0, extension=".csv", size_bytes=1)
    repo.upsert_log_entry("b.csv", "/tmp/b.csv", 2.0, extension=".csv", size_bytes=2)

    assert repo.count_entries() == 2


def test_build_incremental_index_ignores_invalid_extension(tmp_path):
    db_path = tmp_path / "index.db"
    valid = tmp_path / "ok.csv"
    invalid = tmp_path / "nope.bin"
    valid.write_text("v", encoding="utf-8")
    invalid.write_text("x", encoding="utf-8")

    repo = LogIndexRepository(db_path=str(db_path))
    service = LogIndexService(repository=repo)
    summary = service.build_incremental_index(str(tmp_path), allowed_extensions={".csv", ".txt"})

    assert summary["indexed"] == 1
    assert summary["errors"] == 0
    assert repo.count_entries() == 1
