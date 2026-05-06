from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.dashboard.section_title import SectionTitle


class RecentActivityPanel(Card):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("recentActivityPanel")
        self.title = SectionTitle("Atividade recente", "Ultimas analises")
        self.table = QTableWidget(0, 4)
        self.table.setObjectName("recentActivityTable")
        self.table.setHorizontalHeaderLabels(["Data", "Serial", "Componente", "Status"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.content_layout.addWidget(self.title)
        self.content_layout.addWidget(self.table)

    def set_items(self, rows):
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(0)
        for row_data in rows or []:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data.get("data", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(row_data.get("serial", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data.get("componente", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(row_data.get("status", ""))))
        self.table.setUpdatesEnabled(True)
