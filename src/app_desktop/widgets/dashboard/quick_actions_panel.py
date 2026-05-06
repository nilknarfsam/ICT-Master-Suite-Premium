from PyQt5.QtCore import pyqtSignal

from src.app_desktop.widgets.card import Card
from src.app_desktop.widgets.dashboard.section_title import SectionTitle
from src.app_desktop.widgets.primary_button import PrimaryButton


class QuickActionsPanel(Card):
    actionRequested = pyqtSignal(str)

    def __init__(self, is_admin: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("quickActionsPanel")
        self.content_layout.addWidget(SectionTitle("Acoes rapidas", "Atalhos operacionais"))

        self.btn_finder = PrimaryButton("Abrir Finder")
        self.btn_wiki = PrimaryButton("Abrir Wiki")
        self.btn_config = PrimaryButton("Abrir Configuracoes")
        self.btn_reindex = PrimaryButton("Reindexar logs")
        self.btn_reindex.setVisible(is_admin)
        self.btn_config.setVisible(is_admin)

        self.btn_finder.clicked.connect(lambda: self.actionRequested.emit("open_finder"))
        self.btn_wiki.clicked.connect(lambda: self.actionRequested.emit("open_wiki"))
        self.btn_config.clicked.connect(lambda: self.actionRequested.emit("open_config"))
        self.btn_reindex.clicked.connect(lambda: self.actionRequested.emit("reindex"))

        self.content_layout.addWidget(self.btn_finder)
        self.content_layout.addWidget(self.btn_wiki)
        self.content_layout.addWidget(self.btn_config)
        self.content_layout.addWidget(self.btn_reindex)
