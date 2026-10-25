"""Application-wide visual theme for SpectraSoft.

The theme keeps the analytical workspace bright and readable while using a
navy/slate shell and semantic accent colors for navigation, status, and charts.
Page modules may add object names or dynamic properties, but should not define
competing application palettes.
"""

from __future__ import annotations

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget


COLORS = {
    "canvas": "#f3f6fa",
    "surface": "#ffffff",
    "surface_alt": "#eef3f8",
    "shell": "#203047",
    "shell_alt": "#2d3d55",
    "shell_hover": "#38516e",
    "shell_text": "#f8fafc",
    "text": "#1f2937",
    "muted": "#64748b",
    "border": "#d7e0ea",
    "border_strong": "#b9c7d8",
    "teal": "#0f9f9a",
    "teal_dark": "#087f7b",
    "teal_soft": "#dff7f4",
    "blue": "#2563eb",
    "blue_soft": "#e8f0ff",
    "violet": "#7c3aed",
    "violet_soft": "#f0eaff",
    "magenta": "#db2777",
    "magenta_soft": "#fde8f2",
    "amber": "#c77700",
    "amber_soft": "#fff4d6",
    "green": "#16803c",
    "green_soft": "#e4f6e9",
    "red": "#c73535",
    "red_soft": "#fde8e8",
    "chart_blue": "#2563eb",
    "chart_teal": "#0f9f9a",
    "chart_violet": "#7c3aed",
    "chart_magenta": "#db2777",
    "chart_amber": "#d97706",
    "chart_green": "#16803c",
}


