from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QListWidget, QListWidgetItem, QGridLayout, QLineEdit,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDoubleValidator

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")
GROUP_BOX_STYLE = ("QGroupBox{font:bold 9pt Arial;color:black;border:1px solid #999;"
                   "margin-top:8px;padding-top:4px;background:#d4d0c8;}"
                   "QGroupBox::title{subcontrol-origin:margin;left:8px;color:black;}")

ELEMENTS_LIST = [
    "FE1", "C1", "SI1", "MN1", "P1", "S1", "CR1", "NI1", "MO1", "CU1", 
    "V1", "TI1", "W1", "B1", "NB1", "CA1", "CO1", "SN1", "N1", "PB1", 
    "AL1", "CE1"
]

MASTER_ELEMENTS = [
    "FE", "C", "SI", "MN", "P", "S", "V", "CR", "MO", "NI", 
    "AL", "CU", "TI", "W", "B", "NB", "CA", "CO", "SN", "N", "PB", "CE"
]

def get_default_curve_data():
    return {
        "divide": "1", "no": "1", 
        "range_min": ".00000", "range_max": "100.00", 
        "unit": "%", "order": "1", "std": ".000000000",
        "cf_a": ".000000000", "cf_b": ".000000000", 
        "cf_c": "1.00000000", "cf_d": ".000000000"
    }

def get_default_matrix_data():
    # 16 rows total (8 for left table, 8 for right table)
    # [D/L, Ele.Name, Coefficient]
    return [["", "", ".000000000"] for _ in range(16)]

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
        
        for item_text in items:
            list_item = QListWidgetItem(item_text)
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
            self.selected_value = item.text()
            self.accept()

