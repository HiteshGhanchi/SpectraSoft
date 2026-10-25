"""Qt report page for stored analytical results."""

from __future__ import annotations

import json
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPageLayout, QPen, QBrush
from PyQt6.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt6.QtWidgets import (
    QFileDialog,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.analysis.report_service import (
    CORRECTION_SCHEMA_NOTE,
    ReportFilters,
    analytical_frequency,
    build_histogram,
    daily_report,
    export_results_csv,
    finite_number,
    filter_results,
    result_detail,
    stability_report,
    x_r_report,
)
from core.persistence.database import get_session
from core.persistence.result_repository import list_analysis_results
from ui.theme import COLORS


class HistogramWidget(QFrame):
    """Small dependency-free histogram rendered with QPainter."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.histogram = None
        self.setObjectName("chartSurface")
        self.setMinimumHeight(180)
        self.setStyleSheet(
            f"background:{COLORS['surface']};border:1px solid {COLORS['border_strong']};"
        )

    def set_histogram(self, histogram):
        self.histogram = histogram
        self.update()

    def paintEvent(self, a0):  # pragma: no cover - Qt painting is smoke-tested by construction
        super().paintEvent(a0)
        if not self.histogram:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        margin = 24
        chart = self.rect().adjusted(margin, 12, -12, -margin)
        counts = self.histogram.get("counts", [])
        maximum = max(counts or [1])
        bar_width = chart.width() / max(1, len(counts))
        painter.setPen(QPen(QColor(COLORS["muted"]), 1))
        painter.drawLine(chart.left(), chart.bottom(), chart.right(), chart.bottom())
        painter.drawLine(chart.left(), chart.top(), chart.left(), chart.bottom())
        painter.setBrush(QBrush(QColor(COLORS["chart_teal"])))
        for index, count in enumerate(counts):
            height = chart.height() * count / maximum
            painter.drawRect(
                int(chart.left() + index * bar_width + 1),
                int(chart.bottom() - height),
                max(1, int(bar_width - 2)),
                max(1, int(height)),
            )


class ResultReportPage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self._rows = []
        self._display_result_map = {}
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        title = QLabel(f"Filed Analytical Results and Reports - {self.group_name}")
        title.setStyleSheet("background:#5c9bd5;color:white;font:bold 10pt Arial;padding:5px;")
        root.addWidget(title)

        outer = QFrame()
        outer.setStyleSheet("background:#d4d0c8;")
        layout = QVBoxLayout(outer)
        filters = QGridLayout()
        filters.addWidget(QLabel("Report:"), 0, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Daily by group", "Daily by product", "Daily by sample",
            "Long-term X-R", "Analytical frequency", "Stability", "Histogram",
            "Stored result detail", "Stored data modification (read-only)",
        ])
        self.mode_combo.currentIndexChanged.connect(self._load)
        filters.addWidget(self.mode_combo, 0, 1)
        filters.addWidget(QLabel("Job:"), 0, 2)
        self.job_combo = QComboBox()
        self.job_combo.addItems(["All", "X", "Y"])
        self.job_combo.currentIndexChanged.connect(self._load)
        filters.addWidget(self.job_combo, 0, 3)
        filters.addWidget(QLabel("Element:"), 0, 4)
        self.element_combo = QComboBox()
        self.element_combo.currentIndexChanged.connect(self._load)
        filters.addWidget(self.element_combo, 0, 5)
        filters.addWidget(QLabel("Start (YYYY-MM-DD):"), 1, 0)
        self.start_date_edit = QLineEdit()
        self.start_date_edit.setPlaceholderText("optional")
        filters.addWidget(self.start_date_edit, 1, 1)
        filters.addWidget(QLabel("End (YYYY-MM-DD):"), 1, 2)
        self.end_date_edit = QLineEdit()
        self.end_date_edit.setPlaceholderText("optional")
        filters.addWidget(self.end_date_edit, 1, 3)
        filters.addWidget(QLabel("Sample:"), 1, 4)
        self.sample_edit = QLineEdit()
        self.sample_edit.setPlaceholderText("contains...")
        filters.addWidget(self.sample_edit, 1, 5)
        filters.addWidget(QLabel("Product:"), 2, 0)
        self.product_edit = QLineEdit()
        self.product_edit.setPlaceholderText("snapshot product/specification")
        filters.addWidget(self.product_edit, 2, 1, 1, 3)
        filters.addWidget(QLabel("Lower limit:"), 3, 0)
        self.lower_limit_edit = QLineEdit()
        self.lower_limit_edit.setPlaceholderText("histogram optional")
        filters.addWidget(self.lower_limit_edit, 3, 1)
        filters.addWidget(QLabel("Upper limit:"), 3, 2)
        self.upper_limit_edit = QLineEdit()
        self.upper_limit_edit.setPlaceholderText("histogram optional")
        filters.addWidget(self.upper_limit_edit, 3, 3)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._load)
        filters.addWidget(self.refresh_button, 3, 5)
        layout.addLayout(filters)

        action_row = QHBoxLayout()
        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self._export_csv)
        action_row.addWidget(self.export_button)
        self.print_button = QPushButton("Print preview")
        self.print_button.clicked.connect(self._on_print_preview)
        action_row.addWidget(self.print_button)
        self.modification_note = QLabel(CORRECTION_SCHEMA_NOTE)
        self.modification_note.setWordWrap(True)
        self.modification_note.setStyleSheet("color:#704000;")
        action_row.addWidget(self.modification_note, stretch=1)
        layout.addLayout(action_row)

        self.summary_label = QLabel("No filed results")
        layout.addWidget(self.summary_label)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Date", "Job", "Sample", "Product", "Value"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemSelectionChanged.connect(self._show_selected_detail)
        layout.addWidget(self.table, stretch=1)
        self.histogram_widget = HistogramWidget()
        self.histogram_widget.hide()
        layout.addWidget(self.histogram_widget)
        self.detail_label = QLabel("Select a row to see burns, method snapshot, and flags.")
        self.detail_label.setWordWrap(True)
        self.detail_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.detail_label)
        root.addWidget(outer, stretch=1)

    def _parse_date(self, text: str):
        value = text.strip()
        if not value:
            return None
        for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        return None

    def _filters(self):
        return ReportFilters(
            start=self._parse_date(self.start_date_edit.text()),
            end=self._parse_date(self.end_date_edit.text()),
            sample_name=self.sample_edit.text(),
            job="" if self.job_combo.currentText() == "All" else self.job_combo.currentText(),
            product_name=self.product_edit.text(),
        )

    def _limits(self):
        try:
            lower = float(self.lower_limit_edit.text().strip())
            upper = float(self.upper_limit_edit.text().strip())
        except (TypeError, ValueError):
            return None, None
        return (lower, upper) if lower < upper else (None, None)

    def _load(self):
        session = get_session()
        try:
            all_rows = list_analysis_results(
                session,
                self.group_id,
                None if self.job_combo.currentText() == "All" else self.job_combo.currentText(),
            )
            self._rows = filter_results(all_rows, self._filters())
        finally:
            session.close()
        self._refresh_elements()
        self._render_mode()

    def _refresh_elements(self):
        selected = self.element_combo.currentText()
        elements = sorted({
            str(element)
            for result in self._rows
            for element in (getattr(result, "final_concentrations", None) or {})
        })
        self.element_combo.blockSignals(True)
        self.element_combo.clear()
        self.element_combo.addItems(elements)
        if selected in elements:
            self.element_combo.setCurrentText(selected)
        self.element_combo.blockSignals(False)

    def _set_table(self, headers, rows, result_map=None):
        self._display_result_map = result_map or {}
        self.table.clearContents()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column, value in enumerate(row):
                self.table.setItem(row_index, column, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()

    def _render_mode(self):
        self.histogram_widget.hide()
        mode = self.mode_combo.currentText()
        element = self.element_combo.currentText().strip()
        if mode == "Daily by group":
            groups = daily_report(self._rows, "group")
            rows = [(item["key"], item["count"], ", ".join(item["samples"]), ", ".join(item["jobs"]), ", ".join(item["elements"])) for item in groups]
            self._set_table(["Day", "Count", "Samples", "Jobs", "Elements"], rows, {i: group["results"][0] for i, group in enumerate(groups) if group["results"]})
            self.summary_label.setText(f"Daily group report: {len(self._rows)} filed results")
        elif mode in {"Daily by product", "Daily by sample"}:
            grouping = "product" if mode.endswith("product") else "sample"
            groups = daily_report(self._rows, grouping)
            rows = [(item["key"], item["count"], ", ".join(item["samples"]), ", ".join(item["jobs"]), ", ".join(item["elements"])) for item in groups]
            self._set_table(["Group", "Count", "Jobs", "Samples", "Elements"], rows, {i: group["results"][0] for i, group in enumerate(groups) if group["results"]})
            self.summary_label.setText(f"{mode}: {len(self._rows)} filed results")
        elif mode == "Long-term X-R":
            report = x_r_report(self._rows, element) if element else {"points": []}
            rows = [(index + 1, point["occurred_at"], point["count"], f"{point['xbar']:.6g}" if point["xbar"] is not None else "", f"{point['range']:.6g}" if point["range"] is not None else "") for index, point in enumerate(report["points"])]
            self._set_table(["Point", "Date", "Burns", "X-bar", "R"], rows, {i: point["result"] for i, point in enumerate(report["points"])})
            self.summary_label.setText(f"X-R: {len(report['points'])} subgroups; element={element or '(select element)'}")
        elif mode == "Analytical frequency":
            report = analytical_frequency(self._rows)
            rows = [(name, value) for name, value in report["by_day"].items()]
            self._set_table(["Day", "Analysis count"], rows)
            self.summary_label.setText(f"Analytical frequency total: {report['total']}")
        elif mode == "Stability":
            report = stability_report(self._rows, element) if element else {"points": []}
            rows = [(point["occurred_at"], point["sample_name"], point["value"]) for point in report["points"]]
            self._set_table(["Date", "Sample", "Value"], rows, {i: point["result"] for i, point in enumerate(report["points"])})
            self.summary_label.setText(f"Stability: count={report.get('count', 0)} average={report.get('average')} range={report.get('range')}")
        elif mode == "Histogram":
            values = []
            if element:
                for result in self._rows:
                    value = (getattr(result, "final_concentrations", None) or {}).get(element)
                    number = finite_number(value)
                    if number is not None:
                        values.append(number)
            lower_limit, upper_limit = self._limits()
            histogram = build_histogram(values, lower_limit, upper_limit)
            summary = histogram["summary"]
            self._set_table(["Metric", "Count", "Average", "Range", "Capability"], [[element or "(select element)", summary["count"], summary["average"], summary["range"], f"Cp={summary['cp']} Cpk={summary['cpk']}"]])
            self.histogram_widget.set_histogram(histogram)
            self.histogram_widget.show()
            self.summary_label.setText(f"Histogram: under={summary['under_limit']} over={summary['over_limit']}; limits unavailable unless supplied")
        else:
            rows = []
            result_map = {}
            for index, result in enumerate(self._rows):
                detail = result_detail(result)
                rows.append((detail["occurred_at"], detail["job"], detail["sample_name"], detail["product_name"], detail["final_concentrations"]))
                result_map[index] = result
            self._set_table(["Date", "Job", "Sample", "Product", "Final concentrations"], rows, result_map)
            if mode.startswith("Stored data modification"):
                self.summary_label.setText(
                    f"Stored data modification is read-only: {len(self._rows)} original results shown"
                )
            else:
                self.summary_label.setText(f"Stored result detail: {len(self._rows)} results")
        self._show_selected_detail()

    def _show_selected_detail(self):
        index = self.table.currentRow()
        result = self._display_result_map.get(index)
        if result is None and self._rows:
            result = self._rows[0]
        if result is None:
            self.detail_label.setText("No filed result matches the current filters.")
            return
        detail = result_detail(result)
        self.detail_label.setText(
            "Burns: " + json.dumps(detail["burns"], sort_keys=True, default=str)
            + " | Averages: " + json.dumps(detail["averages"], sort_keys=True, default=str)
            + " | Flags: " + json.dumps(detail["flags"], sort_keys=True, default=str)
            + " | method: " + json.dumps(detail["method_snapshot"], sort_keys=True, default=str)
        )

    def _export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export filed results", "filed_results.csv", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(export_results_csv(self._rows, include_details=True))
            self.summary_label.setText(f"Exported {len(self._rows)} results to {path}")
        except OSError as exc:
            QMessageBox.warning(self, "Export failed", str(exc))

    def _on_print_preview(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setPageOrientation(QPageLayout.Orientation.Landscape)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self._render_print_page)
        preview.exec()

    def _render_print_page(self, printer):
        painter = QPainter(printer)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(60, 60, f"SpectraSoft report - {self.group_name}")
        painter.drawText(60, 84, f"Mode: {self.mode_combo.currentText()}   Results: {len(self._rows)}")
        y = 115
        for row in range(min(self.table.rowCount(), 35)):
            values = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    values.append(item.text())
            painter.drawText(60, y, " | ".join(values))
            y += 18
        painter.end()
