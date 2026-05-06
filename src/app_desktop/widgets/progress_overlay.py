"""Overlay de progresso reutilizavel.

Cobre o widget pai com fundo translucido e mostra um cartao central
com mensagem + barra de progresso. Bloqueia cliques na area coberta.

Aparencia controlada por `themes/light.qss` via os objectName:
`progressOverlay`, `progressOverlayCard`, `progressOverlayMessage`,
`progressOverlayBar`.

API:
    overlay = ProgressOverlay(parent)
    overlay.show_with("Reindexando logs...")
    overlay.set_message("Concluindo...")
    overlay.hide()

Por padrao a barra opera em modo indeterminado (range 0,0). Para uso
determinado, basta `set_progress(value, maximum)`.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ProgressOverlay(QWidget):
    """Overlay translucido com cartao de progresso central."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("progressOverlay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.setAlignment(Qt.AlignCenter)

        self._card = QFrame(self)
        self._card.setObjectName("progressOverlayCard")
        self._card.setFrameShape(QFrame.NoFrame)

        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)

        self._message = QLabel("", self._card)
        self._message.setObjectName("progressOverlayMessage")
        self._message.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self._message)

        bar_row = QHBoxLayout()
        bar_row.setContentsMargins(0, 0, 0, 0)
        self._bar = QProgressBar(self._card)
        self._bar.setObjectName("progressOverlayBar")
        self._bar.setRange(0, 0)
        self._bar.setMinimumWidth(280)
        self._bar.setTextVisible(False)
        bar_row.addWidget(self._bar)
        card_layout.addLayout(bar_row)

        outer.addWidget(self._card)
        self.hide()

    def show_with(self, message: str = "") -> None:
        self.set_message(message)
        if isinstance(self.parent(), QWidget):
            self.resize(self.parent().size())
        self.raise_()
        self.show()

    def set_message(self, message: str) -> None:
        self._message.setText(message or "")

    def set_progress(self, value: int, maximum: int = 100) -> None:
        if maximum <= 0:
            self._bar.setRange(0, 0)
            return
        self._bar.setRange(0, maximum)
        self._bar.setValue(value)
        self._bar.setTextVisible(True)

    def set_indeterminate(self) -> None:
        self._bar.setRange(0, 0)
        self._bar.setTextVisible(False)

    def resizeEvent(self, event):  # noqa: N802 (Qt naming)
        super().resizeEvent(event)
        parent = self.parent()
        if isinstance(parent, QWidget):
            self.resize(parent.size())
