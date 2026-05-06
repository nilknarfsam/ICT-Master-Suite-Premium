"""Testes da dataclass DashboardSnapshot.

Sem dependencia de PyQt5: validam apenas estrutura, factory e
metodo `is_empty`.
"""

from src.app_desktop.viewmodels.dashboard.dashboard_snapshot import DashboardSnapshot


def test_snapshot_empty_factory_retorna_dataclass_valido():
    snap = DashboardSnapshot.empty()
    assert isinstance(snap, DashboardSnapshot)
    assert snap.total_hoje == 0
    assert snap.abertos == 0
    assert snap.tratados == 0
    assert snap.top_componente == "N/A"
    assert snap.top_5_componentes == []
    assert snap.db_online is False
    assert snap.index_size == 0
    assert snap.index_ready is False
    assert snap.recent_activity == []
    assert snap.generated_at != ""


def test_snapshot_is_empty_true_para_snapshot_sem_dados():
    assert DashboardSnapshot.empty().is_empty() is True


def test_snapshot_is_empty_false_quando_ha_atividade():
    snap = DashboardSnapshot(
        recent_activity=[("2026-05-06", "SN1", "C1", "TRATADO")],
        generated_at="2026-05-06T10:00:00",
    )
    assert snap.is_empty() is False


def test_snapshot_is_empty_false_quando_db_online():
    snap = DashboardSnapshot(db_online=True, generated_at="x")
    assert snap.is_empty() is False


def test_snapshot_is_empty_false_quando_index_ready():
    snap = DashboardSnapshot(index_ready=True, generated_at="x")
    assert snap.is_empty() is False


def test_snapshot_is_empty_false_quando_total_hoje_positivo():
    snap = DashboardSnapshot(total_hoje=3, generated_at="x")
    assert snap.is_empty() is False


def test_snapshot_e_imutavel():
    snap = DashboardSnapshot.empty()
    try:
        snap.total_hoje = 5  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("DashboardSnapshot deveria ser imutavel (frozen)")
