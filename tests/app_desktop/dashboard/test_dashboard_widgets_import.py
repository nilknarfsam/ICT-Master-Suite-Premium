import pytest

pytest.importorskip("PyQt5")

from PyQt5.QtWidgets import QWidget  # noqa: E402

from src.app_desktop.widgets.dashboard.dashboard_grid import DashboardGrid  # noqa: E402
from src.app_desktop.widgets.dashboard.dashboard_header import DashboardHeader  # noqa: E402
from src.app_desktop.widgets.dashboard.empty_state import EmptyState  # noqa: E402
from src.app_desktop.widgets.dashboard.loading_state import LoadingState  # noqa: E402
from src.app_desktop.widgets.dashboard.metric_card import MetricCard  # noqa: E402
from src.app_desktop.widgets.dashboard.quick_actions_panel import QuickActionsPanel  # noqa: E402
from src.app_desktop.widgets.dashboard.recent_activity_panel import RecentActivityPanel  # noqa: E402
from src.app_desktop.widgets.dashboard.search_summary_panel import SearchSummaryPanel  # noqa: E402
from src.app_desktop.widgets.dashboard.section_title import SectionTitle  # noqa: E402
from src.app_desktop.widgets.dashboard.status_card import StatusCard  # noqa: E402


def test_dashboard_widgets_are_qwidgets():
    for cls in [
        DashboardGrid,
        DashboardHeader,
        EmptyState,
        LoadingState,
        MetricCard,
        QuickActionsPanel,
        RecentActivityPanel,
        SearchSummaryPanel,
        SectionTitle,
        StatusCard,
    ]:
        assert issubclass(cls, QWidget)
