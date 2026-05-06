"""Badge de status reutilizavel.

Aparencia controlada por `themes/light.qss` via seletor de atributo
`QLabel[badge="<kind>"]`. Aceita os tipos: `pass`, `fail`, `warning`,
`info`, `neutral` (alinhados com `themes/tokens.STATUS_COLORS`).
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


_VALID_KINDS = ("pass", "fail", "warning", "info", "neutral")


class StatusBadge(QLabel):
    """QLabel exibido como pill/badge colorido conforme status."""

    def __init__(self, text: str = "", kind: str = "neutral", parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignCenter)
        self.set_status(kind)

    def set_status(self, kind: str) -> None:
        """Atualiza a propriedade `badge` e re-aplica QSS."""
        normalized = kind if kind in _VALID_KINDS else "neutral"
        self.setProperty("badge", normalized)
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        self.update()
