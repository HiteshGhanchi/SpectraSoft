from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")

MASTER_ELEMENTS = [
    ("FE","Fe","273.0"), ("C","C","193.0"), ("SI","Si","212.4"),
    ("MN","Mn","293.3"), ("P","P","178.3"), ("S","S","180.7"),
    ("V","V","311.0"), ("CR","Cr","267.7"), ("CR","Cr","298.9"),
    ("MO","Mo","202.0"), ("MO","Mo","277.5"), ("NI","Ni","231.6"),
    ("NI","Ni","227.7"), ("AL","Al","394.4"), ("CU","Cu","224.2"),
    ("TI","Ti","337.2"), ("W","W","220.4"), ("B","B","182.6"),
    ("NB","Nb","319.5"), ("CA","Ca","396.8"), ("CO","Co","258.0"),
    ("SN","Sn","189.9"), ("N","N","174.5*2"), ("PB","Pb","405.7"),
    ("RH","Rh","421.8"), ("CE","",""),
]

DEFAULT_DATA = [
    ("FE", ".00000", "100.00", "*", "Fe", "FE"),
    ("C", ".00000", "100.00", "", "C", "C"),
    ("SI", ".00000", "100.00", "", "Si", "SI"),
    ("MN", ".00000", "100.00", "", "Mn", "MN"),
    ("P", ".00000", "100.00", "", "P", "P"),
    ("S", ".00000", "100.00", "", "S", "S"),
    ("CR", ".00000", "100.00", "", "Cr", "CR"),
    ("NI", ".00000", "100.00", "", "Ni", "NI"),
    ("MO", ".00000", "100.00", "", "Mo", "MO"),
    ("CU", ".00000", "100.00", "", "Cu", "CU"),
    ("V", ".00000", "100.00", "", "V", "V"),
    ("TI", ".00000", "100.00", "", "Ti", "TI"),
    ("W", ".00000", "100.00", "", "W", "W"),
    ("B", ".00000", "100.00", "", "B", "B"),
    ("NB", ".00000", "100.00", "", "Nb", "NB"),
    ("CA", ".00000", "100.00", "", "Ca", "CA"),
    ("CO", ".00000", "100.00", "", "Co", "CO"),
    ("SN", ".00000", "100.00", "", "Sn", "SN"),
    ("N", ".00000", "100.00", "", "N", "N"),
    ("PB", ".00000", "100.00", "", "Pb", "PB"),
    ("AL", ".00000", "100.00", "", "Al", "AL"),
    ("CE", ".00000", ".00000", "", "", ""),
]

class ElementPickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Element")
        self.setFixedSize(250, 400)
        self.setStyleSheet(f"background:{BG}; color:black; font:9pt Arial;")
        self.selected_ele = None
        self.selected_chem = None
        
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background:white; color:black; border:1px solid #aaa;")
        
        # We only want unique elements for the Name picker
        seen = set()
        for ele, chem, _ in MASTER_ELEMENTS:
            if ele not in seen:
                seen.add(ele)
                item = QListWidgetItem(f"{ele} ({chem})")
                item.setData(Qt.ItemDataRole.UserRole, (ele, chem))
                self.list_widget.addItem(item)
                
        self.list_widget.itemDoubleClicked.connect(self.accept_selection)
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(BTN)
        ok_btn.clicked.connect(self.accept_selection)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(BTN)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def accept_selection(self):
        item = self.list_widget.currentItem()
        if item:
            self.selected_ele, self.selected_chem = item.data(Qt.ItemDataRole.UserRole)
            self.accept()


class ElementPage(QWidget):
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

        # Title bar (Auto-updates CH count)
        self.title_bar = QLabel(f"Element Information - CH  0 - {self.group_name}")
        self.title_bar.setFixedHeight(22)
        self.title_bar.setContentsMargins(8, 0, 0, 0)
        self.title_bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.title_bar.setStyleSheet("background:#5c9bd5;color:white;font:bold 10pt Arial;")
        root.addWidget(self.title_bar)

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
        ml.setSpacing(8)

        # Table Control Buttons
        ctrl_layout = QHBoxLayout()
        btn_insert = QPushButton("S3:Insert")
        btn_insert.setStyleSheet(BTN)
        btn_insert.clicked.connect(self._on_insert)
        
        btn_delete = QPushButton("S4:Delete")
        btn_delete.setStyleSheet(BTN)
        btn_delete.clicked.connect(self._on_delete)
        
        btn_ele = QPushButton("6:Ele.")
        btn_ele.setStyleSheet(BTN)
        btn_ele.clicked.connect(self._on_pick_element)

        ctrl_layout.addWidget(btn_insert)
        ctrl_layout.addWidget(btn_delete)
        ctrl_layout.addWidget(btn_ele)
        ctrl_layout.addStretch()
        ml.addLayout(ctrl_layout)

        # Table Setup
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Ele.Name", "Analytical Range (min)", "Analytical Range (max)", "*", "Chemic.Ele.", "Element"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        self.table.itemChanged.connect(self._update_ch_count)
        ml.addWidget(self.table)

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

    def _update_ch_count(self):
        count = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text().strip():
                count += 1
        self.title_bar.setText(f"Element Information - CH  {count} - {self.group_name}")

    def _add_row(self, row_idx, data):
        self.table.insertRow(row_idx)
        for col_idx, text in enumerate(data):
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, col_idx, item)

    def _on_insert(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            current_row = self.table.rowCount()
        self._add_row(current_row, ["", ".00000", "100.00", "", "", ""])

    def _on_delete(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            self._update_ch_count()

    def _on_pick_element(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Required", "Please select a row first.")
            return

        dialog = ElementPickerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ele, chem = dialog.selected_ele, dialog.selected_chem
            
            # Temporarily disconnect to avoid mass trigger of _update_ch_count
            self.table.itemChanged.disconnect(self._update_ch_count)
            
            self.table.item(current_row, 0).setText(ele)
            self.table.item(current_row, 4).setText(chem)
            self.table.item(current_row, 5).setText(ele)
            
            self.table.itemChanged.connect(self._update_ch_count)
            self._update_ch_count()

    def _collect(self) -> list:
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(6):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return data

    def _apply(self, data: list):
        self.table.setRowCount(0)
        self.table.itemChanged.disconnect(self._update_ch_count)
        
        if not data:
            data = DEFAULT_DATA
            
        for i, row_data in enumerate(data):
            self._add_row(i, row_data)
            
        self.table.itemChanged.connect(self._update_ch_count)
        self._update_ch_count()

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_03_element = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                # Assuming g.page_03_element is a JSON-encoded list of lists in DB
                self._apply(g.page_03_element)
        finally:
            session.close()

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Saved successfully.")

    def _on_next(self):
        self._save()
        try:
            from ui.anainf.page_04_channel import Page04Channel
            self.main_window.set_right_widget(
                Page04Channel(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 04 (Channel) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_02_attenuator import Page02Attenuator
            self.main_window.set_right_widget(
                Page02Attenuator(self.main_window, self.group_id, self.group_name))
        except ImportError:
            pass

    def _on_print(self):
        QMessageBox.information(self, "Print", "Print coming soon.")

    def _on_cancel(self):
        if QMessageBox.question(self, "Cancel", "Discard changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self._load() # Just reload from DB to discard unsaved UI changes
            self._on_pre()