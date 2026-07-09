"""
SpectraSoft — Job 4: Master Curve Recalibration

This job calculates Page 7 Master Curve Correction values.

Workflow:
1. User selects a master correction sample from Page 7 SPL values.
2. User presses Start one or more times to collect N burns.
3. AnalysisWorker returns pre-correction intensities.
4. Software applies:
      Page 4 drift correction
      Page 5 working curve
      Page 6 matrix correction
   but does NOT apply Page 7 master correction.
5. Table shows Element | AVE | N=1 | N=2 | ...
6. User presses Cal / File.
7. Job 4 updates Page 7 AC / MC for rows whose SPL matches selected sample.

Correction modes:
- AC Additive:
      AC = TARGET - C0
      MC = 1.0000

- MC Multiplicative:
      MC = TARGET / C0
      AC = 0.00000

Limit behavior:
- If abs(TARGET - C0) <= D1, no correction is applied:
      AC = 0.00000
      MC = 1.0000

- If D2 > 0 and abs(TARGET - C0) > D2, the row is skipped.

Where:
    C0 = calculated content before Page 7 master correction.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QComboBox,
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


class Job4RunPage(QWidget):
    """Job 4: Master Curve Recalibration page."""

    MODE_AC = "AC"
    MODE_MC = "MC"

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str = "4"):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None

        # Each item is one burn after drift + working curve + matrix,
        # but before Page 7 master correction.
        self.results = []

        self.element_names = []
        self.sample_names = []

        self.an_count = 0
        self.tan_count = 0

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_elements()
        self._load_page7_samples()

        self._build_ui()
        self._populate_sample_combo()
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

        self.title_label = QLabel(f"Job 4: Master Curve Recalibration - {self.group_name}")
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
        self.params_area.setFixedHeight(46)
        outer_layout.addWidget(self.params_area)

        self._build_params_area()

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
            "Ready. Select a Page 7 SPL sample and press Start."
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

        self.btn_cal = QPushButton("Cal / File")
        self.btn_cal.setStyleSheet(btn_style)
        self.btn_cal.clicked.connect(self._on_cal_file)

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
        btn_layout.addWidget(self.btn_cal)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_print)
        btn_layout.addWidget(self.btn_export)

        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(btn_style)
        cancel_btn.clicked.connect(self._on_cancel)
        btn_layout.addWidget(cancel_btn)

        outer_layout.addWidget(btn_bar)

    def _build_params_area(self):
        layout = QVBoxLayout(self.params_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(8)

        lbl_sample = QLabel("SPL Sample:")
        lbl_sample.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_sample)

        self.sample_combo = QComboBox()
        self.sample_combo.setFixedWidth(220)
        self.sample_combo.setStyleSheet(self._combo_style())
        row.addWidget(self.sample_combo)

        lbl_mode = QLabel("Correction Mode:")
        lbl_mode.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl_mode)

        self.mode_combo = QComboBox()
        self.mode_combo.setFixedWidth(180)
        self.mode_combo.addItem("AC Additive", self.MODE_AC)
        self.mode_combo.addItem("MC Multiplicative", self.MODE_MC)
        self.mode_combo.setCurrentIndex(0)
        self.mode_combo.setStyleSheet(self._combo_style())
        row.addWidget(self.mode_combo)

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

    def _combo_style(self) -> str:
        return (
            "QComboBox{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
            "QComboBox QAbstractItemView{"
            "background:white;"
            "color:black;"
            "selection-background-color:#0078d7;"
            "selection-color:white;"
            "}"
        )

    # =========================================================================
    # Data Loading
    # =========================================================================

    def _load_elements(self):
        self.element_names = []

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and isinstance(group.page_03_channel, list):
                for entry in group.page_03_channel:
                    name = str(entry.get("name", "")).strip()
                    ele = str(entry.get("ele", "")).strip()
                    itg = str(entry.get("itg", "")).strip()

                    display_name = name or ele or (f"ITG{itg}" if itg else "")

                    if display_name:
                        self.element_names.append(display_name)

        finally:
            session.close()

    def _load_page7_samples(self):
        """
        Load unique non-empty SPL sample names from Page 7.
        """
        self.sample_names = []

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_07_master:
                return

            data = group.page_07_master

            if not isinstance(data, dict):
                return

            rows = data.get("rows", [])

            if not isinstance(rows, list):
                return

            samples = set()

            for row in rows:
                sample = str(row.get("spl", "")).strip().upper()

                if sample:
                    samples.add(sample)

            self.sample_names = sorted(samples)

        finally:
            session.close()

    def _populate_sample_combo(self):
        self.sample_combo.clear()
        self.sample_combo.addItem("", "")

        for sample in self.sample_names:
            self.sample_combo.addItem(sample, sample)

    def _current_sample(self) -> str:
        return str(self.sample_combo.currentData() or "").strip().upper()

    def _current_mode(self) -> str:
        return str(self.mode_combo.currentData() or self.MODE_AC)

    def _load_group_data_for_correction(self) -> dict:
        """
        Load group data for correction path before Page 7:
        Page 4 drift, Page 5 working curve, Page 6 matrix.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return {}

            return {
                "page_04_drift": group.page_04_drift or {},
                "page_05_wc": group.page_05_wc or {},
                "page_06_matrix": group.page_06_matrix or {},
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
                "No elements configured. Complete Page 3 before running Job 4."
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
    # Correction Path Before Page 7
    # =========================================================================

    def _apply_pre_master_corrections(self, intensities: dict) -> dict:
        """
        Convert pre-correction intensities into content before master correction.

        Chain:
            Page 4 drift correction
            Page 5 working curve
            Page 6 matrix correction

        Page 7 master correction is intentionally not applied here.
        """
        group_data = self._load_group_data_for_correction()
        engine = CorrectionEngine(group_data)

        drift_corrected = engine.apply_drift(intensities)
        content = engine.apply_working_curve(drift_corrected)
        matrix_corrected = engine.apply_matrix(content)

        return matrix_corrected

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
                "Please complete Page 3 before running Job 4."
            )
            return

        sample = self._current_sample()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select an SPL sample registered on Page 7."
            )
            return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.sample_combo.setEnabled(False)
        self.mode_combo.setEnabled(False)

        self.status_label.setText(f"Starting master curve recalibration for {sample}...")
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params={
                "sample_name": sample,
                "job_type": "4"
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
        Receive pre-correction intensities, convert to pre-master content,
        then store one burn result.
        """
        if "intensities" in results:
            pre_corrected = results["intensities"]
        elif "raw_adc" in results:
            pre_corrected = results["raw_adc"]
        else:
            pre_corrected = results

        content_before_master = self._apply_pre_master_corrections(pre_corrected)

        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        self.results.append(content_before_master)

        self.st_counter.setText(f"ST No.: {len(self.results)}")
        self._update_table()

        self.status_label.setText(
            f"Burn {len(self.results)} complete for master sample {self._current_sample()}."
        )
        self.progress_bar.setValue(100)

    def _on_error(self, error_msg: str):
        QMessageBox.critical(self, "Analysis Error", error_msg)

        self.status_label.setText(f"Error: {error_msg}")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.sample_combo.setEnabled(True)
        self.mode_combo.setEnabled(True)
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
                "Reset Current",
                "Clear current master correction burns?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_combo.setEnabled(True)
        self.mode_combo.setEnabled(True)
        self._update_table()
        self.status_label.setText("Current master sample reset.")

    # =========================================================================
    # Cal / File Page 7
    # =========================================================================

    def _on_cal_file(self):
        sample = self._current_sample()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select an SPL sample."
            )
            return

        if not self.results:
            QMessageBox.warning(
                self,
                "No Data",
                "No burns are available. Run Start at least once before Cal / File."
            )
            return

        averages = self._calculate_averages()

        if not averages:
            QMessageBox.warning(
                self,
                "No Data",
                "No valid average content values are available."
            )
            return

        updated, skipped = self._file_master_correction(sample, averages)

        if updated == 0:
            QMessageBox.warning(
                self,
                "No Rows Updated",
                f"No Page 7 rows were updated.\n\nSkipped rows: {skipped}"
            )
            return

        QMessageBox.information(
            self,
            "Master Recalibration Completed",
            f"Master curve correction filed successfully.\n\n"
            f"SPL Sample: {sample}\n"
            f"Rows updated: {updated}\n"
            f"Rows skipped: {skipped}"
        )

        self.status_label.setText(
            f"Cal / File completed. Updated Page 7 for {updated} row(s)."
        )

    def _file_master_correction(self, sample: str, averages: dict) -> tuple[int, int]:
        """
        File calculated AC/MC into Page 7 rows where SPL equals sample.
        """
        mode = self._current_mode()

        session = get_session()
        updated = 0
        skipped = 0

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return 0, 0

            page7 = group.page_07_master or {}

            if not isinstance(page7, dict) or not isinstance(page7.get("rows"), list):
                return 0, 0

            rows = page7["rows"]

            for row in rows:
                row_sample = str(row.get("spl", "")).strip().upper()

                if row_sample != sample:
                    skipped += 1
                    continue

                elem = str(row.get("name", "")).strip()

                if not elem or elem not in averages:
                    skipped += 1
                    continue

                try:
                    c0 = float(averages[elem])
                    target = float(str(row.get("target", "0")).strip() or "0")
                    d1 = abs(float(str(row.get("d1", "0")).strip() or "0"))
                    d2 = abs(float(str(row.get("d2", "0")).strip() or "0"))
                except (TypeError, ValueError):
                    skipped += 1
                    continue

                # If target is zero, this row is effectively unconfigured.
                if target == 0.0:
                    skipped += 1
                    continue

                error = target - c0
                abs_error = abs(error)

                # If within inner limit, no correction.
                if d1 > 0.0 and abs_error <= d1:
                    row["ac"] = "0.00000"
                    row["mc"] = "1.0000"
                    updated += 1
                    continue

                # If beyond outer limit, skip.
                # D2 = 0 means no outer limit is enforced.
                if d2 > 0.0 and abs_error > d2:
                    skipped += 1
                    continue

                if mode == self.MODE_MC:
                    if c0 == 0.0:
                        skipped += 1
                        continue

                    mc = target / c0
                    ac = 0.0

                else:
                    mc = 1.0
                    ac = error

                row["ac"] = f"{ac:.5f}"
                row["mc"] = f"{mc:.4f}"

                updated += 1

            group.page_07_master = {
                "rows": rows
            }
            session.commit()

            return updated, skipped

        finally:
            session.close()

    # =========================================================================
    # Print / Export
    # =========================================================================

    def _on_print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)

        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self._render_print_page)
        preview.exec()

    def _render_print_page(self, printer):
        doc = QTextDocument()
        doc.setHtml(self._generate_html_report())
        doc.print(printer)

    def _generate_html_report(self) -> str:
        title = f"SpectraSoft Job 4 Master Curve Recalibration Report - {self.group_name}"
        timestamp = QDate.currentDate().toString("dd-MM-yyyy")
        sample = self._current_sample() or "Unknown"
        mode = self.mode_combo.currentText()

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

        headers = ""

        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            headers += f"<th>{header_item.text() if header_item else ''}</th>"

        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; font-size: 9pt; }}
                th {{ background-color: #34495e; color: white; padding: 5px; }}
                td {{ border: 1px solid #777; padding: 4px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <p><b>Date:</b> {timestamp}</p>
            <p><b>SPL Sample:</b> {sample}</p>
            <p><b>Correction Mode:</b> {mode}</p>
            <p><b>Burns:</b> {len(self.results)}</p>

            <table>
                <tr>{headers}</tr>
                {''.join(rows)}
            </table>
        </body>
        </html>
        """

    def _on_export(self):
        if not self.results:
            QMessageBox.warning(self, "No Data", "No burns to export.")
            return

        sample = self._current_sample() or "UNKNOWN"

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Job 4 Results",
            f"job4_master_curve_{sample}.csv",
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

                for row_idx in range(self.table.rowCount()):
                    row_data = []

                    for col in range(self.table.columnCount()):
                        item = self.table.item(row_idx, col)
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