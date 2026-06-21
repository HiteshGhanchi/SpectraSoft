"""
SpectraSoft — Page 3: Order of Analytical Channel & Internal Standard

This page maps hardware channels (ITG) to elements, assigns sequences,
and selects the Internal Standard Element (ISE).

Columns:
- AR-No.: Auto-numbered 1 to 32 (read-only)
- ITG: Integrator number (1-45, or 57-61 for virtual) – dropdown
- ELE: Element name – auto-filled from ITG (read-only)
- NAME: User-defined name (up to 5 chars) – editable
- SEQ: Sequence assignment (1, 2, or 3) – dropdown
- ISE: Internal Standard Element – 0 (No) or 1 (Yes), only one allowed

Rules:
- Maximum 32 elements per group
- Only one ISE allowed (enforced automatically)
- ELE is read-only
- Virtual integrators (57-61) allowed for special calculations

Saved JSON example:
[
    {"itg": "1", "ele": "FE", "name": "Fe", "seq": "1", "ise": 1},
    {"itg": "2", "ele": "C", "name": "C", "seq": "1", "ise": 0},
    ...
]
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.database import get_session
from core.models import AnalyticalGroup, MasterElement

MAX_ELEMENTS = 32


class ChannelPage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._load()

    # =========================================================================
    # Build ITG Options
    # =========================================================================

    def _build_itg_options(self) -> dict:
        """Return a dict {display_string: itg_number} for dropdown."""
        session = get_session()
        try:
            elements = session.query(MasterElement).order_by(
                MasterElement.itg_no).all()
            opts = {}
            for e in elements:
                if e.ele_name:
                    opts[f"{e.itg_no}: {e.ele_name}"] = str(e.itg_no)
            if opts:
                return opts
        finally:
            session.close()

        # Fallback defaults
        defaults = [
            ("1", "FE"), ("2", "C"), ("3", "SI"), ("4", "MN"),
            ("5", "P"), ("6", "S"), ("7", "V"), ("8", "CR"),
            ("9", "MO"), ("10", "NI"), ("11", "AL"), ("12", "CU"),
            ("13", "TI"), ("14", "W"), ("15", "B"), ("16", "NB"),
            ("17", "CA"), ("18", "CO"), ("19", "SN"), ("20", "N"),
            ("21", "PB"), ("22", "RH"), ("23", "CE")
        ]
        # Virtual integrators 57-61
        virtual = [
            ("57", "CE_VIRT"), ("58", "VIRT1"), ("59", "VIRT2"),
            ("60", "VIRT3"), ("61", "VIRT4")
        ]
        all_items = defaults + virtual
        return {f"{itg}: {ele}": itg for itg, ele in all_items}

    # =========================================================================
    # UI Construction
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        self.title_bar = QLabel(f"Element Information - CH 0 - {self.group_name}")
        self.title_bar.setFixedHeight(24)
        self.title_bar.setContentsMargins(12, 0, 0, 0)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.title_bar.setStyleSheet(
            "background:#5c9bd5;"
            "color:white;"
            "font:bold 10pt Arial;"
        )
        root.addWidget(self.title_bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        ol.addWidget(scroll)

        inner = QWidget()
        inner.setAutoFillBackground(True)
        ip = inner.palette()
        ip.setColor(inner.backgroundRole(), Qt.GlobalColor.lightGray)
        inner.setPalette(ip)
        scroll.setWidget(inner)

        ml = QVBoxLayout(inner)
        ml.setContentsMargins(20, 16, 20, 12)
        ml.setSpacing(8)

        # ── Table Title ──────────────────────────────────────────────────
        title = QLabel("ORDER OF ANALYTICAL CHANNEL & INTERNAL STANDARD")
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
        ml.addWidget(title)

        # ── Single Centered Table ────────────────────────────────────────
        self.table = self._create_table()
        table_container = QHBoxLayout()
        table_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_container.addWidget(self.table)
        ml.addLayout(table_container)

        # ── Control Buttons ──────────────────────────────────────────────
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_style = (
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

        btn_clear = QPushButton("Clear All")
        btn_clear.setStyleSheet(btn_style)
        btn_clear.clicked.connect(self._on_clear)

        ctrl_layout.addWidget(btn_clear)
        ctrl_layout.addStretch()

        info_lbl = QLabel("ISE must be at the top of the list (row 1)")
        info_lbl.setStyleSheet(
            "QLabel{"
            "color:#666666;"
            "font:9pt Arial;"
            "border:none;"
            "}"
        )
        ctrl_layout.addWidget(info_lbl)

        ml.addLayout(ctrl_layout)

        # ── Bottom Nav ──────────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(12, 4, 12, 8)
        bbl.setSpacing(4)

        for txt, slot in [
            ("1:OK", self._on_ok),
            ("2:Next", self._on_next),
            ("3:Pre.", self._on_pre),
            ("4:Print", self._on_print),
        ]:
            b = QPushButton(txt)
            b.setStyleSheet(btn_style)
            b.clicked.connect(slot)
            bbl.addWidget(b)

        bbl.addStretch()

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(btn_style)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)

        root.addWidget(btn_bar)

    # =========================================================================
    # Table Creation
    # =========================================================================

    def _create_table(self) -> QTableWidget:
        """Create a single centered table with 6 columns and 32 rows."""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["AR-No.", "ITG", "ELE", "NAME", "SEQ", "ISE"])

        # Excel-style table styling
        table.setStyleSheet(
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
            "QTableWidget::item:!selected{"
            "color:black;"
            "}"
            "QTableWidget QLineEdit { color: black; background: white; }"
        )

        # Column widths - fixed to avoid horizontal scrolling
        table.setColumnWidth(0, 50)   # AR-No.
        table.setColumnWidth(1, 100)  # ITG
        table.setColumnWidth(2, 50)   # ELE
        table.setColumnWidth(3, 80)   # NAME
        table.setColumnWidth(4, 50)   # SEQ
        table.setColumnWidth(5, 50)   # ISE

        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )

        # Row height
        table.verticalHeader().setDefaultSectionSize(27)

        # Set 32 rows
        table.setRowCount(MAX_ELEMENTS)

        # Populate rows
        for i in range(MAX_ELEMENTS):
            row_num = i + 1

            # AR-No. (read-only)
            ar_item = QTableWidgetItem(str(row_num))
            ar_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ar_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            ar_item.setBackground(QColor("#d4d0c8"))
            ar_item.setForeground(QColor("black"))
            table.setItem(i, 0, ar_item)

            # ITG dropdown (combobox)
            combo = QComboBox()
            combo.addItem("")  # empty option
            itg_opts = self._build_itg_options()
            for display, itg_val in itg_opts.items():
                combo.addItem(display, itg_val)
            combo.setStyleSheet(
                "QComboBox{"
                "background:white;"
                "color:black;"
                "border:1px solid #888888;"
                "font:9pt Arial;"
                "padding:0px 2px;"
                "}"
                "QComboBox::drop-down{"
                "border:none;"
                "width:12px;"
                "}"
                "QComboBox QAbstractItemView{"
                "background:white;"
                "color:black;"
                "}"
            )
            combo.currentIndexChanged.connect(
                lambda idx, r=i, t=table: self._on_itg_changed(r, t)
            )
            table.setCellWidget(i, 1, combo)

            # ELE (read-only, auto-filled)
            ele_item = QTableWidgetItem("")
            ele_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ele_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            ele_item.setBackground(QColor("#d4d0c8"))
            ele_item.setForeground(QColor("black"))
            table.setItem(i, 2, ele_item)

            # NAME (editable)
            name_item = QTableWidgetItem("")
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            name_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsEditable
            )
            name_item.setForeground(QColor("black"))  # Ensure black text
            table.setItem(i, 3, name_item)

            # SEQ dropdown (1,2,3)
            seq_combo = QComboBox()
            seq_combo.addItems(["", "1", "2", "3"])
            seq_combo.setStyleSheet(
                "QComboBox{"
                "background:white;"
                "color:black;"
                "border:1px solid #888888;"
                "font:9pt Arial;"
                "padding:0px 2px;"
                "}"
                "QComboBox::drop-down{"
                "border:none;"
                "width:12px;"
                "}"
                "QComboBox QAbstractItemView{"
                "background:white;"
                "color:black;"
                "}"
            )
            table.setCellWidget(i, 4, seq_combo)

            # ISE dropdown (0 or 1)
            ise_combo = QComboBox()
            ise_combo.addItems(["0", "1"])
            ise_combo.setStyleSheet(
                "QComboBox{"
                "background:white;"
                "color:black;"
                "border:1px solid #888888;"
                "font:9pt Arial;"
                "padding:0px 2px;"
                "}"
                "QComboBox::drop-down{"
                "border:none;"
                "width:12px;"
                "}"
                "QComboBox QAbstractItemView{"
                "background:white;"
                "color:black;"
                "}"
            )
            ise_combo.currentIndexChanged.connect(self._on_ise_changed)
            table.setCellWidget(i, 5, ise_combo)

        # Calculate table height: 32 rows × 27 + header (27) = 891px
        table_height = (MAX_ELEMENTS * 27) + 27 + 3
        table.setFixedHeight(table_height)

        return table

    # =========================================================================
    # Event Handlers
    # =========================================================================

    def _on_itg_changed(self, row: int, table: QTableWidget):
        """Update ELE column when ITG is selected."""
        combo = table.cellWidget(row, 1)
        ele_item = table.item(row, 2)
        if not combo or not ele_item:
            return

        selected = combo.currentData()  # the ITG number (string)
        if selected:
            # Get element name from master
            session = get_session()
            try:
                elem = session.query(MasterElement).filter_by(itg_no=int(selected)).first()
                if elem and elem.ele_name:
                    ele_item.setText(elem.ele_name)
                else:
                    ele_item.setText("")
            finally:
                session.close()
        else:
            ele_item.setText("")

        self._update_ch_count()

    def _on_ise_changed(self):
        """Ensure only one ISE is selected (value = 1) across all rows."""
        # Find all rows where ISE = 1
        ise_rows = []
        for row in range(self.table.rowCount()):
            ise_combo = self.table.cellWidget(row, 5)
            if ise_combo and ise_combo.currentText() == "1":
                ise_rows.append(row)

        if len(ise_rows) > 1:
            # Keep only the first one, reset others to 0
            for row in ise_rows[1:]:
                ise_combo = self.table.cellWidget(row, 5)
                if ise_combo:
                    ise_combo.blockSignals(True)
                    ise_combo.setCurrentIndex(0)  # 0 = "0"
                    ise_combo.blockSignals(False)
            QMessageBox.warning(
                self,
                "ISE Limit",
                "Only one Internal Standard Element (ISE) is allowed.\n"
                "ISE set to row(s) " + ", ".join(str(r+1) for r in ise_rows[:1])
            )

        self._update_ch_count()

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _collect(self) -> list:
        """Collect data from table into a list of dicts."""
        data = []
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 1)
            ele_item = self.table.item(row, 2)
            name_item = self.table.item(row, 3)
            seq_combo = self.table.cellWidget(row, 4)
            ise_combo = self.table.cellWidget(row, 5)

            itg = combo.currentData() if combo else ""
            ele = ele_item.text().strip() if ele_item else ""
            name = name_item.text().strip() if name_item else ""
            seq = seq_combo.currentText().strip() if seq_combo else ""
            ise = int(ise_combo.currentText()) if ise_combo else 0

            if itg:  # only save rows with an ITG selected
                data.append({
                    "itg": str(itg),
                    "ele": ele,
                    "name": name,
                    "seq": seq,
                    "ise": ise
                })
        return data

    def _populate_table_from_data(self, data: list):
        """Fill table from a list of dicts."""
        # Clear all combos
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 1)
            if combo:
                combo.setCurrentIndex(0)
            ele_item = self.table.item(row, 2)
            if ele_item:
                ele_item.setText("")
            name_item = self.table.item(row, 3)
            if name_item:
                name_item.setText("")
            seq_combo = self.table.cellWidget(row, 4)
            if seq_combo:
                seq_combo.setCurrentIndex(0)
            ise_combo = self.table.cellWidget(row, 5)
            if ise_combo:
                ise_combo.setCurrentIndex(0)  # default to 0

        # Fill data
        for idx, entry in enumerate(data):
            if idx >= MAX_ELEMENTS:
                break

            row = idx
            itg_val = entry.get("itg", "")
            ele_val = entry.get("ele", "")
            name_val = entry.get("name", "")
            seq_val = entry.get("seq", "")
            ise_val = entry.get("ise", 0)

            # ITG combo: find index by data
            combo = self.table.cellWidget(row, 1)
            if combo:
                index = combo.findData(itg_val)
                if index >= 0:
                    combo.setCurrentIndex(index)
                else:
                    combo.setCurrentIndex(0)

            # ELE (will be auto-filled by the above signal, but set manually to be safe)
            ele_item = self.table.item(row, 2)
            if ele_item and ele_val:
                ele_item.setText(ele_val)

            # NAME
            name_item = self.table.item(row, 3)
            if name_item:
                name_item.setText(name_val)

            # SEQ combo
            seq_combo = self.table.cellWidget(row, 4)
            if seq_combo:
                idx_seq = seq_combo.findText(seq_val)
                if idx_seq >= 0:
                    seq_combo.setCurrentIndex(idx_seq)
                else:
                    seq_combo.setCurrentIndex(0)

            # ISE combo
            ise_combo = self.table.cellWidget(row, 5)
            if ise_combo:
                ise_str = str(ise_val)
                idx_ise = ise_combo.findText(ise_str)
                if idx_ise >= 0:
                    ise_combo.setCurrentIndex(idx_ise)
                else:
                    ise_combo.setCurrentIndex(0)

        self._update_ch_count()

    def _load_data(self):
        """Load saved data from database."""
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_03_channel:
                data = g.page_03_channel
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    self._populate_table_from_data(data)
                    return
        finally:
            session.close()

        # No valid data – clear all
        self._populate_table_from_data([])

    def _save_data(self):
        """Save data to database."""
        data = self._collect()
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_03_channel = data
                session.commit()
        finally:
            session.close()

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _update_ch_count(self):
        """Update CH count in title bar."""
        count = 0
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 1)
            if combo and combo.currentData():
                count += 1
        self.title_bar.setText(f"Element Information - CH {count} - {self.group_name}")

    # =========================================================================
    # Button Actions
    # =========================================================================

    def _on_clear(self):
        """Clear all rows."""
        if QMessageBox.question(
            self,
            "Clear All",
            "Remove all elements?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self._populate_table_from_data([])
            self._update_ch_count()

    # =========================================================================
    # Navigation
    # =========================================================================

    def _on_ok(self):
        self._save_data()
        self._show_msg("Saved", "Element information saved successfully.")

    def _on_next(self):
        self._save_data()
        try:
            from ui.anainf.page_04_drift import DriftCorrectionPage
            self.main_window.set_right_widget(
                DriftCorrectionPage(self.main_window, self.group_id, self.group_name)
            )
        except ImportError:
            self._show_msg("Next Page", "Page 4 (Channel) is not built yet.")

    def _on_pre(self):
        self._save_data()
        try:
            from ui.anainf.page_02_attenuator import AttenuatorPage
            self.main_window.set_right_widget(
                AttenuatorPage(self.main_window, self.group_id, self.group_name)
            )
        except ImportError:
            pass

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        if self._show_question("Cancel", "Discard changes?"):
            self._load()
            self._on_pre()

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
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
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

    # =========================================================================
    # Load/Save Entry Points
    # =========================================================================

    def _load(self):
        self._load_data()

    def _save(self):
        self._save_data()