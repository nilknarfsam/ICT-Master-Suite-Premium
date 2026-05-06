from PyQt5.QtWidgets import QLabel, QProgressBar

from src.app_desktop.widgets.card import Card


class LoadingState(Card):
    def __init__(self, message: str = "Carregando...", parent=None):
        super().__init__(parent)
        self.setObjectName("loadingState")
        self.lbl = QLabel(message)
        self.lbl.setObjectName("loadingStateMessage")
        self.bar = QProgressBar()
        self.bar.setObjectName("loadingStateBar")
        self.bar.setRange(0, 0)
        self.bar.setTextVisible(False)
        self.content_layout.addWidget(self.lbl)
        self.content_layout.addWidget(self.bar)

    def set_message(self, message: str):
        self.lbl.setText(message or "Carregando...")