APPLICATION_STYLE = f"""
* {{
    font-family: "Sans Serif";
    font-size: 9pt;
    color: {COLORS['text']};
}}

QMainWindow, #mainWindow, #contentSurface {{
    background-color: {COLORS['canvas']};
    color: {COLORS['text']};
}}

#navigationRail {{
    background-color: {COLORS['shell']};
    color: {COLORS['shell_text']};
    border: none;
}}

QLabel#brandLabel, QLabel#navigationTitle, QLabel#shellContextLabel {{
    color: {COLORS['shell_text']};
    background: transparent;
    font-weight: 700;
}}

QMenuBar, QMenuBar#topMenuBar {{
    background-color: {COLORS['shell']};
    color: {COLORS['shell_text']};
    border: none;
    padding: 3px 8px;
}}

QMenuBar::item {{
    background: transparent;
    color: {COLORS['shell_text']};
    padding: 6px 10px;
    border-radius: 5px;
}}

QMenuBar::item:selected, QMenuBar::item:pressed {{
    background-color: {COLORS['shell_hover']};
}}

QMenu {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border_strong']};
    padding: 5px;
}}

QMenu::item {{
    padding: 7px 24px 7px 10px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['teal_soft']};
    color: {COLORS['teal_dark']};
}}

QStatusBar, QStatusBar#statusBar {{
    background-color: {COLORS['shell']};
    color: {COLORS['shell_text']};
    border-top: 1px solid {COLORS['shell_alt']};
    padding: 3px 8px;
}}

QStatusBar QLabel {{
    color: {COLORS['shell_text']};
    background: transparent;
}}

#pageSurface {{
    background-color: {COLORS['canvas']};
}}

QLabel#pageHeader {{
    background-color: {COLORS['shell_alt']};
    color: {COLORS['shell_text']};
    font-size: 11pt;
    font-weight: 700;
    padding: 9px 14px;
    border: none;
}}

QLabel#sectionTitle {{
    background-color: {COLORS['surface']};
    color: {COLORS['shell']};
    font-size: 10pt;
    font-weight: 700;
    padding: 8px 10px;
    border: 1px solid {COLORS['border']};
    border-bottom: 2px solid {COLORS['teal']};
    border-radius: 6px 6px 0 0;
}}

#contentCard, QGroupBox {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    margin-top: 12px;
    padding: 12px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: {COLORS['shell']};
    font-weight: 700;
    background-color: {COLORS['surface']};
}}

QLabel#mutedLabel, QLabel#infoLabel, QLabel#selectionHint {{
    color: {COLORS['muted']};
    background: transparent;
}}

QLabel#warningLabel {{
    color: {COLORS['amber']};
    background-color: {COLORS['amber_soft']};
    border: 1px solid #f3d18a;
    border-radius: 5px;
    padding: 7px 9px;
}}

QLabel#errorLabel {{
    color: {COLORS['red']};
    background-color: {COLORS['red_soft']};
    border: 1px solid #efb7b7;
    border-radius: 5px;
    padding: 7px 9px;
}}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit,
QPlainTextEdit, QTextEdit {{
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border_strong']};
    border-radius: 5px;
    padding: 6px 8px;
    selection-background-color: {COLORS['teal']};
    selection-color: white;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus,
QPlainTextEdit:focus, QTextEdit:focus {{
    border: 2px solid {COLORS['teal']};
    padding: 5px 7px;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QPushButton {{
    background-color: {COLORS['surface']};
    color: {COLORS['shell']};
    border: 1px solid {COLORS['border_strong']};
    border-radius: 5px;
    padding: 7px 13px;
    min-height: 16px;
}}

QPushButton:hover {{
    background-color: {COLORS['surface_alt']};
    border-color: {COLORS['teal']};
}}

QPushButton:pressed {{
    background-color: {COLORS['teal_soft']};
}}

QPushButton:disabled {{
    background-color: {COLORS['surface_alt']};
    color: #9aa8b8;
    border-color: {COLORS['border']};
}}

QPushButton#primaryButton {{
    background-color: {COLORS['teal']};
    color: white;
    border-color: {COLORS['teal_dark']};
    font-weight: 700;
}}

QPushButton#primaryButton:hover {{
    background-color: {COLORS['teal_dark']};
}}

QPushButton#secondaryButton {{
    background-color: {COLORS['surface']};
    color: {COLORS['shell']};
}}

QPushButton#dangerButton {{
    background-color: {COLORS['red_soft']};
    color: {COLORS['red']};
    border-color: #efb7b7;
}}

QListWidget, QTreeWidget, QTableWidget, QTableView {{
    background-color: {COLORS['surface']};
    alternate-background-color: #f8fafc;
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['teal_soft']};
    selection-color: {COLORS['teal_dark']};
    border-radius: 5px;
}}

QHeaderView::section {{
    background-color: {COLORS['shell_alt']};
    color: {COLORS['shell_text']};
    border: none;
    border-right: 1px solid #455975;
    border-bottom: 1px solid #455975;
    padding: 7px 8px;
    font-weight: 700;
}}

QListWidget::item, QTreeWidget::item {{
    padding: 7px 8px;
    border-radius: 4px;
}}

QListWidget#groupList::item:selected, QListWidget::item:selected {{
    background-color: {COLORS['teal']};
    color: white;
}}

#navigationRail QLineEdit {{
    background-color: {COLORS['shell_alt']};
    color: {COLORS['shell_text']};
    border-color: #526782;
}}

#navigationRail QPushButton {{
    background-color: transparent;
    color: {COLORS['shell_text']};
    border-color: transparent;
    text-align: left;
}}

#navigationRail QPushButton:hover {{
    background-color: {COLORS['shell_hover']};
    border-color: {COLORS['shell_hover']};
}}

#navigationRail QPushButton#primaryButton {{
    background-color: {COLORS['teal']};
    color: white;
}}

QScrollArea {{
    background-color: transparent;
    border: none;
}}

QTabWidget::pane {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 5px;
}}

QTabBar::tab {{
    background-color: {COLORS['surface_alt']};
    color: {COLORS['muted']};
    border: 1px solid {COLORS['border']};
    padding: 7px 12px;
    margin-right: 3px;
    border-radius: 5px 5px 0 0;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['surface']};
    color: {COLORS['teal_dark']};
    border-bottom-color: {COLORS['surface']};
    font-weight: 700;
}}

QToolTip {{
    background-color: {COLORS['shell']};
    color: white;
    border: 1px solid {COLORS['shell_alt']};
    padding: 5px 7px;
}}

QProgressBar {{
    background-color: {COLORS['surface_alt']};
    border: 1px solid {COLORS['border']};
    border-radius: 5px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['teal']};
    border-radius: 4px;
}}

#chartSurface {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
}}

QLabel[chartSeries="blue"] {{ color: {COLORS['chart_blue']}; }}
QLabel[chartSeries="teal"] {{ color: {COLORS['chart_teal']}; }}
QLabel[chartSeries="violet"] {{ color: {COLORS['chart_violet']}; }}
QLabel[chartSeries="magenta"] {{ color: {COLORS['chart_magenta']}; }}
QLabel[chartSeries="amber"] {{ color: {COLORS['chart_amber']}; }}
QLabel[chartSeries="green"] {{ color: {COLORS['chart_green']}; }}
"""


