"""Snapshot imutavel do estado do dashboard.

Estrutura agregada produzida pelo `DashboardLoaderWorker` e consumida
pelo `DashboardViewModel`. Mantida como `dataclass(frozen=True)` para
garantir que widgets nao mutem o estado por engano.

Esta estrutura tambem e o futuro contrato IPC entre Python (Core) e
React/Electron na Fase 6 — manter campos estaveis e serializaveis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple


ActivityRow = Tuple[str, str, str, str]  # (data, serial, componente, status)
ComponentRow = Tuple[str, int]            # (componente, qtd)


@dataclass(frozen=True)
class DashboardSnapshot:
    """Estado consolidado do dashboard num instante."""

    total_hoje: int = 0
    abertos: int = 0
    tratados: int = 0
    top_componente: str = "N/A"
    top_5_componentes: List[ComponentRow] = field(default_factory=list)
    db_online: bool = False
    index_size: int = 0
    index_ready: bool = False
    recent_activity: List[ActivityRow] = field(default_factory=list)
    generated_at: str = ""

    @staticmethod
    def empty() -> "DashboardSnapshot":
        """Retorna snapshot vazio para estado inicial/erro."""
        return DashboardSnapshot(generated_at=datetime.now().isoformat())

    def is_empty(self) -> bool:
        """True quando nao ha sinal de dados validos.

        Util para decidir entre estado `empty` (sem DB e sem indice e sem
        atividade) e `success`/`error` no ViewModel.
        """
        return (
            not self.db_online
            and not self.index_ready
            and not self.recent_activity
            and self.total_hoje == 0
        )
