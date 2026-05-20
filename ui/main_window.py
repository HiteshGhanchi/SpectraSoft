"""
SpectraSoft — Main Window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStatusBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QAction, QColor

from constants import APP_NAME, APP_VERSION, SIMULATION_MODE

BG = "#d4d0c8"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analytical Information")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        self._hw_connected = False
        self._build_menu()
        self._build_body()
        self._build_status_bar()

        self._hw_timer = QTimer()
        self._hw_timer.timeout.connect(self._check_hardware)
        self._hw_timer.start(3000)
        self._check_hardware()

        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)
        self._update_clock()

    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            f"QMenuBar{{background:{BG};color:black;}}"
            "QMenuBar::item{background:#d4d0c8;color:black;padding:3px 8px;}"
            "QMenuBar::item:selected{background:#0078d7;color:white;}"
            f"QMenu{{background:{BG};color:black;}}"
            "QMenu::item:selected{background:#0078d7;color:white;}"
        )

        self._ana_actions = []

        # Settings menu
        settings_m = mb.addMenu("Settings")
        sc_action = QAction("Source Codes", self)
        sc_action.triggered.connect(self._open_source_codes)
        settings_m.addAction(sc_action)

    def _build_body(self):
        root = QWidget()
        root.setStyleSheet(f"background:{BG};")
        self.setCentralWidget(root)

        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        from ui.anainf.group_panel import GroupPanel
        self._group_panel = GroupPanel(self)
        self._group_panel.setFixedWidth(210)
        h.addWidget(self._group_panel)

        self._div = QFrame()
        self._div.setFrameShape(QFrame.Shape.VLine)
        self._div.setFrameShadow(QFrame.Shadow.Sunken)
        self._div.setStyleSheet("color:#aaa;")
        h.addWidget(self._div)

        self._right = QWidget()
        self._right.setStyleSheet(f"background:{BG};")
        right_layout = QVBoxLayout(self._right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        self._right_layout = right_layout
        h.addWidget(self._right, stretch=1)

        self._show_home_content()

    def set_right_widget(self, widget):
        while self._right_layout.count():
            item = self._right_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._right_layout.addWidget(widget)

    def set_left_panel_visible(self, visible: bool):
        self._group_panel.setVisible(visible)
        self._div.setVisible(visible)

    def _show_home_content(self):
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint = QLabel("Select a group and double-click to open")
        hint.setStyleSheet("color:#666;font:9pt Arial;")
        v.addWidget(hint)
        self.set_right_widget(w)

    def _build_status_bar(self):
        sb = QStatusBar()
        sb.setStyleSheet(f"background:{BG};color:black;")
        self.setStatusBar(sb)

        self._hw_label = QLabel()
        self._hw_label.setStyleSheet("color:black;")
        sb.addWidget(self._hw_label)

        self._clock_label = QLabel()
        self._clock_label.setStyleSheet("color:black;")
        sb.addPermanentWidget(self._clock_label)

        self._set_hw_status(False)

    def _set_hw_status(self, connected: bool):
        self._hw_connected = connected
        if connected:
            self._hw_label.setText("  ● Hardware connected")
            self._hw_label.setStyleSheet("color:green;font-weight:bold;")
        elif SIMULATION_MODE:
            self._hw_label.setText("  ○ Simulation mode ON")
            self._hw_label.setStyleSheet("color:#555;")
        else:
            self._hw_label.setText("  ○ Hardware not connected — plug in USB")
            self._hw_label.setStyleSheet("color:#cc0000;font-weight:bold;")

    def _update_clock(self):
        self._clock_label.setText(
            QDateTime.currentDateTime().toString("dd-MM-yyyy   hh:mm")
        )

    def _check_hardware(self):
        if SIMULATION_MODE:
            return
        try:
            from core.hardware import hw
            connected = hw.detect_port()
            if connected != self._hw_connected:
                self._set_hw_status(connected)
        except Exception:
            if self._hw_connected:
                self._set_hw_status(False)

    def _open_source_codes(self):
        from ui.settings.source_codes_page import SourceCodesPage
        self.set_right_widget(SourceCodesPage(self))

    def _show_home(self):
        self._show_home_content()