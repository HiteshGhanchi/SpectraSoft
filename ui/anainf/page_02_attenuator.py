from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QFrame,
    QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QIntValidator

from core.database import get_session
from core.models import AnalyticalGroup, MasterElement

BG  = "#d4d0c8"
BTN = (
    "QPushButton{background:#d4d0c8;color:black;"
    "border:2px outset #ffffff;font:9pt Arial;padding:3px 8px;min-width:65px;}"
    "QPushButton:pressed{border:2px inset #888;}"
)
HDR = (
    "QLabel{background:#d4d0c8;color:black;"
    "border:1px solid #aaa;font:9pt Arial;"
    "padding:1px 4px;}"
)

# CHANGED: Gray background to show they are not editable
CELL_RO = (          
    "QLabel{background:#e8e8e8;color:#555555;"
    "border:1px solid #aaa;font:9pt Arial;padding:1px 4px;}"
)

# Editable cells (ATT value) stay white
CELL_ED = (          
    "QLineEdit{background:white;color:black;"
    "border:1px solid #aaa;font:9pt Arial;padding:1px 4px;}"
)

# Empty rows to fill up to minimum slots
EMPTY_ROW = ("", "", 0)


class AttenuatorPage(QWidget):

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(BG))
        self.setPalette(p)
        self._att_entries = []   # list of QLineEdit for ATT values
        self._rows = []          # list of (ele, wavelength, att_entry)
        self._build_ui()
        self._load()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Blue title bar
        bar = QLabel(f"Attenuator Information - {self.group_name}")
        bar.setFixedHeight(22)
        bar.setContentsMargins(8, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(
            "background:#5c9bd5;color:white;font:bold 10pt Arial;"
        )
        root.addWidget(bar)

        # White sunken outer frame
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)
        ol.setSpacing(0)

        # Scrollable grey inner area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        ol.addWidget(scroll)

        inner = QWidget()
        inner.setAutoFillBackground(True)
        ip = inner.palette()
        ip.setColor(inner.backgroundRole(), QColor(BG))
        inner.setPalette(ip)
        scroll.setWidget(inner)

        ml = QVBoxLayout(inner)
        ml.setContentsMargins(10, 10, 10, 6)
        ml.setSpacing(8)

        # ── Two-column attenuator table ───────────────────────────────
        tbl_row = QHBoxLayout()
        tbl_row.setSpacing(16)
        tbl_row.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Left and right column grids
        self._left_grid  = self._make_col_grid()
        self._right_grid = self._make_col_grid()

        tbl_row.addLayout(self._left_grid)
        tbl_row.addLayout(self._right_grid)
        tbl_row.addStretch()

        ml.addLayout(tbl_row)
        ml.addStretch()

        # ── Bottom nav buttons ────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), QColor(BG))
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(10, 4, 10, 8)
        bbl.setSpacing(4)

        for txt, slot in [
            ("1:OK",    self._on_ok),
            ("2:Next",  self._on_next),
            ("3:Pre.",  self._on_pre),
            ("4:Print", self._on_print),
        ]:
            b = QPushButton(txt)
            b.setStyleSheet(BTN)
            b.clicked.connect(slot)
            bbl.addWidget(b)

        bbl.addStretch()

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)

        root.addWidget(btn_bar)

    def _make_col_grid(self) -> QGridLayout:
        """Create a column grid with header row."""
        g = QGridLayout()
        g.setSpacing(0)
        g.setAlignment(Qt.AlignmentFlag.AlignTop)

        # CHANGED: Removed the empty first column, shifted remaining columns
        col_specs = [
            ("Ele.", 52),
            ("W.L.", 70),   # Wavelength header
            ("ATT", 52),
        ]
        
        for ci, (txt, w) in enumerate(col_specs):
            h = QLabel(txt)
            h.setFixedWidth(w)
            h.setFixedHeight(22)
            h.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h.setStyleSheet(HDR)
            g.addWidget(h, 0, ci)

        return g

    def _populate_grids(self, rows):
        """
        Fill both column grids with data rows dynamically.
        Splits data evenly across left and right columns.
        """
        # Clear existing data rows (keep header row 0)
        self._att_entries.clear()
        self._rows.clear()

        # Dynamically split rows so columns are balanced
        midpoint = max(16, (len(rows) + 1) // 2)
        left_rows  = rows[:midpoint]
        right_rows = rows[midpoint:]

        # Pad to ensure UI structure matches traditional look (at least 16 rows per col)
        while len(left_rows) < 16:
            left_rows.append(EMPTY_ROW)
        while len(right_rows) < len(left_rows):
            right_rows.append(EMPTY_ROW)

        validator = QIntValidator(0, 255)

        for grid, data_rows in [(self._left_grid, left_rows),
                                  (self._right_grid, right_rows)]:
            for ri, (ele, wl, att) in enumerate(data_rows):
                row = ri + 1  # row 0 is header

                # CHANGED: Shifted column indices down by 1 because the blank column was removed
                
                # Element code (read-only grayed display)
                ele_lbl = QLabel(ele)
                ele_lbl.setFixedWidth(52)
                ele_lbl.setFixedHeight(20)
                ele_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                ele_lbl.setStyleSheet(CELL_RO)
                grid.addWidget(ele_lbl, row, 0)

                # Wavelength (read-only grayed display)
                wl_lbl = QLabel(wl)
                wl_lbl.setFixedWidth(70)
                wl_lbl.setFixedHeight(20)
                wl_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                wl_lbl.setStyleSheet(CELL_RO)
                grid.addWidget(wl_lbl, row, 1)

                # ATT value (editable white integer)
                att_e = QLineEdit(str(att) if ele else "")
                att_e.setFixedWidth(52)
                att_e.setFixedHeight(20)
                att_e.setAlignment(Qt.AlignmentFlag.AlignCenter)
                att_e.setStyleSheet(CELL_ED)
                
                # If it's a blank padding row, disable editing entirely
                if not ele:
                    att_e.setReadOnly(True)
                    att_e.setStyleSheet(CELL_RO)
                else:
                    att_e.setValidator(validator)
                    
                grid.addWidget(att_e, row, 2)

                self._att_entries.append(att_e)
                self._rows.append((ele, wl, att_e))

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------

    def _collect(self) -> dict:
        rows = []
        for ele, wl, att_e in self._rows:
            if ele:  # only save non-empty rows
                try:
                    att_val = int(att_e.text()) if att_e.text() else 0
                except ValueError:
                    att_val = 0
                rows.append({
                    "element":    ele,
                    "wavelength": wl,
                    "att_value":  att_val,
                })
        return {"rows": rows}

    def _load(self):
        """
        Pulls element definitions from MasterElement DB, and merges 
        with specific attenuator values saved in the AnalyticalGroup JSON.
        """
        session = get_session()
        try:
            # 1. Fetch all available elements from Master DB
            master_elements = session.query(MasterElement).order_by(MasterElement.display_order).all()
            
            # 2. Fetch the saved attenuator values for this specific analytical group
            saved_att_values = {}
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_02_attenuator and g.page_02_attenuator.get("rows"):
                # Create a lookup dictionary keyed by (element, wavelength)
                for r in g.page_02_attenuator["rows"]:
                    saved_att_values[(r["element"], r["wavelength"])] = r.get("att_value", 0)

            # 3. Construct rows combining master definition and group-specific saved values
            rows = []
            for me in master_elements:
                ele = me.ele_name or ""
                wl = me.wavelength or ""
                
                # Fetch saved value, default to 0 if no value exists yet
                att = saved_att_values.get((ele, wl), 0)
                rows.append((ele, wl, att))

            self._populate_grids(rows)

        finally:
            session.close()

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_02_attenuator = self._collect()
                session.commit()
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Buttons
    # ------------------------------------------------------------------

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Attenuator information saved.")

    def _on_next(self):
        self._save()
        from ui.anainf.page_03_element import ElementPage
        self.main_window.set_right_widget(
            ElementPage(self.main_window, self.group_id, self.group_name))

    def _on_pre(self):
        self._save()
        from ui.anainf.page_01_condition import AnalyticalConditionPage
        self.main_window.set_right_widget(
            AnalyticalConditionPage(self.main_window, self.group_id, self.group_name))

    def _on_print(self):
        QMessageBox.information(self, "Print", "Print coming soon.")

    def _on_cancel(self):
        if QMessageBox.question(
            self, "Cancel", "Discard changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            from ui.anainf.page_01_condition import AnalyticalConditionPage
            self.main_window.set_right_widget(
                AnalyticalConditionPage(self.main_window, self.group_id, self.group_name))