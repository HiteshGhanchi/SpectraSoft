from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QStyledItemDelegate, QLineEdit, QGroupBox,
    QRadioButton, QButtonGroup, QSpinBox
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

# The 22 standard LAS 2023 elements
ELEMENTS = [
    "FE", "C", "SI", "MN", "P", "S", "CR", "NI", "MO", "CU", "V",
    "TI", "W", "B", "NB", "CA", "CO", "SN", "N", "PB", "AL", "CE"
]

def get_default_table_data():
    """Returns the default limits for all 22 elements."""
    data = {}
    for ele in ELEMENTS:
        data[ele] = {
            "target": ".00000",
            "ctrl_l": ".00000",
            "ctrl_h": "100.00",
            "scale_l": ".00000",
            "scale_h": "100.00"
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

class ControlChartPage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        
        # References for setting collection
        self.ui_refs = {}
        
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
        bar = QLabel(f"Control Chart Information - {self.group_name}")
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

        # --- TOP SETTINGS SECTION ---
        settings_layout = QHBoxLayout()
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 1. Control Line (Checkable GroupBox)
        gb_cl = QGroupBox("Control Line")
        gb_cl.setStyleSheet(GROUP_BOX_STYLE)
        gb_cl.setCheckable(True)
        gb_cl.setChecked(False)
        vl_cl = QVBoxLayout(gb_cl)
        rb_cl_std = QRadioButton("Standard Range")
        rb_cl_ctrl = QRadioButton("Control Range")
        rb_cl_std.setChecked(True)
        bg_cl = QButtonGroup(self)
        bg_cl.addButton(rb_cl_std); bg_cl.addButton(rb_cl_ctrl)
        vl_cl.addWidget(rb_cl_std); vl_cl.addWidget(rb_cl_ctrl)
        settings_layout.addWidget(gb_cl)
        self.ui_refs["cl_box"] = gb_cl
        self.ui_refs["cl_std"] = rb_cl_std

        # 2. Sigma Line (Checkable GroupBox)
        gb_sig = QGroupBox("Sigma Line")
        gb_sig.setStyleSheet(GROUP_BOX_STYLE)
        gb_sig.setCheckable(True)
        gb_sig.setChecked(True)
        vl_sig = QVBoxLayout(gb_sig)
        rb_s1 = QRadioButton("±1.0STD")
        rb_s15 = QRadioButton("±1.5STD")
        rb_s2 = QRadioButton("±2.0STD")
        rb_s3 = QRadioButton("±3.0STD")
        rb_s2.setChecked(True)
        bg_sig = QButtonGroup(self)
        for rb in (rb_s1, rb_s15, rb_s2, rb_s3):
            bg_sig.addButton(rb)
            vl_sig.addWidget(rb)
        settings_layout.addWidget(gb_sig)
        self.ui_refs["sig_box"] = gb_sig
        self.ui_refs["sig_btns"] = [rb_s1, rb_s15, rb_s2, rb_s3]

        # 3. Center Line
        gb_cen = QGroupBox("Center line")
        gb_cen.setStyleSheet(GROUP_BOX_STYLE)
        vl_cen = QVBoxLayout(gb_cen)
        rb_c_avg = QRadioButton("Average")
        rb_c_med = QRadioButton("Median")
        rb_c_tgt = QRadioButton("Target")
        rb_c_avg.setChecked(True)
        bg_cen = QButtonGroup(self)
        for rb in (rb_c_avg, rb_c_med, rb_c_tgt):
            bg_cen.addButton(rb)
            vl_cen.addWidget(rb)
        settings_layout.addWidget(gb_cen)
        self.ui_refs["cen_btns"] = [rb_c_avg, rb_c_med, rb_c_tgt]

        # 4. Other Settings (Class Mark & Display Scale)
        vl_other = QVBoxLayout()
        
        # Class Mark
        hl_cm = QHBoxLayout()
        hl_cm.addWidget(QLabel("Class Mark:"))
        spin_cm = QSpinBox()
        spin_cm.setRange(1, 999)
        spin_cm.setValue(1)
        spin_cm.setStyleSheet("background: white; color: black;")
        hl_cm.addWidget(spin_cm)
        vl_other.addLayout(hl_cm)
        self.ui_refs["class_mark"] = spin_cm
        
        # Display Scale
        gb_ds = QGroupBox("Display Scale")
        gb_ds.setStyleSheet(GROUP_BOX_STYLE)
        hl_ds = QHBoxLayout(gb_ds)
        rb_ds_auto = QRadioButton("Auto")
        rb_ds_fixed = QRadioButton("Fixed")
        rb_ds_auto.setChecked(True)
        bg_ds = QButtonGroup(self)
        bg_ds.addButton(rb_ds_auto); bg_ds.addButton(rb_ds_fixed)
        hl_ds.addWidget(rb_ds_auto); hl_ds.addWidget(rb_ds_fixed)
        vl_other.addWidget(gb_ds)
        self.ui_refs["ds_auto"] = rb_ds_auto

        settings_layout.addLayout(vl_other)
        settings_layout.addStretch()
        ml.addLayout(settings_layout)

        # --- TABLE SETUP ---
        self.table = QTableWidget(len(ELEMENTS), 6)
        self.table.setHorizontalHeaderLabels([
            "Ele.Name", "Target", "Control Range L", "Control Range H", 
            "Scale Range L", "Scale Range H"
        ])
        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setStyleSheet("""
            QTableWidget { background: white; color: black; border: 1px solid #aaa; font: 9pt Arial; gridline-color: #aaa; }
            QHeaderView::section { background: #d4d0c8; color: black; border: 1px solid #aaa; font: 9pt Arial; padding: 2px; }
        """)
        
        float_delegate = FloatDelegate(self.table)
        for col in range(1, 6):
            self.table.setItemDelegateForColumn(col, float_delegate)
        
        # Initialize Rows
        for i, ele in enumerate(ELEMENTS):
            item_ele = QTableWidgetItem(ele)
            item_ele.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            item_ele.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_ele.setBackground(QColor("#f0f0f0"))
            self.table.setItem(i, 0, item_ele)
            
            for col in range(1, 6):
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
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        data = {"settings": {}, "table": {}}
        
        # 1. Collect Settings
        data["settings"]["cl_enabled"] = self.ui_refs["cl_box"].isChecked()
        data["settings"]["cl_type"] = "Standard" if self.ui_refs["cl_std"].isChecked() else "Control"
        
        data["settings"]["sig_enabled"] = self.ui_refs["sig_box"].isChecked()
        sig_vals = ["1.0", "1.5", "2.0", "3.0"]
        data["settings"]["sig_val"] = "2.0" # Default fallback
        for i, rb in enumerate(self.ui_refs["sig_btns"]):
            if rb.isChecked(): data["settings"]["sig_val"] = sig_vals[i]
            
        cen_vals = ["Average", "Median", "Target"]
        data["settings"]["cen_val"] = "Average"
        for i, rb in enumerate(self.ui_refs["cen_btns"]):
            if rb.isChecked(): data["settings"]["cen_val"] = cen_vals[i]
            
        data["settings"]["class_mark"] = self.ui_refs["class_mark"].value()
        data["settings"]["disp_scale"] = "Auto" if self.ui_refs["ds_auto"].isChecked() else "Fixed"

        # 2. Collect Table
        for i, ele in enumerate(ELEMENTS):
            data["table"][ele] = {
                "target": self.table.item(i, 1).text().strip() if self.table.item(i, 1) else "",
                "ctrl_l": self.table.item(i, 2).text().strip() if self.table.item(i, 2) else "",
                "ctrl_h": self.table.item(i, 3).text().strip() if self.table.item(i, 3) else "",
                "scale_l": self.table.item(i, 4).text().strip() if self.table.item(i, 4) else "",
                "scale_h": self.table.item(i, 5).text().strip() if self.table.item(i, 5) else ""
            }
        return data

    def _apply(self, data: dict):
        settings = data.get("settings", {})
        table_data = data.get("table", get_default_table_data())
        
        # 1. Apply Settings
        self.ui_refs["cl_box"].setChecked(settings.get("cl_enabled", False))
        if settings.get("cl_type", "Standard") == "Standard":
            self.ui_refs["cl_std"].setChecked(True)
        else:
            self.ui_refs["cl_box"].findChildren(QRadioButton)[1].setChecked(True)
            
        self.ui_refs["sig_box"].setChecked(settings.get("sig_enabled", True))
        sig_map = {"1.0": 0, "1.5": 1, "2.0": 2, "3.0": 3}
        sig_idx = sig_map.get(settings.get("sig_val", "2.0"), 2)
        self.ui_refs["sig_btns"][sig_idx].setChecked(True)
        
        cen_map = {"Average": 0, "Median": 1, "Target": 2}
        cen_idx = cen_map.get(settings.get("cen_val", "Average"), 0)
        self.ui_refs["cen_btns"][cen_idx].setChecked(True)
        
        self.ui_refs["class_mark"].setValue(settings.get("class_mark", 1))
        
        if settings.get("disp_scale", "Auto") == "Auto":
            self.ui_refs["ds_auto"].setChecked(True)
        else:
            self.ui_refs["ds_auto"].parent().findChildren(QRadioButton)[1].setChecked(True)

        # 2. Apply Table
        for i, ele in enumerate(ELEMENTS):
            row = table_data.get(ele, get_default_table_data()[ele])
            
            if self.table.item(i, 1): self.table.item(i, 1).setText(row.get("target", ".00000"))
            if self.table.item(i, 2): self.table.item(i, 2).setText(row.get("ctrl_l", ".00000"))
            if self.table.item(i, 3): self.table.item(i, 3).setText(row.get("ctrl_h", "100.00"))
            if self.table.item(i, 4): self.table.item(i, 4).setText(row.get("scale_l", ".00000"))
            if self.table.item(i, 5): self.table.item(i, 5).setText(row.get("scale_h", "100.00"))

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_13_control_chart = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_13_control_chart:
                self._apply(g.page_13_control_chart)
            else:
                self._apply({}) # Triggers defaults
        finally:
            session.close()

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Saved successfully.")

    def _on_next(self):
        self._save()
        
        # Prompt user about wrap-around since this is the last page
        QMessageBox.information(self, "End of Editor", "This is the final page. Wrapping back to Analytical Condition.")
        
        try:
            # Safely attempt to import the first page regardless of the exact class name used
            try:
                from ui.anainf.page_01_condition import ConditionPage as FirstPage
            except ImportError:
                from ui.anainf.page_01_condition import Page01Condition as FirstPage
                
            self.main_window.set_right_widget(
                FirstPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            pass

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_12_analytical_mode import AnalyticalModePage
            self.main_window.set_right_widget(
                AnalyticalModePage(self.main_window, self.group_id, self.group_name))
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