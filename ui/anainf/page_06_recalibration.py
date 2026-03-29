from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox,
    QListWidget, QListWidgetItem, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QDoubleValidator

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"
BTN = ("QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
       "font:9pt Arial;padding:3px 8px;min-width:65px;}"
       "QPushButton:pressed{border:2px inset #888;}")

# The 22 standard LAS 2023 elements, appended with '1' as specified
ELEMENTS_LIST = [
    "FE1", "C1", "SI1", "MN1", "P1", "S1", "CR1", "NI1", "MO1", "CU1", 
    "V1", "TI1", "W1", "B1", "NB1", "CA1", "CO1", "SN1", "N1", "PB1", 
    "AL1", "CE1"
]

def get_default_ele_data():
    """Returns the default dictionary structure for a single element's recalibration data."""
    return {
        "sn_h": "", "sn_l": "", "sn_k": "",
        "tg_h": ".00000", "tg_l": ".00000", "tg_k": ".00000",
        "rg_h": ".00000", "rg_l": ".00000", "rg_k": ".00000",
        "cf_a": "1.0000", "cf_b": ".00000", "cf_k": "1.0000"
    }

class RecalibrationPage(QWidget):
    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id    = group_id
        self.group_name  = group_name
        
        # Internal data store: maps "FE1" -> dict of values
        self.data_store = {ele: get_default_ele_data() for ele in ELEMENTS_LIST}
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
        bar = QLabel(f"Recalibration Information - {self.group_name}")
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
        ml.setSpacing(15)

        # --- LEFT PANEL: Element List ---
        self.ele_list = QListWidget()
        self.ele_list.setFixedWidth(120)
        self.ele_list.setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: 9pt Arial;")
        self.ele_list.addItems(ELEMENTS_LIST)
        self.ele_list.currentItemChanged.connect(self._on_list_changed)
        ml.addWidget(self.ele_list)

        # --- RIGHT PANEL: Data Entry ---
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Grid Layout for inputs
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Headers
        headers = ["", "High / Alpha", "Low / Beta", "K"]
        for col, text in enumerate(headers):
            lbl = QLabel(text)
            lbl.setStyleSheet("color: black; font: bold 9pt Arial;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(lbl, 0, col)
            
        # Row 1: Sample Name
        grid.addWidget(self._make_label("Sample Name"), 1, 0)
        self.ui_sn_h = self._make_line_edit()
        self.ui_sn_l = self._make_line_edit()
        self.ui_sn_k = self._make_line_edit()
        grid.addWidget(self.ui_sn_h, 1, 1)
        grid.addWidget(self.ui_sn_l, 1, 2)
        grid.addWidget(self.ui_sn_k, 1, 3)

        # Row 2: Target
        grid.addWidget(self._make_label("Target"), 2, 0)
        self.ui_tg_h = self._make_line_edit(is_float=True)
        self.ui_tg_l = self._make_line_edit(is_float=True)
        self.ui_tg_k = self._make_line_edit(is_float=True)
        grid.addWidget(self.ui_tg_h, 2, 1)
        grid.addWidget(self.ui_tg_l, 2, 2)
        grid.addWidget(self.ui_tg_k, 2, 3)

        # Row 3: Range
        grid.addWidget(self._make_label("Range"), 3, 0)
        self.ui_rg_h = self._make_line_edit(is_float=True)
        self.ui_rg_l = self._make_line_edit(is_float=True)
        self.ui_rg_k = self._make_line_edit(is_float=True)
        grid.addWidget(self.ui_rg_h, 3, 1)
        grid.addWidget(self.ui_rg_l, 3, 2)
        grid.addWidget(self.ui_rg_k, 3, 3)

        # Row 4: Coefficient
        grid.addWidget(self._make_label("Coefficient"), 4, 0)
        self.ui_cf_a = self._make_line_edit(is_float=True)
        self.ui_cf_b = self._make_line_edit(is_float=True)
        self.ui_cf_k = self._make_line_edit(is_float=True)
        grid.addWidget(self.ui_cf_a, 4, 1)
        grid.addWidget(self.ui_cf_b, 4, 2)
        grid.addWidget(self.ui_cf_k, 4, 3)

        right_panel.addLayout(grid)
        
        # Sub-panel Buttons (S2, S3, S5)
        sub_btn_layout = QHBoxLayout()
        sub_btn_layout.setContentsMargins(0, 20, 0, 0)
        
        btn_next_ele = QPushButton("S2:N.Ele")
        btn_next_ele.setStyleSheet(BTN)
        btn_next_ele.clicked.connect(self._on_next_ele)
        
        btn_prev_ele = QPushButton("S3:P.Ele")
        btn_prev_ele.setStyleSheet(BTN)
        btn_prev_ele.clicked.connect(self._on_prev_ele)
        
        btn_init = QPushButton("S5:Init.")
        btn_init.setStyleSheet(BTN)
        btn_init.clicked.connect(self._on_init)
        
        sub_btn_layout.addWidget(btn_prev_ele)
        sub_btn_layout.addWidget(btn_next_ele)
        sub_btn_layout.addStretch()
        sub_btn_layout.addWidget(btn_init)
        
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
        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(BTN)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)
        root.addWidget(btn_bar)

    def _make_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: black; font: 9pt Arial;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return lbl

    def _make_line_edit(self, is_float=False):
        le = QLineEdit()
        le.setStyleSheet("background: white; color: black; border: 1px solid #aaa; font: 9pt Arial;")
        le.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_float:
            # Allows decimals, e.g. .00000
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            le.setValidator(validator)
        return le

    def _on_list_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        if previous:
            # Save the UI fields into our data dictionary for the outgoing element
            self._save_ui_to_element(previous.text())
            
        if current:
            # Load the dictionary data into the UI fields for the incoming element
            self.current_ele = current.text()
            self._load_element_to_ui(self.current_ele)

    def _save_ui_to_element(self, ele_name):
        """Scrape UI line edits and save into memory."""
        if ele_name not in self.data_store:
            return
            
        self.data_store[ele_name] = {
            "sn_h": self.ui_sn_h.text(), "sn_l": self.ui_sn_l.text(), "sn_k": self.ui_sn_k.text(),
            "tg_h": self.ui_tg_h.text(), "tg_l": self.ui_tg_l.text(), "tg_k": self.ui_tg_k.text(),
            "rg_h": self.ui_rg_h.text(), "rg_l": self.ui_rg_l.text(), "rg_k": self.ui_rg_k.text(),
            "cf_a": self.ui_cf_a.text(), "cf_b": self.ui_cf_b.text(), "cf_k": self.ui_cf_k.text()
        }

    def _load_element_to_ui(self, ele_name):
        """Push memory data into UI line edits."""
        d = self.data_store.get(ele_name, get_default_ele_data())
        
        self.ui_sn_h.setText(d.get("sn_h", ""))
        self.ui_sn_l.setText(d.get("sn_l", ""))
        self.ui_sn_k.setText(d.get("sn_k", ""))
        
        self.ui_tg_h.setText(d.get("tg_h", ".00000"))
        self.ui_tg_l.setText(d.get("tg_l", ".00000"))
        self.ui_tg_k.setText(d.get("tg_k", ".00000"))
        
        self.ui_rg_h.setText(d.get("rg_h", ".00000"))
        self.ui_rg_l.setText(d.get("rg_l", ".00000"))
        self.ui_rg_k.setText(d.get("rg_k", ".00000"))
        
        self.ui_cf_a.setText(d.get("cf_a", "1.0000"))
        self.ui_cf_b.setText(d.get("cf_b", ".00000"))
        self.ui_cf_k.setText(d.get("cf_k", "1.0000"))

    def _on_next_ele(self):
        curr_row = self.ele_list.currentRow()
        if curr_row < self.ele_list.count() - 1:
            self.ele_list.setCurrentRow(curr_row + 1)

    def _on_prev_ele(self):
        curr_row = self.ele_list.currentRow()
        if curr_row > 0:
            self.ele_list.setCurrentRow(curr_row - 1)

    def _on_init(self):
        if not self.current_ele: return
        
        reply = QMessageBox.question(
            self, "Confirm", "Initialize Coefficient. OK?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.ui_cf_a.setText("1.0000")
            self.ui_cf_b.setText(".00000")
            self.ui_cf_k.setText("1.0000")
            # Save it immediately
            self._save_ui_to_element(self.current_ele)

    def _collect(self) -> dict:
        # Ensure the currently visible fields are saved to the dictionary before collecting
        if self.current_ele:
            self._save_ui_to_element(self.current_ele)
        return self.data_store

    def _apply(self, data: dict):
        if not data:
            self.data_store = {ele: get_default_ele_data() for ele in ELEMENTS_LIST}
        else:
            # Merge loaded data, keeping default structure for missing elements safely
            for ele in ELEMENTS_LIST:
                if ele in data:
                    self.data_store[ele] = data[ele]
                else:
                    self.data_store[ele] = get_default_ele_data()
        
        # Select the first element by default
        self.ele_list.setCurrentRow(0)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_06_recalibration = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_06_recalibration:
                self._apply(g.page_06_recalibration)
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
            from ui.anainf.page_07_working_curve import WorkingCurvePage
            self.main_window.set_right_widget(
                WorkingCurvePage(self.main_window, self.group_id, self.group_name))
        except ImportError:
            QMessageBox.information(self, "Next Page", "Page 07 (Working Curve) is not built yet.")

    def _on_pre(self):
        self._save()
        try:
            from ui.anainf.page_05_measurement import MeasurementPage
            self.main_window.set_right_widget(
                MeasurementPage(self.main_window, self.group_id, self.group_name))
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