from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QDialog, QListWidget, QListWidgetItem, QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator

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

# LAS 2023 Defaults exactly as requested in REMAINING_WORK.toml
DEFAULT_DATA = [
    ["FE", "273.0", "1", "", "", ""],
    ["C", "193.0", "2", "", "FE", "273.0"],
    ["SI", "212.4", "2", "", "FE", "273.0"],
    ["MN", "293.3", "2", "", "FE", "273.0"],
    ["P", "178.3", "1", "", "FE", "273.0"],
    ["S", "180.7", "1", "", "FE", "273.0"],
    ["CR", "267.7", "2", "", "FE", "273.0"],
    ["NI", "231.6", "2", "", "FE", "273.0"],
    ["MO", "202.0", "2", "", "FE", "273.0"],
    ["CU", "224.2", "2", "", "FE", "273.0"],
    ["V", "311.0", "2", "", "FE", "273.0"],
    ["TI", "337.2", "1", "", "FE", "273.0"],
    ["W", "220.4", "2", "", "FE", "273.0"],
    ["B", "182.6", "1", "", "FE", "273.0"],
    ["NB", "319.5", "2", "", "FE", "273.0"],
    ["CA", "396.8", "1", "", "FE", "273.0"],
    ["CO", "258.0", "2", "", "FE", "273.0"],
    ["SN", "189.9", "2", "", "FE", "273.0"],
    ["N", "174.5*2", "2", "", "FE", "273.0"],
    ["PB", "405.7", "1", "", "FE", "273.0"],
    ["AL", "394.4", "1", "", "FE", "273.0"],
    ["CE", "", "1", "", "", ""]
]

class ContextPickerDialog(QDialog):
    def __init__(self, title, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(250, 400)
        self.setStyleSheet(f"background:{BG}; color:black; font:9pt Arial;")
        self.selected_value = None
        
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background:white; color:black; border:1px solid #aaa;")
        
        for item_text, item_data in items:
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item_data)
            self.list_widget.addItem(list_item)
                
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
            self.selected_value = item.data(Qt.ItemDataRole.UserRole)
            self.accept()


