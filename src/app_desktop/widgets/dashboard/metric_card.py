from PyQt5.QtWidgets import QLabel

from src.app_desktop.widgets.card import Card


class MetricCard(Card):
    def __init__(self, title: str, value: str = "0", caption: str = "", tone: str = "neutral", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setProperty("tone", tone)
        self.lbl_title = QLabel(title)
        self.lbl_title.setProperty("role", "metric-title")
        self.lbl_value = QLabel(str(value))
        self.lbl_value.setProperty("role", "metric-value")
        self.lbl_caption = QLabel(caption)
        self.lbl_caption.setProperty("role", "metric-caption")
        self.lbl_caption.setVisible(bool(caption))
        self.content_layout.addWidget(self.lbl_title)
        self.content_layout.addWidget(self.lbl_value)
        self.content_layout.addWidget(self.lbl_caption)

    def set_value(self, value):
        self.lbl_value.setText(str(value))

    def set_caption(self, caption: str):
        self.lbl_caption.setText(caption or "")
        self.lbl_caption.setVisible(bool(caption))
