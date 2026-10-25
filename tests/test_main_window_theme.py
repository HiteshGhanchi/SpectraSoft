import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


def test_main_window_is_resizable_and_uses_themed_shell():
    from ui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    assert not window.isMinimized()
    assert window.minimumSize().width() >= 1200
    assert window.minimumSize().height() >= 720
    assert window.objectName() == "mainWindow"
    assert window.menuBar().objectName() == "topMenuBar"
    assert window.statusBar().objectName() == "statusBar"
    assert window._group_panel.objectName() == "navigationRail"
    assert window._group_panel.testAttribute(Qt.WidgetAttribute.WA_StyledBackground)
    assert window._right.objectName() == "contentSurface"
    assert not window._group_panel.isHidden()


def test_main_window_content_layout_has_expanding_right_panel():
    from ui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    assert window._right.sizePolicy().horizontalPolicy().name == "Expanding"
    assert window._right_layout.count() == 1
    assert window._right_layout.itemAt(0).widget() is not None
