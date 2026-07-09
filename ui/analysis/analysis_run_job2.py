"""
SpectraSoft — Job 2: 1-Point Recalibration

This page performs 1-point recalibration using Page 4 K sample mappings.

Workflow:
1. User selects a Page 4 K sample name.
2. User presses Start one or more times to collect N burns.
3. The table shows Element | AVE | N=1 | N=2 | ...
4. User presses Cal / File.
5. The software updates Page 4 k value for every row where:
       K sample name == selected sample name

Formula:
    k = K_Target / (alpha * I_K + beta)

Where:
    I_K      = current measured AVE intensity for the selected K sample
    K_Target = stored K Target from Page 4
    alpha    = current Page 4 alpha
    beta     = current Page 4 beta

Important:
- Uses processed intensities from AnalysisWorker, not raw ADC.
- Blank K values are skipped.
- "*" K values are skipped.
- Existing alpha and beta values are preserved.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QProgressBar, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QTextDocument, QPageLayout
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog

from core.analysis_worker import AnalysisWorker
from core.database import get_session
from core.models import AnalyticalGroup

import csv


class Job2RecalPage(QWidget):
    """Job 2: 1-Point Recalibration page."""

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str = "2"):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None
        self.results = []
        self.element_names = []
        self.required_samples = []

        self.an_count = 0
        self.tan_count = 0

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._setup_job_ui()
        self._load_elements()
        self._load_required_samples()
        self._populate_sample_dropdown()
        self._update_table()
        self._update_summary()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ─────────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(24)
        title_bar.setStyleSheet("background:#5c9bd5;")

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(12, 0, 12, 0)

        self.title_label = QLabel(f"Job 2: 1-Point Recalibration - {self.group_name}")
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

        # ── Parameter Area ───────────────────────────────────────────────
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
            "Ready. Select a Page 4 K sample, run burns, then press Cal / File."
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

        # ── Summary Label ────────────────────────────────────────────────
        self.summary_label = QLabel("")
        self.summary_label.setFixedHeight(34)
        self.summary_label.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#333333;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.summary_label)

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

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setStyleSheet(btn_style)
        self.btn_export.clicked.connect(self._on_export)

        self.btn_print = QPushButton("Print")
        self.btn_print.setStyleSheet(btn_style)
        self.btn_print.clicked.connect(self._on_print)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_cal)
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_print)

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

        lbl = QLabel("K Sample:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QComboBox()
        self.sample_name.setFixedWidth(280)
        self.sample_name.setStyleSheet(
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
    # Load Page 3 / Page 4 Data
    # =========================================================================

    def _load_elements(self):
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

    def _load_required_samples(self):
        """
        Load unique K sample names from Page 4.

        Job 2 uses only K samples.
        Blank and "*" are ignored.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_04_drift:
                self.required_samples = []
                return

            page4 = group.page_04_drift

            if not isinstance(page4, dict):
                self.required_samples = []
                return

            rows = page4.get("rows", [])

            if not isinstance(rows, list):
                self.required_samples = []
                return

            samples = set()

            for row in rows:
                sample = str(row.get("k_sample", "")).strip().upper()

                if not sample:
                    continue

                if sample == "*":
                    continue

                samples.add(sample)

            self.required_samples = sorted(samples)

        finally:
            session.close()

    def _populate_sample_dropdown(self):
        self.sample_name.clear()
        self.sample_name.addItem("", "")

        for sample in self.required_samples:
            self.sample_name.addItem(sample, sample)

    def _current_sample_name(self) -> str:
        return str(self.sample_name.currentData() or "").strip().upper()

    # =========================================================================
    # Table / Averages
    # =========================================================================

    def _update_table(self):
        if not self.element_names:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.status_label.setText(
                "No elements configured. Complete Page 3 before running Job 2."
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

    def _update_summary(self):
        self.summary_label.setText(
            f"K samples from Page 4: {', '.join(self.required_samples) if self.required_samples else 'None'}"
        )

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
                "Please complete Page 3 before running Job 2."
            )
            return

        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select a K sample from Page 4."
            )
            return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.sample_name.setEnabled(False)

        self.status_label.setText(f"Starting 1-point recalibration burn for {sample}...")
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params={
                "sample_name": sample,
                "job_type": "2"
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
        if "intensities" in results:
            data = results["intensities"]
        elif "raw_adc" in results:
            data = results["raw_adc"]
        else:
            data = results

        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        self.results.append(data)

        self.st_counter.setText(f"ST No.: {len(self.results)}")
        self._update_table()

        self.status_label.setText(
            f"Burn {len(self.results)} complete for sample {self._current_sample_name()}."
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
                "Reset Current Sample",
                "Clear burns for the currently selected K sample?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self.status_label.setText("Current K sample reset.")

    # =========================================================================
    # Cal / File
    # =========================================================================

    def _on_cal_file(self):
        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please select a K sample before calculating k."
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
                "No valid average intensities are available."
            )
            return

        updated, skipped = self._calculate_and_file_k(sample, averages)

        if updated == 0:
            QMessageBox.warning(
                self,
                "No Rows Updated",
                "No Page 4 rows were updated.\n\n"
                f"Skipped rows: {skipped}"
            )
            return

        QMessageBox.information(
            self,
            "1-Point Recalibration Completed",
            f"k values filed successfully.\n\n"
            f"K Sample: {sample}\n"
            f"Rows updated: {updated}\n"
            f"Rows skipped: {skipped}"
        )

        self.status_label.setText(
            f"Cal / File completed. Updated k for {updated} rows."
        )

    def _calculate_and_file_k(self, sample: str, averages: dict) -> tuple[int, int]:
        """
        Calculate and file k into Page 4.

        For each Page 4 row:
        - K sample must match selected sample.
        - K sample must not be blank or "*".
        - Element must exist in measured averages.
        - K target must be valid and non-zero.
        - alpha and beta are read from Page 4.
        - denominator alpha * I_K + beta must not be zero.

        Formula:
            k = K_Target / (alpha * I_K + beta)
        """
        session = get_session()
        updated = 0
        skipped = 0

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return 0, 0

            page4 = group.page_04_drift

            if not isinstance(page4, dict) or not isinstance(page4.get("rows"), list):
                return 0, 0

            rows = page4["rows"]

            for row in rows:
                elem = str(row.get("name", "")).strip()

                if not elem:
                    skipped += 1
                    continue

                k_sample = str(row.get("k_sample", "")).strip().upper()

                if not k_sample or k_sample == "*":
                    skipped += 1
                    continue

                if k_sample != sample:
                    skipped += 1
                    continue

                if elem not in averages:
                    skipped += 1
                    continue

                try:
                    i_k = float(averages[elem])
                    k_target = float(str(row.get("k_target", "0")).strip() or "0")
                    alpha = float(str(row.get("alpha", "1")).strip() or "1")
                    beta = float(str(row.get("beta", "0")).strip() or "0")
                except (TypeError, ValueError):
                    skipped += 1
                    continue

                if k_target == 0.0:
                    skipped += 1
                    continue

                denominator = (alpha * i_k) + beta

                if denominator == 0.0:
                    skipped += 1
                    continue

                k_coeff = k_target / denominator

                row["k_coeff"] = f"{k_coeff:.4f}"

                # Preserve alpha and beta. If missing, restore neutral defaults.
                if not str(row.get("alpha", "")).strip():
                    row["alpha"] = "1.0000"

                if not str(row.get("beta", "")).strip():
                    row["beta"] = "0.00000"

                updated += 1

            group.page_04_drift = page4
            session.commit()

            return updated, skipped

        finally:
            session.close()

    # =========================================================================
    # Export / Print
    # =========================================================================

    def _on_export(self):
        if not self.results:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Job 2 Results",
            "job2_recalibration_results.csv",
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
            <h1>SpectraSoft Job 2 Recalibration Report - {self.group_name}</h1>
            <p><b>Date:</b> {timestamp}</p>
            <p><b>K Sample:</b> {sample}</p>
            <p><b>Burns:</b> {len(self.results)}</p>

            <table>
                <tr>{headers}</tr>
                {''.join(rows)}
            </table>
        </body>
        </html>
        """

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