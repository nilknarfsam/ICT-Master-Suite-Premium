from PyQt5.QtWidgets import QLabel

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.status_badge import StatusBadge


class StatusCard(Card):
    def __init__(self, title: str, description: str = "", kind: str = "neutral", parent=None):
        super().__init__(parent)
        self.setObjectName("statusCard")
        self.lbl_title = QLabel(title)
        self.lbl_title.setProperty("role", "status-card-title")
        self.badge = StatusBadge(kind=kind)
        self.lbl_description = QLabel(description)
        self.lbl_description.setProperty("role", "status-card-description")
        self.content_layout.addWidget(self.lbl_title)
        self.content_layout.addWidget(self.badge)
        self.content_layout.addWidget(self.lbl_description)

    def set_status(self, kind: str, description: str):
        self.badge.set_status(kind)
        self.badge.setText(kind.upper())
        self.lbl_description.setText(description or "")
