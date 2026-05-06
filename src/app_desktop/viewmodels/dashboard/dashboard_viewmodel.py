from datetime import datetime

from PyQt5.QtCore import QObject, QMetaObject, Qt, QThread, pyqtSignal

from src.app_desktop.viewmodels.dashboard.dashboard_loader_worker import DashboardLoaderWorker
from src.app_desktop.viewmodels.dashboard.dashboard_snapshot import DashboardSnapshot


class DashboardViewModel(QObject):
    metricsUpdated = pyqtSignal(dict)
    recentActivityUpdated = pyqtSignal(list)
    searchSummaryUpdated = pyqtSignal(dict)
    loadingStateChanged = pyqtSignal(bool)
    errorOccurred = pyqtSignal(str)
    uiStateChanged = pyqtSignal(str)
    quickActionRequested = pyqtSignal(str)

    def __init__(self, log_analysis_service, log_index_service, parent=None):
        super().__init__(parent)
        self._thread = QThread(self)
        self._worker = DashboardLoaderWorker(log_analysis_service, log_index_service)
        self._worker.moveToThread(self._thread)
        self._worker.snapshotReady.connect(self._on_snapshot_ready)
        self._worker.loadFailed.connect(self._on_load_failed)
        self._thread.start()
        self._is_loading = False

    def refresh(self):
        if self._is_loading:
            return
        self._is_loading = True
        self.loadingStateChanged.emit(True)
        self.uiStateChanged.emit("loading")
        QMetaObject.invokeMethod(self._worker, "start_load", Qt.QueuedConnection)

    def request_quick_action(self, name: str):
        self.quickActionRequested.emit(name)

    def _on_snapshot_ready(self, snapshot: DashboardSnapshot):
        self._is_loading = False
        metrics_payload = {
            "total_hoje": snapshot.total_hoje,
            "abertos": snapshot.abertos,
            "tratados": snapshot.tratados,
            "top_componente": snapshot.top_componente,
            "top_5_componentes": snapshot.top_5_componentes,
            "db_online": snapshot.db_online,
            "updated_at": self._fmt_time(snapshot.generated_at),
        }
        self.metricsUpdated.emit(metrics_payload)
        self.recentActivityUpdated.emit(
            [
                {
                    "data": self._fmt_time(row[0]),
                    "serial": row[1],
                    "componente": row[2],
                    "status": row[3],
                    "kind": self._status_kind(row[3]),
                }
                for row in snapshot.recent_activity
            ]
        )
        self.searchSummaryUpdated.emit(
            {
                "index_ready": snapshot.index_ready,
                "index_size": snapshot.index_size,
                "generated_at": self._fmt_time(snapshot.generated_at),
            }
        )
        state = "empty" if snapshot.is_empty() else "success"
        self.uiStateChanged.emit(state)
        self.loadingStateChanged.emit(False)

    def _on_load_failed(self, message: str):
        self._is_loading = False
        self.errorOccurred.emit(message)
        self.uiStateChanged.emit("error")
        self.loadingStateChanged.emit(False)

    @staticmethod
    def _status_kind(status: str) -> str:
        normalized = (status or "").upper()
        if "TRAT" in normalized:
            return "pass"
        if "ABER" in normalized:
            return "warning"
        if "ERRO" in normalized:
            return "fail"
        return "neutral"

    @staticmethod
    def _fmt_time(value: str) -> str:
        if not value:
            return "--:--"
        try:
            if "T" in value:
                return datetime.fromisoformat(value).strftime("%H:%M")
            return str(value)[:16]
        except Exception:
            return str(value)

    def shutdown(self):
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(2000)
