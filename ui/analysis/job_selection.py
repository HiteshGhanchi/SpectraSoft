"""
SpectraSoft — Job Selection Menu

Displays F1-F10 menu for selecting analysis jobs.
Clicking a job opens the Analysis Run page with that job selected.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class JobSelectionPage(QWidget):
    """F1-F10 job selection menu."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._update_hv_button()  # Sync HV status on load

    # =========================================================================
    # UI Construction
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar with HV Button ──────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("background:#5c9bd5;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)

        title_label = QLabel("Job Selection")
        title_label.setStyleSheet("color:white;font:bold 10pt Arial;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        self.hv_btn = QPushButton("HV: OFF")
        self.hv_btn.setStyleSheet(
            "QPushButton{"
            "background:#dc3545;"
            "color:white;"
            "border:2px outset #888888;"
            "font:9pt Arial;"
            "padding:2px 8px;"
            "}"
        )
        self.hv_btn.setFixedWidth(80)
        self.hv_btn.clicked.connect(self._toggle_hv)
        title_layout.addWidget(self.hv_btn)

        root.addWidget(title_bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(20, 20, 20, 20)

        # ── Info Text ────────────────────────────────────────────────────
        info = QLabel("Select a job to run. Press the corresponding key or click the button.")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#666666;"
            "font:9pt Arial;"
            "border:none;"
            "padding:4px 0px;"
            "}"
        )
        ol.addWidget(info)

        # ── Job Buttons (F1-F10) ──────────────────────────────────────
        jobs = [
            ("2", "1-Point Recalibration", "Quick daily drift check"),
            ("3", "2-Point Recalibration", "Full daily drift correction"),
            ("4", "Master Curve Recalibration", "Fine-tune using master standard"),
            ("5", "INT.1 (Raw Intensity)", "Pre-correction intensity"),
            ("6", "INT.2 (Drift Corrected)", "Post-correction intensity"),
            ("7", "INT.2 for Working Curve", "Measure standards for regression"),
            ("8", "INT.2 for Target", "Set target values (first-time setup)"),
            ("X", "CONT (Content Analysis)", "Routine sample analysis"),
            ("Y", "Special 3-Time Analysis", "Multi-burn with variance check"),
        ]

        grid = QGridLayout()
        grid.setSpacing(8)

        btn_style = (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:8px 12px;"
            "min-width:80px;"
            "text-align:left;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

        for row, (key, name, desc) in enumerate(jobs):
            btn = QPushButton(f"{key}: {name}")
            btn.setStyleSheet(btn_style)
            btn.setToolTip(desc)
            btn.clicked.connect(lambda checked, k=key: self._on_job_selected(k))
            grid.addWidget(btn, row // 3, row % 3)

        # ── Add Stretch to center grid ──────────────────────────────────
        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addLayout(grid)
        wrapper.addStretch()
        ol.addLayout(wrapper)

        # ── Bottom Nav ──────────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(12, 4, 12, 8)
        bbl.setSpacing(4)

        btn_style_nav = (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(btn_style_nav)
        canc.clicked.connect(self._on_cancel)
        bbl.addStretch()
        bbl.addWidget(canc)

        root.addWidget(btn_bar)

    # =========================================================================
    # HV Controls
    # =========================================================================

    def _toggle_hv(self):
        """Toggle HV on/off."""
        self.main_window.toggle_hv()
        self._update_hv_button()

    def _update_hv_button(self):
        """Update HV button appearance based on current status."""
        if self.main_window.get_hv_status():
            self.hv_btn.setText("HV: ON")
            self.hv_btn.setStyleSheet(
                "QPushButton{"
                "background:#28a745;"
                "color:white;"
                "border:2px outset #888888;"
                "font:9pt Arial;"
                "padding:2px 8px;"
                "}"
            )
        else:
            self.hv_btn.setText("HV: OFF")
            self.hv_btn.setStyleSheet(
                "QPushButton{"
                "background:#dc3545;"
                "color:white;"
                "border:2px outset #888888;"
                "font:9pt Arial;"
                "padding:2px 8px;"
                "}"
            )

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_job_selected(self, job_type: str):
        """Open analysis run page with selected job type."""
        # Get the current group from left panel
        gid, gname = self._get_current_group()
        if gid is None:
            QMessageBox.warning(
                self,
                "No Group",
                "Please select an analytical group first."
            )
            return

        from ui.analysis.analysis_run import AnalysisRunPage
        self.main_window.set_right_widget(
            AnalysisRunPage(self.main_window, gid, gname, job_type)
        )

    def _get_current_group(self):
        """Get selected group from left panel."""
        if hasattr(self.main_window, '_group_panel'):
            if hasattr(self.main_window._group_panel, '_selected'):
                return self.main_window._group_panel._selected()
        return None, None

    def _on_cancel(self):
        self.main_window._show_home_content()

    def wants_fullscreen(self) -> bool:
        return True