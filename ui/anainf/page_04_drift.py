"""
SpectraSoft — Page 4: Drift Correction Target Values

Manual-style Page 4 table:

AR-No. | NAME | H | L | K | H Target | L Target | K Target | α | β | k

Rows are generated from Page 3 channel information.

Important:
- No PDF/example target values are inserted automatically.
- H, L, and K sample names are optional.
- H, L, and K sample names are always stored in uppercase when entered.
- Internal Standard anchor rows default to H=L=K="*" and neutral drift values.
- Rows marked with "*" are skipped by Job 8 target filing.
- H Target, L Target, and K Target default to 0.00000.
- α defaults to 1.0000.
- β defaults to 0.00000.
- k defaults to 1.0000.
- All cells are editable for now.
- Later, Job 8 / recalibration jobs may auto-file values here.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup


class DriftCorrectionPage(QWidget):

    COL_AR = 0
    COL_NAME = 1
    COL_H = 2
    COL_L = 3
    COL_K = 4
    COL_H_TARGET = 5
    COL_L_TARGET = 6
    COL_K_TARGET = 7
    COL_ALPHA = 8
    COL_BETA = 9
    COL_K_COEFF = 10

    HEADERS = [
        "AR-No.",
        "NAME",
        "H",
        "L",
        "K",
        "H Target",
        "L Target",
        "K Target",
        "α",
        "β",
        "k",
    ]

    SAMPLE_COLUMNS = {COL_H, COL_L, COL_K}

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
        bar = QLabel(f"Drift Correction Target Values - {self.group_name}")
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

        # ── Table Title ──────────────────────────────────────────────────
        title = QLabel("DRIFT CORRECTION TARGET VALUES")
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

        # ── Table ────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

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
        header.setStretchLastSection(True)
        header.setSectionsClickable(False)
        header.setHighlightSections(False)

        self.table.setColumnWidth(self.COL_AR, 60)
        self.table.setColumnWidth(self.COL_NAME, 80)
        self.table.setColumnWidth(self.COL_H, 90)
        self.table.setColumnWidth(self.COL_L, 90)
        self.table.setColumnWidth(self.COL_K, 90)
        self.table.setColumnWidth(self.COL_H_TARGET, 95)
        self.table.setColumnWidth(self.COL_L_TARGET, 95)
        self.table.setColumnWidth(self.COL_K_TARGET, 95)
        self.table.setColumnWidth(self.COL_ALPHA, 85)
        self.table.setColumnWidth(self.COL_BETA, 85)
        self.table.setColumnWidth(self.COL_K_COEFF, 85)

        for col in range(len(self.HEADERS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.table.itemChanged.connect(self._on_item_changed)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Help Note ─────────────────────────────────────────────────────
        note = QLabel(
            "Rows are generated from Page 3. H, L, and K sample names are optional "
            "and are stored in uppercase when entered. Internal Standard rows use '*' "
            "and are skipped by Job 8. Targets default to 0.00000; "
            "α=1.0000, β=0.00000, k=1.0000."
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

        # ── Bottom Navigation ─────────────────────────────────────────────
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
    # Uppercase Handling
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        """
        Force H, L, and K sample names to uppercase when entered.
        Empty values are allowed.
        """
        if self._updating_table:
            return

        if item.column() not in self.SAMPLE_COLUMNS:
            return

        current = item.text()
        upper = current.upper()

        if current != upper:
            self._updating_table = True
            item.setText(upper)
            self._updating_table = False

    # =========================================================================
    # Page 3 Source Rows
    # =========================================================================

    def _rows_from_page3(self) -> list:
        """
        Build Page 4 rows from Page 3 active analytical rows.

        AR-No. and NAME are filled from Page 3.
        H/L/K are optional and start blank for normal rows.

        Internal Standard anchor rows:
        - Identified when this row's ITG is referenced by another row's ise_ref.
        - Its own ise_ref is 0.
        - Defaults to H=L=K="*".
        - Targets stay 0.00000.
        - Coefficients stay neutral.
        """
        session = get_session()

        try:
            g = session.get(AnalyticalGroup, self.group_id)

            if not g or not g.page_03_channel:
                return []

            page3_rows = g.page_03_channel

            # ITGs referenced as internal standard by other elements.
            referenced_itgs = set()

            for entry in page3_rows:
                try:
                    ise_ref = int(entry.get("ise_ref", 0))
                except (TypeError, ValueError):
                    ise_ref = 0

                if ise_ref > 0:
                    referenced_itgs.add(str(ise_ref))

            rows = []

            for idx, entry in enumerate(page3_rows):
                name = str(entry.get("name", "")).strip()
                ele = str(entry.get("ele", "")).strip()
                itg = str(entry.get("itg", "")).strip()

                display_name = name or ele or (f"ITG{itg}" if itg else "")

                if not display_name:
                    continue

                try:
                    own_ise_ref = int(entry.get("ise_ref", 0))
                except (TypeError, ValueError):
                    own_ise_ref = 0

                is_internal_standard_anchor = (
                    itg in referenced_itgs and own_ise_ref == 0
                )

                if is_internal_standard_anchor:
                    h_sample = "*"
                    l_sample = "*"
                    k_sample = "*"
                else:
                    h_sample = ""
                    l_sample = ""
                    k_sample = ""

                rows.append({
                    "ar_no": str(idx + 1),
                    "name": display_name,

                    # Optional sample names.
                    # Internal standard anchor rows use "*" as skip marker.
                    "h_sample": h_sample,
                    "l_sample": l_sample,
                    "k_sample": k_sample,

                    # Day-1 target values unknown until Job 8/manual entry.
                    "h_target": "0.00000",
                    "l_target": "0.00000",
                    "k_target": "0.00000",

                    # Neutral drift correction state.
                    "alpha": "1.0000",
                    "beta": "0.00000",
                    "k_coeff": "1.0000",
                })

            return rows

        finally:
            session.close()

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _populate_table(self, rows: list):
        self._updating_table = True

        self.table.setRowCount(len(rows))

        for row_idx, row_data in enumerate(rows):
            self._set_cell(row_idx, self.COL_AR, str(row_data.get("ar_no", row_idx + 1)))
            self._set_cell(row_idx, self.COL_NAME, str(row_data.get("name", "")))

            self._set_cell(row_idx, self.COL_H, self._upper_text(row_data.get("h_sample", "")))
            self._set_cell(row_idx, self.COL_L, self._upper_text(row_data.get("l_sample", "")))
            self._set_cell(row_idx, self.COL_K, self._upper_text(row_data.get("k_sample", "")))

            # Show default target values even when saved value is blank.
            self._set_cell(
                row_idx,
                self.COL_H_TARGET,
                self._normalize_float_text(row_data.get("h_target", ""), "0.00000", 5)
            )
            self._set_cell(
                row_idx,
                self.COL_L_TARGET,
                self._normalize_float_text(row_data.get("l_target", ""), "0.00000", 5)
            )
            self._set_cell(
                row_idx,
                self.COL_K_TARGET,
                self._normalize_float_text(row_data.get("k_target", ""), "0.00000", 5)
            )

            # Show neutral drift correction defaults even when saved value is blank.
            self._set_cell(
                row_idx,
                self.COL_ALPHA,
                self._normalize_float_text(row_data.get("alpha", ""), "1.0000", 4)
            )
            self._set_cell(
                row_idx,
                self.COL_BETA,
                self._normalize_float_text(row_data.get("beta", ""), "0.00000", 5)
            )
            self._set_cell(
                row_idx,
                self.COL_K_COEFF,
                self._normalize_float_text(row_data.get("k_coeff", ""), "1.0000", 4)
            )

        self.table.resizeRowsToContents()

        self._updating_table = False

    def _set_cell(self, row: int, col: int, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        item.setFlags(
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsEditable
        )

        self.table.setItem(row, col, item)

    def _collect(self) -> dict:
        rows = []

        for row in range(self.table.rowCount()):
            row_data = {
                "ar_no": self._cell_text(row, self.COL_AR),
                "name": self._cell_text(row, self.COL_NAME),
                "h_sample": self._upper_text(self._cell_text(row, self.COL_H)),
                "l_sample": self._upper_text(self._cell_text(row, self.COL_L)),
                "k_sample": self._upper_text(self._cell_text(row, self.COL_K)),
                "h_target": self._normalize_float_text(
                    self._cell_text(row, self.COL_H_TARGET),
                    "0.00000",
                    5
                ),
                "l_target": self._normalize_float_text(
                    self._cell_text(row, self.COL_L_TARGET),
                    "0.00000",
                    5
                ),
                "k_target": self._normalize_float_text(
                    self._cell_text(row, self.COL_K_TARGET),
                    "0.00000",
                    5
                ),
                "alpha": self._normalize_float_text(
                    self._cell_text(row, self.COL_ALPHA),
                    "1.0000",
                    4
                ),
                "beta": self._normalize_float_text(
                    self._cell_text(row, self.COL_BETA),
                    "0.00000",
                    5
                ),
                "k_coeff": self._normalize_float_text(
                    self._cell_text(row, self.COL_K_COEFF),
                    "1.0000",
                    4
                ),
            }

            rows.append(row_data)

        return {
            "rows": rows
        }

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        return item.text().strip() if item else ""

    def _upper_text(self, value) -> str:
        return str(value or "").strip().upper()

    def _normalize_float_text(self, text: str, default: str, decimals: int) -> str:
        raw = str(text or "").strip()

        if raw == "":
            raw = default

        try:
            value = float(raw)
            return f"{value:.{decimals}f}"
        except ValueError:
            return default

    def _save(self):
        data = self._collect()

        session = get_session()

        try:
            g = session.get(AnalyticalGroup, self.group_id)

            if g:
                g.page_04_drift = data
                session.commit()

        finally:
            session.close()

    def _load(self):
        session = get_session()

        try:
            g = session.get(AnalyticalGroup, self.group_id)

            if g and g.page_04_drift:
                data = g.page_04_drift

                if isinstance(data, dict) and isinstance(data.get("rows"), list):
                    self._populate_table(data["rows"])
                    return

        finally:
            session.close()

        self._populate_table(self._rows_from_page3())

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
        return msg.exec()

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_ok(self):
        self._save()
        self._load()
        self._show_msg("Saved", "Drift correction data saved successfully.")

    def _on_next(self):
        self._save()

        try:
            from ui.anainf.page_05_working_curve import WorkingCurvePage
            self.main_window.set_right_widget(
                WorkingCurvePage(self.main_window, self.group_id, self.group_name)
            )
        except ImportError:
            self._show_msg("Next Page", "Page 5 is not built yet.")

    def _on_pre(self):
        self._save()

        try:
            from ui.anainf.page_03_channel import ChannelPage
            self.main_window.set_right_widget(
                ChannelPage(self.main_window, self.group_id, self.group_name)
            )
        except ImportError:
            pass

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        if self._show_question(
            "Cancel",
            "Discard changes?"
        ) == QMessageBox.StandardButton.Yes:
            self._load()
            self.main_window._show_home_content()