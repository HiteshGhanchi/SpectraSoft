"""
SpectraSoft — Job Y: Special 3-Time Analysis

This is a high-precision content analysis job.

Workflow:
1. User enters sample name.
2. User presses Start for repeated burns.
3. Each burn goes through the full Job X correction pipeline:
      Page 4 drift correction
      Page 5 working curve
      Page 6 matrix correction
      Page 7 master correction
      Page 9 purity calculation
4. Table shows Element | AVE | N=1 | N=2 | N=3
5. For 3 burns, AVE is calculated from the best two closest values per element.
6. For 1 or 2 burns, AVE is calculated from available burns.

Important:
- Job Y does not file calibration coefficients.
- Job Y is for final high-precision content reporting.
- Page 8 formatting is used for display order and decimal formatting.
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


class JobYRunPage(QWidget):
    """Job Y: Special 3-Time Analysis page."""

    MAX_BURNS = 3

    def __init__(self, main_window, group_id: int, group_name: str, job_type: str = "Y"):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self.job_type = job_type

        self.worker = None

        # Each item is final content result for one burn:
        # {"C": 0.1234, "SI": 0.6500, ...}
        self.results = []

        self.element_names = []

        self.an_count = 0
        self.tan_count = 0

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_elements()
        self._build_ui()
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

        self.title_label = QLabel(f"Job Y: Special 3-Time Analysis - {self.group_name}")
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
            "Ready. Enter sample name and press Start. Up to 3 burns are used."
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

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(btn_style)
        self.btn_reset.clicked.connect(self._on_reset)

        self.btn_print = QPushButton("Print")
        self.btn_print.setStyleSheet(btn_style)
        self.btn_print.clicked.connect(self._on_print)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setStyleSheet(btn_style)
        self.btn_export.clicked.connect(self._on_export)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
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

        lbl = QLabel("Sample Name:")
        lbl.setStyleSheet("color:black;font:9pt Arial;")
        row.addWidget(lbl)

        self.sample_name = QLineEdit("")
        self.sample_name.setPlaceholderText("Enter unknown sample name")
        self.sample_name.setFixedWidth(260)
        self.sample_name.setStyleSheet(
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
        )
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

    def _load_group_data_for_correction(self) -> dict:
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return {}

            return {
                "page_04_drift": group.page_04_drift or {},
                "page_05_wc": group.page_05_wc or {},
                "page_06_matrix": group.page_06_matrix or {},
                "page_07_master": group.page_07_master or {},
                "page_08_display": group.page_08_display or {},
                "page_09_purity": group.page_09_purity or {},
            }

        finally:
            session.close()

    # =========================================================================
    # Correction Pipeline
    # =========================================================================

    def _apply_content_pipeline(self, intensities: dict) -> dict:
        group_data = self._load_group_data_for_correction()
        engine = CorrectionEngine(group_data)
        return engine.apply_all(intensities)

    def _display_element_names(self) -> list:
        group_data = self._load_group_data_for_correction()
        page8 = group_data.get("page_08_display", {})

        if not isinstance(page8, dict):
            return list(self.element_names)

        rows = page8.get("rows", [])

        if not isinstance(rows, list):
            return list(self.element_names)

        ordered = []

        for row in rows:
            try:
                order = int(float(str(row.get("order", "0")).strip() or "0"))
            except (TypeError, ValueError):
                order = 0

            name = str(row.get("name", "")).strip()

            if order > 0 and name:
                ordered.append((order, name))

        if not ordered:
            return list(self.element_names)

        ordered.sort(key=lambda x: x[0])
        return [name for _, name in ordered]

    def _format_value_for_element(self, elem: str, value) -> str:
        group_data = self._load_group_data_for_correction()
        page8 = group_data.get("page_08_display", {})

        deci = 0
        magn = 0

        if isinstance(page8, dict) and isinstance(page8.get("rows"), list):
            for row in page8["rows"]:
                name = str(row.get("name", "")).strip()

                if name.upper() == elem.upper():
                    deci = self._to_int(row.get("deci", 0), 0)
                    magn = self._to_int(row.get("magn", 0), 0)
                    break

        return CorrectionEngine.format_value(value, deci=deci, magn=magn)

    # =========================================================================
    # Table
    # =========================================================================

    def _update_table(self):
        if not self.element_names:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.status_label.setText(
                "No elements configured. Complete Page 3 before running Job Y."
            )
            return

        display_elements = self._display_element_names()
        num_burns = len(self.results)
        num_cols = 2 + num_burns

        self.table.setRowCount(len(display_elements))
        self.table.setColumnCount(num_cols)

        headers = ["Element", "AVE"]

        for i in range(num_burns):
            headers.append(f"N={i + 1}")

        self.table.setHorizontalHeaderLabels(headers)

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 100)

        for i in range(num_burns):
            self.table.setColumnWidth(2 + i, 100)

        averages = self._calculate_special_averages()

        for row, elem in enumerate(display_elements):
            elem_item = QTableWidgetItem(elem)
            elem_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, elem_item)

            if elem in averages:
                avg_text = self._format_value_for_element(elem, averages[elem])
            else:
                avg_text = ""

            avg_item = QTableWidgetItem(avg_text)
            avg_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 1, avg_item)

            for burn_index, burn in enumerate(self.results):
                if elem in burn:
                    text = self._format_value_for_element(elem, burn[elem])
                else:
                    text = ""

                val_item = QTableWidgetItem(text)
                val_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, 2 + burn_index, val_item)

        self.table.resizeRowsToContents()

    def _calculate_special_averages(self) -> dict:
        averages = {}

        for elem in self.element_names:
            values = []

            for burn in self.results:
                if elem in burn:
                    try:
                        values.append(float(burn[elem]))
                    except (TypeError, ValueError):
                        pass

            if not values:
                continue

            if len(values) <= 2:
                averages[elem] = sum(values) / len(values)
                continue

            # For 3 burns, pick the closest two values.
            best_pair = None
            best_diff = None

            for i in range(len(values)):
                for j in range(i + 1, len(values)):
                    diff = abs(values[i] - values[j])

                    if best_diff is None or diff < best_diff:
                        best_diff = diff
                        best_pair = (values[i], values[j])

            if best_pair:
                averages[elem] = sum(best_pair) / 2.0
            else:
                averages[elem] = sum(values) / len(values)

        return averages

    def _update_footer_counts(self):
        self.an_label.setText(f"AN: {self.an_count}")
        self.tan_label.setText(f"TAN: {self.tan_count}")

    def _to_int(self, value, default=0) -> int:
        try:
            return int(float(str(value).strip()))
        except (TypeError, ValueError):
            return default

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_start(self):
        if self.worker and self.worker.isRunning():
            return

        if len(self.results) >= self.MAX_BURNS:
            QMessageBox.information(
                self,
                "Maximum Burns",
                "Job Y uses up to 3 burns. Reset before running another set."
            )
            return

        if not self.element_names:
            QMessageBox.warning(
                self,
                "No Elements",
                "No elements are configured for this analytical group.\n\n"
                "Please complete Page 3 before running Job Y."
            )
            return

        sample = self._current_sample_name()

        if not sample:
            QMessageBox.warning(
                self,
                "Sample Required",
                "Please enter the sample name before analysis."
            )
            return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.sample_name.setEnabled(False)

        self.status_label.setText(
            f"Starting special analysis burn {len(self.results) + 1}/3 for {sample}..."
        )
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(
            group_id=self.group_id,
            params={
                "sample_name": sample,
                "job_type": "Y"
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
            pre_corrected = results["intensities"]
        elif "raw_adc" in results:
            pre_corrected = results["raw_adc"]
        else:
            pre_corrected = results

        final_content = self._apply_content_pipeline(pre_corrected)

        self.an_count += 1
        self.tan_count += 1
        self._update_footer_counts()

        self.results.append(final_content)

        self.st_counter.setText(f"ST No.: {len(self.results)}")
        self._update_table()

        if len(self.results) >= self.MAX_BURNS:
            self.status_label.setText(
                "Three burns complete. AVE uses the closest two values per element."
            )
        else:
            self.status_label.setText(
                f"Burn {len(self.results)} complete. Run next burn if needed."
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

    def _on_reset(self):
        if self.results:
            reply = QMessageBox.question(
                self,
                "Reset",
                "Clear all burns for this sample?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

        self.results = []
        self.st_counter.setText("ST No.: —")
        self.sample_name.setEnabled(True)
        self._update_table()
        self.status_label.setText("Reset. Ready for new sample.")

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
        title = f"SpectraSoft Job Y Special 3-Time Analysis Report - {self.group_name}"
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
            <h1>{title}</h1>
            <p><b>Date:</b> {timestamp}</p>
            <p><b>Sample:</b> {sample}</p>
            <p><b>Burns:</b> {len(self.results)}</p>
            <p><b>AVE Rule:</b> If 3 burns exist, closest two values are averaged per element.</p>

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

        sample = self._current_sample_name() or "UNKNOWN"

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Job Y Analysis",
            f"joby_special_{sample}.csv",
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