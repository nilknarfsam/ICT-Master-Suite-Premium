from src.core.sync.offline_sync_service import (
    init_db_local,
    sincronizar_espelho_local,
    sincronizar_fila_offline,
)


class SyncApplicationService:
    """Serviço de aplicação para sincronização offline/background."""

    def sincronizar_fila_offline(self):
        return sincronizar_fila_offline()

    def sincronizar_espelho_local(self):
        return sincronizar_espelho_local()

    def init_db_local(self):
        return init_db_local()
