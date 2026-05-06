from PyQt5.QtWidgets import QGridLayout, QWidget


class DashboardGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setHorizontalSpacing(12)
        self._layout.setVerticalSpacing(12)

    def add_row(self, *widgets):
        self._rows.append(list(widgets))
        self._apply_breakpoint(self.width() or 1200)

    def _clear_layout(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(self)

    def _apply_breakpoint(self, width: int):
        self._clear_layout()
        if width >= 1200:
            cols = 4
        elif width >= 800:
            cols = 2
        else:
            cols = 1
        row_idx = 0
        for row in self._rows:
            col_idx = 0
            for widget in row:
                self._layout.addWidget(widget, row_idx, col_idx, 1, 1)
                col_idx += 1
                if col_idx >= cols:
                    row_idx += 1
                    col_idx = 0
            row_idx += 1

    def resizeEvent(self, event):  # noqa: N802
        super().resizeEvent(event)
        self._apply_breakpoint(self.width())
