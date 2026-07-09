"""
SpectraSoft — Job 7: INT.2 for Working Curve

This page measures working-curve standard samples.

Workflow:
1. User enters a standard sample name.
2. User presses Start one or more times to collect N burns.
3. AnalysisWorker returns pre-correction intensities.
4. CorrectionEngine applies Page 4 drift correction.
5. Table shows Element | AVE | N=1 | N=2 | ...
6. User presses Store Standard.
7. The AVE drift-corrected intensities are saved into:
       AnalyticalGroup.page_05_wc_measurements

Important:
- Job 7 does not calculate a,b,c,d.
- Job 7 only stores drift-corrected measured intensities for standards.
- Regression module later uses these intensities plus certified chemical values
  to calculate Page 5 coefficients.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QLineEdit,
    QProgressBar, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QTextDocument, QPageLayout
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from core.analysis_worker import AnalysisWorker
from core.correction_engine import CorrectionEngine
from core.database import get_session
from core.models import AnalyticalGroup

import csv


class Job7RunPage(QWidget):
    """Job 7: INT.2 for Working Curve page."""

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None

        # Current standard sample burns:
        # [
        #   {"C": 45.12000, "SI": 32.45000, ...},
        #   {"C": 45.22000, "SI": 32.51000, ...}
        # ]
        self.results = []

        self.element_names = []

        self.an_count = 0
        self.tan_count = 0

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._setup_job_ui()
        self._load_elements()
        self._update_table()

    # =========================================================================
    # UI
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

        self.title_label = QLabel(f"Job 7: INT.2 for Working Curve - {self.group_name}")
        self.title_label.setStyleSheet("color:white;font:bold 10pt Arial;")

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        root.addWidget(title_bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")

        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(10, 10, 10, 10)
        outer_layout.setSpacing(6)

        # ── Parameters ────────────────────────────────────────────────────
        self.params_area = QWidget()
        self.params_area.setFixedHeight(44)
        outer_layout.addWidget(self.params_area)

        # ── Progress Bar ─────────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
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
        outer_layout.addWidget(self.progress_bar)

        # ── Status Label ─────────────────────────────────────────────────
        self.status_label = QLabel(
            "Ready. Enter a standard sample name, then press Start."
        )
        self.status_label.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#333333;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.status_label)

        # ── ST Counter ───────────────────────────────────────────────────
        self.st_counter = QLabel("ST No.: —")
        self.st_counter.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.st_counter.setStyleSheet("font:bold 9pt Arial; color:#555555;")
        outer_layout.addWidget(self.st_counter)

        # ── Results Table ────────────────────────────────────────────────
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

        outer_layout.addWidget(self.table, stretch=1)

        # ── Footer ───────────────────────────────────────────────────────
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

        footer_layout.addStretch()

        outer_layout.addWidget(footer)

        # ── Buttons ──────────────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)

        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)

        btn_bar.setFixedHeight(40)

        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(0, 4, 0, 4)
        btn_layout.setSpacing(4)

        btn_style = self._button_style()

        self.btn_start = QPushButton("Start")
        self.btn_start.setStyleSheet(btn_style)
        self.btn_start.clicked.connect(self._on_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setStyleSheet(btn_style)
        self.btn_stop.clicked.connect(self._on_stop)
        self.btn_stop.setEnabled(False)

        self.btn_store = QPushButton("Store Standard")
        self.btn_store.setStyleSheet(btn_style)
        self.btn_store.clicked.connect(self._on_store_standard)

        self.btn_reset = QPushButton("Reset Current")
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.clicked.connect(self._on_reset_current)

        self.btn_print = QPushButton("Print")
        self.btn_print.setStyleSheet(btn_style)
        self.btn_print.clicked.connect(self._on_print)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setStyleSheet(btn_style)
        self.btn_export.clicked.connect(self._on_export)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_store)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_print)
        btn_layout.addWidget(self.btn_export)

        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(btn_style)
        cancel_btn.clicked.connect(self._on_cancel)
        btn_layout.addWidget(cancel_btn)

        outer_layout.addWidget(btn_bar)

    def _setup_job_ui(self):
        if self.params_area.layout():
            while self.params_area.layout().count():
                item = self.params_area.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            old_layout = self.params_area.layout()
            if old_layout:
                old_layout.deleteLater()

        layout = QVBoxLayout(self.params_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(8)

        lbl = QLabel("Standard Sample:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QLineEdit("")
        self.sample_name.setPlaceholderText("Enter standard sample name")
        self.sample_name.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
        self.sample_name.setFixedWidth(260)
        self.sample_name.textEdited.connect(self._on_sample_name_edited)
        row.addWidget(self.sample_name)

        row.addStretch()
        layout.addLayout(row)

    def _button_style(self) -> str:
        return (
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

    # =========================================================================
    # Sample Name
    # =========================================================================

    def _on_sample_name_edited(self, text: str):
        upper = text.upper()

        if text != upper:
            pos = self.sample_name.cursorPosition()
            self.sample_name.blockSignals(True)
            self.sample_name.setText(upper)
            self.sample_name.setCursorPosition(pos)
            self.sample_name.blockSignals(False)

    def _current_sample_name(self) -> str:
        return self.sample_name.text().strip().upper()

    # =========================================================================
    # Data Loading
    # =========================================================================

    def _load_elements(self):
        """
        Load element/display names from Page 3.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_03_channel:
                for entry in group.page_03_channel:
                    name = str(entry.get("name", "")).strip()
                    ele = str(entry.get("ele", "")).strip()
                    itg = str(entry.get("itg", "")).strip()

                    display_name = name or ele or (f"ITG{itg}" if itg else "")

                    if display_name:
                        self.element_names.append(display_name)

        finally:
            session.close()

    def _load_group_data_for_correction(self) -> dict:
        """
        Load Page 4 data for CorrectionEngine.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return {}

            return {
                "page_04_drift": group.page_04_drift or {}
            }

        finally:
            session.close()

    # =========================================================================
    # Table
    # =========================================================================

    def _update_table(self):
        if not self.element_names:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.status_label.setText(
                "No elements configured. Complete Page 3 before running Job 7."
            )
            return

        num_burns = len(self.results)
        num_cols = 2 + num_burns

        self.table.setRowCount(len(self.element_names))
        self.table.setColumnCount(num_cols)

        headers = ["Element", "AVE"]

        for i in range(num_burns):
            headers.append(f"N={i + 1}")

        self.table.setHorizontalHeaderLabels(headers)

        self.table.setColumnWidth(0, 90)
        self.table.setColumnWidth(1, 90)

        for i in range(num_burns):
            self.table.setColumnWidth(2 + i, 90)

        averages = self._calculate_averages()

        for row, elem in enumerate(self.element_names):
            elem_item = QTableWidgetItem(elem)
            elem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, elem_item)

            if elem in averages:
                avg_item = QTableWidgetItem(f"{averages:.5f}")
                avg_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 1, avg_item)

            for burn_index, burn in enumerate(self.results):
                val = burn.get(elem, 0.0)

                try:
                    val_float = float(val)
                except (TypeError, ValueError):
                    val_float = 0.0

                val_item = QTableWidgetItem(f"{val_float:.5f}")
                val_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.table.setItem(row, 2 + burn_index, val_item)

        self.table.resizeRowsToContents()

    def _calculate_averages(self) -> dict:
        averages = {}

        for elem in self.element_names:
            values = []

            for burn in self.results:
                if elem in burn:
                    try:
                        values.append(float(burn[elem]))
                    except (TypeError, ValueError):
                        pass

            if values:
                averages[elem] = sum(values) / len(values)

        return averages

    def _update_footer_counts(self):
        self.an_label.setText(f"AN: {self.an_count}")
        self.tan_label.setText(f"TAN: {self.tan_count}")

    # =========================================================================
    # Drift Correction
    # =========================================================================

    def _apply_drift_correction(self, intensities: dict) -> dict:
        """
        Apply Page 4 drift correction using CorrectionEngine.
        """
        group_data = self._load_group_data_for_correction()
        engine = CorrectionEngine(group_data)
        return engine.apply_drift(intensities)

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_start(self):
        if self.worker and self.worker.isRunning():
            return

        if not self.element_names:
            QMessageBox.warning(
                self,
                "No Elements",
                "No elements are configured for this analytical group.\n\n"
                "Please complete Page 3 before running Job 7."
            )
            return

        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please enter the standard sample name."
            )
            return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.sample_name.setEnabled(False)

        self.status_label.setText(f"Starting working-curve measurement for {sample}...")
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params={
                "sample_name": sample,
                "job_type": "7"
            }
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
        """
        Receive pre-correction intensities, apply Page 4 drift correction,
        and store corrected values in the current sample burn table.
        """
        if "intensities" in results:
            pre_corrected = results["intensities"]
        elif "raw_adc" in results:
            pre_corrected = results["raw_adc"]
        else:
            pre_corrected = results

        corrected = self._apply_drift_correction(pre_corrected)

        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        self.results.append(corrected)

        self.st_counter.setText(f"ST No.: {len(self.results)}")
        self._update_table()

        self.status_label.setText(
            f"Burn {len(self.results)} complete for standard {self._current_sample_name()}."
        )
        self.progress_bar.setValue(100)

    def _on_error(self, error_msg: str):
        QMessageBox.critical(self, "Analysis Error", error_msg)

        self.status_label.setText(f"Error: {error_msg}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.sample_name.setEnabled(True)
        self.progress_bar.setValue(0)

    def _on_finished(self):
        self.worker = None

        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

        if self.status_label.text() == "Stopping...":
            self.status_label.setText("Stopped")

    def _on_reset_current(self):
        if self.results:
            reply = QMessageBox.question(
                self,
                "Reset Current Standard",
                "Clear burns for the currently selected standard?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self.status_label.setText("Current standard reset.")

    # =========================================================================
    # Store Standard
    # =========================================================================

    def _on_store_standard(self):
        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please enter a standard sample name before storing."
            )
            return

        if not self.results:
            QMessageBox.warning(
                self,
                "No Data",
                "No burns are available. Run Start at least once before storing."
            )
            return

        averages = self._calculate_averages()

        if not averages:
            QMessageBox.warning(
                self,
                "No Data",
                "No valid average intensities are available."
            )
            return

        saved = self._save_standard_measurement(sample, averages, len(self.results))

        if saved:
            QMessageBox.information(
                self,
                "Stored",
                f"Working-curve measurement stored successfully.\n\n"
                f"Sample: {sample}\n"
                f"Burns: {len(self.results)}"
            )

            self.results = []
            self.st_counter.setText("ST No.: —")
            self.sample_name.setText("")
            self.sample_name.setEnabled(True)
            self._update_table()
            self.status_label.setText("Standard stored. Enter next standard sample.")

    def _save_standard_measurement(self, sample: str, averages: dict, burn_count: int) -> bool:
        """
        Save or overwrite Job 7 measured IDC values into:
            AnalyticalGroup.page_05_wc_measurements
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return False

            data = group.page_05_wc_measurements or {}

            if not isinstance(data, dict):
                data = {}

            measurements = data.get("measurements", [])

            if not isinstance(measurements, list):
                measurements = []

            existing_index = None

            for idx, entry in enumerate(measurements):
                existing_sample = str(entry.get("sample", "")).strip().upper()

                if existing_sample == sample:
                    existing_index = idx
                    break

            if existing_index is not None:
                reply = QMessageBox.question(
                    self,
                    "Overwrite Standard",
                    f"Standard sample '{sample}' already exists.\n\nOverwrite it?",
                    QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No
                )

                if reply != QMessageBox.StandardButton.Yes:
                    return False

            clean_intensities = {}

            for elem, value in averages.items():
                try:
                    clean_intensities[elem] = float(value)
                except (TypeError, ValueError):
                    clean_intensities[elem] = 0.0

            record = {
                "sample": sample,
                "burns": int(burn_count),
                "intensities": clean_intensities,
            }

            if existing_index is not None:
                measurements[existing_index] = record
            else:
                measurements.append(record)

            data["measurements"] = measurements

            group.page_05_wc_measurements = data
            session.commit()

            return True

        finally:
            session.close()

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
        title = f"SpectraSoft Job 7 Working Curve Report - {self.group_name}"
        timestamp = QDate.currentDate().toString("dd-MM-yyyy")
        sample = self._current_sample_name() or "Unknown"

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

        header_html = ""

        for i in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(i)
            header_text = header_item.text() if header_item else ""
            header_html += f"<th>{header_text}</th>"

        table_html = f"""
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>{header_html}</tr>
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
                <tr>
                    <td><b>Sample:</b> {sample}</td>
                    <td><b>Date:</b> {timestamp}</td>
                </tr>
                <tr>
                    <td><b>Job:</b> 7 / INT.2 for Working Curve</td>
                    <td><b>Burns:</b> {len(self.results)}</td>
                </tr>
            </table>

            {table_html}

            <p style="margin-top:20px;font-size:9pt;color:#666;">
                Generated by SpectraSoft
            </p>
        </body>
        </html>
        """

    # =========================================================================
    # Export
    # =========================================================================

    def _on_export(self):
        if not self.results:
            QMessageBox.warning(self, "No Data", "No burns to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Working Curve Measurement",
            "job7_working_curve_measurement.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)

                headers = []

                for col in range(self.table.columnCount()):
                    header_item = self.table.horizontalHeaderItem(col)
                    headers.append(header_item.text() if header_item else "")

                writer.writerow(headers)

                for row in range(self.table.rowCount()):
                    row_data = []

                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")

                    writer.writerow(row_data)

            QMessageBox.information(
                self,
                "Exported",
                f"Results exported to:\n{path}"
            )

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
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
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