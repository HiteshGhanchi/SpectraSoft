from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QComboBox, QStyledItemDelegate, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")

# Dropdown Options
PI_OPTIONS = ["I:Integ.Mode", "P:PDA.Mode"]
METHOD_OPTIONS = [
    "0:Integation", "2:Distribution", "6:Metarographic", 
    "9:Interval integration", "A:To Get Sampling Count", "I:Input For DCA"
]
AREA_OPTIONS = ["S:Spark Area", "A:Arc Area", "T:Total Area"]

# LAS 2023 Defaults exactly as spec'd in the TOML
DEFAULT_DATA = [
    ["FE", "I:Integ.Mode", "2:Distribution", "20", "80", "", "T:Total Area"],
    ["C", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["SI", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["MN", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["P", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "S:Spark Area"],
    ["S", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "S:Spark Area"],
    ["CR", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["NI", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["MO", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["CU", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["V", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["TI", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "S:Spark Area"],
    ["W", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["B", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "S:Spark Area"],
    ["NB", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["CA", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "A:Arc Area"],
    ["CO", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["SN", "I:Integ.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["N", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
    ["PB", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "A:Arc Area"],
    ["AL", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "A:Arc Area"],
    ["CE", "P:PDA.Mode", "9:Interval integration", "20", "80", "", "T:Total Area"],
]

class IntegerDelegate(QStyledItemDelegate):
    """Restricts table cells to only accept integer values (for M, N, I columns)."""
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QIntValidator(0, 99999, editor))
        return editor

class MeasurementPage(QWidget):
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
        bar = QLabel(f"Measurement Mode - {self.group_name}")
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

        # Table Setup (7 columns)
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "Ele.Name", "P/I", "Method", "M", "N", "I", "Area"
        ])
        
        # Apply Integer Validator Delegate to M (3), N (4), and I (5)
        int_delegate = IntegerDelegate(self.table)
        self.table.setItemDelegateForColumn(3, int_delegate)
        self.table.setItemDelegateForColumn(4, int_delegate)
        self.table.setItemDelegateForColumn(5, int_delegate)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
            QComboBox { background: white; color: black; border: none; }
        """)
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
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    def _create_combobox(self, options, current_text):
        cb = QComboBox()
        cb.addItems(options)
        cb.setCurrentText(current_text)
        return cb

    def _add_row(self, row_idx, data):
        self.table.insertRow(row_idx)
        
        # Column 0: Ele.Name (Text)
        item_ele = QTableWidgetItem(data[0])
        item_ele.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItem(row_idx, 0, item_ele)

        # Column 1: P/I (ComboBox)
        self.table.setCellWidget(row_idx, 1, self._create_combobox(PI_OPTIONS, data[1]))
        
        # Column 2: Method (ComboBox)
        self.table.setCellWidget(row_idx, 2, self._create_combobox(METHOD_OPTIONS, data[2]))

        # Columns 3, 4, 5: M, N, I (Text with int delegate)
        for col_idx in (3, 4, 5):
            item_int = QTableWidgetItem(data[col_idx])
            item_int.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, col_idx, item_int)

        # Column 6: Area (ComboBox)
        self.table.setCellWidget(row_idx, 6, self._create_combobox(AREA_OPTIONS, data[6]))

    def _collect(self) -> dict:
        rows = []
        for row in range(self.table.rowCount()):
            # Extract Text
            ele = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
            m   = self.table.item(row, 3).text() if self.table.item(row, 3) else ""
            n   = self.table.item(row, 4).text() if self.table.item(row, 4) else ""
            i   = self.table.item(row, 5).text() if self.table.item(row, 5) else ""
            
            # Extract ComboBox values
            pi_widget = self.table.cellWidget(row, 1)
            pi = pi_widget.currentText() if isinstance(pi_widget, QComboBox) else ""
            
            method_widget = self.table.cellWidget(row, 2)
            method = method_widget.currentText() if isinstance(method_widget, QComboBox) else ""
            
            area_widget = self.table.cellWidget(row, 6)
            area = area_widget.currentText() if isinstance(area_widget, QComboBox) else ""
            
            rows.append([ele, pi, method, m, n, i, area])
            
        return {"rows": rows}

    def _apply(self, data: dict):
        self.table.setRowCount(0)
        rows = data.get("rows", [])
        
        if not rows:
            rows = DEFAULT_DATA
            
        for i, row in enumerate(rows):
            # Pad the row safely in case of corrupted DB json
            while len(row) < 7: row.append("")
            self._add_row(i, row)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_05_measurement = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_05_measurement:
                self._apply(g.page_05_measurement)
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
            from ui.anainf.page_06_recalibration import RecalibrationPage
            self.main_window.set_right_widget(
                RecalibrationPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 06 (Recalibration) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_04_channel import ChannelPage
            self.main_window.set_right_widget(
                ChannelPage(self.main_window, self.group_id, self.group_name))
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