"""
SpectraSoft — Page 1: Analytical Condition
Loads in the RIGHT panel. Group list stays visible on left.
Follows tkinter reference layout.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QGroupBox, QFrame, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.database import get_session
from core.models import AnalyticalGroup

BG = "#d4d0c8"

BTN = (
    "QPushButton{background:#d4d0c8;color:black;"
    "border:2px outset #ffffff;font:9pt Arial;"
    "padding:3px 8px;min-width:65px;}"
    "QPushButton:pressed{border:2px inset #888;}"
)
GRP = (
    "QGroupBox{font:9pt Arial;color:black;"
    "border:1px solid #999;margin-top:8px;"
    "padding-top:4px;background:#d4d0c8;}"
    "QGroupBox::title{subcontrol-origin:margin;left:8px;color:black;}"
)
ENTRY = "QLineEdit{background:white;color:black;border:1px solid #aaa;font:9pt Arial;}"
CMB   = "QComboBox{background:white;color:black;border:1px solid #aaa;font:9pt Arial;}" \
        "QComboBox QAbstractItemView{background:white;color:black;}"

SOURCE_OPTS = [
    "3 Peak Spark","Normal Spark","Combined Spark",
    "Arclike Spark","Cleaning","High Voltage Spark",
    "AD OFFSET","ITG OFFSET","SH OFFSET","NOISE TEST","Lamp",
]

# Monitor dropdown options: "ELEMENT  WAVELENGTH" pairs (matches old software exactly)
# Elements with 2 channels appear twice with different wavelengths
MONITOR_OPTIONS = [
    "None",
    "FE   273.0", "C    193.0", "SI   212.4", "MN   293.3",
    "P    178.3", "S    180.7", "V    311.0",
    "CR   267.7", "CR   298.9",
    "MO   202.0", "MO   277.5",
    "NI   231.6", "NI   227.7",
    "AL   394.4", "CU   224.2", "TI   337.2",
    "W    220.4", "B    182.6", "NB   319.5",
    "CA   396.8", "CO   258.0", "SN   189.9",
    "N    174.5*2", "PB   405.7", "RH   421.8",
]

def _parse_monitor(option: str):
    """Split 'FE   273.0' into ('FE', '273.0')."""
    parts = option.strip().split()
    if len(parts) >= 2:
        return parts[0], parts[1]
    return option, ""

# Keep backward compat map for auto-fill (first wavelength per element)
MONITOR_MAP = {
    "None":"","FE":"273.0","C":"193.0","SI":"212.4",
    "MN":"293.3","P":"178.3","S":"180.7","V":"311.0",
    "CR":"267.7","MO":"202.0","NI":"231.6","AL":"394.4",
    "CU":"224.2","TI":"337.2","W":"220.4","B":"182.6",
    "NB":"319.5","CA":"396.8","CO":"258.0","SN":"189.9",
    "N":"174.5*2","PB":"405.7","RH":"421.8",
}


def lbl(text, w=None):
    l = QLabel(text)
    l.setFont(QFont("Arial", 9))
    l.setStyleSheet("color:black;background:transparent;")
    if w:
        l.setFixedWidth(w)
    return l


def entry(default="", w=70):
    e = QLineEdit(str(default))
    e.setFixedWidth(w)
    e.setStyleSheet(ENTRY)
    return e


def combo(opts, default=None, w=145):
    c = QComboBox()
    c.addItems(opts)
    c.setFixedWidth(w)
    c.setStyleSheet(CMB)
    if default and default in opts:
        c.setCurrentText(default)
    return c


class AnalyticalConditionPage(QWidget):

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

        # ── Blue title bar ────────────────────────────────────────────
        bar = QLabel(f"Analytical Condition - {self.group_name}")
        bar.setFixedHeight(22)
        bar.setContentsMargins(8, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(
            "background:#5c9bd5;color:white;font:bold 10pt Arial;"
        )
        root.addWidget(bar)

        # ── White sunken content frame ────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)
        ol.setSpacing(0)

        # Scrollable inner grey area
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
        ml.setContentsMargins(10, 10, 10, 4)
        ml.setSpacing(6)

        # ── Analytical Method ─────────────────────────────────────────
        grp_m = QGroupBox("Analytical Method")
        grp_m.setStyleSheet(GRP)
        gml = QHBoxLayout(grp_m)
        gml.setContentsMargins(8, 6, 8, 6)
        self._method = combo(
            ["P:PDA+Integ. Mode", "I:Integration Mode"],
            "P:PDA+Integ. Mode", w=200
        )
        gml.addWidget(self._method)
        gml.addStretch()
        ml.addWidget(grp_m)

        # ── SEQ ───────────────────────────────────────────────────────
        grp_s = QGroupBox("SEQ")
        grp_s.setStyleSheet(GRP)
        sg = QGridLayout(grp_s)
        sg.setContentsMargins(8, 6, 8, 6)
        sg.setHorizontalSpacing(4)
        sg.setVerticalSpacing(3)

        # Headers
        for ci, txt in enumerate(["", "SEQ1", "SEQ2", "SEQ3", "Clean", ""]):
            h = lbl(txt)
            h.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sg.addWidget(h, 0, ci)

        sg.addWidget(lbl("Sec."), 1, 5)

        # Purge
        sg.addWidget(lbl("Purge", 55), 1, 0)
        self._purge = entry("3", 55)
        sg.addWidget(self._purge, 1, 1)

        # Source
        sg.addWidget(lbl("Source", 55), 2, 0)
        self._src1 = combo(SOURCE_OPTS, "3 Peak Spark", 145)
        self._src2 = combo(SOURCE_OPTS, "Normal Spark",  145)
        self._src3 = combo(SOURCE_OPTS, "Lamp",          145)
        self._srcc = combo(SOURCE_OPTS, "Cleaning",      145)
        sg.addWidget(self._src1, 2, 1)
        sg.addWidget(self._src2, 2, 2)
        sg.addWidget(self._src3, 2, 3)
        sg.addWidget(self._srcc, 2, 4)

        # Preburn
        sg.addWidget(lbl("Preburn", 55), 3, 0)
        self._pb1 = entry("200", 55); sg.addWidget(self._pb1, 3, 1)
        self._pb2 = entry("200", 55); sg.addWidget(self._pb2, 3, 2)
        self._pb3 = entry("0",   55); sg.addWidget(self._pb3, 3, 3)
        sg.addWidget(lbl("Pulse"), 3, 4)

        # Integ
        sg.addWidget(lbl("Integ.", 55), 4, 0)
        self._ig1 = entry("300", 55); sg.addWidget(self._ig1, 4, 1)
        self._ig2 = entry("23",  55); sg.addWidget(self._ig2, 4, 2)
        self._ig3 = entry("0",   55); sg.addWidget(self._ig3, 4, 3)
        sg.addWidget(lbl("Pulse"), 4, 4)

        # Clean
        sg.addWidget(lbl("Clean", 55), 5, 0)
        self._clean = entry("0", 55)
        sg.addWidget(self._clean, 5, 4)
        sg.addWidget(lbl("Pulse"), 5, 5)

        ml.addWidget(grp_s)

        # ── Level Cut Information ─────────────────────────────────────
        grp_l = QGroupBox("Level Cut Information")
        grp_l.setStyleSheet(GRP)
        ll = QVBoxLayout(grp_l)
        ll.setContentsMargins(8, 6, 8, 6)
        ll.setSpacing(6)

        # Monitor Ele. — 3 pairs each with element dropdown + wavelength field
        # Layout: "Monitor Ele." label | [ele][val] | [ele][val] | [ele][val]
        mon_grid = QGridLayout()
        mon_grid.setSpacing(3)
        mon_grid.setColumnStretch(10, 1)

        mon_grid.addWidget(lbl("Monitor Ele.", 85), 0, 0)

        self._mon_ele = []

        col = 1
        # Defaults match LAS 2023: V 311.0, V 311.0, SI 212.4
        for opt_def in ["V    311.0", "V    311.0", "SI   212.4"]:
            ec = combo(MONITOR_OPTIONS, opt_def, 110)
            mon_grid.addWidget(ec, 0, col);     col += 1
            self._mon_ele.append(ec)

        ll.addLayout(mon_grid)

        # H/L Level table with visible cell borders
        # Columns: row-label | SEQ1 SEQ2 SEQ3 | SEQ1 SEQ2 SEQ3 | SEQ1 SEQ2 SEQ3
        CELL = (
            "QLineEdit{background:white;color:black;"
            "border:1px solid #aaa;font:9pt Arial;"
            "padding:1px;}"
        )
        HDR_CELL = (
            "QLabel{background:#d4d0c8;color:black;"
            "border:1px solid #aaa;font:8pt Arial;"
            "padding:1px 2px;}"
        )
        ROW_LBL = (
            "QLabel{background:#d4d0c8;color:black;"
            "border:1px solid #aaa;font:9pt Arial;"
            "padding:1px 4px;}"
        )

        tbl = QGridLayout()
        tbl.setSpacing(0)

        # Top-left empty cell
        tl = QLabel("")
        tl.setFixedSize(80, 22)
        tl.setStyleSheet(HDR_CELL)
        tbl.addWidget(tl, 0, 0)

        # Column headers — SEQ1 SEQ2 SEQ3 repeated 3 times
        for ci, txt in enumerate(["SEQ1","SEQ2","SEQ3"]*3):
            h = QLabel(txt)
            h.setFixedSize(58, 22)
            h.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h.setStyleSheet(HDR_CELL)
            tbl.addWidget(h, 0, ci+1)

        self._h, self._l = [], []
        h_defs = ["0","0","0","0","0","0","0","0","0"]
        l_defs = ["20","20","0","0","0","0","0","0","0"]

        for row_i, (row_lbl, defs, store) in enumerate([
            ("H.Level(%)", h_defs, self._h),
            ("L.Level(%)", l_defs, self._l),
        ], start=1):
            rl = QLabel(row_lbl)
            rl.setFixedSize(80, 22)
            rl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            rl.setStyleSheet(ROW_LBL)
            tbl.addWidget(rl, row_i, 0)

            for ci, val in enumerate(defs):
                e = QLineEdit(val)
                e.setFixedSize(58, 22)
                e.setAlignment(Qt.AlignmentFlag.AlignCenter)
                e.setStyleSheet(CELL)
                tbl.addWidget(e, row_i, ci+1)
                store.append(e)

        tbl_wrapper = QHBoxLayout()
        tbl_wrapper.addLayout(tbl)
        tbl_wrapper.addStretch()
        ll.addLayout(tbl_wrapper)

        # S2 Detail
        det = QPushButton("S2:Detail")
        det.setFixedWidth(85)
        det.setStyleSheet(BTN)
        det.clicked.connect(self._on_s2_detail)
        ll.addWidget(det)

        ml.addWidget(grp_l)
        ml.addStretch()

        # ── Bottom navigation buttons ─────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), QColor(BG))
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(10, 4, 10, 8)
        bbl.setSpacing(4)

        for txt, slot in [
            ("1:OK",    self._on_ok),
            ("2:Next",  self._on_next),
            ("3:Pre.",  self._on_pre),
            ("4:Print", self._on_print),
        ]:
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

    # ------------------------------------------------------------------ Data

    def _collect(self):
        return {
            "analytical_method": self._method.currentText(),
            "purge_seq1":   self._purge.text(),
            "source_seq1":  self._src1.currentText(),
            "source_seq2":  self._src2.currentText(),
            "source_seq3":  self._src3.currentText(),
            "source_clean": self._srcc.currentText(),
            "preburn_seq1": self._pb1.text(),
            "preburn_seq2": self._pb2.text(),
            "preburn_seq3": self._pb3.text(),
            "integ_seq1":   self._ig1.text(),
            "integ_seq2":   self._ig2.text(),
            "integ_seq3":   self._ig3.text(),
            "clean_value":  self._clean.text(),
            "monitor_elements": [
                {"option":  self._mon_ele[i].currentText(),
                 "element": _parse_monitor(self._mon_ele[i].currentText())[0],
                 "value":   _parse_monitor(self._mon_ele[i].currentText())[1]}
                for i in range(3)
            ],
            "h_level": [e.text() for e in self._h],
            "l_level": [e.text() for e in self._l],
        }

    def _apply(self, d):
        if not d:
            return
        self._method.setCurrentText(d.get("analytical_method","P:PDA+Integ. Mode"))
        self._purge.setText(d.get("purge_seq1","3"))
        self._src1.setCurrentText(d.get("source_seq1","3 Peak Spark"))
        self._src2.setCurrentText(d.get("source_seq2","Normal Spark"))
        self._src3.setCurrentText(d.get("source_seq3","Lamp"))
        self._srcc.setCurrentText(d.get("source_clean","Cleaning"))
        self._pb1.setText(d.get("preburn_seq1","200"))
        self._pb2.setText(d.get("preburn_seq2","200"))
        self._pb3.setText(d.get("preburn_seq3","0"))
        self._ig1.setText(d.get("integ_seq1","300"))
        self._ig2.setText(d.get("integ_seq2","23"))
        self._ig3.setText(d.get("integ_seq3","0"))
        self._clean.setText(d.get("clean_value","0"))
        for i, m in enumerate(d.get("monitor_elements",[])):
            if i < 3:
                opt = m.get("option", "")
                if not opt:
                    ele = m.get("element","")
                    wl  = m.get("value","")
                    opt = f"{ele}   {wl}" if ele and ele != "None" else "None"
                self._mon_ele[i].setCurrentText(opt)
        for i, v in enumerate(d.get("h_level",[])):
            if i < 9: self._h[i].setText(v)
        for i, v in enumerate(d.get("l_level",[])):
            if i < 9: self._l[i].setText(v)

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_01_condition = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_01_condition:
                self._apply(g.page_01_condition)
        finally:
            session.close()

    # ------------------------------------------------------------------ Buttons

    def _on_ok(self):
        self._save()
        QMessageBox.information(self, "Saved", "Settings saved successfully!")

    def _on_next(self):
        self._save()
        from ui.anainf.page_02_attenuator import AttenuatorPage
        self.main_window.set_right_widget(
            AttenuatorPage(self.main_window, self.group_id, self.group_name))

    def _on_pre(self):
        self._save()
        self.main_window._show_home_content()

    def _on_print(self):
        QMessageBox.information(self, "Print", "Print coming soon.")

    def _on_cancel(self):
        if QMessageBox.question(
            self, "Cancel", "Discard changes?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.main_window._show_home_content()

    def _on_s2_detail(self):
        QMessageBox.information(self, "S2:Detail",
            "Detail Condition popup — coming in next build.")