class SeqDelegate(QStyledItemDelegate):
    """Restricts the SEQ column to only accept '1', '2', or '3'."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QIntValidator(1, 3, editor)
        editor.setValidator(validator)
        return editor


class Page04Channel(QWidget):
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
        bar = QLabel(f"Channel Information - {self.group_name}")
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
        ml.setSpacing(8)

        # Table Setup (6 columns based on TOML specs)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Ele.Name", "W.Length", "SEQ", "W-No.", "Internal Element", ""
        ])
        
        # Apply Validator to SEQ column (Index 2)
        self.table.setItemDelegateForColumn(2, SeqDelegate(self.table))

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        ml.addWidget(self.table)

        # Table Control Buttons (Centered below table)
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addStretch()
        
        btn_add = QPushButton("S2:Add")
        btn_add.setStyleSheet(BTN)
        btn_add.clicked.connect(self._on_add)
        
        btn_insert = QPushButton("S3:Insert")
        btn_insert.setStyleSheet(BTN)
        btn_insert.clicked.connect(self._on_insert)
        
        btn_delete = QPushButton("S4:Delete")
        btn_delete.setStyleSheet(BTN)
        btn_delete.clicked.connect(self._on_delete)

        ctrl_layout.addWidget(btn_add)
        ctrl_layout.addWidget(btn_insert)
        ctrl_layout.addWidget(btn_delete)
        ctrl_layout.addStretch()
        ml.addLayout(ctrl_layout)
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
        
        btn_ele = QPushButton("6:Ele.")
        btn_ele.setStyleSheet(BTN)
        btn_ele.clicked.connect(self._on_pick_element)
        bbl.addWidget(btn_ele)
        
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        
        root.addWidget(btn_bar)

    def _add_row(self, row_idx, data):
        self.table.insertRow(row_idx)
        for col_idx, text in enumerate(data):
            if col_idx >= 6: break
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, col_idx, item)

    def _on_add(self):
        row = self.table.rowCount()
        self._add_row(row, ["", "", "1", "", "", ""])

    def _on_insert(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            current_row = self.table.rowCount()
        self._add_row(current_row, ["", "", "1", "", "", ""])

    def _on_delete(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def _on_pick_element(self):
        current_row = self.table.currentRow()
        current_col = self.table.currentColumn()
        
        if current_row < 0:
            QMessageBox.warning(self, "Selection Required", "Please select a cell first.")
            return

        if current_col == 0:
            # Mode 1: Element Name
            items = []
            seen = set()
            for ele, _, _ in MASTER_ELEMENTS:
                if ele not in seen and ele != "CE":
                    seen.add(ele)
                    items.append((ele, ele))
            items.append(("CE", "CE"))
            
            dialog = ContextPickerDialog("Select Element", items, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.table.item(current_row, 0).setText(dialog.selected_value)

        elif current_col == 1:
            # Mode 2: Wavelength for currently typed element
            ele_item = self.table.item(current_row, 0)
            target_ele = ele_item.text().strip().upper() if ele_item else ""
            
            items = []
            for ele, _, wave in MASTER_ELEMENTS:
                if ele == target_ele and wave:
                    items.append((wave, wave))
            
            if not items:
                QMessageBox.information(self, "No Wavelengths", f"No specific wavelengths found for '{target_ele}'.")
                return
                
            dialog = ContextPickerDialog(f"Wavelengths for {target_ele}", items, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.table.item(current_row, 1).setText(dialog.selected_value)

        elif current_col in (4, 5):
            # Mode 3: Internal Element (Element + Wavelength)
            items = []
            for ele, _, wave in MASTER_ELEMENTS:
                if ele and wave:
                    display = f"{ele}   {wave}"
                    items.append((display, (ele, wave)))
                    
            dialog = ContextPickerDialog("Select Internal Element", items, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                sel_ele, sel_wave = dialog.selected_value
                self.table.item(current_row, 4).setText(sel_ele)
                self.table.item(current_row, 5).setText(sel_wave)
        else:
            QMessageBox.warning(self, "Invalid Column", "Please select the Ele.Name, W.Length, or Internal Element column to use this button.")

    def _collect(self) -> dict:
        rows = []
        for row in range(self.table.rowCount()):
            row_data = {
                "ele_name": self.table.item(row, 0).text() if self.table.item(row, 0) else "",
                "w_length": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
                "seq":      self.table.item(row, 2).text() if self.table.item(row, 2) else "1",
                "w_no":     self.table.item(row, 3).text() if self.table.item(row, 3) else "",
                "int_ele":  self.table.item(row, 4).text() if self.table.item(row, 4) else "",
                "int_wav":  self.table.item(row, 5).text() if self.table.item(row, 5) else "",
            }
            rows.append(row_data)
        return {"rows": rows}

    def _apply(self, data: dict):
        self.table.setRowCount(0)
        rows = data.get("rows", [])
        
        if not rows:
            # Load Defaults
            for i, row_data in enumerate(DEFAULT_DATA):
                self._add_row(i, row_data)
        else:
            for i, row in enumerate(rows):
                self._add_row(i, [
                    row.get("ele_name", ""),
                    row.get("w_length", ""),
                    row.get("seq", "1"),
                    row.get("w_no", ""),
                    row.get("int_ele", ""),
                    row.get("int_wav", "")
                ])

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_04_channel = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_04_channel:
                self._apply(g.page_04_channel)
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
            from ui.anainf.page_05_measurement import MeasurementPage
            self.main_window.set_right_widget(
                MeasurementPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 05 (Measurement) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_03_element import ElementPage
            self.main_window.set_right_widget(
                ElementPage(self.main_window, self.group_id, self.group_name))
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