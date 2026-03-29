"""
SpectraSoft — Main Window
Layout: group list always visible on left, page content on right.
Matches old PDAWin layout exactly.
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
        self.setWindowTitle("Analytical Information  [Password-Locked]")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        self._hw_connected = False
        self._build_menu()
        self._build_body()
        self._build_status_bar()

        # Hardware poll every 3s
        self._hw_timer = QTimer()
        self._hw_timer.timeout.connect(self._check_hardware)
        self._hw_timer.start(3000)
        self._check_hardware()

        # Clock every second
        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)
        self._update_clock()

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------

    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            f"QMenuBar{{background:{BG};color:black;}}"
            "QMenuBar::item{background:#d4d0c8;color:black;padding:3px 8px;}"
            "QMenuBar::item:selected{background:#0078d7;color:white;}"
            f"QMenu{{background:{BG};color:black;}}"
            "QMenu::item:selected{background:#0078d7;color:white;}"
        )

        def menu(name):
            return mb.addMenu(name)

        def act(m, label, slot):
            a = QAction(label, self)
            a.triggered.connect(slot)
            m.addAction(a)
            return a

        file_m = menu("File(F)")
        act(file_m, "Exit", self.close)

        menu("Edit(E)").setEnabled(False)
        menu("Display(V)").setEnabled(False)

        ana_m = menu("Analysis(A)")
        self._ana_actions = [
            act(ana_m, "Concentration Analysis", self._open_analysis),
            act(ana_m, "Recalibration Analysis", self._stub),
            act(ana_m, "Master Curve Analysis",  self._stub),
            act(ana_m, "Intensity Analysis",      self._stub),
        ]

        prep_m = menu("Prepare(P)")
        act(prep_m, "Manual Scan",           self._stub)
        act(prep_m, "Attenuator Adjustment", self._stub)

        inf_m = menu("Inf.(I)")
        act(inf_m, "Analytical Information", self._show_home)
        inf_m.addSeparator()
        act(inf_m, "Global Calibration Info", self._stub)

        menu("Result Manager(R)").setEnabled(False)
        menu("Maintenance(M)").setEnabled(False)

        help_m = menu("Help(H)")
        act(help_m, f"About {APP_NAME}", self._about)

    # ------------------------------------------------------------------
    # Body — left panel always visible, right panel changes
    # ------------------------------------------------------------------

    def _build_body(self):
        root = QWidget()
        root.setStyleSheet(f"background:{BG};")
        self.setCentralWidget(root)

        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        # ── Permanent left panel (group list) ─────────────────────────
        from ui.anainf.group_panel import GroupPanel
        self._group_panel = GroupPanel(self)
        self._group_panel.setFixedWidth(210)
        h.addWidget(self._group_panel)

        # Thin vertical divider
        div = QFrame()
        div.setFrameShape(QFrame.Shape.VLine)
        div.setFrameShadow(QFrame.Shadow.Sunken)
        div.setStyleSheet("color:#aaa;")
        h.addWidget(div)

        # ── Right content area ────────────────────────────────────────
        self._right = QWidget()
        self._right.setStyleSheet(f"background:{BG};")
        right_layout = QVBoxLayout(self._right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        self._right_layout = right_layout
        h.addWidget(self._right, stretch=1)

        # Default: show empty right panel with instruction
        self._show_home_content()

    def set_right_widget(self, widget):
        """Replace the right panel content."""
        # Remove existing widgets from right layout
        while self._right_layout.count():
            item = self._right_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._right_layout.addWidget(widget)

    def _show_home_content(self):
        """Show the default right panel (empty grey, just a hint)."""
        w = QWidget()
        w.setStyleSheet(f"background:{BG};")
        v = QVBoxLayout(w)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint = QLabel("Select a group and click  1:Select")
        hint.setStyleSheet("color:#666;font:9pt Arial;")
        v.addWidget(hint)
        self.set_right_widget(w)

    # ------------------------------------------------------------------
    # Status bar
    # ------------------------------------------------------------------

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
        for a in self._ana_actions:
            a.setEnabled(connected or SIMULATION_MODE)
        if connected:
            self._hw_label.setText("  ● Hardware connected")
            self._hw_label.setStyleSheet("color:green;font-weight:bold;")
        elif SIMULATION_MODE:
            self._hw_label.setText("  ○ Hardware not connected  (Simulation mode ON)")
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

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _show_home(self):
        self._show_home_content()

    def _open_analysis(self):
        QMessageBox.information(self, "Coming soon",
            "Analysis module will be available once hardware is ready.")

    def _stub(self):
        QMessageBox.information(self, "Coming soon",
            "This feature will be available in the next release.")

    def _about(self):
        QMessageBox.about(self, f"About {APP_NAME}",
            f"<b>{APP_NAME}</b> v{APP_VERSION}<br><br>"
            "Optical Emission Spectrometer Control Software")