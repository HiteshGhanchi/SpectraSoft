import os
from unittest.mock import Mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication


def test_workflow_guide_explains_inputs_flow_and_hardware_identifiers():
    from ui.help.workflow_guide_page import WorkflowGuidePage

    app = QApplication.instance() or QApplication([])
    page = WorkflowGuidePage(Mock())

    text = page.content.toPlainText()
    assert page.objectName() == "pageSurface"
    assert "Working flow" in text
    assert "Input parameters" in text
    assert "AR-No." in text
    assert "ITG" in text
    assert "Element name" in text
    assert "ITG number is used for physical channel selection" in text
    assert "AR-No. is not sent to the spectrometer" in text


def test_main_window_exposes_workflow_guide_action():
    from ui.main_window import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    assert window.action_workflow_guide.text() == "Workflow Guide"
    window._open_workflow_guide()
    assert window._active_right_widget.objectName() == "pageSurface"
