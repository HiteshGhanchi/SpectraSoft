"""
SpectraSoft — Page 7: Master Curve Correction Sample and Target Value

Manual-style Page 7 table:

AR-No. | NAME | SPL | TARGET | D1 | D2 | AC | MC

Purpose:
- Stores Master Curve / y-correction registration values.
- These values are used after Page 6 matrix correction.
- Job 4: Master Curve Recalibration may later auto-file AC and MC values here.
- User can also manually enter/override values.

Meaning:
- SPL    : Master correction sample name
- TARGET : Certified target concentration/value of the master sample
- D1     : Inner correction limit
- D2     : Outer correction limit
- AC     : Additive correction
- MC     : Multiplicative correction

Formula concept:
    C_master = (C_input * MC) + AC

Neutral/default:
    TARGET = 0.00000
    D1     = 0.00000
    D2     = 0.00000
    AC     = 0.00000
    MC     = 1.0000

Saved to:
    AnalyticalGroup.page_07_master
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


class MasterCurvePage(QWidget):
    """
    Page 7: Master Curve Correction Sample and Target Value.
    """

    COL_AR = 0
    COL_NAME = 1
    COL_SPL = 2
    COL_TARGET = 3
    COL_D1 = 4
    COL_D2 = 5
    COL_AC = 6
    COL_MC = 7

    HEADERS = [
        "AR-No.",
        "NAME",
        "SPL",
        "TARGET",
        "D1",
        "D2",
        "AC",
        "MC",
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
        bar = QLabel(f"Master Curve Correction - {self.group_name}")
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
        title = QLabel("MASTER CURVE CORRECTION SAMPLE AND TARGET VALUE")
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
            "SPL is the master correction sample name. TARGET, D1, D2, and AC default "
            "to 0.00000. MC defaults to 1.0000. Job 4 may later auto-file AC and MC."
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

        self.table.setColumnWidth(self.COL_AR, 60)
        self.table.setColumnWidth(self.COL_NAME, 90)
        self.table.setColumnWidth(self.COL_SPL, 90)
        self.table.setColumnWidth(self.COL_TARGET, 100)
        self.table.setColumnWidth(self.COL_D1, 90)
        self.table.setColumnWidth(self.COL_D2, 90)
        self.table.setColumnWidth(self.COL_AC, 90)
        self.table.setColumnWidth(self.COL_MC, 90)

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
            "Default Page 7 state applies no master curve correction: AC=0.00000, MC=1.0000."
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
        Build Page 7 rows from Page 3 active analytical rows.

        Only AR-No. and NAME come from Page 3.
        All correction fields use neutral/default values.
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
                    "spl": "",
                    "target": "0.00000",
                    "d1": "0.00000",
                    "d2": "0.00000",
                    "ac": "0.00000",
                    "mc": "1.0000",
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
                self.COL_SPL,
                self._upper_text(row_data.get("spl", ""))
            )

            self._set_cell(
                row_idx,
                self.COL_TARGET,
                self._normalize_float_text(row_data.get("target", ""), "0.00000", 5)
            )

            self._set_cell(
                row_idx,
                self.COL_D1,
                self._normalize_float_text(row_data.get("d1", ""), "0.00000", 5)
            )

            self._set_cell(
                row_idx,
                self.COL_D2,
                self._normalize_float_text(row_data.get("d2", ""), "0.00000", 5)
            )

            self._set_cell(
                row_idx,
                self.COL_AC,
                self._normalize_float_text(row_data.get("ac", ""), "0.00000", 5)
            )

            self._set_cell(
                row_idx,
                self.COL_MC,
                self._normalize_float_text(row_data.get("mc", ""), "1.0000", 4)
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

        if item.column() == self.COL_SPL:
            current = item.text()
            upper = current.upper()

            if current != upper:
                self._updating_table = True
                item.setText(upper)
                self._updating_table = False

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_07_master:
                data = group.page_07_master

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
        Merge saved Page 7 data into current Page 3 row order.
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

                for key in ["spl", "target", "d1", "d2", "ac", "mc"]:
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
                "spl": self._upper_text(self._cell_text(row, self.COL_SPL)),
                "target": self._normalize_float_text(
                    self._cell_text(row, self.COL_TARGET),
                    "0.00000",
                    5
                ),
                "d1": self._normalize_float_text(
                    self._cell_text(row, self.COL_D1),
                    "0.00000",
                    5
                ),
                "d2": self._normalize_float_text(
                    self._cell_text(row, self.COL_D2),
                    "0.00000",
                    5
                ),
                "ac": self._normalize_float_text(
                    self._cell_text(row, self.COL_AC),
                    "0.00000",
                    5
                ),
                "mc": self._normalize_float_text(
                    self._cell_text(row, self.COL_MC),
                    "1.0000",
                    4
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
                group.page_07_master = data
                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        return item.text().strip() if item else ""

    def _upper_text(self, value) -> str:
        return str(value or "").strip().upper()

    def _normalize_float_text(self, value, default: str, decimals: int) -> str:
        raw = str(value or "").strip()

        if raw == "":
            raw = default

        try:
            return f"{float(raw):.{decimals}f}"

        except (TypeError, ValueError):
            return default

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_reset(self):
        if QMessageBox.question(
            self,
            "Reset",
            "Reset Page 7 Master Curve Correction values to defaults?\n\n"
            "TARGET = 0.00000\n"
            "D1 = 0.00000\n"
            "D2 = 0.00000\n"
            "AC = 0.00000\n"
            "MC = 1.0000\n\n"
            "This only changes the table. Click OK to save.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self._populate_table(self._rows_from_page3())

    def _on_ok(self):
        self._save()
        self._show_msg("Saved", "Master curve correction data saved successfully.")

    def _on_next(self):
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
            self._show_msg("Next Page", "Page 8 is not built yet.")

    def _on_pre(self):
        self._save()

        try:
            from ui.anainf.page_06_matrix import CorrectionPage

            self.main_window.set_right_widget(
                CorrectionPage(
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