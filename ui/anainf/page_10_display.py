from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QStackedWidget, QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator

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

def get_default_display_data():
    """Returns sequential order and 0s for magnification/formatting."""
    data = {"tab1_disp": []}
    for i, ele in enumerate(ELEMENTS):
        data["tab1_disp"].append({
            "ele": ele,
            "order": str(i + 1),
            "magn": "0",
            "int_val": "0",
            "deci": "0"
        })
    return data

class IntegerDelegate(QStyledItemDelegate):
    """Restricts table cells to accept only integers."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QIntValidator(-9999, 9999, editor))
        editor.setStyleSheet("background: white; color: black; font: 9pt Arial;")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return editor

class DisplayPage(QWidget):
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
        bar = QLabel(f"Display and Printout Format - {self.group_name}")
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
        ml.setSpacing(10)

        # --- STACKED WIDGET FOR TABS ---
        self.stack = QStackedWidget()
        
        # Tab 1: Disp. and Print
        self.tab_disp = QWidget()
        disp_layout = QVBoxLayout(self.tab_disp)
        disp_layout.setContentsMargins(0, 0, 0, 0)
        
        self.table = QTableWidget(len(ELEMENTS), 5)
        self.table.setHorizontalHeaderLabels(["Ele.Name", "Order", "Magn.", "Int.", "Deci."])
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        
        int_delegate = IntegerDelegate(self.table)
        for col in range(1, 5):
            self.table.setItemDelegateForColumn(col, int_delegate)

        for i, ele in enumerate(ELEMENTS):
            item_ele = QTableWidgetItem(ele)
            item_ele.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_ele.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_ele.setBackground(QColor("#f0f0f0"))
            self.table.setItem(i, 0, item_ele)
            
            for col in range(1, 5):
                item_val = QTableWidgetItem("")
                item_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(i, col, item_val)
                
        disp_layout.addWidget(self.table)
        self.stack.addWidget(self.tab_disp)

        # Tab 2: Trans. (Placeholder)
        self.tab_trans = QWidget()
        trans_layout = QVBoxLayout(self.tab_trans)
        lbl_trans = QLabel("Transmission Mode Layout\n[TBD - Pending Screenshot]")
        lbl_trans.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_trans.setStyleSheet("color: #666; font: bold 14pt Arial;")
        trans_layout.addWidget(lbl_trans)
        self.stack.addWidget(self.tab_trans)

        ml.addWidget(self.stack, stretch=1)

        # Sub-panel Navigation Buttons (S2, S3)
        sub_btn_layout = QHBoxLayout()
        btn_dp = QPushButton("S2:D/P")
        btn_dp.setStyleSheet(BTN)
        btn_dp.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        btn_trans = QPushButton("S3:Trans.")
        btn_trans.setStyleSheet(BTN)
        btn_trans.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        sub_btn_layout.addWidget(btn_dp)
        sub_btn_layout.addWidget(btn_trans)
        sub_btn_layout.addStretch()
        ml.addLayout(sub_btn_layout)

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
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        data = {"tab1_disp": []}
        for i, ele in enumerate(ELEMENTS):
            row_data = {
                "ele": ele,
                "order": self.table.item(i, 1).text().strip() if self.table.item(i, 1) else "",
                "magn":  self.table.item(i, 2).text().strip() if self.table.item(i, 2) else "",
                "int_val": self.table.item(i, 3).text().strip() if self.table.item(i, 3) else "",
                "deci":  self.table.item(i, 4).text().strip() if self.table.item(i, 4) else ""
            }
            data["tab1_disp"].append(row_data)
        # Note: Add 'tab2_trans' collection here later once built
        return data

    def _apply(self, data: dict):
        if not data:
            data = get_default_display_data()
            
        rows = data.get("tab1_disp", [])
        if not rows:
            rows = get_default_display_data()["tab1_disp"]
            
        for i, row_data in enumerate(rows):
            if i >= self.table.rowCount(): break
            
            if self.table.item(i, 1): self.table.item(i, 1).setText(row_data.get("order", ""))
            if self.table.item(i, 2): self.table.item(i, 2).setText(row_data.get("magn", "0"))
            if self.table.item(i, 3): self.table.item(i, 3).setText(row_data.get("int_val", "0"))
            if self.table.item(i, 4): self.table.item(i, 4).setText(row_data.get("deci", "0"))

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_10_display = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_10_display:
                self._apply(g.page_10_display)
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
            from ui.anainf.page_11_master_curve import MasterCurvePage
            self.main_window.set_right_widget(
                MasterCurvePage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 11 (Master Curve) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_09_standard import StandardPage
            self.main_window.set_right_widget(
                StandardPage(self.main_window, self.group_id, self.group_name))
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