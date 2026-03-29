from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDoubleValidator

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")

# The 22 standard LAS 2023 elements
ELEMENTS = [
    "FE", "C", "SI", "MN", "P", "S", "CR", "NI", "MO", "CU", "V",
    "TI", "W", "B", "NB", "CA", "CO", "SN", "N", "PB", "AL", "CE"
]

def get_default_master_curve_data():
    """Returns the default row structure for all 22 elements."""
    data = {}
    for ele in ELEMENTS:
        data[ele] = {
            "mc_sample": "",
            "target": ".00000",
            "d1": ".00000",
            "d2": "100.00",
            "ac": ".00000",
            "mc": "1.0000",
            "flag": ""
        }
    return data

class FloatDelegate(QStyledItemDelegate):
    """Restricts table cells to accept only valid float/decimal numbers."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        editor.setValidator(validator)
        editor.setStyleSheet("background: white; color: black; font: 9pt Arial;")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return editor

class MasterCurvePage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(BG))
        self.setPalette(p)
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Title bar
        bar = QLabel(f"Master Curve Information - {self.group_name}")
        bar.setFixedHeight(22)
        bar.setContentsMargins(8, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet("background:#5c9bd5;color:white;font:bold 10pt Arial;")
        root.addWidget(bar)

        # White outer frame
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)

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
        ml.setSpacing(15)

        # --- TABLE SETUP ---
        # 8 Columns: Ele.Name | M.C.Sample | Target | D1 | D2 | AC | MC | Flag
        self.table = QTableWidget(len(ELEMENTS), 8)
        self.table.setHorizontalHeaderLabels([
            "Ele.Name", "M.C.Sample", "Target", "D1", "D2", "AC", "MC", "Flag"
        ])
        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        
        # Apply FloatDelegate to numeric columns (Target: 2, D1: 3, D2: 4, AC: 5, MC: 6)
        float_delegate = FloatDelegate(self.table)
        for col in range(2, 7):
            self.table.setItemDelegateForColumn(col, float_delegate)
        
        # Initialize Rows
        for i, ele in enumerate(ELEMENTS):
            item_ele = QTableWidgetItem(ele)
            item_ele.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_ele.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_ele.setBackground(QColor("#f0f0f0"))
            self.table.setItem(i, 0, item_ele)
            
            for col in range(1, 8):
                item_val = QTableWidgetItem("")
                item_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, col, item_val)

        ml.addWidget(self.table)
        ml.addStretch()

        # Bottom nav buttons
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), QColor(BG))
        btn_bar.setPalette(bbp)
        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(10, 4, 10, 8)
        bbl.setSpacing(4)
        
        for txt, slot in [("1:OK", self._on_ok), ("2:Next", self._on_next),
                           ("3:Pre.", self._on_pre), ("4:Print", self._on_print)]:
            b = QPushButton(txt)
            b.setStyleSheet(BTN)
            b.clicked.connect(slot)
            bbl.addWidget(b)
            
        bbl.addStretch()
        
        # Add the custom 7:Init. button requested in the TOML
        btn_init = QPushButton("7:Init.")
        btn_init.setStyleSheet(BTN)
        btn_init.clicked.connect(self._on_init)
        bbl.addWidget(btn_init)
        
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    # ----------------------- Core Functions -----------------------

    def _on_init(self):
        reply = QMessageBox.question(
            self, "Confirm Initialization", 
            "Initialize all Master Curve parameters to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._apply({}) # Empty dict triggers default loading
            self._save()

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        data = {}
        for i, ele in enumerate(ELEMENTS):
            data[ele] = {
                "mc_sample": self.table.item(i, 1).text().strip() if self.table.item(i, 1) else "",
                "target": self.table.item(i, 2).text().strip() if self.table.item(i, 2) else "",
                "d1": self.table.item(i, 3).text().strip() if self.table.item(i, 3) else "",
                "d2": self.table.item(i, 4).text().strip() if self.table.item(i, 4) else "",
                "ac": self.table.item(i, 5).text().strip() if self.table.item(i, 5) else "",
                "mc": self.table.item(i, 6).text().strip() if self.table.item(i, 6) else "",
                "flag": self.table.item(i, 7).text().strip() if self.table.item(i, 7) else "",
            }
        return data

    def _apply(self, data: dict):
        if not data:
            data = get_default_master_curve_data()
            
        for i, ele in enumerate(ELEMENTS):
            ele_data = data.get(ele, get_default_master_curve_data()[ele])
            
            if self.table.item(i, 1): self.table.item(i, 1).setText(ele_data.get("mc_sample", ""))
            if self.table.item(i, 2): self.table.item(i, 2).setText(ele_data.get("target", ".00000"))
            if self.table.item(i, 3): self.table.item(i, 3).setText(ele_data.get("d1", ".00000"))
            if self.table.item(i, 4): self.table.item(i, 4).setText(ele_data.get("d2", "100.00"))
            if self.table.item(i, 5): self.table.item(i, 5).setText(ele_data.get("ac", ".00000"))
            if self.table.item(i, 6): self.table.item(i, 6).setText(ele_data.get("mc", "1.0000"))
            if self.table.item(i, 7): self.table.item(i, 7).setText(ele_data.get("flag", ""))

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_11_master_curve = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_11_master_curve:
                self._apply(g.page_11_master_curve)
            else:
                self._apply({}) # Triggers defaults
        finally:
            session.close()

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Saved successfully.")

    def _on_next(self):
        self._save()
        try:
            from ui.anainf.page_12_analytical_mode import AnalyticalModePage
            self.main_window.set_right_widget(
                AnalyticalModePage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 12 (Analytical Mode) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_10_display import DisplayPage
            self.main_window.set_right_widget(
                DisplayPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            pass

    def _on_print(self):
        QMessageBox.information(self, "Print", "Print coming soon.")

    def _on_cancel(self):
        if QMessageBox.question(self, "Cancel", "Discard changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self._load()
            self._on_pre()