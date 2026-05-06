from PyQt5.QtWidgets import QLabel

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.dashboard.section_title import SectionTitle
from src.app_desktop.widgets.status_badge import StatusBadge


class SearchSummaryPanel(Card):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("searchSummaryPanel")
        self.title = SectionTitle("Resumo de busca/index", "Estado atual do indice")
        self.badge = StatusBadge("INDEX", "neutral")
        self.lbl_count = QLabel("Entradas no indice: 0")
        self.lbl_count.setProperty("role", "search-summary-metric")
        self.lbl_updated = QLabel("--:--")
        self.lbl_updated.setProperty("role", "search-summary-metric-value")
        self.content_layout.addWidget(self.title)
        self.content_layout.addWidget(self.badge)
        self.content_layout.addWidget(self.lbl_count)
        self.content_layout.addWidget(self.lbl_updated)

    def set_data(self, payload: dict):
        ready = bool(payload.get("index_ready", False))
        self.badge.set_status("pass" if ready else "warning")
        self.badge.setText("INDEX PRONTO" if ready else "INDEX INDISPONIVEL")
        self.lbl_count.setText(f"Entradas no indice: {int(payload.get('index_size', 0) or 0)}")
        self.lbl_updated.setText(payload.get("generated_at", "--:--"))
