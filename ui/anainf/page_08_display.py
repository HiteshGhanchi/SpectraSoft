"""
SpectraSoft — Page 8: Display & Print Format

Manual-style Page 8 table:

AR-No. | NAME | ORDER | FIG | DECI | MAGN

Purpose:
- Controls display and print order for analytical results.
- Controls numeric formatting for final content analysis display/reporting.

Column meaning:
- ORDER:
    Display/print sequence.
    0 = not configured / not printed in old software.
    In this modern app, Job X may use fallback:
        if all ORDER values are 0, display all elements in Page 3 order.
        if any ORDER values are > 0, display only ORDER > 0 sorted by ORDER.

- FIG:
    Total display/print character width.
    Mostly useful for old fixed-width printers.
    Stored for compatibility.

- DECI:
    Number of decimal places.
    0 = floating/default formatting in old software.
    In this modern app, 0 may be interpreted as default precision.

- MAGN:
    Power-of-10 display multiplier.
    Example:
        actual value = 0.0021
        MAGN = 4
        displayed value = 21.0

Defaults:
    ORDER = 0
    FIG   = 0
    DECI  = 0
    MAGN  = 0

Saved to:
    AnalyticalGroup.page_08_display
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup


class DisplayOrderPage(QWidget):
    """
    Page 8: Analytical Element Display and Printing Order.
    """

    COL_AR = 0
    COL_NAME = 1
    COL_ORDER = 2
    COL_FIG = 3
    COL_DECI = 4
    COL_MAGN = 5

    HEADERS = [
        "AR-No.",
        "NAME",
        "ORDER",
        "FIG",
        "DECI",
        "MAGN",
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
        bar = QLabel(f"Display & Print Format - {self.group_name}")
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
        title = QLabel("ANALYTICAL ELEMENT DISPLAY AND PRINTING ORDER")
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

        # ── Help Note ────────────────────────────────────────────────────
        note = QLabel(
            "ORDER controls report sequence. FIG is display width. DECI is decimal places. "
            "MAGN applies 10^MAGN display scaling. Defaults are all 0."
        )
        note.setFixedHeight(38)
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
        self.table.setColumnWidth(self.COL_NAME, 130)
        self.table.setColumnWidth(self.COL_ORDER, 90)
        self.table.setColumnWidth(self.COL_FIG, 90)
        self.table.setColumnWidth(self.COL_DECI, 90)
        self.table.setColumnWidth(self.COL_MAGN, 90)

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
            "If all ORDER values are 0, Job X can display active elements in Page 3 order."
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
            ("Next", self._on_next),
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
        """
        Build Page 8 rows from Page 3 active analytical rows.

        AR-No. and NAME come from Page 3.
        Display/print values default to 0.
        """
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
                    "order": "0",
                    "fig": "0",
                    "deci": "0",
                    "magn": "0",
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

            self._set_cell(
                row_idx,
                self.COL_ORDER,
                self._normalize_int_text(row_data.get("order", ""), "0")
            )

            self._set_cell(
                row_idx,
                self.COL_FIG,
                self._normalize_int_text(row_data.get("fig", ""), "0")
            )

            self._set_cell(
                row_idx,
                self.COL_DECI,
                self._normalize_int_text(row_data.get("deci", ""), "0")
            )

            self._set_cell(
                row_idx,
                self.COL_MAGN,
                self._normalize_int_text(row_data.get("magn", ""), "0")
            )

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
    # Edit Normalization
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._updating_table:
            return

        if item.column() not in {
            self.COL_ORDER,
            self.COL_FIG,
            self.COL_DECI,
            self.COL_MAGN,
        }:
            return

        current = item.text().strip()
        normalized = self._normalize_int_text(current, "0")

        if current != normalized:
            self._updating_table = True
            item.setText(normalized)
            self._updating_table = False

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_08_display:
                data = group.page_08_display

                if isinstance(data, dict) and isinstance(data.get("rows"), list):
                    saved_rows = data["rows"]

                    page3_rows = self._rows_from_page3()
                    merged_rows = self._merge_page3_with_saved(page3_rows, saved_rows)

                    self._populate_table(merged_rows)
                    return

        finally:
            session.close()

        self._populate_table(self._rows_from_page3())

    def _merge_page3_with_saved(self, page3_rows: list, saved_rows: list) -> list:
        """
        Merge saved Page 8 data into current Page 3 row order.
        """
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

                for key in ["order", "fig", "deci", "magn"]:
                    if key in saved:
                        merged_row[key] = saved.get(key)

                merged.append(merged_row)
            else:
                merged.append(row)

        return merged

    def _collect(self) -> dict:
        rows = []

        for row in range(self.table.rowCount()):
            row_data = {
                "ar_no": self._cell_text(row, self.COL_AR),
                "name": self._cell_text(row, self.COL_NAME),
                "order": self._normalize_int_text(
                    self._cell_text(row, self.COL_ORDER),
                    "0"
                ),
                "fig": self._normalize_int_text(
                    self._cell_text(row, self.COL_FIG),
                    "0"
                ),
                "deci": self._normalize_int_text(
                    self._cell_text(row, self.COL_DECI),
                    "0"
                ),
                "magn": self._normalize_int_text(
                    self._cell_text(row, self.COL_MAGN),
                    "0"
                ),
            }

            rows.append(row_data)

        return {
            "rows": rows
        }

    def _save(self):
        data = self._collect()

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group:
                group.page_08_display = data
                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        return item.text().strip() if item else ""

    def _normalize_int_text(self, value, default: str = "0") -> str:
        raw = str(value or "").strip()

        if raw == "":
            raw = default

        try:
            num = int(float(raw))
        except (TypeError, ValueError):
            num = int(default)

        return str(num)

    # =========================================================================
    # Public Helper for Job X Later
    # =========================================================================

    @staticmethod
    def format_value(value, deci: int = 0, magn: int = 0) -> str:
        """
        Utility to format final content values according to Page 8 rules.

        This can be reused later by Job X.

        Rule:
        - Apply multiplier: displayed = value * (10 ** magn)
        - If deci > 0: fixed decimal places
        - If deci == 0: use default floating format
        """
        try:
            val = float(value)
        except (TypeError, ValueError):
            val = 0.0

        try:
            m = int(magn)
        except (TypeError, ValueError):
            m = 0

        try:
            d = int(deci)
        except (TypeError, ValueError):
            d = 0

        displayed = val * (10 ** m)

        if d > 0:
            return f"{displayed:.{d}f}"

        return f"{displayed:.6g}"

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_reset(self):
        if QMessageBox.question(
            self,
            "Reset",
            "Reset Page 8 display and print format to defaults?\n\n"
            "ORDER = 0\n"
            "FIG = 0\n"
            "DECI = 0\n"
            "MAGN = 0\n\n"
            "This only changes the table. Click OK to save.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self._populate_table(self._rows_from_page3())

    def _on_ok(self):
        self._save()
        self._show_msg("Saved", "Display and print format saved successfully.")

    def _on_next(self):
        self._save()

        # Old manual Page 9 Data Transmission is skipped in this modern app.
        # Manual Page 10 Purity Calculation is stored as page_09_purity in schema.
        try:
            from ui.anainf.page_09_purity import PurityCalculationPage

            self.main_window.set_right_widget(
                PurityCalculationPage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            self._show_msg(
                "Next Page",
                "Purity Calculation page is not built yet.\n\n"
                "Data Transmission page is intentionally skipped for now."
            )

    def _on_pre(self):
        self._save()

        try:
            from ui.anainf.page_07_master import MasterCurvePage

            self.main_window.set_right_widget(
                MasterCurvePage(
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