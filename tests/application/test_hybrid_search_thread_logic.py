from src.app_desktop.threads import BuscaThread


def test_hybrid_index_available_skips_scanner(monkeypatch):
    thread = BuscaThread("abc123", ["dir1"])
    emitted = {"lista": None, "summary": None}
    thread.lista_arquivos.connect(lambda payload: emitted.__setitem__("lista", payload))
    thread.search_summary.connect(lambda payload: emitted.__setitem__("summary", payload))

    monkeypatch.setattr(
        thread.log_search_service,
        "search_with_index",
        lambda term, options: [("abc123_fail.csv", "/tmp/a.csv", 10.0)],
    )

    called = {"scanner": False}

    def fake_scanner(_):
        called["scanner"] = True
        return []

    monkeypatch.setattr(thread, "_scandir_recursivo", fake_scanner)

    thread.run()

    assert called["scanner"] is False
    assert emitted["lista"] == [("abc123_fail.csv", "/tmp/a.csv")]
    assert emitted["summary"]["total_original"] == 1
    assert emitted["summary"]["total_exibido"] == 1
    assert emitted["summary"]["limitado"] is False


def test_hybrid_index_unavailable_uses_scanner(monkeypatch):
    thread = BuscaThread("abc123", ["dir1"])
    emitted = {"lista": None, "summary": None}
    thread.lista_arquivos.connect(lambda payload: emitted.__setitem__("lista", payload))
    thread.search_summary.connect(lambda payload: emitted.__setitem__("summary", payload))

    monkeypatch.setattr(thread.log_search_service, "search_with_index", lambda term, options: None)
    monkeypatch.setattr("src.app_desktop.threads.os.path.exists", lambda path: True)
    monkeypatch.setattr(thread, "_scandir_recursivo", lambda path: [(10.0, "abc123_fail.csv", "/tmp/a.csv")])

    thread.run()

    assert emitted["lista"] == [("abc123_fail.csv", "/tmp/a.csv")]
    assert emitted["summary"]["total_original"] == 1


def test_hybrid_index_error_falls_back_to_scanner(monkeypatch):
    thread = BuscaThread("abc123", ["dir1"])
    emitted = {"lista": None}
    thread.lista_arquivos.connect(lambda payload: emitted.__setitem__("lista", payload))

    def boom(term, options):
        raise RuntimeError("index error")

    monkeypatch.setattr(thread.log_search_service, "search_with_index", boom)
    monkeypatch.setattr("src.app_desktop.threads.os.path.exists", lambda path: True)
    monkeypatch.setattr(thread, "_scandir_recursivo", lambda path: [(9.0, "abc123_fail.csv", "/tmp/b.csv")])

    thread.run()

    assert emitted["lista"] == [("abc123_fail.csv", "/tmp/b.csv")]


def test_hybrid_index_result_conversion_to_ui_format(monkeypatch):
    thread = BuscaThread("abc123", ["dir1"])
    emitted = {"lista": None}
    thread.lista_arquivos.connect(lambda payload: emitted.__setitem__("lista", payload))

    monkeypatch.setattr(
        thread.log_search_service,
        "search_with_index",
        lambda term, options: [
            ("abc123_fail_1.csv", "/tmp/a1.csv", 11.0),
            ("abc123_fail_2.csv", "/tmp/a2.csv", 10.0),
        ],
    )

    thread.run()

    assert emitted["lista"] == [
        ("abc123_fail_1.csv", "/tmp/a1.csv"),
        ("abc123_fail_2.csv", "/tmp/a2.csv"),
    ]
