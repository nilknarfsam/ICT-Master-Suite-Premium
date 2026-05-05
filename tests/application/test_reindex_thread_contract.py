import pytest


def test_reindex_thread_basic_contract():
    pytest.importorskip("PyQt5")
    from src.app_desktop.threads import ReindexThread

    thread = ReindexThread(base_paths=["/tmp/logs"], rebuild=True, allowed_extensions={".csv"})

    assert thread.base_paths == ["/tmp/logs"]
    assert thread.rebuild is True
    assert thread.allowed_extensions == {".csv"}
    assert hasattr(thread, "progress_msg")
    assert hasattr(thread, "finished_summary")
    assert hasattr(thread, "failed")
