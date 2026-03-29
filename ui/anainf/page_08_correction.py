from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

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

def get_default_correction_data():
    """FE gets 'I', everything else gets 'N' by default."""
    data = {}
    for ele in ELEMENTS:
        if ele == "FE":
            data[ele] = "I"
        else:
            data[ele] = "N"
    return data

class YNIDelegate(QStyledItemDelegate):
    """Restricts the Y/N/I columns to accept only 1 character."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setMaxLength(1)
        editor.setStyleSheet("background: white; color: black; font: 9pt Arial;")
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return editor

class CorrectionPage(QWidget):
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
        bar = QLabel(f"100% Correction - {self.group_name}")
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
        # 11 rows, 4 columns (Ele | Y/N/I | Ele | Y/N/I)
        self.table = QTableWidget(11, 4)
        self.table.setHorizontalHeaderLabels(["Ele.Name", "Y/N/I", "Ele.Name", "Y/N/I"])
        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        
        # Apply 1-char text delegate to editable columns
        delegate = YNIDelegate(self.table)
        self.table.setItemDelegateForColumn(1, delegate)
        self.table.setItemDelegateForColumn(3, delegate)
        
        # Populate Static Element Names
        for i, ele in enumerate(ELEMENTS):
            row = i % 11
            col_ele = 0 if i < 11 else 2
            col_val = 1 if i < 11 else 3
            
            # Element Name Item (Read-Only, Greyed slightly)
            item_ele = QTableWidgetItem(ele)
            item_ele.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_ele.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_ele.setBackground(QColor("#f0f0f0"))
            self.table.setItem(row, col_ele, item_ele)
            
            # Value Item (Editable)
            item_val = QTableWidgetItem("")
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, col_val, item_val)

        ml.addWidget(self.table)

        # --- LEGEND ---
        legend_text = (
            "Y: Require 100% correction\n"
            "N: Not require 100% correction\n"
            "I: Base Element\n"
            "Space = same meaning as I"
        )
        legend_lbl = QLabel(legend_text)
        legend_lbl.setStyleSheet("color: black; font: 9pt Arial;")
        ml.addWidget(legend_lbl)
        
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
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        data = {}
        for i, ele in enumerate(ELEMENTS):
            row = i % 11
            col_val = 1 if i < 11 else 3
            item = self.table.item(row, col_val)
            val = item.text().strip().upper() if item else ""
            data[ele] = val
        return data

    def _apply(self, data: dict):
        if not data:
            data = get_default_correction_data()
            
        for i, ele in enumerate(ELEMENTS):
            row = i % 11
            col_val = 1 if i < 11 else 3
            val = data.get(ele, "N") # Fallback to N if corrupted
            
            item = self.table.item(row, col_val)
            if item:
                item.setText(val)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_08_correction = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_08_correction:
                self._apply(g.page_08_correction)
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
            from ui.anainf.page_09_standard import StandardPage
            self.main_window.set_right_widget(
                StandardPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 09 (Standard) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_07_working_curve import WorkingCurvePage
            self.main_window.set_right_widget(
                WorkingCurvePage(self.main_window, self.group_id, self.group_name))
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