"""Worker assincrono para carregamento de dados do dashboard.

Vive em uma `QThread` propria movida pelo `DashboardViewModel`. Faz as
chamadas a `LogAnalysisService` e `LogIndexApplicationService` em
background e emite um snapshot agregado (sucesso) ou mensagem de erro
(falha) — UI nunca toca services diretamente.

Foi colocado em `viewmodels/dashboard/` (em vez de
`src/app_desktop/threads.py`) para preservar 100 por cento o contrato
publico do `threads.py`. Ver guideline em
`docs/PHASE_4_2_DASHBOARD_PREMIUM_PLAN.md`.
"""

from datetime import datetime
from typing import Any, List

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from src.app_desktop.viewmodels.dashboard.dashboard_snapshot import DashboardSnapshot


class DashboardLoaderWorker(QObject):
    """Carrega o snapshot do dashboard em thread propria.

    Sinais:
        snapshotReady(DashboardSnapshot): emitido em sucesso.
        loadFailed(str): emitido quando uma excecao impede a montagem
            do snapshot (raro — chamadas individuais sao protegidas).
    """

    snapshotReady = pyqtSignal(object)
    loadFailed = pyqtSignal(str)

    def __init__(
        self,
        log_analysis_service: Any,
        log_index_service: Any,
        recent_limit: int = 10,
        parent=None,
    ):
        super().__init__(parent)
        self._log_analysis = log_analysis_service
        self._log_index = log_index_service
        self._recent_limit = recent_limit

    @pyqtSlot()
    def start_load(self) -> None:
        """Slot disparado via `QMetaObject.invokeMethod(...)`.

        Cada chamada a service e independente: falha em uma nao impede
        a montagem do restante. Apenas falha global (excecao no
        construtor do snapshot, etc.) emite `loadFailed`.
        """
        try:
            stats = self._safe_call(self._log_analysis.get_ict_statistics, default={})
            progress = self._safe_call(
                self._log_analysis.get_progress_statistics, default={}
            )
            recent = self._safe_call(
                self._log_analysis.get_latest_analyses,
                self._recent_limit,
                default=[],
            )
            index_ready = self._safe_call(
                self._log_index.is_index_available, default=False
            )
            index_size = self._safe_call(self._log_index.count_entries, default=0)

            top_5: List = list(stats.get("top_5_componentes", []) or [])
            recent_normalized = [tuple(item) for item in (recent or [])]

            snapshot = DashboardSnapshot(
                total_hoje=int(stats.get("total_hoje", 0) or 0),
                abertos=int(progress.get("abertos", 0) or 0),
                tratados=int(progress.get("tratados", 0) or 0),
                top_componente=str(stats.get("top_componente", "N/A") or "N/A"),
                top_5_componentes=top_5,
                db_online=bool(stats.get("db_online", False)),
                index_size=int(index_size or 0),
                index_ready=bool(index_ready),
                recent_activity=recent_normalized,
                generated_at=datetime.now().isoformat(timespec="seconds"),
            )
            self.snapshotReady.emit(snapshot)
        except Exception as exc:  # noqa: BLE001
            self.loadFailed.emit(f"{type(exc).__name__}: {exc}")

    @staticmethod
    def _safe_call(fn, *args, default=None, **kwargs):
        """Chama `fn` capturando excecoes; retorna `default` em erro.

        Util para nao deixar uma falha pontual (ex.: DB offline)
        impedir a montagem do snapshot inteiro.
        """
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            print(f"DashboardLoaderWorker._safe_call falhou em {getattr(fn, '__name__', fn)}: {exc}")
            return default
