"""
SpectraSoft — Page 9: Purity Calculation Information

Note:
- In the original manual, this corresponds to Page 10 / Screen 5.13.
- In this modern software, old Page 9 Data Transmission is skipped.
- Therefore this page is stored as:
      AnalyticalGroup.page_09_purity

Purpose:
- Defines whether purity / balance calculation is active.
- Defines which element is the base element.
- Defines which elements are impurities to subtract from 100%.

Manual-style logic:
- Calculation Y/N:
    Y = purity calculation active
    N = purity calculation inactive

- +/-:
    + = Base element calculated by balance
    - = Impurity element subtracted from 100%
    blank = ignored

Formula:
    C_base = 100 - sum(C_impurities)

Defaults:
    Calculation Y/N = N
    +/- markings = blank for all rows
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QComboBox
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup


class PurityCalculationPage(QWidget):
    """
    Page 9 in this app: Purity Calculation Information.

    Original manual equivalent:
        Page 10 / Screen 5.13
    """

    COL_AR = 0
    COL_NAME = 1
    COL_MARK = 2

    HEADERS = [
        "AR-No.",
        "NAME",
        "+/-",
    ]

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name
        self._updating_table = False

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

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
        bar = QLabel(f"Purity Calculation - {self.group_name}")
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
        title = QLabel("PURITY CALCULATION INFORMATION")
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

        # ── Calculation Switch ───────────────────────────────────────────
        switch_row = QHBoxLayout()
        switch_row.setSpacing(8)

        calc_label = QLabel("Calculation Y/N:")
        calc_label.setStyleSheet("font:9pt Arial;color:black;")
        switch_row.addWidget(calc_label)

        self.calc_combo = QComboBox()
        self.calc_combo.addItems(["N", "Y"])
        self.calc_combo.setFixedWidth(70)
        self.calc_combo.setStyleSheet(
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
        switch_row.addWidget(self.calc_combo)

        switch_row.addStretch()

        outer_layout.addLayout(switch_row)

        # ── Help Note ────────────────────────────────────────────────────
        note = QLabel(
            "Use '+' for the base element calculated by balance. "
            "Use '-' for impurity elements subtracted from 100%. "
            "Blank rows are ignored. Default Calculation Y/N is N."
        )
        note.setFixedHeight(42)
        note.setWordWrap(True)
        note.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#555555;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(note)

        # ── Table ────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

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

        self.table.setColumnWidth(self.COL_AR, 70)
        self.table.setColumnWidth(self.COL_NAME, 140)
        self.table.setColumnWidth(self.COL_MARK, 80)

        for col in range(len(self.HEADERS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.table.itemChanged.connect(self._on_item_changed)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Control Row ──────────────────────────────────────────────────
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_reset = QPushButton("Reset to Defaults")
        btn_reset.setStyleSheet(self._button_style())
        btn_reset.clicked.connect(self._on_reset)
        ctrl_layout.addWidget(btn_reset)

        ctrl_layout.addStretch()

        info_lbl = QLabel(
            "If Calculation Y/N is N, Job X will skip purity balance calculation."
        )
        info_lbl.setStyleSheet(
            "QLabel{"
            "color:#555555;"
            "font:9pt Arial;"
            "border:none;"
            "background:#d4d0c8;"
            "}"
        )
        ctrl_layout.addWidget(info_lbl)

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
            ("Previous", self._on_pre),
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
    # Page 3 Rows
    # =========================================================================

    def _rows_from_page3(self) -> list:
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_03_channel:
                return []

            if not isinstance(group.page_03_channel, list):
                return []

            rows = []

            for idx, entry in enumerate(group.page_03_channel):
                name = str(entry.get("name", "")).strip()
                ele = str(entry.get("ele", "")).strip()
                itg = str(entry.get("itg", "")).strip()

                display_name = name or ele or (f"ITG{itg}" if itg else "")

                if not display_name:
                    continue

                rows.append({
                    "ar_no": str(idx + 1),
                    "name": display_name,
                    "mark": "",
                })

            return rows

        finally:
            session.close()

    # =========================================================================
    # Table Population
    # =========================================================================

    def _populate_table(self, rows: list):
        self._updating_table = True

        self.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            self._set_cell(
                row_idx,
                self.COL_AR,
                str(row_data.get("ar_no", row_idx + 1)),
                editable=False
            )

            self._set_cell(
                row_idx,
                self.COL_NAME,
                str(row_data.get("name", "")),
                editable=False
            )

            mark = str(row_data.get("mark", "")).strip()

            if mark not in ["", "+", "-"]:
                mark = ""

            self._set_cell(row_idx, self.COL_MARK, mark)

        self.table.resizeRowsToContents()

        self._updating_table = False

    def _set_cell(self, row: int, col: int, text: str, editable: bool = True):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

        if editable:
            flags |= Qt.ItemFlag.ItemIsEditable
        else:
            item.setBackground(Qt.GlobalColor.lightGray)

        item.setFlags(flags)
        self.table.setItem(row, col, item)

    # =========================================================================
    # Edit Validation
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._updating_table:
            return

        if item.column() != self.COL_MARK:
            return

        value = item.text().strip()

        if value not in ["", "+", "-"]:
            self._updating_table = True
            item.setText("")
            self._updating_table = False

            self._show_msg(
                "Invalid Mark",
                "+/- value must be blank, '+', or '-'.",
                QMessageBox.Icon.Warning
            )

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_09_purity:
                data = group.page_09_purity

                if isinstance(data, dict):
                    calc = str(data.get("calculation", "N")).strip().upper()

                    if calc not in ["Y", "N"]:
                        calc = "N"

                    self.calc_combo.setCurrentText(calc)

                    if isinstance(data.get("rows"), list):
                        saved_rows = data["rows"]
                        page3_rows = self._rows_from_page3()
                        merged_rows = self._merge_page3_with_saved(page3_rows, saved_rows)
                        self._populate_table(merged_rows)
                        return

        finally:
            session.close()

        self.calc_combo.setCurrentText("N")
        self._populate_table(self._rows_from_page3())

    def _merge_page3_with_saved(self, page3_rows: list, saved_rows: list) -> list:
        saved_lookup = {}

        for row in saved_rows:
            ar_no = str(row.get("ar_no", "")).strip()
            name = str(row.get("name", "")).strip()

            if ar_no:
                saved_lookup[f"AR:{ar_no}"] = row

            if name:
                saved_lookup[f"NAME:{name.upper()}"] = row

        merged = []

        for row in page3_rows:
            ar_key = f"AR:{str(row.get('ar_no', '')).strip()}"
            name_key = f"NAME:{str(row.get('name', '')).strip().upper()}"

            saved = saved_lookup.get(ar_key) or saved_lookup.get(name_key)

            if saved:
                merged_row = dict(row)

                if "mark" in saved:
                    merged_row["mark"] = saved.get("mark")

                merged.append(merged_row)
            else:
                merged.append(row)

        return merged

    def _collect(self) -> dict:
        rows = []

        calc = self.calc_combo.currentText().strip().upper()

        if calc not in ["Y", "N"]:
            calc = "N"

        for row in range(self.table.rowCount()):
            mark = self._cell_text(row, self.COL_MARK)

            if mark not in ["", "+", "-"]:
                mark = ""

            rows.append({
                "ar_no": self._cell_text(row, self.COL_AR),
                "name": self._cell_text(row, self.COL_NAME),
                "mark": mark,
            })

        return {
            "calculation": calc,
            "rows": rows,
        }

    def _validate(self) -> bool:
        calc = self.calc_combo.currentText().strip().upper()

        if calc != "Y":
            return True

        base_count = 0

        for row in range(self.table.rowCount()):
            mark = self._cell_text(row, self.COL_MARK)

            if mark == "+":
                base_count += 1

        if base_count != 1:
            self._show_msg(
                "Invalid Purity Setup",
                "When Calculation Y/N is Y, exactly one base element must be marked with '+'.",
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
                group.page_09_purity = data
                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        return item.text().strip() if item else ""

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_reset(self):
        if QMessageBox.question(
            self,
            "Reset",
            "Reset purity calculation information to defaults?\n\n"
            "Calculation Y/N = N\n"
            "+/- markings = blank\n\n"
            "This only changes the table. Click OK to save.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self.calc_combo.setCurrentText("N")
        self._populate_table(self._rows_from_page3())

    def _on_ok(self):
        if not self._validate():
            return

        self._save()
        self._show_msg("Saved", "Purity calculation information saved successfully.")

    def _on_pre(self):
        if not self._validate():
            return

        self._save()

        try:
            from ui.anainf.page_08_display import DisplayOrderPage

            self.main_window.set_right_widget(
                DisplayOrderPage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            pass

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