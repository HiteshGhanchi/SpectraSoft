import os
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication, QHeaderView, QSizePolicy


def _empty_session():
    session = Mock()
    session.query.return_value.order_by.return_value.all.return_value = []
    return session


def test_master_elements_uses_full_width_responsive_table_and_bottom_actions():
    from ui.settings.master_elements_page import MasterElementsPage

    app = QApplication.instance() or QApplication([])
    with patch(
        "ui.settings.master_elements_page.get_session",
        return_value=_empty_session(),
    ):
        page = MasterElementsPage(Mock())

    assert page.table_frame.sizePolicy().horizontalPolicy() == QSizePolicy.Policy.Expanding
    assert page.table_frame.sizePolicy().verticalPolicy() == QSizePolicy.Policy.Expanding
    header = page.table.horizontalHeader()
    assert header.sectionResizeMode(1) == QHeaderView.ResizeMode.Stretch
    assert header.sectionResizeMode(2) == QHeaderView.ResizeMode.Stretch
    assert page.content_layout.indexOf(page.table_frame) < page.content_layout.indexOf(page.button_row)