class WorkingCurvePage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        
        # Internal Data Store: ele_name -> {"curves": {1: dict, 2: dict...}, "matrix": list}
        self.data_store = {
            ele: {"curves": {"1": get_default_curve_data()}, "matrix": get_default_matrix_data()} 
            for ele in ELEMENTS_LIST
        }
        self.current_ele = None
        
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
        bar = QLabel(f"Working Curve and Matrix Coefficient - {self.group_name}")
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

        ml = QHBoxLayout(inner)
        ml.setContentsMargins(10, 10, 10, 6)
        ml.setSpacing(10)

        # --- LEFT PANEL: Element List ---
        self.ele_list = QListWidget()
        self.ele_list.setFixedWidth(120)
        self.ele_list.setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: 9pt Arial;")
        self.ele_list.addItems(ELEMENTS_LIST)
        self.ele_list.currentItemChanged.connect(self._on_list_changed)
        ml.addWidget(self.ele_list)

        # --- RIGHT PANEL: Details ---
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # 1. Working Curve GroupBox
        wc_group = QGroupBox("Working Curve")
        wc_group.setStyleSheet(GROUP_BOX_STYLE)
        wc_layout = QGridLayout(wc_group)
        
        wc_layout.addWidget(self._label("Divide:"), 0, 0)
        self.ui_divide = self._line_edit()
        wc_layout.addWidget(self.ui_divide, 0, 1)
        
        wc_layout.addWidget(self._label("No.:"), 0, 2)
        self.ui_no = QComboBox()
        self.ui_no.addItems(["1", "2", "3", "4"])
        self.ui_no.setStyleSheet("background: white; color: black; border: 1px solid #aaa;")
        self.ui_no.currentTextChanged.connect(self._on_curve_no_changed)
        wc_layout.addWidget(self.ui_no, 0, 3)

        wc_layout.addWidget(self._label("Range:"), 1, 0)
        rng_lay = QHBoxLayout()
        self.ui_rng_min = self._line_edit()
        self.ui_rng_max = self._line_edit()
        rng_lay.addWidget(self.ui_rng_min)
        rng_lay.addWidget(QLabel("-"))
        rng_lay.addWidget(self.ui_rng_max)
        wc_layout.addLayout(rng_lay, 1, 1, 1, 3)

        wc_layout.addWidget(self._label("Unit:"), 2, 0)
        self.ui_unit = self._line_edit()
        wc_layout.addWidget(self.ui_unit, 2, 1)

        wc_layout.addWidget(self._label("Order:"), 2, 2)
        self.ui_order = self._line_edit()
        wc_layout.addWidget(self.ui_order, 2, 3)

        wc_layout.addWidget(self._label("STD.:"), 3, 0)
        self.ui_std = self._line_edit()
        wc_layout.addWidget(self.ui_std, 3, 1, 1, 3)

        # Coefficients row
        coef_lay = QHBoxLayout()
        coef_lay.addWidget(self._label("a:"))
        self.ui_cf_a = self._line_edit()
        coef_lay.addWidget(self.ui_cf_a)
        
        coef_lay.addWidget(self._label("b:"))
        self.ui_cf_b = self._line_edit()
        coef_lay.addWidget(self.ui_cf_b)
        
        coef_lay.addWidget(self._label("c:"))
        self.ui_cf_c = self._line_edit()
        coef_lay.addWidget(self.ui_cf_c)
        
        coef_lay.addWidget(self._label("d:"))
        self.ui_cf_d = self._line_edit()
        coef_lay.addWidget(self.ui_cf_d)
        wc_layout.addLayout(coef_lay, 4, 0, 1, 4)
        
        right_panel.addWidget(wc_group)

        # 2. Matrix Coefficient GroupBox
        mat_group = QGroupBox("Matrix Coefficient")
        mat_group.setStyleSheet(GROUP_BOX_STYLE)
        mat_layout = QHBoxLayout(mat_group)
        
        self.table_left = self._create_matrix_table()
        self.table_right = self._create_matrix_table()
        
        mat_layout.addWidget(self.table_left)
        mat_layout.addWidget(self.table_right)
        right_panel.addWidget(mat_group)

        # Sub-panel Navigation Buttons
        sub_btn_layout = QHBoxLayout()
        for txt, slot in [
            ("S3:P.Ele", self._on_prev_ele), 
            ("S2:N.Ele", self._on_next_ele),
            ("S9:P.W.C", self._on_prev_wc),
            ("S8:N.W.C", self._on_next_wc)
        ]:
            b = QPushButton(txt)
            b.setStyleSheet(BTN)
            b.clicked.connect(slot)
            sub_btn_layout.addWidget(b)
        sub_btn_layout.addStretch()
        right_panel.addLayout(sub_btn_layout)
        
        ml.addLayout(right_panel, stretch=1)

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

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: black; font: 9pt Arial;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return lbl

    def _line_edit(self):
        le = QLineEdit()
        le.setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: 9pt Arial;")
        return le

    def _create_matrix_table(self):
        table = QTableWidget(8, 3)
        table.setHorizontalHeaderLabels(["D/L", "Ele.Name", "Coefficient"])
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
            QComboBox { background: white; color: black; border: none; }
        """)
        for r in range(8):
            cb = QComboBox()
            cb.addItems(["", "L"])
            table.setCellWidget(r, 0, cb)
            for c in (1, 2):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(r, c, item)
        return table

    # ----------------------- Navigation & Binding -----------------------

    def _on_list_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        if previous:
            self._save_ui_to_element(previous.text(), self.ui_no.currentText())
            
        if current:
            self.current_ele = current.text()
            # Force No. to "1" on element change to avoid confusion
            self.ui_no.blockSignals(True)
            self.ui_no.setCurrentText("1")
            self.ui_no.blockSignals(False)
            self._load_element_to_ui(self.current_ele, "1")

    def _on_curve_no_changed(self, new_no):
        if not self.current_ele: return
        # User switched curves via dropdown. Save old curve data, load new.
        # Note: we don't know the PREVIOUS 'No' value natively here, so we must track it if needed.
        # But QComboBox currentTextChanged happens AFTER change. 
        pass 
        # For simplicity in this offline editor, we just collect all UI state on Save/Switch.

    def _save_ui_to_element(self, ele_name, curve_no="1"):
        """Scrape UI and save into memory dict."""
        if ele_name not in self.data_store: return
        
        # Save Curve Data
        curve_data = {
            "divide": self.ui_divide.text(), "no": self.ui_no.currentText(),
            "range_min": self.ui_rng_min.text(), "range_max": self.ui_rng_max.text(),
            "unit": self.ui_unit.text(), "order": self.ui_order.text(), "std": self.ui_std.text(),
            "cf_a": self.ui_cf_a.text(), "cf_b": self.ui_cf_b.text(), 
            "cf_c": self.ui_cf_c.text(), "cf_d": self.ui_cf_d.text()
        }
        self.data_store[ele_name]["curves"][curve_no] = curve_data

        # Save Matrix Data
        matrix = []
        for table in (self.table_left, self.table_right):
            for r in range(8):
                dl = table.cellWidget(r, 0).currentText()
                ele = table.item(r, 1).text() if table.item(r, 1) else ""
                coef = table.item(r, 2).text() if table.item(r, 2) else ""
                matrix.append([dl, ele, coef])
        self.data_store[ele_name]["matrix"] = matrix

    def _load_element_to_ui(self, ele_name, curve_no="1"):
        """Push memory data into UI fields."""
        ele_data = self.data_store.get(ele_name, {})
        curves = ele_data.get("curves", {})
        curve_data = curves.get(curve_no, get_default_curve_data())
        
        self.ui_divide.setText(curve_data.get("divide", "1"))
        self.ui_no.blockSignals(True)
        self.ui_no.setCurrentText(curve_data.get("no", "1"))
        self.ui_no.blockSignals(False)
        self.ui_rng_min.setText(curve_data.get("range_min", ".00000"))
        self.ui_rng_max.setText(curve_data.get("range_max", "100.00"))
        self.ui_unit.setText(curve_data.get("unit", "%"))
        self.ui_order.setText(curve_data.get("order", "1"))
        self.ui_std.setText(curve_data.get("std", ".000000000"))
        
        self.ui_cf_a.setText(curve_data.get("cf_a", ".000000000"))
        self.ui_cf_b.setText(curve_data.get("cf_b", ".000000000"))
        self.ui_cf_c.setText(curve_data.get("cf_c", "1.00000000"))
        self.ui_cf_d.setText(curve_data.get("cf_d", ".000000000"))

        matrix = ele_data.get("matrix", get_default_matrix_data())
        idx = 0
        for table in (self.table_left, self.table_right):
            for r in range(8):
                if idx < len(matrix):
                    dl, el, cf = matrix[idx]
                    table.cellWidget(r, 0).setCurrentText(dl)
                    table.item(r, 1).setText(el)
                    table.item(r, 2).setText(cf)
                idx += 1

    def _on_next_ele(self):
        curr_row = self.ele_list.currentRow()
        if curr_row < self.ele_list.count() - 1:
            self.ele_list.setCurrentRow(curr_row + 1)

    def _on_prev_ele(self):
        curr_row = self.ele_list.currentRow()
        if curr_row > 0:
            self.ele_list.setCurrentRow(curr_row - 1)

    def _on_next_wc(self):
        curr_idx = self.ui_no.currentIndex()
        if curr_idx < self.ui_no.count() - 1:
            self._save_ui_to_element(self.current_ele, self.ui_no.currentText())
            self.ui_no.setCurrentIndex(curr_idx + 1)
            self._load_element_to_ui(self.current_ele, self.ui_no.currentText())

    def _on_prev_wc(self):
        curr_idx = self.ui_no.currentIndex()
        if curr_idx > 0:
            self._save_ui_to_element(self.current_ele, self.ui_no.currentText())
            self.ui_no.setCurrentIndex(curr_idx - 1)
            self._load_element_to_ui(self.current_ele, self.ui_no.currentText())

    def _on_pick_element(self):
        # Determine which table currently has focus/selection
        active_table = None
        if self.table_left.hasFocus() or self.table_left.selectedItems():
            active_table = self.table_left
        elif self.table_right.hasFocus() or self.table_right.selectedItems():
            active_table = self.table_right
            
        if not active_table or active_table.currentColumn() != 1:
            QMessageBox.warning(self, "Selection Required", "Please select an 'Ele.Name' cell in the Matrix tables first.")
            return

        dialog = ContextPickerDialog("Select Element", MASTER_ELEMENTS, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            active_table.item(active_table.currentRow(), 1).setText(dialog.selected_value)

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        if self.current_ele:
            self._save_ui_to_element(self.current_ele, self.ui_no.currentText())
        return self.data_store

    def _apply(self, data: dict):
        if not data:
            self.data_store = {
                ele: {"curves": {"1": get_default_curve_data()}, "matrix": get_default_matrix_data()} 
                for ele in ELEMENTS_LIST
            }
        else:
            self.data_store = data
            
        self.ele_list.setCurrentRow(0)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_07_working_curve = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_07_working_curve:
                self._apply(g.page_07_working_curve)
            else:
                self._apply({}) 
        finally:
            session.close()

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Saved successfully.")

    def _on_next(self):
        self._save()
        try:
            from ui.anainf.page_08_correction import CorrectionPage
            self.main_window.set_right_widget(
                CorrectionPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 08 (Correction) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_06_recalibration import RecalibrationPage
            self.main_window.set_right_widget(
                RecalibrationPage(self.main_window, self.group_id, self.group_name))
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