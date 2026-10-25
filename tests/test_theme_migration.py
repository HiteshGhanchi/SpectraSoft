import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QVBoxLayout


def _widgets(root):
    return [root, *root.findChildren(QWidget)]


def test_harmonize_widget_tree_removes_legacy_visual_overrides():
    from ui.theme import COLORS, apply_theme, harmonize_widget_tree

    app = QApplication.instance() or QApplication([])
    apply_theme(app)
    root = QWidget()
    root.setStyleSheet("background:#d4d0c8;")
    layout = QVBoxLayout(root)
    button = QPushButton("Save")
    button.setStyleSheet(
        "background:#d4d0c8;color:#000000;border:2px outset #aaaaaa;"
    )
    layout.addWidget(button)

    harmonize_widget_tree(root)

    assert root.objectName() == "pageSurface"
    assert COLORS["canvas"] in root.styleSheet()
    assert COLORS["teal"] in button.styleSheet()
    assert button.objectName() == "primaryButton"
    assert "outset" not in root.styleSheet()


def test_theme_targets_custom_widget_object_names_and_primary_actions():
    from ui.theme import APPLICATION_STYLE, COLORS, apply_theme, harmonize_widget_tree

    app = QApplication.instance() or QApplication([])
    apply_theme(app)
    root = QWidget()
    layout = QVBoxLayout(root)
    button = QPushButton("Save")
    button.setStyleSheet("background:#d4d0c8;color:white;border:2px outset #aaaaaa;")
    layout.addWidget(button)

    harmonize_widget_tree(root)

    assert "#navigationRail" in APPLICATION_STYLE
    assert "#pageSurface" in APPLICATION_STYLE
    assert "#chartSurface" in APPLICATION_STYLE
    assert button.objectName() == "primaryButton"
    assert COLORS["teal"] in button.styleSheet()
    assert "outset" not in button.styleSheet()


def test_main_window_migrates_active_page_surface_and_maintenance_controls():
    from ui.main_window import MainWindow
    from ui.theme import apply_theme

    app = QApplication.instance() or QApplication([])
    apply_theme(app)
    window = MainWindow()
    window._open_maintenance()

    assert window._active_right_widget.objectName() == "pageSurface"
    for widget in _widgets(window._active_right_widget):
        assert "#d4d0c8" not in widget.styleSheet().lower()
        assert "outset" not in widget.styleSheet().lower()
        assert "inset" not in widget.styleSheet().lower()


def test_chart_widgets_use_light_surface_and_accent_colors():
    from ui.adjustment.adjustment_graph import AdjustmentGraphWidget
    from ui.regression.working_curve_chart import WorkingCurveChart
    from ui.theme import COLORS, apply_theme

    app = QApplication.instance() or QApplication([])
    apply_theme(app)

    adjustment = AdjustmentGraphWidget()
    working_curve = WorkingCurveChart()

    assert adjustment.objectName() == "chartSurface"
    assert working_curve.objectName() == "chartSurface"
    assert COLORS["surface"] in adjustment.styleSheet()
    assert COLORS["border_strong"] in adjustment.styleSheet()
    assert COLORS["surface"] in working_curve.styleSheet()
    assert COLORS["border_strong"] in working_curve.styleSheet()
