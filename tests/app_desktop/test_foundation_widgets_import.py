"""Smoke tests dos widgets base da UI Premium.

Apenas valida que as classes podem ser importadas e que herdam dos
tipos PyQt5 esperados. Nao instancia widgets — evita dependencia de
display em ambientes headless.
"""

import pytest

pytest.importorskip("PyQt5")

from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QWidget  # noqa: E402

from src.app_desktop.layouts.master_detail_layout import MasterDetailLayout  # noqa: E402
from src.app_desktop.widgets.card import Card  # noqa: E402
from src.app_desktop.widgets.primary_button import PrimaryButton  # noqa: E402
from src.app_desktop.widgets.progress_overlay import ProgressOverlay  # noqa: E402
from src.app_desktop.widgets.status_badge import StatusBadge  # noqa: E402


def test_primary_button_subclass_qpushbutton():
    assert issubclass(PrimaryButton, QPushButton)


def test_card_subclass_qframe():
    assert issubclass(Card, QFrame)


def test_status_badge_subclass_qlabel():
    assert issubclass(StatusBadge, QLabel)


def test_progress_overlay_subclass_qwidget():
    assert issubclass(ProgressOverlay, QWidget)


def test_master_detail_layout_subclass_qwidget():
    assert issubclass(MasterDetailLayout, QWidget)
