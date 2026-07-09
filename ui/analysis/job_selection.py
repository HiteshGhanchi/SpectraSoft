"""
SpectraSoft — Job Selection Menu

Currently implemented:
- 1-Point Recalibration
- 2-Point Recalibration
- INT.1 Raw Intensity
- INT.2 Drift Corrected
- INT.2 for Target
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt


class JobSelectionPage(QWidget):
    """Job selection menu."""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()

    # =========================================================================
    # UI Construction
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("background:#5c9bd5;")

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)

        title_label = QLabel("Job Selection")
        title_label.setStyleSheet("color:white;font:bold 10pt Arial;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

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
        ol.setSpacing(14)

        instruction = QLabel(
            "Select an analytical job.\n"
            "Available now: Job 2, Job 3, Job 5, Job 6, and Job 8."
        )
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet(
            "QLabel{"
            "background:white;"
            "color:#333333;"
            "font:10pt Arial;"
            "border:none;"
            "padding:8px;"
            "}"
        )
        ol.addWidget(instruction)

        jobs = [
            ("1-Point Recalibration", self._open_job2),
            ("2-Point Recalibration", self._open_job3),
            ("Master Curve Recalibration", self._open_job4),
            ("INT.1 Raw Intensity", self._open_job5),
            ("INT.2 Drift Corrected", self._open_job6),
            ("INT.2 for Working Curve", self._open_job7),
            ("INT.2 for Target", self._open_job8),
            ("Content Analysis", None),
            ("Special 3-Time Analysis", None),
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
            "min-width:180px;"
            "text-align:left;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

        btn_disabled_style = (
            "QPushButton{"
            "background:#e0e0e0;"
            "color:#888888;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:8px 12px;"
            "min-width:180px;"
            "text-align:left;"
            "}"
        )

        for index, (name, slot) in enumerate(jobs):
            btn = QPushButton(name)

            if slot:
                btn.setStyleSheet(btn_style)
                btn.clicked.connect(slot)
            else:
                btn.setStyleSheet(btn_disabled_style)
                btn.setEnabled(False)
                btn.setToolTip("This job is not implemented yet.")

            grid.addWidget(btn, index // 3, index % 3)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addLayout(grid)
        wrapper.addStretch()

        ol.addLayout(wrapper)
        ol.addStretch()

        # ── Bottom Navigation ────────────────────────────────────────────
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
            "min-width:70px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(btn_style_nav)
        cancel_btn.clicked.connect(self._on_cancel)

        bbl.addStretch()
        bbl.addWidget(cancel_btn)

        root.addWidget(btn_bar)

    # =========================================================================
    # Open Jobs
    # =========================================================================

    def _open_job2(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job2 import Job2RecalPage

        self.main_window.set_right_widget(
            Job2RecalPage(
                self.main_window,
                gid,
                gname,
                "2"
            )
        )

    def _open_job3(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job3 import Job3RecalPage

        self.main_window.set_right_widget(
            Job3RecalPage(
                self.main_window,
                gid,
                gname,
                "3"
            )
        )
    
    def _open_job4(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job4 import Job4RunPage

        self.main_window.set_right_widget(
            Job4RunPage(
                self.main_window,
                gid,
                gname,
                "4"
            )
        )

    def _open_job5(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job5 import Job5RunPage

        self.main_window.set_right_widget(
            Job5RunPage(
                self.main_window,
                gid,
                gname,
                "5"
            )
        )

    def _open_job6(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job6 import Job6RunPage

        self.main_window.set_right_widget(
            Job6RunPage(
                self.main_window,
                gid,
                gname,
                "6"
            )
        )

    def _open_job8(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job8 import Job8RunPage

        self.main_window.set_right_widget(
            Job8RunPage(
                self.main_window,
                gid,
                gname,
                "8"
            )
        )
    
    def _open_job7(self):
        gid, gname = self._get_current_group()

        if gid is None:
            self._warn_no_group()
            return

        from ui.analysis.analysis_run_job7 import Job7RunPage

        self.main_window.set_right_widget(
            Job7RunPage(
                self.main_window,
                gid,
                gname,
                "7"
            )
        )

    # =========================================================================
    # Helpers
    # =========================================================================

    def _warn_no_group(self):
        QMessageBox.warning(
            self,
            "No Group Selected",
            "Please select an analytical group first."
        )

    def _get_current_group(self):
        if hasattr(self.main_window, "_group_panel"):
            if hasattr(self.main_window._group_panel, "_selected"):
                return self.main_window._group_panel._selected()

        return None, None

    def _on_cancel(self):
        self.main_window._show_home_content()

    def wants_fullscreen(self) -> bool:
        return True