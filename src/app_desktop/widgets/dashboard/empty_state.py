from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.primary_button import PrimaryButton


class EmptyState(Card):
    actionClicked = pyqtSignal()

    def __init__(self, title: str = "", message: str = "", action_label: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("emptyState")
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("emptyStateTitle")
        self.lbl_message = QLabel(message)
        self.lbl_message.setObjectName("emptyStateMessage")
        self.btn_action = PrimaryButton(action_label)
        self.btn_action.clicked.connect(self.actionClicked.emit)
        self.btn_action.setVisible(bool(action_label))
        self.content_layout.addWidget(self.lbl_title)
        self.content_layout.addWidget(self.lbl_message)
        self.content_layout.addWidget(self.btn_action)

    def configure(self, title: str, message: str, action_label: str = ""):
        self.lbl_title.setText(title or "")
        self.lbl_message.setText(message or "")
        self.btn_action.setText(action_label or "")
        self.btn_action.setVisible(bool(action_label))
