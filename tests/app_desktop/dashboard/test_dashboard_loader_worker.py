"""Testes do DashboardLoaderWorker.

Usa `pytest.importorskip("PyQt5")` por causa do herdar `QObject`, mas
nao instancia `QApplication` nem `QThread` — apenas chama `start_load()`
diretamente para validar a montagem do snapshot.
"""

import pytest

pytest.importorskip("PyQt5")

from src.app_desktop.viewmodels.dashboard.dashboard_loader_worker import (  # noqa: E402
    DashboardLoaderWorker,
)
from src.app_desktop.viewmodels.dashboard.dashboard_snapshot import DashboardSnapshot  # noqa: E402


class _FakeAnalysisService:
    def __init__(self, stats=None, progress=None, recent=None, raise_in=None):
        self._stats = stats or {}
        self._progress = progress or {}
        self._recent = recent or []
        self._raise_in = raise_in or set()

    def get_ict_statistics(self):
        if "stats" in self._raise_in:
            raise RuntimeError("boom-stats")
        return self._stats

    def get_progress_statistics(self):
        if "progress" in self._raise_in:
            raise RuntimeError("boom-progress")
        return self._progress

    def get_latest_analyses(self, limite=10):
        if "recent" in self._raise_in:
            raise RuntimeError("boom-recent")
        return self._recent[:limite]


class _FakeIndexService:
    def __init__(self, available=True, count=0, raise_in=None):
        self._available = available
        self._count = count
        self._raise_in = raise_in or set()

    def is_index_available(self):
        if "available" in self._raise_in:
            raise RuntimeError("boom-available")
        return self._available

    def count_entries(self):
        if "count" in self._raise_in:
            raise RuntimeError("boom-count")
        return self._count


def test_start_load_emite_snapshot_para_servicos_saudaveis(qtbot=None):
    captured = []

    def _on_ready(snapshot):
        captured.append(snapshot)

    analysis = _FakeAnalysisService(
        stats={
            "total_hoje": 12,
            "top_componente": "U7",
            "top_5_componentes": [("U7", 10), ("U8", 2)],
            "db_online": True,
        },
        progress={"abertos": 4, "tratados": 8},
        recent=[("2026-05-06", "SN1", "U7", "TRATADO")],
    )
    index = _FakeIndexService(available=True, count=42)
    worker = DashboardLoaderWorker(analysis, index, recent_limit=5)
    worker.snapshotReady.connect(_on_ready)

    worker.start_load()

    assert len(captured) == 1
    snap = captured[0]
    assert isinstance(snap, DashboardSnapshot)
    assert snap.total_hoje == 12
    assert snap.abertos == 4
    assert snap.tratados == 8
    assert snap.top_componente == "U7"
    assert snap.top_5_componentes == [("U7", 10), ("U8", 2)]
    assert snap.db_online is True
    assert snap.index_size == 42
    assert snap.index_ready is True
    assert snap.recent_activity == [("2026-05-06", "SN1", "U7", "TRATADO")]
    assert snap.generated_at != ""


def test_start_load_tolera_falha_individual_em_um_servico():
    captured = []
    worker = DashboardLoaderWorker(
        _FakeAnalysisService(
            stats={"total_hoje": 5, "db_online": True},
            progress={"abertos": 1, "tratados": 4},
            recent=[],
            raise_in={"recent"},
        ),
        _FakeIndexService(available=False, count=0),
    )
    worker.snapshotReady.connect(lambda s: captured.append(s))

    worker.start_load()

    assert len(captured) == 1
    assert captured[0].total_hoje == 5
    assert captured[0].recent_activity == []
    assert captured[0].index_ready is False


def test_start_load_emite_load_failed_em_excecao_global(monkeypatch):
    failures = []
    worker = DashboardLoaderWorker(_FakeAnalysisService(), _FakeIndexService())
    worker.loadFailed.connect(lambda msg: failures.append(msg))

    def _explode(*args, **kwargs):
        raise RuntimeError("snapshot-boom")

    monkeypatch.setattr(
        "src.app_desktop.viewmodels.dashboard.dashboard_loader_worker.DashboardSnapshot",
        _explode,
    )

    worker.start_load()

    assert len(failures) == 1
    assert "snapshot-boom" in failures[0]


def test_start_load_normaliza_recent_em_tuplas():
    captured = []
    worker = DashboardLoaderWorker(
        _FakeAnalysisService(recent=[["2026-05-06", "SN2", "U8", "EM_ABERTO"]]),
        _FakeIndexService(),
    )
    worker.snapshotReady.connect(lambda s: captured.append(s))

    worker.start_load()

    assert captured[0].recent_activity == [("2026-05-06", "SN2", "U8", "EM_ABERTO")]
