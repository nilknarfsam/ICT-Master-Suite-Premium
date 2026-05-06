"""Card reutilizavel para agrupamento visual de conteudo.

Apenas estrutura (QFrame com `objectName="card"`) + `content_layout`
exposto para o consumidor adicionar widgets. Aparencia fica em
`themes/light.qss` (`QFrame#card`).
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout


class Card(QFrame):
    """Container visual com cantos arredondados e borda sutil."""

    def __init__(self, parent=None, hoverable: bool = False):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.NoFrame)
        if hoverable:
            self.setProperty("hoverable", "true")
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(12)
