"""Botao primario reutilizavel da UI Premium.

Define apenas um seletor semantico (`role="primary"`); a aparencia
fica em `themes/light.qss` (`QPushButton[role="primary"]`).
"""

from PyQt5.QtWidgets import QPushButton


class PrimaryButton(QPushButton):
    """QPushButton com papel semantico de acao primaria."""

    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setProperty("role", "primary")
        self.setCursor(self.cursor())