def primary_button_style() -> str:
    """Return the shared primary-action style for legacy page helpers."""

    return f"""
        QPushButton {{
            background-color: {COLORS['teal']};
            color: white;
            border: 1px solid {COLORS['teal_dark']};
            border-radius: 5px;
            padding: 7px 13px;
            font-weight: 700;
        }}
        QPushButton:hover {{ background-color: {COLORS['teal_dark']}; }}
    """


def secondary_button_style() -> str:
    """Return the shared secondary-action style for legacy page helpers."""

    return f"""
        QPushButton {{
            background-color: {COLORS['surface']};
            color: {COLORS['shell']};
            border: 1px solid {COLORS['border_strong']};
            border-radius: 5px;
            padding: 7px 13px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['surface_alt']};
            border-color: {COLORS['teal']};
        }}
    """


def page_header_style() -> str:
    """Return the shared page header style for legacy page title labels."""

    return f"""
        background-color: {COLORS['shell_alt']};
        color: {COLORS['shell_text']};
        font-size: 11pt;
        font-weight: 700;
        padding: 9px 14px;
    """


def apply_theme(app: QApplication) -> None:
    """Apply the application-wide stylesheet and platform-neutral font."""

    app.setStyleSheet(APPLICATION_STYLE)
    app.setFont(QFont("Sans Serif", 9))


def harmonize_widget_tree(root: QWidget) -> None:
    """Bring legacy page-local visual overrides into the shared theme.

    Existing pages contain many inline styles from the original desktop
    palette. This function changes only those visual declarations after a page
    is constructed; it does not touch widget values, signals, layouts, or
    domain behavior.
    """

    replacements = {
        "#d4d0c8": COLORS["canvas"],
        "#c0b8a8": COLORS["shell"],
        "#5c9bd5": COLORS["shell_alt"],
        "#0078d7": COLORS["teal"],
        "#888888": COLORS["border_strong"],
        "#aaaaaa": COLORS["border"],
        "#999999": COLORS["border_strong"],
        "#777777": COLORS["muted"],
        "#666666": COLORS["muted"],
        "#555555": COLORS["text"],
        "#000000": COLORS["text"],
        "#cce5ff": COLORS["teal_soft"],
        "#f0ece4": COLORS["surface_alt"],
        "#e8e8e8": COLORS["surface_alt"],
        "Arial": "Sans Serif",
        "outset": "solid",
        "inset": "solid",
    }

    if not root.objectName():
        root.setObjectName("pageSurface")

    for widget in (root, *root.findChildren(QWidget)):
        widget.setAutoFillBackground(False)
        if isinstance(widget, QPushButton):
            text = widget.text().lower()
            if any(token in text for token in ("delete", "cancel", "retire")):
                widget.setObjectName("dangerButton" if "delete" in text or "retire" in text else "secondaryButton")
            elif any(
                token in text
                for token in (
                    "save", "ok", "apply", "run", "next", "add", "create",
                    "export", "import", "activate", "record", "verify",
                )
            ):
                widget.setObjectName("primaryButton")
            else:
                widget.setObjectName("secondaryButton")
            if widget.objectName() == "primaryButton":
                widget.setStyleSheet(primary_button_style())
            elif widget.objectName() == "dangerButton":
                widget.setStyleSheet(
                    f"QPushButton {{ background-color: {COLORS['red_soft']}; "
                    f"color: {COLORS['red']}; border: 1px solid #efb7b7; "
                    "border-radius: 5px; padding: 7px 13px; }}"
                )
            else:
                widget.setStyleSheet(secondary_button_style())
            continue

        stylesheet = widget.styleSheet()
        if not stylesheet:
            continue
        for old, new in replacements.items():
            stylesheet = stylesheet.replace(old, new)
        widget.setStyleSheet(stylesheet)
