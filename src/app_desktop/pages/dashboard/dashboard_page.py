from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QFrame, QLabel

from src.app_desktop.viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel
from src.app_desktop.widgets.dashboard.dashboard_grid import DashboardGrid
from src.app_desktop.widgets.dashboard.dashboard_header import DashboardHeader
from src.app_desktop.widgets.dashboard.empty_state import EmptyState
from src.app_desktop.widgets.dashboard.loading_state import LoadingState
from src.app_desktop.widgets.dashboard.metric_card import MetricCard
from src.app_desktop.widgets.dashboard.quick_actions_panel import QuickActionsPanel
from src.app_desktop.widgets.dashboard.recent_activity_panel import RecentActivityPanel
from src.app_desktop.widgets.dashboard.search_summary_panel import SearchSummaryPanel


class DashboardPage(QWidget):
    quickActionRequested = pyqtSignal(str)

    def __init__(self, log_analysis_service, log_index_service, is_admin: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardPage")
        self._first_show = True
        self.vm = DashboardViewModel(log_analysis_service, log_index_service, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.error_banner = QFrame()
        self.error_banner.setObjectName("dashboardErrorBanner")
        eb_layout = QVBoxLayout(self.error_banner)
        self.error_label = QLabel("")
        self.error_label.setObjectName("dashboardErrorBannerText")
        eb_layout.addWidget(self.error_label)
        self.error_banner.setVisible(False)

        self.header = DashboardHeader("Dashboard Premium", "Aguardando dados...")
        self.metric_total = MetricCard("Total hoje", "0")
        self.metric_open = MetricCard("Abertos", "0", tone="warning")
        self.metric_done = MetricCard("Tratados", "0", tone="positive")
        self.metric_top = MetricCard("Top componente", "N/A")
        self.activity = RecentActivityPanel()
        self.summary = SearchSummaryPanel()
        self.actions = QuickActionsPanel(is_admin=is_admin)
        self.loading = LoadingState("Carregando dashboard...")
        self.empty = EmptyState("Sem dados", "Nao ha dados para exibir no dashboard no momento.")
        self.empty.setVisible(False)

        self.grid = DashboardGrid()
        self.grid.add_row(self.metric_total, self.metric_open, self.metric_done, self.metric_top)
        self.grid.add_row(self.activity, self.summary)
        self.grid.add_row(self.actions)

        layout.addWidget(self.error_banner)
        layout.addWidget(self.header)
        layout.addWidget(self.loading)
        layout.addWidget(self.empty)
        layout.addWidget(self.grid)

        self.header.refreshClicked.connect(self.vm.refresh)
        self.actions.actionRequested.connect(self.vm.request_quick_action)
        self.vm.quickActionRequested.connect(self.quickActionRequested.emit)

        self.vm.metricsUpdated.connect(self._on_metrics)
        self.vm.recentActivityUpdated.connect(self.activity.set_items)
        self.vm.searchSummaryUpdated.connect(self.summary.set_data)
        self.vm.loadingStateChanged.connect(self._on_loading)
        self.vm.uiStateChanged.connect(self._on_state)
        self.vm.errorOccurred.connect(self._on_error)

    def _on_metrics(self, payload: dict):
        self.metric_total.set_value(payload.get("total_hoje", 0))
        self.metric_open.set_value(payload.get("abertos", 0))
        self.metric_done.set_value(payload.get("tratados", 0))
        self.metric_top.set_value(payload.get("top_componente", "N/A"))
        self.header.set_subtitle(f"Atualizado em {payload.get('updated_at', '--:--')}")

    def _on_loading(self, loading: bool):
        self.loading.setVisible(loading)
        self.grid.setVisible(not loading)
        self.header.btn_refresh.setEnabled(not loading)

    def _on_state(self, state: str):
        self.empty.setVisible(state == "empty")
        if state == "empty":
            self.grid.setVisible(False)
        elif state != "loading":
            self.grid.setVisible(True)

    def _on_error(self, message: str):
        self.error_label.setText(message)
        self.error_banner.setVisible(True)

    def showEvent(self, event):  # noqa: N802
        super().showEvent(event)
        if self._first_show:
            self._first_show = False
            self.vm.refresh()

    def shutdown(self):
        self.vm.shutdown()
