import pytest

pytest.importorskip("PyQt5")

from src.app_desktop.viewmodels.dashboard.dashboard_snapshot import DashboardSnapshot
from src.app_desktop.viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel


class _FakeAnalysis:
    def get_ict_statistics(self):
        return {"total_hoje": 1, "top_componente": "U1", "top_5_componentes": [], "db_online": True}

    def get_progress_statistics(self):
        return {"abertos": 0, "tratados": 1}

    def get_latest_analyses(self, limite=10):
        return [("2026-05-06T10:11:00", "SN", "U1", "TRATADO")]


class _FakeIndex:
    def is_index_available(self):
        return True

    def count_entries(self):
        return 9


def test_viewmodel_status_kind_mapping():
    assert DashboardViewModel._status_kind("TRATADO") == "pass"
    assert DashboardViewModel._status_kind("EM_ABERTO") == "warning"
    assert DashboardViewModel._status_kind("ERRO") == "fail"
    assert DashboardViewModel._status_kind("OUTRO") == "neutral"


def test_viewmodel_process_snapshot_emits_payloads():
    vm = DashboardViewModel(_FakeAnalysis(), _FakeIndex())
    metrics, recent, summary, states = [], [], [], []
    vm.metricsUpdated.connect(lambda p: metrics.append(p))
    vm.recentActivityUpdated.connect(lambda p: recent.append(p))
    vm.searchSummaryUpdated.connect(lambda p: summary.append(p))
    vm.uiStateChanged.connect(lambda s: states.append(s))
    vm._on_snapshot_ready(
        DashboardSnapshot(
            total_hoje=3,
            abertos=1,
            tratados=2,
            top_componente="U7",
            db_online=True,
            index_size=12,
            index_ready=True,
            recent_activity=[("2026-05-06T10:11:00", "SN1", "U7", "TRATADO")],
            generated_at="2026-05-06T10:12:00",
        )
    )
    assert metrics and metrics[0]["total_hoje"] == 3
    assert recent and recent[0][0]["kind"] == "pass"
    assert summary and summary[0]["index_size"] == 12
    assert states and states[-1] == "success"
    vm.shutdown()
