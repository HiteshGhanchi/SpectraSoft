"""
SpectraSoft — Chemical Standards Page

This page stores certified/lab chemical values for working curve standards.

These values are used by the Regression Calculation module together with
Job 7 measured drift-corrected intensities.

Rows:
- Standard sample names

Columns:
- Active Page 3 elements

Saved to:
    AnalyticalGroup.page_05_chemical_standards

Saved JSON example:
{
    "standards": [
        {
            "sample": "STD_01",
            "values": {
                "C": 0.12000,
                "SI": 0.25000,
                "MN": 0.70000
            }
        },
        {
            "sample": "STD_02",
            "values": {
                "C": 0.35000,
                "SI": 0.60000,
                "MN": 1.20000
            }
        }
    ]
}

Notes:
- Sample names are stored uppercase.
- Blank chemical values are allowed and ignored by Regression.
- Regression uses only standards where both:
    1. Job 7 intensity exists
    2. Certified chemical value exists
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QTableWidget,
    QTableWidgetItem, QAbstractItemView, QHeaderView,
    QFileDialog
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup

import csv


class ChemicalStandardsPage(QWidget):
    """
    Chemical standards registration page.

    This is a Regression / Working Curve setup page.
    It does not operate hardware.
    """

    COL_SAMPLE = 0

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        self.element_names = []
        self._updating_table = False

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_elements()
        self._build_ui()
        self._load()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        bar = QLabel(f"Chemical Standards - {self.group_name}")
        bar.setFixedHeight(24)
        bar.setContentsMargins(12, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(
            "background:#5c9bd5;"
            "color:white;"
            "font:bold 10pt Arial;"
        )
        root.addWidget(bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:#d4d0c8;")
        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(14, 14, 14, 10)
        outer_layout.setSpacing(8)

        # ── Page Title ───────────────────────────────────────────────────
        title = QLabel("CHEMICAL STANDARD VALUES")
        title.setFixedHeight(24)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:black;"
            "font:bold 10pt Arial;"
            "border:1px solid #888888;"
            "padding:3px 0px;"
            "}"
        )
        outer_layout.addWidget(title)

        # ── Info Label ───────────────────────────────────────────────────
        self.info_label = QLabel(
            "Enter certified chemical percentages for each standard sample. "
            "Sample names are stored in uppercase. Blank values are allowed."
        )
        self.info_label.setFixedHeight(38)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#555555;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.info_label)

        # ── Table ────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(1 + len(self.element_names))
        self.table.setHorizontalHeaderLabels(["Sample"] + self.element_names)

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
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.table.verticalHeader().setDefaultSectionSize(27)

        header = self.table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setHighlightSections(False)
        header.setStretchLastSection(True)

        self.table.setColumnWidth(self.COL_SAMPLE, 140)

        for col in range(1, self.table.columnCount()):
            self.table.setColumnWidth(col, 90)

        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.table.itemChanged.connect(self._on_item_changed)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Control Buttons ──────────────────────────────────────────────
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_add = QPushButton("Add Standard")
        btn_add.setStyleSheet(self._button_style())
        btn_add.clicked.connect(self._on_add_standard)
        ctrl_layout.addWidget(btn_add)

        btn_delete = QPushButton("Delete Selected")
        btn_delete.setStyleSheet(self._button_style())
        btn_delete.clicked.connect(self._on_delete_selected)
        ctrl_layout.addWidget(btn_delete)

        btn_import_job7 = QPushButton("Import Job 7 Samples")
        btn_import_job7.setStyleSheet(self._button_style())
        btn_import_job7.clicked.connect(self._on_import_job7_samples)
        ctrl_layout.addWidget(btn_import_job7)

        btn_import_csv = QPushButton("Import CSV")
        btn_import_csv.setStyleSheet(self._button_style())
        btn_import_csv.clicked.connect(self._on_import_csv)
        ctrl_layout.addWidget(btn_import_csv)

        btn_export_csv = QPushButton("Export CSV")
        btn_export_csv.setStyleSheet(self._button_style())
        btn_export_csv.clicked.connect(self._on_export_csv)
        ctrl_layout.addWidget(btn_export_csv)

        ctrl_layout.addStretch()

        outer_layout.addLayout(ctrl_layout)

        # ── Bottom Navigation ────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        btn_bar.setStyleSheet("background:#d4d0c8;")

        nav = QHBoxLayout(btn_bar)
        nav.setContentsMargins(12, 4, 12, 8)
        nav.setSpacing(4)

        for text, slot in [
            ("OK", self._on_ok),
            ("Regression", self._on_regression),
            ("Page 5", self._on_page5),
            ("Print", self._on_print),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(self._button_style())
            btn.clicked.connect(slot)
            nav.addWidget(btn)

        nav.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(self._button_style())
        cancel_btn.clicked.connect(self._on_cancel)
        nav.addWidget(cancel_btn)

        root.addWidget(btn_bar)

    # =========================================================================
    # Styles
    # =========================================================================

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
    # Page 3 Elements
    # =========================================================================

    def _load_elements(self):
        """
        Load active element/display names from Page 3.

        Uses the same display key as analysis jobs:
            NAME if present, else ELE, else ITG fallback.
        """
        self.element_names = []

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

    # =========================================================================
    # Table Helpers
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        """
        Force sample names to uppercase.
        """
        if self._updating_table:
            return

        if item.column() != self.COL_SAMPLE:
            return

        current = item.text()
        upper = current.upper()

        if current != upper:
            self._updating_table = True
            item.setText(upper)
            self._updating_table = False

    def _add_empty_row(self, sample: str = "", values: dict = None):
        values = values or {}

        row = self.table.rowCount()
        self.table.insertRow(row)

        sample_item = QTableWidgetItem(str(sample or "").upper())
        sample_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        sample_item.setFlags(
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsEditable
        )
        self.table.setItem(row, self.COL_SAMPLE, sample_item)

        for idx, elem in enumerate(self.element_names, start=1):
            value = values.get(elem, "")

            if value == "" or value is None:
                text = ""
            else:
                try:
                    text = f"{float(value):.5f}"
                except (TypeError, ValueError):
                    text = ""

            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            item.setFlags(
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsEditable
            )
            self.table.setItem(row, idx, item)

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)

        if not item:
            return ""

        return item.text().strip()

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            data = group.page_05_chemical_standards if group else {}

            standards = []

            if isinstance(data, dict):
                standards = data.get("standards", [])

                if not isinstance(standards, list):
                    standards = []

        finally:
            session.close()

        self._updating_table = True
        self.table.setRowCount(0)

        for entry in standards:
            sample = str(entry.get("sample", "")).strip().upper()
            values = entry.get("values", {})

            if not isinstance(values, dict):
                values = {}

            if sample:
                self._add_empty_row(sample, values)

        self._updating_table = False

        if self.table.rowCount() == 0:
            self._add_empty_row()

    def _collect(self) -> dict:
        standards = []

        for row in range(self.table.rowCount()):
            sample = self._cell_text(row, self.COL_SAMPLE).upper()

            if not sample:
                continue

            values = {}

            for col, elem in enumerate(self.element_names, start=1):
                text = self._cell_text(row, col)

                if text == "":
                    continue

                try:
                    values[elem] = float(text)
                except ValueError:
                    raise ValueError(
                        f"Invalid numeric value for sample '{sample}', element '{elem}': {text}"
                    )

            standards.append({
                "sample": sample,
                "values": values,
            })

        return {
            "standards": standards
        }

    def _validate(self) -> bool:
        seen = set()

        for row in range(self.table.rowCount()):
            sample = self._cell_text(row, self.COL_SAMPLE).upper()

            # Completely blank rows are allowed.
            if not sample:
                continue

            if sample in seen:
                self._show_msg(
                    "Duplicate Sample",
                    f"Sample '{sample}' is entered more than once.",
                    QMessageBox.Icon.Warning
                )
                return False

            seen.add(sample)

            for col, elem in enumerate(self.element_names, start=1):
                text = self._cell_text(row, col)

                if text == "":
                    continue

                try:
                    float(text)
                except ValueError:
                    self._show_msg(
                        "Invalid Value",
                        f"Sample '{sample}', element '{elem}' has invalid value:\n{text}",
                        QMessageBox.Icon.Warning
                    )
                    return False

        return True

    def _save(self):
        data = self._collect()

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group:
                group.page_05_chemical_standards = data
                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Button Actions
    # =========================================================================

    def _on_add_standard(self):
        self._add_empty_row()

    def _on_delete_selected(self):
        selected = self.table.selectionModel().selectedRows()

        if not selected:
            self._show_msg(
                "Delete",
                "Please select a row to delete.",
                QMessageBox.Icon.Warning
            )
            return

        row = selected[0].row()
        sample = self._cell_text(row, self.COL_SAMPLE)

        if QMessageBox.question(
            self,
            "Delete Standard",
            f"Delete selected standard '{sample or '(blank)'}'?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self.table.removeRow(row)

        if self.table.rowCount() == 0:
            self._add_empty_row()

    def _on_import_job7_samples(self):
        """
        Import sample names from Job 7 working curve measurements.

        This fills only missing sample rows.
        It does not overwrite chemical values.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            data = group.page_05_wc_measurements if group else {}

            measurements = []

            if isinstance(data, dict):
                measurements = data.get("measurements", [])

                if not isinstance(measurements, list):
                    measurements = []

        finally:
            session.close()

        if not measurements:
            self._show_msg(
                "No Job 7 Data",
                "No Job 7 working curve measurements are available.",
                QMessageBox.Icon.Warning
            )
            return

        existing = set()

        for row in range(self.table.rowCount()):
            sample = self._cell_text(row, self.COL_SAMPLE).upper()

            if sample:
                existing.add(sample)

        added = 0

        for entry in measurements:
            sample = str(entry.get("sample", "")).strip().upper()

            if not sample:
                continue

            if sample in existing:
                continue

            self._add_empty_row(sample)
            existing.add(sample)
            added += 1

        self._show_msg(
            "Import Complete",
            f"Imported {added} sample name(s) from Job 7 measurements."
        )

    def _on_import_csv(self):
        """
        Import CSV format:

            Sample,C,SI,MN,...
            STD_01,0.12,0.25,0.70
            STD_02,0.35,0.60,1.20

        Headers must match Page 3 element/display names.
        """
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Chemical Standards",
            "",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            if not reader.fieldnames or "Sample" not in reader.fieldnames:
                raise ValueError("CSV must contain a 'Sample' column.")

            self.table.setRowCount(0)

            for csv_row in rows:
                sample = str(csv_row.get("Sample", "")).strip().upper()

                if not sample:
                    continue

                values = {}

                for elem in self.element_names:
                    raw = str(csv_row.get(elem, "")).strip()

                    if raw == "":
                        continue

                    values[elem] = float(raw)

                self._add_empty_row(sample, values)

            if self.table.rowCount() == 0:
                self._add_empty_row()

            self._show_msg("Imported", "Chemical standards imported successfully.")

        except Exception as e:
            self._show_msg(
                "Import Failed",
                str(e),
                QMessageBox.Icon.Critical
            )

    def _on_export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chemical Standards",
            "chemical_standards.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                writer.writerow(["Sample"] + self.element_names)

                for row in range(self.table.rowCount()):
                    sample = self._cell_text(row, self.COL_SAMPLE)

                    if not sample:
                        continue

                    out_row = [sample]

                    for col in range(1, self.table.columnCount()):
                        out_row.append(self._cell_text(row, col))

                    writer.writerow(out_row)

            self._show_msg(
                "Exported",
                f"Chemical standards exported to:\n{path}"
            )

        except Exception as e:
            self._show_msg(
                "Export Failed",
                str(e),
                QMessageBox.Icon.Critical
            )

    def _on_ok(self):
        if not self._validate():
            return

        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Data",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        self._show_msg("Saved", "Chemical standard values saved successfully.")

    def _on_regression(self):
        if not self._validate():
            return

        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Data",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        try:
            from ui.regression.regression_calculation_page import RegressionCalculationPage

            self.main_window.set_right_widget(
                RegressionCalculationPage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            self._show_msg(
                "Regression",
                "Regression Calculation page is not built yet."
            )

    def _on_page5(self):
        if not self._validate():
            return

        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Data",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        try:
            from ui.anainf.page_05_working_curve import WorkingCurvePage

            self.main_window.set_right_widget(
                WorkingCurvePage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            self._show_msg(
                "Page 5",
                "Working Curve Coefficients page is not built yet."
            )

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        if self._show_question("Cancel", "Discard changes?"):
            self._load()
            self.main_window._show_home_content()

    # =========================================================================
    # Message Helpers
    # =========================================================================

    def _show_msg(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
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
        msg.exec()

    def _show_question(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
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
        return msg.exec() == QMessageBox.StandardButton.Yes