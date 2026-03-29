from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QStackedWidget, QLineEdit, QSpinBox, QComboBox,
    QCheckBox, QRadioButton, QGroupBox, QGridLayout, QButtonGroup
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")
GROUP_BOX_STYLE = ("QGroupBox{font:bold 9pt Arial;color:black;border:1px solid #999;"
                   "margin-top:8px;padding-top:4px;background:#d4d0c8;}"
                   "QGroupBox::title{subcontrol-origin:margin;left:8px;color:black;}")


class AnalyticalModePage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        
        # Store references to dynamically created UI elements for easy data collection
        self.ui_refs = {
            "common_ref": None,
            "cont": {},
            "int": {},
            "recal": {}
        }
        
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
        bar = QLabel(f"Analytical Mode - {self.group_name}")
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

        # --- TOP COMMON SECTION ---
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Reference:"))
        self.ui_refs["common_ref"] = QLineEdit()
        self.ui_refs["common_ref"].setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: 9pt Arial;")
        top_layout.addWidget(self.ui_refs["common_ref"])
        
        btn_refer = QPushButton("8:Refer.")
        btn_refer.setStyleSheet(BTN)
        top_layout.addWidget(btn_refer)
        ml.addLayout(top_layout)

        # --- TAB SWITCHER BUTTONS ---
        tab_btn_layout = QHBoxLayout()
        btn_cont = QPushButton("S2:Cont.")
        btn_int = QPushButton("S3:Int.")
        btn_recal = QPushButton("S4:Recal.")
        
        for b in (btn_cont, btn_int, btn_recal):
            b.setStyleSheet(BTN)
            tab_btn_layout.addWidget(b)
        tab_btn_layout.addStretch()
        ml.addLayout(tab_btn_layout)

        # --- STACKED WIDGET (TABS) ---
        self.stack = QStackedWidget()
        
        # Connect buttons to stack index
        btn_cont.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_int.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_recal.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # Build individual tabs
        self.tab_cont = self._create_tab("cont", is_cont=True)
        self.tab_int = self._create_tab("int", is_int=True)
        self.tab_recal = self._create_tab("recal", is_recal=True)
        
        self.stack.addWidget(self.tab_cont)
        self.stack.addWidget(self.tab_int)
        self.stack.addWidget(self.tab_recal)
        
        ml.addWidget(self.stack, stretch=1)

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

    def _create_tab(self, tab_key, is_cont=False, is_int=False, is_recal=False):
        """Generates the layout for a specific tab, tracking inputs in self.ui_refs."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        refs = self.ui_refs[tab_key]

        # 1. Number of Analysis
        num_lay = QHBoxLayout()
        num_lay.addWidget(QLabel("Number of Analysis:"))
        spin_num = QSpinBox()
        spin_num.setRange(1, 99)
        spin_num.setStyleSheet("background: white; color: black;")
        num_lay.addWidget(spin_num)
        num_lay.addStretch()
        layout.addLayout(num_lay)
        refs["num_analysis"] = spin_num

        # 2. Display Layout
        grp_disp_lay = QGroupBox("Display Layout")
        grp_disp_lay.setStyleSheet(GROUP_BOX_STYLE)
        gl_disp = QGridLayout(grp_disp_lay)
        
        gl_disp.addWidget(QLabel("Row of Ele:"), 0, 0)
        le_row = QLineEdit("1")
        le_row.setValidator(QIntValidator(1, 99))
        le_row.setStyleSheet("background:white; color:black; width:40px;")
        gl_disp.addWidget(le_row, 0, 1)
        refs["row_ele"] = le_row
        
        gl_disp.addWidget(QLabel("Col. of Each Result:"), 0, 2)
        le_col = QLineEdit("1")
        le_col.setValidator(QIntValidator(1, 99))
        le_col.setStyleSheet("background:white; color:black; width:40px;")
        gl_disp.addWidget(le_col, 0, 3)
        refs["col_res"] = le_col
        
        gl_disp.addWidget(QLabel("Magn.:"), 0, 4)
        cb_magn = QComboBox()
        cb_magn.addItems(["75", "100", "125", "150", "200"])
        cb_magn.setCurrentText("100")
        cb_magn.setStyleSheet("background:white; color:black;")
        gl_disp.addWidget(cb_magn, 0, 5)
        refs["magn"] = cb_magn
        layout.addWidget(grp_disp_lay)

        # 3. Display Items & Print Items
        h_items = QHBoxLayout()
        
        grp_disp_item = QGroupBox("Display item")
        grp_disp_item.setStyleSheet(GROUP_BOX_STYLE)
        vl_di = QVBoxLayout(grp_disp_item)
        chk_dr = QCheckBox("R value"); chk_dsd = QCheckBox("S.D."); chk_dcv = QCheckBox("C.V.")
        for c in (chk_dr, chk_dsd, chk_dcv): vl_di.addWidget(c)
        refs["disp_r"] = chk_dr; refs["disp_sd"] = chk_dsd; refs["disp_cv"] = chk_dcv
        h_items.addWidget(grp_disp_item)
        
        grp_print_item = QGroupBox("Print item")
        grp_print_item.setStyleSheet(GROUP_BOX_STYLE)
        vl_pi = QVBoxLayout(grp_print_item)
        chk_pe = QCheckBox("Each Result"); chk_pr = QCheckBox("R value")
        chk_psd = QCheckBox("S.D."); chk_pcv = QCheckBox("C.V.")
        for c in (chk_pe, chk_pr, chk_psd, chk_pcv): vl_pi.addWidget(c)
        refs["print_each"] = chk_pe; refs["print_r"] = chk_pr
        refs["print_sd"] = chk_psd; refs["print_cv"] = chk_pcv
        h_items.addWidget(grp_print_item)

        # 4. Print Mode
        grp_print_mode = QGroupBox("Print mode")
        grp_print_mode.setStyleSheet(GROUP_BOX_STYLE)
        vl_pm = QVBoxLayout(grp_print_mode)
        rb_auto = QRadioButton("Auto")
        rb_manu = QRadioButton("Manu")
        rb_auto.setChecked(True)
        vl_pm.addWidget(rb_auto)
        vl_pm.addWidget(rb_manu)
        # Group them so they are exclusive
        bg_pm = QButtonGroup(widget)
        bg_pm.addButton(rb_auto); bg_pm.addButton(rb_manu)
        refs["print_mode_auto"] = rb_auto
        h_items.addWidget(grp_print_mode)
        
        layout.addLayout(h_items)

        # --- EXTRA SECTIONS ---
        if is_cont:
            grp_am = QGroupBox("Analysis method")
            grp_am.setStyleSheet(GROUP_BOX_STYLE)
            hl_am = QHBoxLayout(grp_am)
            rb_norm = QRadioButton("Normal")
            rb_4t = QRadioButton("4-times analysis")
            rb_4t.setChecked(True) # Default from TOML
            bg_am = QButtonGroup(widget)
            bg_am.addButton(rb_norm); bg_am.addButton(rb_4t)
            hl_am.addWidget(rb_norm); hl_am.addWidget(rb_4t)
            layout.addWidget(grp_am)
            refs["meth_norm"] = rb_norm
            
            grp_si = QGroupBox("SampleIndex")
            grp_si.setStyleSheet(GROUP_BOX_STYLE)
            vl_si = QVBoxLayout(grp_si)
            le_si1 = QLineEdit(); le_si2 = QLineEdit()
            for le in (le_si1, le_si2):
                le.setStyleSheet("background:white; color:black;")
                vl_si.addWidget(le)
            layout.addWidget(grp_si)
            refs["si_1"] = le_si1; refs["si_2"] = le_si2
            
            # Extra Buttons for Cont.
            hl_btns = QHBoxLayout()
            btn_det = QPushButton("7:Detail"); btn_file = QPushButton("5:FileMode"); btn_trans = QPushButton("6:Trans.Mode")
            for b in (btn_det, btn_file, btn_trans):
                b.setStyleSheet(BTN)
                hl_btns.addWidget(b)
            hl_btns.addStretch()
            layout.addLayout(hl_btns)

        if is_recal:
            grp_rm = QGroupBox("Recal. Method")
            grp_rm.setStyleSheet(GROUP_BOX_STYLE)
            hl_rm = QHBoxLayout(grp_rm)
            rb_1p = QRadioButton("1point Recal.")
            rb_2p = QRadioButton("2point Recal.")
            rb_2p.setChecked(True) # Default
            bg_rm = QButtonGroup(widget)
            bg_rm.addButton(rb_1p); bg_rm.addButton(rb_2p)
            hl_rm.addWidget(rb_1p); hl_rm.addWidget(rb_2p)
            layout.addWidget(grp_rm)
            refs["rm_1p"] = rb_1p

        return widget

    # ----------------------- Database Binding -----------------------

    def _collect(self) -> dict:
        data = {"common_ref": self.ui_refs["common_ref"].text().strip()}
        
        for tab in ["cont", "int", "recal"]:
            refs = self.ui_refs[tab]
            tab_data = {
                "num_analysis": refs["num_analysis"].value(),
                "row_ele": refs["row_ele"].text(),
                "col_res": refs["col_res"].text(),
                "magn": refs["magn"].currentText(),
                "disp_r": refs["disp_r"].isChecked(),
                "disp_sd": refs["disp_sd"].isChecked(),
                "disp_cv": refs["disp_cv"].isChecked(),
                "print_each": refs["print_each"].isChecked(),
                "print_r": refs["print_r"].isChecked(),
                "print_sd": refs["print_sd"].isChecked(),
                "print_cv": refs["print_cv"].isChecked(),
                "print_mode": "Auto" if refs["print_mode_auto"].isChecked() else "Manu"
            }
            
            if tab == "cont":
                tab_data["analysis_method"] = "Normal" if refs["meth_norm"].isChecked() else "4-times"
                tab_data["si_1"] = refs["si_1"].text()
                tab_data["si_2"] = refs["si_2"].text()
                
            if tab == "recal":
                tab_data["recal_method"] = "1point" if refs["rm_1p"].isChecked() else "2point"
                
            data[tab] = tab_data
            
        return data

    def _apply(self, data: dict):
        if not data:
            data = {} # Will leave defaults we set during UI build
            
        self.ui_refs["common_ref"].setText(data.get("common_ref", ""))
        
        for tab in ["cont", "int", "recal"]:
            tab_data = data.get(tab, {})
            refs = self.ui_refs[tab]
            
            refs["num_analysis"].setValue(tab_data.get("num_analysis", 1))
            refs["row_ele"].setText(tab_data.get("row_ele", "1"))
            refs["col_res"].setText(tab_data.get("col_res", "1"))
            refs["magn"].setCurrentText(tab_data.get("magn", "100"))
            
            refs["disp_r"].setChecked(tab_data.get("disp_r", False))
            refs["disp_sd"].setChecked(tab_data.get("disp_sd", False))
            refs["disp_cv"].setChecked(tab_data.get("disp_cv", False))
            
            refs["print_each"].setChecked(tab_data.get("print_each", False))
            refs["print_r"].setChecked(tab_data.get("print_r", False))
            refs["print_sd"].setChecked(tab_data.get("print_sd", False))
            refs["print_cv"].setChecked(tab_data.get("print_cv", False))
            
            if tab_data.get("print_mode", "Auto") == "Auto":
                refs["print_mode_auto"].setChecked(True)
            else:
                # We didn't save manu ref directly, but auto grouped will toggle it
                refs["print_mode_auto"].setChecked(False) # This unchecks Auto and checks Manu
                
            if tab == "cont":
                is_norm = tab_data.get("analysis_method", "4-times") == "Normal"
                refs["meth_norm"].setChecked(is_norm)
                refs["si_1"].setText(tab_data.get("si_1", ""))
                refs["si_2"].setText(tab_data.get("si_2", ""))
                
            if tab == "recal":
                is_1p = tab_data.get("recal_method", "2point") == "1point"
                refs["rm_1p"].setChecked(is_1p)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_12_analytical_mode = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_12_analytical_mode:
                self._apply(g.page_12_analytical_mode)
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
            from ui.anainf.page_13_control_chart import ControlChartPage
            self.main_window.set_right_widget(
                ControlChartPage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 13 (Control Chart) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_11_master_curve import MasterCurvePage
            self.main_window.set_right_widget(
                MasterCurvePage(self.main_window, self.group_id, self.group_name))
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