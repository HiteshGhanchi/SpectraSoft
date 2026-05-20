"""
SpectraSoft — Page 1: Analytical Condition

Saved JSON example:
{
    "analytical_method": "P:PDA+Integ. Mode",
    "purge_seq1": "3",
    "source_seq1": "1: Normal Spark",
    "source_seq2": "2: High Power Spark",
    "source_seq3": "0: Fatigue Lamp",
    "source_clean": "5: Cleaning Spark",
    "preburn_seq1": "200",
    "preburn_seq2": "200",
    "preburn_seq3": "0",
    "integ_seq1": "300",
    "integ_seq2": "23",
    "integ_seq3": "0",
    "clean_value": "0"
}
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton,
    QGroupBox, QFrame, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.database import get_session
from core.models import AnalyticalGroup, SourceCode

BG    = "#d4d0c8"
BTN   = (
    "QPushButton{background:#d4d0c8;color:black;"
    "border:2px outset #ffffff;font:9pt Arial;"
    "padding:3px 8px;min-width:65px;}"
    "QPushButton:pressed{border:2px inset #888;}"
)
GRP   = (
    "QGroupBox{font:9pt Arial;color:black;"
    "border:1px solid #999;margin-top:8px;"
    "padding-top:4px;background:#d4d0c8;}"
    "QGroupBox::title{subcontrol-origin:margin;left:8px;color:black;}"
)
CMB   = (
    "QComboBox{background:white;color:black;border:1px solid #888;font:9pt Arial;}"
    "QComboBox QAbstractItemView{background:white;color:black;}"
)
# Editable cell
CELL_ED = (
    "QLineEdit{background:white;color:black;"
    "border:1px solid #888;font:9pt Arial;padding:1px 3px;}"
)
# Read-only greyed cell
CELL_RO = (
    "QLineEdit{background:#d4d0c8;color:#888;"
    "border:1px solid #888;font:9pt Arial;padding:1px 3px;}"
)
# Header cell style
HDR = (
    "QLabel{background:#d4d0c8;color:black;"
    "border:1px solid #888;font:bold 9pt Arial;"
    "padding:2px 4px;}"
)
# Row label style
ROW = (
    "QLabel{background:#d4d0c8;color:black;"
    "border:1px solid #888;font:9pt Arial;"
    "padding:2px 4px;}"
)
# Unit label (Pulse/Sec) style
UNIT = (
    "QLabel{background:#d4d0c8;color:black;"
    "border:1px solid #888;font:9pt Arial;"
    "padding:2px 4px;}"
)

ROW_H = 24
LBL_W = 60
COL_W = 155
UNIT_W = 50


def _load_source_options() -> list:
    session = get_session()
    try:
        rows = session.query(SourceCode).order_by(SourceCode.entry_no).all()
        opts = []
        for r in rows:
            if r.name and r.name.strip():
                opts.append(f"{format(r.entry_no, 'X')}: {r.name.strip()}")
        return opts if opts else ["(no sources defined)"]
    finally:
        session.close()


def _hdr(text, w=COL_W):
    l = QLabel(text)
    l.setFixedSize(w, ROW_H)
    l.setAlignment(Qt.AlignmentFlag.AlignCenter)
    l.setStyleSheet(HDR)
    return l


def _row_lbl(text):
    l = QLabel(text)
    l.setFixedSize(LBL_W, ROW_H)
    l.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    l.setStyleSheet(ROW)
    return l


def _unit(text):
    l = QLabel(text)
    l.setFixedSize(UNIT_W, ROW_H)
    l.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    l.setStyleSheet(UNIT)
    return l


def _ed(default=""):
    e = QLineEdit(str(default))
    e.setFixedSize(COL_W, ROW_H)
    e.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    e.setStyleSheet(CELL_ED)
    return e


def _ro():
    """Non-editable greyed cell."""
    e = QLineEdit("")
    e.setFixedSize(COL_W, ROW_H)
    e.setReadOnly(True)
    e.setStyleSheet(CELL_RO)
    return e


def _cmb(opts, w=COL_W):
    c = QComboBox()
    c.addItems(opts)
    c.setFixedSize(w, ROW_H)
    c.setStyleSheet(CMB)
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
        self._source_opts = _load_source_options()
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Title bar
        bar = QLabel(f"Analytical Condition - {self.group_name}")
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
        ml.setSpacing(8)

        # ── Analytical Method ─────────────────────────────────────────
        meth_row = QHBoxLayout()
        meth_row.setSpacing(8)
        meth_lbl = QLabel("Analytical Method")
        meth_lbl.setStyleSheet("color:black;font:9pt Arial;")
        self._method = _cmb(["P:PDA+Integ. Mode", "I:Integration Mode"], w=200)
        meth_row.addWidget(meth_lbl)
        meth_row.addWidget(self._method)
        meth_row.addStretch()
        ml.addLayout(meth_row)

        # ── SEQ group ────────────────────────────────────────────────
        grp_s = QGroupBox("SEQ")
        grp_s.setStyleSheet(GRP)
        sg = QGridLayout(grp_s)
        sg.setContentsMargins(8, 8, 8, 8)
        sg.setSpacing(0)

        # Row 0 — column headers
        sg.addWidget(_hdr(""),       0, 0)   # blank top-left
        sg.addWidget(_hdr("SEQ1"),   0, 1)
        sg.addWidget(_hdr("SEQ2"),   0, 2)
        sg.addWidget(_hdr("SEQ3"),   0, 3)
        sg.addWidget(_hdr("Clean"),  0, 4)
        sg.addWidget(_unit(""),      0, 5)

        # Row 1 — Purge (only SEQ1 editable)
        sg.addWidget(_row_lbl("Purge"),  1, 0)
        self._purge = _ed("0")
        sg.addWidget(self._purge,        1, 1)
        sg.addWidget(_ro(),              1, 2)
        sg.addWidget(_ro(),              1, 3)
        sg.addWidget(_ro(),              1, 4)
        sg.addWidget(_unit("Sec."),      1, 5)

        # Row 2 — Source (all 4 editable dropdowns)
        sg.addWidget(_row_lbl("Source"), 2, 0)
        self._src1 = _cmb(self._source_opts)
        self._src2 = _cmb(self._source_opts)
        self._src3 = _cmb(self._source_opts)
        self._srcc = _cmb(self._source_opts)
        sg.addWidget(self._src1,         2, 1)
        sg.addWidget(self._src2,         2, 2)
        sg.addWidget(self._src3,         2, 3)
        sg.addWidget(self._srcc,         2, 4)
        sg.addWidget(_unit(""),          2, 5)

        # Row 3 — Preburn (SEQ1-3 editable, Clean = read-only "Pulse")
        sg.addWidget(_row_lbl("Preburn"), 3, 0)
        self._pb1 = _ed("0")
        self._pb2 = _ed("0")
        self._pb3 = _ed("0")
        sg.addWidget(self._pb1,           3, 1)
        sg.addWidget(self._pb2,           3, 2)
        sg.addWidget(self._pb3,           3, 3)
        sg.addWidget(_ro(),               3, 4)
        sg.addWidget(_unit("Pulse"),      3, 5)

        # Row 4 — Integ (SEQ1-3 editable, Clean = read-only "Pulse")
        sg.addWidget(_row_lbl("Integ."),  4, 0)
        self._ig1 = _ed("0")
        self._ig2 = _ed("0")
        self._ig3 = _ed("0")
        sg.addWidget(self._ig1,           4, 1)
        sg.addWidget(self._ig2,           4, 2)
        sg.addWidget(self._ig3,           4, 3)
        sg.addWidget(_ro(),               4, 4)
        sg.addWidget(_unit("Pulse"),      4, 5)

        # Row 5 — Clean (only Clean column editable)
        sg.addWidget(_row_lbl("Clean"),   5, 0)
        sg.addWidget(_ro(),               5, 1)
        sg.addWidget(_ro(),               5, 2)
        sg.addWidget(_ro(),               5, 3)
        self._clean = _ed("0")
        sg.addWidget(self._clean,         5, 4)
        sg.addWidget(_unit("Pulse"),      5, 5)

        ml.addWidget(grp_s)
        ml.addStretch()

        # ── Bottom nav ────────────────────────────────────────────────
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
        }

    def _apply(self, d):
        if not d:
            return
        self._method.setCurrentText(
            d.get("analytical_method", "P:PDA+Integ. Mode"))
        self._purge.setText(d.get("purge_seq1", "3"))
        self._pb1.setText(d.get("preburn_seq1", "200"))
        self._pb2.setText(d.get("preburn_seq2", "200"))
        self._pb3.setText(d.get("preburn_seq3", "0"))
        self._ig1.setText(d.get("integ_seq1", "300"))
        self._ig2.setText(d.get("integ_seq2", "23"))
        self._ig3.setText(d.get("integ_seq3", "0"))
        self._clean.setText(d.get("clean_value", "0"))
        for combo_w, key in [
            (self._src1, "source_seq1"),
            (self._src2, "source_seq2"),
            (self._src3, "source_seq3"),
            (self._srcc, "source_clean"),
        ]:
            saved = d.get(key, "")
            for i in range(combo_w.count()):
                if combo_w.itemText(i) == saved:
                    combo_w.setCurrentIndex(i)
                    break

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
        QMessageBox.information(self, "Saved", "Settings saved successfully.")

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