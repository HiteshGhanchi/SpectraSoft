"""
SpectraSoft — Job 5: INT.1 (Raw Intensity)

This page is dedicated to Job 5 only.
It shows raw intensity (normalized or relative) with multi-burn support.
Columns: Element, AVE, N=1, N=2, ..., R, S.D., C.V.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QLineEdit,
    QProgressBar, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QDate, QDateTime
from PyQt6.QtGui import QColor, QTextDocument, QPageLayout, QKeySequence, QShortcut
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from core.analysis_worker import AnalysisWorker
from core.database import get_session
from core.models import AnalyticalGroup

import csv
import math


class Job5RunPage(QWidget):
    """Job 5: Raw Intensity analysis page."""

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type   # Should be '5'

        self.worker = None
        self.results = []          # list of dict: each burn result {element: intensity}
        self.element_names = []
        self.is_running = False

        # Counters for status footer
        self.an_count = 0          # Analysis number since last waste discharge
        self.tan_count = 0         # Total number of emission times

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._setup_job_ui()
        self._load_elements()
        self._update_table()

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

        self.title_label = QLabel(f"Job 5: Raw Intensity - {self.group_name}")
        self.title_label.setStyleSheet("color:white;font:bold 10pt Arial;")
        title_layout.addWidget(self.title_label)
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
        ol.setContentsMargins(10, 10, 10, 10)
        ol.setSpacing(6)

        # ── Job Parameters Area (Sample Name + ST Number) ──────────────
        self.params_area = QWidget()
        self.params_area.setFixedHeight(70)
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
        self.status_label = QLabel("Ready. Press F1: Start to begin.")
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

        # ── ST Counter ──────────────────────────────────────────────────
        self.st_counter = QLabel("ST No.: —")
        self.st_counter.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.st_counter.setStyleSheet("font:bold 9pt Arial; color:#555555;")
        ol.addWidget(self.st_counter)

        # ── Results Table (with scroll) ────────────────────────────────
        self.table = QTableWidget()
        self.table.setStyleSheet(
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
            "background:white;"
            "}"
            "QHeaderView::section{"
            "background:#0078d7;"
            "color:white;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:2px 4px;"
            "}"
            "QTableWidget::item:selected{"
            "background:#cce5ff;"
            "color:black;"
            "}"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setDefaultSectionSize(27)
        ol.addWidget(self.table, stretch=1)  # Table takes remaining space

        # ── Status Footer ──────────────────────────────────────────────────
        footer = QWidget()
        footer.setAutoFillBackground(True)
        fbp = footer.palette()
        fbp.setColor(footer.backgroundRole(), Qt.GlobalColor.lightGray)
        footer.setPalette(fbp)
        footer.setStyleSheet("background:#d4d0c8; border-top:1px solid #888888;")
        footer.setFixedHeight(28)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 4, 10, 4)
        footer_layout.setSpacing(20)

        self.an_label = QLabel("AN: 0")
        self.an_label.setStyleSheet("font:9pt Arial; color:black;")
        footer_layout.addWidget(self.an_label)

        self.tan_label = QLabel("TAN: 0")
        self.tan_label.setStyleSheet("font:9pt Arial; color:black;")
        footer_layout.addWidget(self.tan_label)

        self.hv_status_label = QLabel("HV: OFF")
        self.hv_status_label.setStyleSheet("font:9pt Arial; color:red;")
        footer_layout.addWidget(self.hv_status_label)

        footer_layout.addStretch()
        ol.addWidget(footer)

        # ── Bottom Navigation ────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)
        btn_bar.setFixedHeight(40)  # Fixed height for buttons

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(0, 4, 0, 4)
        bbl.setSpacing(4)

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

        self.btn_print = QPushButton("F4: Print")
        self.btn_print.setStyleSheet(btn_style)
        self.btn_print.clicked.connect(self._on_print)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setStyleSheet(btn_style)
        self.btn_export.clicked.connect(self._on_export)

        self.btn_reset = QPushButton("F7: Reset")
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.clicked.connect(self._on_reset)

        bbl.addWidget(self.btn_start)
        bbl.addWidget(self.btn_stop)
        bbl.addWidget(self.btn_print)
        bbl.addWidget(self.btn_export)
        bbl.addWidget(self.btn_reset)
        bbl.addStretch()

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(btn_style)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)

        ol.addWidget(btn_bar)  # Button bar at the very bottom

        # ── Keyboard Shortcuts ────────────────────────────────────────────
        QShortcut(QKeySequence("F1"), self, activated=self._on_start)
        QShortcut(QKeySequence("F2"), self, activated=self._on_stop)
        QShortcut(QKeySequence("F4"), self, activated=self._on_print)
        QShortcut(QKeySequence("F7"), self, activated=self._on_reset)
        QShortcut(QKeySequence("9"),  self, activated=self._on_cancel)

    # =========================================================================
    # Job-Specific UI Setup
    # =========================================================================

    def _setup_job_ui(self):
        """Set up job-specific parameters UI (sample name + ST number inputs)."""
        # Properly clear the params_area
        if self.params_area.layout():
            # Remove all child widgets
            while self.params_area.layout().count():
                item = self.params_area.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            # Delete the layout itself
            old_layout = self.params_area.layout()
            if old_layout:
                old_layout.deleteLater()

        # Create new layout
        layout = QVBoxLayout(self.params_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # ── Row 1: Sample Name (user-facing save label) ──────────────
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        lbl1 = QLabel("Sample Name:")
        lbl1.setStyleSheet("color:black;font:9pt Arial;")
        lbl1.setFixedWidth(90)
        row1.addWidget(lbl1)
        self.sample_name = QLineEdit("UNKNOWN-001")
        self.sample_name.setStyleSheet(
            "QLineEdit{background:white;color:black;border:1px solid #888888;"
            "font:9pt Arial;padding:2px 4px;}"
        )
        self.sample_name.setFixedWidth(200)
        row1.addWidget(self.sample_name)
        row1.addStretch()
        layout.addLayout(row1)

        # ── Row 2: ST Number (CSV lookup key for demo mode) ───────────
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        lbl2 = QLabel("ST Number:")
        lbl2.setStyleSheet("color:black;font:9pt Arial;")
        lbl2.setFixedWidth(90)
        row2.addWidget(lbl2)
        self.st_number_input = QLineEdit("")
        self.st_number_input.setPlaceholderText("e.g. ABCD, DEFG, DEFAULT, SJDJEDJ")
        self.st_number_input.setStyleSheet(
            "QLineEdit{background:white;color:black;border:1px solid #888888;"
            "font:9pt Arial;padding:2px 4px;}"
        )
        self.st_number_input.setFixedWidth(200)
        row2.addWidget(self.st_number_input)
        row2.addStretch()
        layout.addLayout(row2)
    # =========================================================================
    # Data Loading
    # =========================================================================

    def _load_elements(self):
        """Load element names from Page 3."""
        session = get_session()
        try:
            group = session.get(AnalyticalGroup, self.group_id)
            if group and group.page_03_channel:
                for entry in group.page_03_channel:
                    ele = entry.get("ele", "")
                    if ele:
                        self.element_names.append(ele)
            if not self.element_names:
                # No elements defined; user must set up Page 3.
                self.element_names = []
        finally:
            session.close()

    # =========================================================================
    # Table Management
    # =========================================================================

    def _update_table(self):
        """Update the results table with all burns and statistics."""
        if not self.element_names:
            # Show a message or empty table with headers
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        num_burns = len(self.results)
        # Columns: Element, AVE, N=1, N=2, ..., R, SD, CV
        # Total columns = 1 (Element) + 1 (AVE) + num_burns + 3 (R,SD,CV)
        num_cols = 2 + num_burns + 3

        self.table.setRowCount(len(self.element_names))
        self.table.setColumnCount(num_cols)

        headers = ["Element", "AVE"]
        for i in range(num_burns):
            headers.append(f"N={i+1}")
        headers.extend(["R", "S.D.", "C.V."])

        self.table.setHorizontalHeaderLabels(headers)

        # Set column widths
        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 70)
        for i in range(num_burns):
            self.table.setColumnWidth(2 + i, 70)
        self.table.setColumnWidth(2 + num_burns, 60)    # R
        self.table.setColumnWidth(3 + num_burns, 60)    # S.D.
        self.table.setColumnWidth(4 + num_burns, 60)    # C.V.

        # Fill data
        for row, elem in enumerate(self.element_names):
            # Element name
            elem_item = QTableWidgetItem(elem)
            elem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, elem_item)

            # Collect values for this element across burns
            values = []
            for burn in self.results:
                val = burn.get(elem, 0.0)
                values.append(val)

            if values:
                # Average
                avg = sum(values) / len(values)
                avg_item = QTableWidgetItem(f"{avg:.3f}")
                avg_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 1, avg_item)

                # Individual burns
                for i, val in enumerate(values):
                    val_item = QTableWidgetItem(f"{val:.3f}")
                    val_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                    self.table.setItem(row, 2 + i, val_item)

                # R (Range)
                r_val = max(values) - min(values)
                r_item = QTableWidgetItem(f"{r_val:.3f}")
                r_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 2 + num_burns, r_item)

                # S.D. (sample standard deviation)
                if len(values) > 1:
                    mean = avg
                    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
                    sd = math.sqrt(variance)
                else:
                    sd = 0.0
                sd_item = QTableWidgetItem(f"{sd:.3f}")
                sd_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 3 + num_burns, sd_item)

                # C.V. (Coefficient of Variation)
                if avg != 0:
                    cv = (sd / avg) * 100
                else:
                    cv = 0.0
                cv_item = QTableWidgetItem(f"{cv:.2f}%")
                cv_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 4 + num_burns, cv_item)

        self.table.resizeRowsToContents()

    # =========================================================================
    # HV Controls
    # =========================================================================

    def _toggle_hv(self):
        self.main_window.toggle_hv()
        self._update_hv_button()
        self._update_footer_hv()

    def _update_hv_button(self):
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

    def _update_footer_hv(self):
        if self.main_window.get_hv_status():
            self.hv_status_label.setText("HV: ON")
            self.hv_status_label.setStyleSheet("font:9pt Arial; color:green;")
        else:
            self.hv_status_label.setText("HV: OFF")
            self.hv_status_label.setStyleSheet("font:9pt Arial; color:red;")

    def _update_footer_counts(self):
        self.an_label.setText(f"AN: {self.an_count}")
        self.tan_label.setText(f"TAN: {self.tan_count}")

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_start(self):
        if self.worker and self.worker.isRunning():
            return

        # Check HV
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
                self._update_footer_hv()
            else:
                return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.status_label.setText("Starting analysis...")
        self.progress_bar.setValue(0)

        params = {
            "sample_name": self.sample_name.text().strip(),
            "st_number":   self.st_number_input.text().strip(),
        }

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params=params
        )
        self.worker.progress.connect(self._on_progress)
        self.worker.result.connect(self._on_result)
        self.worker.error.connect(self._on_error)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.status_label.setText("Stopping...")
            self.btn_stop.setEnabled(False)

    def _on_progress(self, step: str, percent: int):
        self.status_label.setText(step)
        self.progress_bar.setValue(percent)

    def _on_result(self, results: dict):
        # Extract the intensity data
        if "intensities" in results:
            data = results["intensities"]
        elif "raw_adc" in results:
            data = results["raw_adc"]
        else:
            data = results

        # Increment counters
        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        # Store result
        self.results.append(data)
        self.st_counter.setText(f"ST No.: {len(self.results)}")

        # Update table
        self._update_table()

        self.status_label.setText(f"Burn {len(self.results)} complete.")
        self.progress_bar.setValue(100)

    def _on_error(self, error_msg: str):
        QMessageBox.critical(self, "Analysis Error", error_msg)
        self.status_label.setText(f"Error: {error_msg}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress_bar.setValue(0)

    def _on_finished(self):
        self.worker = None
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

        if self.status_label.text() == "Stopping...":
            self.status_label.setText("Stopped")

    def _on_reset(self):
        """Reset all burns for current sample."""
        if self.results:
            reply = QMessageBox.question(
                self,
                "Reset",
                "Clear all burns for this sample?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.results = []
                self.st_counter.setText("ST No.: —")
                self._update_table()
                self.status_label.setText("Reset. Ready for new sample.")

    # =========================================================================
    # Print
    # =========================================================================

    def _on_print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self._render_print_page)
        preview.exec()

    def _render_print_page(self, printer):
        doc = QTextDocument()
        html = self._generate_html_report()
        doc.setHtml(html)
        doc.print(printer)

    def _generate_html_report(self) -> str:
        """Generate HTML report for printing."""
        title = f"SpectraSoft Job 5 Report - {self.group_name}"
        timestamp = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")
        sample = self.sample_name.text() if hasattr(self, 'sample_name') else "Unknown"

        # Build table rows
        rows = []
        if self.table.rowCount() > 0 and self.table.columnCount() > 0:
            for row in range(self.table.rowCount()):
                row_html = "<tr>"
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    val = item.text() if item else ""
                    row_html += f"<td>{val}</td>"
                row_html += "</tr>"
                rows.append(row_html)

        table_html = f"""
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    {''.join(f'<th>{self.table.horizontalHeaderItem(i).text()}</th>' for i in range(self.table.columnCount()))}
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """

        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                .meta {{ margin-bottom: 20px; }}
                .meta td {{ padding: 2px 10px; }}
                table {{ border-collapse: collapse; width: 100%; font-size: 10pt; }}
                th {{ background-color: #34495e; color: white; padding: 6px 8px; }}
                td {{ padding: 4px 8px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <table class="meta">
                <tr><td><b>Sample:</b> {sample}</td>
                    <td><b>Date:</b> {timestamp}</td></tr>
                <tr><td><b>Job:</b> 5 (INT.1)</td>
                    <td><b>Burns:</b> {len(self.results)}</td></tr>
            </table>
            {table_html}
            <p style="margin-top:20px;font-size:9pt;color:#666;">
                Generated by SpectraSoft
            </p>
        </body>
        </html>
        """

    # =========================================================================
    # Export to CSV
    # =========================================================================

    def _on_export(self):
        if not self.results:
            QMessageBox.warning(self, "No Data", "No burns to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Analysis Results", "analysis_results.csv",
            "CSV Files (*.csv)"
        )
        if not path:
            return

        try:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)

                # Header
                headers = ["Element"]
                for i in range(len(self.results)):
                    headers.append(f"N={i+1}")
                headers.extend(["AVE", "R", "S.D.", "C.V."])
                writer.writerow(headers)

                # Data
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)

            QMessageBox.information(self, "Exported",
                f"Results exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

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
        self.main_window.set_right_widget(JobSelectionPage(self.main_window))

    def wants_fullscreen(self) -> bool:
        return True