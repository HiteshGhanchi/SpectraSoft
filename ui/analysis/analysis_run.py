"""
SpectraSoft — Analysis Run Page

Runs the selected job and displays results.
Uses AnalysisWorker for background execution.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QLineEdit, QComboBox, QProgressBar, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer

from core.analysis_worker import AnalysisWorker
from core.database import get_session
from core.models import AnalyticalGroup


class AnalysisRunPage(QWidget):
    """Main analysis execution page."""

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None
        self.results = None

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._update_hv_button()
        self._setup_job_ui()

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

        title_label = QLabel(f"Analysis - {self.group_name} (Job {self.job_type})")
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
        ol.setContentsMargins(20, 16, 20, 12)

        # ── Job Parameters Area ──────────────────────────────────────────
        self.params_area = QWidget()
        self.params_layout = QVBoxLayout(self.params_area)
        self.params_layout.setContentsMargins(0, 0, 0, 0)
        self.params_layout.setSpacing(6)
        ol.addWidget(self.params_area)

        # ── Progress Bar ─────────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(
            "QProgressBar{"
            "background:#f0f0f0;"
            "border:1px solid #888888;"
            "height:20px;"
            "text-align:center;"
            "}"
            "QProgressBar::chunk{"
            "background:#0078d7;"
            "}"
        )
        self.progress_bar.setValue(0)
        ol.addWidget(self.progress_bar)

        # ── Status Label ─────────────────────────────────────────────────
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#333333;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        ol.addWidget(self.status_label)

        # ── Results Table ────────────────────────────────────────────────
        self.results_table = QTableWidget()
        self.results_table.setStyleSheet(
            "QTableWidget{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "gridline-color:#888888;"
            "font:9pt Arial;"
            "}"
            "QTableWidget::item{"
            "border:1px solid #888888;"
            "padding:0px 4px;"
            "color:black;"
            "}"
            "QHeaderView::section{"
            "background:#0078d7;"
            "color:white;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:2px 4px;"
            "}"
        )
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.results_table.verticalHeader().setDefaultSectionSize(27)
        ol.addWidget(self.results_table)

        # ── Control Buttons ──────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(0, 8, 0, 0)

        btn_style = (
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

        self.btn_start = QPushButton("F1: Start")
        self.btn_start.setStyleSheet(btn_style)
        self.btn_start.clicked.connect(self._on_start)

        self.btn_stop = QPushButton("F2: Stop")
        self.btn_stop.setStyleSheet(btn_style)
        self.btn_stop.clicked.connect(self._on_stop)
        self.btn_stop.setEnabled(False)

        bbl.addWidget(self.btn_start)
        bbl.addWidget(self.btn_stop)
        bbl.addStretch()

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(btn_style)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)

        ol.addLayout(bbl)

        self.params_area.setFixedHeight(80)

    # =========================================================================
    # HV Controls
    # =========================================================================

    def _toggle_hv(self):
        """Toggle HV on/off."""
        self.main_window.toggle_hv()
        self._update_hv_button()

    def _update_hv_button(self):
        """Update HV button appearance based on status."""
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
    # Job-specific UI Setup
    # =========================================================================

    def _setup_job_ui(self):
        """Set up job-specific parameters UI."""
        # Properly clear all items from the layout
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                sub_layout = item.layout()
                while sub_layout.count():
                    sub_item = sub_layout.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                sub_layout.deleteLater()

        if self.job_type == 'X':
            self._setup_content_analysis_params()
        elif self.job_type == 'Y':
            self._setup_3time_params()
        elif self.job_type == '2':
            self._setup_1point_recal_params()
        elif self.job_type == '3':
            self._setup_2point_recal_params()
        elif self.job_type == '4':
            self._setup_master_curve_params()
        elif self.job_type == '8':
            self._setup_target_params()
        else:
            # Jobs 5, 6, 7 don't need special params
            label = QLabel("Place sample on spark stand and press Start.")
            label.setStyleSheet("color:#333333;font:9pt Arial;")
            self.params_layout.addWidget(label)

    def _setup_content_analysis_params(self):
        """Job X: Content Analysis."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("Sample Name:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QLineEdit("UNKNOWN-001")
        self.sample_name.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.sample_name.setFixedWidth(200)
        row.addWidget(self.sample_name)

        row.addStretch()
        self.params_layout.addLayout(row)

    def _setup_3time_params(self):
        """Job Y: 3-Time Analysis."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("Sample Name:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QLineEdit("UNKNOWN-001")
        self.sample_name.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.sample_name.setFixedWidth(200)
        row.addWidget(self.sample_name)

        row.addStretch()
        self.params_layout.addLayout(row)

    def _setup_1point_recal_params(self):
        """Job 2: 1-Point Recalibration."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("K Sample:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.k_sample = QLineEdit("C")
        self.k_sample.setMaxLength(1)
        self.k_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.k_sample.setFixedWidth(80)
        row.addWidget(self.k_sample)

        row.addStretch()
        self.params_layout.addLayout(row)

    def _setup_2point_recal_params(self):
        """Job 3: 2-Point Recalibration."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl_h = QLabel("H Sample:")
        lbl_h.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_h)

        self.h_sample = QLineEdit("A")
        self.h_sample.setMaxLength(1)
        self.h_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.h_sample.setFixedWidth(80)
        row.addWidget(self.h_sample)

        lbl_l = QLabel("L Sample:")
        lbl_l.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_l)

        self.l_sample = QLineEdit("B")
        self.l_sample.setMaxLength(1)
        self.l_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.l_sample.setFixedWidth(80)
        row.addWidget(self.l_sample)

        row.addStretch()
        self.params_layout.addLayout(row)

    def _setup_master_curve_params(self):
        """Job 4: Master Curve Recalibration."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("Master Sample:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.master_sample = QLineEdit("M")
        self.master_sample.setMaxLength(1)
        self.master_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.master_sample.setFixedWidth(80)
        row.addWidget(self.master_sample)

        row.addStretch()
        self.params_layout.addLayout(row)

    def _setup_target_params(self):
        """Job 8: INT.2 for Target."""
        row = QHBoxLayout()
        row.setSpacing(8)

        lbl_h = QLabel("H Sample:")
        lbl_h.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_h)

        self.h_sample = QLineEdit("A")
        self.h_sample.setMaxLength(1)
        self.h_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.h_sample.setFixedWidth(80)
        row.addWidget(self.h_sample)

        lbl_l = QLabel("L Sample:")
        lbl_l.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_l)

        self.l_sample = QLineEdit("B")
        self.l_sample.setMaxLength(1)
        self.l_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.l_sample.setFixedWidth(80)
        row.addWidget(self.l_sample)

        lbl_k = QLabel("K Sample:")
        lbl_k.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_k)

        self.k_sample = QLineEdit("C")
        self.k_sample.setMaxLength(1)
        self.k_sample.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.k_sample.setFixedWidth(80)
        row.addWidget(self.k_sample)

        row.addStretch()
        self.params_layout.addLayout(row)

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_start(self):
        """Start the analysis."""
        if self.worker and self.worker.isRunning():
            return

        # ── HV CHECK ──────────────────────────────────────────────────────
        if not self.main_window.get_hv_status():
            reply = QMessageBox.question(
                self,
                "HV is OFF",
                "PMT power (HV) is OFF. Turn it ON?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.main_window.toggle_hv()
                self._update_hv_button()
            else:
                return

        # Disable UI
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_label.setText("Starting...")
        self.progress_bar.setValue(0)

        # Build params
        params = {}
        if hasattr(self, 'sample_name'):
            params["sample_name"] = self.sample_name.text().strip()
        if hasattr(self, 'h_sample'):
            params["h_sample"] = self.h_sample.text().strip()
        if hasattr(self, 'l_sample'):
            params["l_sample"] = self.l_sample.text().strip()
        if hasattr(self, 'k_sample'):
            params["k_sample"] = self.k_sample.text().strip()
        if hasattr(self, 'master_sample'):
            params["master_sample"] = self.master_sample.text().strip()

        # Create and start worker
        self.worker = AnalysisWorker(
            group_id=self.group_id,
            job_type=self.job_type,
            params=params
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.result.connect(self._on_result)
        self.worker.error.connect(self._on_error)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_stop(self):
        """Stop the running analysis."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.status_label.setText("Stopping...")
            self.btn_stop.setEnabled(False)

    def _on_progress(self, step: str, percent: int):
        """Update progress bar and status."""
        self.status_label.setText(step)
        self.progress_bar.setValue(percent)

    def _on_result(self, results: dict):
        """Display results."""
        self.results = results
        self._display_results(results)

    def _on_error(self, error_msg: str):
        """Handle error."""
        QMessageBox.critical(self, "Analysis Error", error_msg)
        self.status_label.setText(f"Error: {error_msg}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress_bar.setValue(0)

    def _on_finished(self):
        """Clean up after analysis."""
        self.worker = None
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

        # If no results were set (error case), status label was already set
        if self.status_label.text() == "Stopping...":
            self.status_label.setText("Stopped")

    def _display_results(self, results: dict):
        """Populate results table."""
        # Get the raw intensities
        raw = results.get("raw_intensities", {})
        if not raw:
            self.results_table.setRowCount(0)
            return

        # Sort by element name
        items = sorted(raw.items(), key=lambda x: x[0])

        # Set up table
        self.results_table.setRowCount(len(items))
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Element", "ADC Value"])

        for row, (key, value) in enumerate(items):
            # Element (parse "FE|273.0" -> "FE")
            element = key.split("|")[0] if "|" in key else key
            self.results_table.setItem(row, 0, QTableWidgetItem(element))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(value)))

        self.results_table.resizeColumnsToContents()
        self.status_label.setText(f"Analysis complete. {len(items)} elements measured.")

    # =========================================================================
    # Navigation
    # =========================================================================

    def _on_cancel(self):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Cancel Analysis",
                "Analysis is still running. Stop and cancel?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                QTimer.singleShot(500, self._go_back)
            else:
                return
        else:
            self._go_back()

    def _go_back(self):
        from ui.analysis.job_selection import JobSelectionPage
        self.main_window.set_right_widget(
            JobSelectionPage(self.main_window)
        )

    def wants_fullscreen(self) -> bool:
        return True