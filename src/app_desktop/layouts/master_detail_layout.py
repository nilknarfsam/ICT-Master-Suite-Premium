"""Layout master/detail reutilizavel.

Expoe duas areas (`master_area` e `detail_area`) divididas por um
QSplitter horizontal. As areas sao QWidget vazios — o consumidor
adiciona seus proprios layouts/widgets.

Aparencia controlada por `themes/light.qss` via os objectName:
`masterDetailSplitter`, `masterArea`, `detailArea`.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QSplitter, QWidget


class MasterDetailLayout(QWidget):
    """Container com area mestre (esquerda) + detalhe (direita)."""

    def __init__(
        self,
        parent: QWidget = None,
        orientation: Qt.Orientation = Qt.Horizontal,
        master_initial_size: int = 320,
        detail_initial_size: int = 720,
    ):
        super().__init__(parent)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._splitter = QSplitter(orientation, self)
        self._splitter.setObjectName("masterDetailSplitter")
        self._splitter.setChildrenCollapsible(False)
        self._splitter.setHandleWidth(4)

        self.master_area = QWidget(self._splitter)
        self.master_area.setObjectName("masterArea")

        self.detail_area = QWidget(self._splitter)
        self.detail_area.setObjectName("detailArea")

        self._splitter.addWidget(self.master_area)
        self._splitter.addWidget(self.detail_area)
        self._splitter.setStretchFactor(0, 0)
        self._splitter.setStretchFactor(1, 1)
        self._splitter.setSizes([master_initial_size, detail_initial_size])

        outer.addWidget(self._splitter)

    def splitter(self) -> QSplitter:
        return self._splitter
