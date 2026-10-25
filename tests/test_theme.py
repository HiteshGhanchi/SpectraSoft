import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication


def test_application_style_contains_light_shell_and_graph_palette():
    from ui.theme import APPLICATION_STYLE, COLORS

    assert COLORS["canvas"] in APPLICATION_STYLE
    assert COLORS["surface"] in APPLICATION_STYLE
    assert COLORS["shell"] in APPLICATION_STYLE
    assert COLORS["teal"] in APPLICATION_STYLE
    assert COLORS["chart_blue"] in APPLICATION_STYLE
    assert COLORS["chart_violet"] in APPLICATION_STYLE
    assert COLORS["chart_amber"] in APPLICATION_STYLE
    assert "border-radius" in APPLICATION_STYLE
    assert "outset" not in APPLICATION_STYLE
    assert "inset" not in APPLICATION_STYLE
    assert "#d4d0c8" not in APPLICATION_STYLE.lower()


def test_apply_theme_installs_stylesheet_and_platform_font():
    from ui.theme import apply_theme

    app = QApplication.instance() or QApplication([])
    apply_theme(app)

    assert app.styleSheet()
    assert app.font().family() == "Sans Serif"
    assert app.font().pointSize() == 9
