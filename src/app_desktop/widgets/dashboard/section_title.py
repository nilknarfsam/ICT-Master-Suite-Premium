from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class SectionTitle(QWidget):
    def __init__(self, text: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.title = QLabel(text)
        self.title.setObjectName("sectionTitleText")
        self.subtitle = QLabel(subtitle)
        self.subtitle.setObjectName("sectionTitleSubtitle")
        self.subtitle.setVisible(bool(subtitle))
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

    def set_subtitle(self, subtitle: str):
        self.subtitle.setText(subtitle or "")
        self.subtitle.setVisible(bool(subtitle))
