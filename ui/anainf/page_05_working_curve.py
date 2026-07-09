"""
SpectraSoft — Page 5: Working Curve Coefficients & Channel Skip

This page stores polynomial coefficients used to convert drift-corrected
intensity INT.2 into concentration.

Formula:
    C = a*I^3 + b*I^2 + c*I + d

Rows are generated from Page 3 active analytical channels.

Manual-style columns:
- ELE: Element name from Page 3
- NAME: Display/report name from Page 3
- a: Cubic coefficient
- b: Quadratic coefficient
- c: Linear coefficient
- d: Intercept
- Y/N: Working curve / 100% correction flag
        I = Internal Standard
        Y = 100% correction active
        N = 100% correction inactive
        blank = unset/manual
- SKIP: Channel skip marker, normally blank or "+"
- POINT: Skip point / threshold, default 0.00000

Important:
- No PDF/example coefficient values are inserted automatically.
- Neutral/default equation is:
      a = 0.00000000
      b = 0.00000000
      c = 1.00000000
      d = 0.00000000
  which means C = I.
- Coefficients are editable.
- Y/N, SKIP, and POINT are editable.
- Coefficients are usually auto-filed later by Regression module.
- Previous saved coefficients are backed up before each save.
- Saved coefficients are tied to the selected Analytical Group.
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


class WorkingCurvePage(QWidget):

    COL_ELE = 0
    COL_NAME = 1
    COL_A = 2
    COL_B = 3
    COL_C = 4
    COL_D = 5
    COL_YN = 6
    COL_SKIP = 7
    COL_POINT = 8

    HEADERS = [
        "ELE",
        "NAME",
        "a",
        "b",
        "c",
        "d",
        "Y/N",
        "SKIP",
        "POINT",
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
        bar = QLabel(f"Working Curve Coefficients - {self.group_name}")
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
        title = QLabel("WORKING CURVE COEFFICIENTS & CHANNEL SKIP")
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
            "Y/N: I = Internal Standard, Y = 100% correction active, "
            "N = inactive. SKIP is normally blank or '+'. POINT defaults to 0.00000."
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

        self.table.setColumnWidth(self.COL_ELE, 70)
        self.table.setColumnWidth(self.COL_NAME, 80)
        self.table.setColumnWidth(self.COL_A, 105)
        self.table.setColumnWidth(self.COL_B, 105)
        self.table.setColumnWidth(self.COL_C, 105)
        self.table.setColumnWidth(self.COL_D, 105)
        self.table.setColumnWidth(self.COL_YN, 60)
        self.table.setColumnWidth(self.COL_SKIP, 60)
        self.table.setColumnWidth(self.COL_POINT, 90)

        for col in range(len(self.HEADERS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.table.itemChanged.connect(self._on_item_changed)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Info / Reset Row ─────────────────────────────────────────────
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_reset = QPushButton("Reset Coefficients")
        btn_reset.setStyleSheet(self._button_style())
        btn_reset.clicked.connect(self._on_reset)
        ctrl_layout.addWidget(btn_reset)

        btn_restore = QPushButton("Restore Previous")
        btn_restore.setStyleSheet(self._button_style())
        btn_restore.clicked.connect(self._on_restore_previous)
        ctrl_layout.addWidget(btn_restore)

        ctrl_layout.addStretch()

        info_lbl = QLabel(
            "Coefficients are normally filed by Regression. Manual override is allowed."
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
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

    # =========================================================================
    # Table Editing / Validation Helpers
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._updating_table:
            return

        col = item.column()
        text = item.text().strip()

        # Normalize Y/N column.
        if col == self.COL_YN:
            value = text.upper()

            if value not in ["", "I", "Y", "N"]:
                self._updating_table = True
                item.setText("")
                self._updating_table = False
                self._show_msg(
                    "Invalid Y/N",
                    "Y/N must be blank, I, Y, or N.",
                    QMessageBox.Icon.Warning
                )
                return

            if value != text:
                self._updating_table = True
                item.setText(value)
                self._updating_table = False

        # Normalize SKIP column.
        elif col == self.COL_SKIP:
            value = text.upper()

            if value not in ["", "+"]:
                self._updating_table = True
                item.setText("")
                self._updating_table = False
                self._show_msg(
                    "Invalid SKIP",
                    "SKIP must be blank or '+'.",
                    QMessageBox.Icon.Warning
                )
                return

            if value != text:
                self._updating_table = True
                item.setText(value)
                self._updating_table = False

    # =========================================================================
    # Page 3 Rows
    # =========================================================================

    def _rows_from_page3(self) -> list:
        """
        Build Page 5 rows from Page 3 active analytical rows.

        Internal Standard rows default to Y/N = I.
        Normal rows default to Y/N = Y.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_03_channel:
                return []

            page3_rows = group.page_03_channel
            page4 = group.page_04_drift or {}

            referenced_itgs = set()

            for entry in page3_rows:
                try:
                    ise_ref = int(entry.get("ise_ref", 0))
                except (TypeError, ValueError):
                    ise_ref = 0

                if ise_ref > 0:
                    referenced_itgs.add(str(ise_ref))

            page4_lookup = {}

            if isinstance(page4, dict) and isinstance(page4.get("rows"), list):
                for row in page4["rows"]:
                    key = str(row.get("name", "")).strip().upper()

                    if key:
                        page4_lookup[key] = row

            rows = []

            for idx, entry in enumerate(page3_rows):
                ele = str(entry.get("ele", "")).strip()
                name = str(entry.get("name", "")).strip()
                itg = str(entry.get("itg", "")).strip()

                display_key = name or ele or (f"ITG{itg}" if itg else "")

                if not display_key:
                    continue

                try:
                    own_ise_ref = int(entry.get("ise_ref", 0))
                except (TypeError, ValueError):
                    own_ise_ref = 0

                is_internal_standard = (
                    itg in referenced_itgs and own_ise_ref == 0
                )

                page4_row = page4_lookup.get(display_key.upper())

                if page4_row:
                    h_sample = str(page4_row.get("h_sample", "")).strip()
                    l_sample = str(page4_row.get("l_sample", "")).strip()
                    k_sample = str(page4_row.get("k_sample", "")).strip()

                    if h_sample == "*" and l_sample == "*" and k_sample == "*":
                        is_internal_standard = True

                yn_default = "I" if is_internal_standard else "Y"

                rows.append({
                    "ar_no": str(idx + 1),
                    "element": display_key,
                    "ele": ele or display_key,
                    "name": name or display_key,

                    # Neutral working curve:
                    # C = I
                    "a": "0.00000000",
                    "b": "0.00000000",
                    "c": "1.00000000",
                    "d": "0.00000000",

                    "yn": yn_default,
                    "norm": yn_default,
                    "skip": "",
                    "point": "0.00000",
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
            self._set_text_cell(
                row_idx,
                self.COL_ELE,
                str(row_data.get("ele", row_data.get("element", ""))),
                editable=False
            )

            self._set_text_cell(
                row_idx,
                self.COL_NAME,
                str(row_data.get("name", row_data.get("element", ""))),
                editable=False
            )

            self._set_text_cell(
                row_idx,
                self.COL_A,
                self._normalize_float_text(row_data.get("a", ""), "0.00000000", 8)
            )
            self._set_text_cell(
                row_idx,
                self.COL_B,
                self._normalize_float_text(row_data.get("b", ""), "0.00000000", 8)
            )
            self._set_text_cell(
                row_idx,
                self.COL_C,
                self._normalize_float_text(row_data.get("c", ""), "1.00000000", 8)
            )
            self._set_text_cell(
                row_idx,
                self.COL_D,
                self._normalize_float_text(row_data.get("d", ""), "0.00000000", 8)
            )

            yn = str(
                row_data.get(
                    "yn",
                    row_data.get("norm", "Y")
                )
            ).strip().upper()

            if yn not in ["", "I", "Y", "N"]:
                yn = "Y"

            self._set_text_cell(row_idx, self.COL_YN, yn)

            skip = str(row_data.get("skip", "")).strip().upper()

            if skip not in ["", "+"]:
                skip = ""

            self._set_text_cell(row_idx, self.COL_SKIP, skip)

            self._set_text_cell(
                row_idx,
                self.COL_POINT,
                self._normalize_float_text(row_data.get("point", ""), "0.00000", 5)
            )

        self.table.resizeRowsToContents()

        self._updating_table = False

    def _set_text_cell(self, row: int, col: int, text: str, editable: bool = True):
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
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_05_wc:
                data = group.page_05_wc

                if isinstance(data, dict) and isinstance(data.get("coefficients"), list):
                    saved_rows = data["coefficients"]

                    page3_rows = self._rows_from_page3()
                    merged_rows = self._merge_page3_with_saved(page3_rows, saved_rows)

                    self._populate_table(merged_rows)
                    return

        finally:
            session.close()

        self._populate_table(self._rows_from_page3())

    def _merge_page3_with_saved(self, page3_rows: list, saved_rows: list) -> list:
        saved_lookup = {}

        for row in saved_rows:
            element = str(row.get("element", "")).strip()
            ele = str(row.get("ele", "")).strip()
            name = str(row.get("name", "")).strip()

            if element:
                saved_lookup[element.upper()] = row

            if name:
                saved_lookup[name.upper()] = row

            if ele:
                saved_lookup[ele.upper()] = row

        merged = []

        for row in page3_rows:
            element_key = str(row.get("element", "")).strip().upper()
            ele_key = str(row.get("ele", "")).strip().upper()
            name_key = str(row.get("name", "")).strip().upper()

            saved = (
                saved_lookup.get(element_key) or
                saved_lookup.get(name_key) or
                saved_lookup.get(ele_key)
            )

            if saved:
                merged_row = dict(row)

                for key in ["a", "b", "c", "d", "yn", "norm", "skip", "point"]:
                    if key in saved:
                        merged_row[key] = saved.get(key)

                # Backward compatibility:
                # old page stored only "skip" as numeric threshold.
                # If "point" is missing and old skip looks numeric, move it to point.
                if "point" not in saved:
                    old_skip = saved.get("skip", "")

                    try:
                        float(str(old_skip).strip())
                        merged_row["point"] = old_skip
                        merged_row["skip"] = ""
                    except (TypeError, ValueError):
                        pass

                merged.append(merged_row)
            else:
                merged.append(row)

        return merged

    def _collect(self) -> dict:
        coefficients = []

        for row in range(self.table.rowCount()):
            ele = self._cell_text(row, self.COL_ELE)
            name = self._cell_text(row, self.COL_NAME)

            if not ele and not name:
                continue

            element_key = name or ele

            yn = self._cell_text(row, self.COL_YN).upper()

            if yn not in ["", "I", "Y", "N"]:
                yn = "Y"

            skip = self._cell_text(row, self.COL_SKIP).upper()

            if skip not in ["", "+"]:
                skip = ""

            coefficients.append({
                "element": element_key,
                "ele": ele,
                "name": name,
                "a": self._to_float(self._cell_text(row, self.COL_A), 0.0),
                "b": self._to_float(self._cell_text(row, self.COL_B), 0.0),
                "c": self._to_float(self._cell_text(row, self.COL_C), 1.0),
                "d": self._to_float(self._cell_text(row, self.COL_D), 0.0),

                # Manual-style Page 5 fields:
                "yn": yn,
                "norm": yn,      # compatibility with older code
                "skip": skip,    # blank or "+"
                "point": self._to_float(self._cell_text(row, self.COL_POINT), 0.0),
            })

        return {
            "coefficients": coefficients
        }

    def _save(self):
        new_data = self._collect()

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group:
                old_data = group.page_05_wc or {}
                old_coefficients = []

                if isinstance(old_data, dict):
                    old_coefficients = old_data.get("coefficients", [])

                    if not isinstance(old_coefficients, list):
                        old_coefficients = []

                group.page_05_wc = {
                    "coefficients": new_data.get("coefficients", []),
                    "backup_coefficients": old_coefficients,
                }

                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)

        if not item:
            return ""

        return item.text().strip()

    def _to_float(self, text, default: float = 0.0) -> float:
        try:
            value = str(text or "").strip()

            if value == "":
                return default

            return float(value)

        except (TypeError, ValueError):
            return default

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
            "Reset all working curve coefficients to neutral default values?\n\n"
            "a = 0.00000000\n"
            "b = 0.00000000\n"
            "c = 1.00000000\n"
            "d = 0.00000000\n\n"
            "Y/N, SKIP, and POINT will also reset to default values.\n\n"
            "This only changes the table. Click OK to save.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        page3_defaults = self._rows_from_page3()
        self._populate_table(page3_defaults)

    def _on_restore_previous(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_05_wc:
                self._show_msg(
                    "No Backup",
                    "No previous working curve coefficients are available.",
                    QMessageBox.Icon.Warning
                )
                return

            data = group.page_05_wc

            if not isinstance(data, dict):
                self._show_msg(
                    "No Backup",
                    "No previous working curve coefficients are available.",
                    QMessageBox.Icon.Warning
                )
                return

            backup = data.get("backup_coefficients", [])

            if not isinstance(backup, list) or not backup:
                self._show_msg(
                    "No Backup",
                    "No previous working curve coefficients are available.",
                    QMessageBox.Icon.Warning
                )
                return

        finally:
            session.close()

        reply = QMessageBox.question(
            self,
            "Restore Previous",
            "Restore the previous working curve coefficients?\n\n"
            "The table will be restored first. Click OK to save.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        page3_rows = self._rows_from_page3()
        merged_rows = self._merge_page3_with_saved(page3_rows, backup)
        self._populate_table(merged_rows)

        self._show_msg(
            "Restored",
            "Previous working curve coefficients restored in the table.\n\n"
            "Click OK to save them."
        )

    def _on_ok(self):
        self._save()
        self._show_msg("Saved", "Working curve data saved successfully.")

    def _on_next(self):
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
            self._show_msg("Next Page", "Page 6 is not built yet.")

    def _on_pre(self):
        self._save()

        try:
            from ui.anainf.page_04_drift import DriftCorrectionPage

            self.main_window.set_right_widget(
                DriftCorrectionPage(
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
    # Message Box Helpers
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