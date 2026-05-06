import pytest

pytest.importorskip("PyQt5")

from PyQt5.QtWidgets import QWidget  # noqa: E402

from src.app_desktop.pages.dashboard.dashboard_page import DashboardPage  # noqa: E402


def test_dashboard_page_is_qwidget():
    assert issubclass(DashboardPage, QWidget)
