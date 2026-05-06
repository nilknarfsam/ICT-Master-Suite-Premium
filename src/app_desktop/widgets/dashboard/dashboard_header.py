from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.primary_button import PrimaryButton


class DashboardHeader(Card):
    refreshClicked = pyqtSignal()

    def __init__(self, title: str = "Dashboard", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardHeader")
        self.content_layout.setSpacing(8)
        row = QHBoxLayout()
        text_col = QVBoxLayout()
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("dashboardHeaderTitle")
        self.lbl_subtitle = QLabel(subtitle)
        self.lbl_subtitle.setObjectName("dashboardHeaderSubtitle")
        text_col.addWidget(self.lbl_title)
        text_col.addWidget(self.lbl_subtitle)
        self.btn_refresh = PrimaryButton("Atualizar")
        self.btn_refresh.clicked.connect(self.refreshClicked.emit)
        row.addLayout(text_col)
        row.addStretch()
        row.addWidget(self.btn_refresh)
        self.content_layout.addLayout(row)

    def set_subtitle(self, subtitle: str):
        self.lbl_subtitle.setText(subtitle or "")
