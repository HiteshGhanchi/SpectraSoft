"""
SpectraSoft — Source Codes Settings Page
16 fixed rows (0-F). Name column editable.
"""

import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.database import get_session
from core.models import SourceCode

BG  = "#d4d0c8"
BTN = (
    "QPushButton{background:#d4d0c8;color:black;border:2px outset #ffffff;"
    "font:9pt Arial;padding:3px 8px;min-width:80px;}"
    "QPushButton:pressed{border:2px inset #888;}"
)
NUM_ROWS = 16


class SourceCodesPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        bar = QLabel("Settings — Source Codes")
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
        ol.setContentsMargins(16, 16, 16, 8)
        ol.setSpacing(10)

        info = QLabel(
            "Entry No. (0–F) is the hardware command value sent over UART.\n"
            "Edit the Name column to label each source type."
        )
        info.setStyleSheet("color:#444;font:9pt Arial;")
        ol.addWidget(info)

        # Table — 2 columns, 16 rows
        self.table = QTableWidget(NUM_ROWS, 2)
        self.table.setHorizontalHeaderLabels(["Entry No.", "Name"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 100)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.table.setStyleSheet("""
            QTableWidget {
                background: white; color: black;
                border: 1px solid #aaa; font: 9pt Arial;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background: #d4d0c8; color: black;
                border: 1px solid #aaa; font: 9pt Arial; padding: 3px;
            }
        """)
        ol.addWidget(self.table)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        for label, slot in [
            ("Save",   self._on_save),
            ("Export", self._on_export),
            ("Import", self._on_import),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(BTN)
            b.clicked.connect(slot)
            btn_row.addWidget(b)

        btn_row.addStretch()
        ol.addLayout(btn_row)

    def _load(self):
        session = get_session()
        try:
            rows = session.query(SourceCode).order_by(
                SourceCode.entry_no).all()

            # Seed 16 empty rows if DB is empty
            if not rows:
                for i in range(NUM_ROWS):
                    session.add(SourceCode(entry_no=i, name=""))
                session.commit()
                rows = session.query(SourceCode).order_by(
                    SourceCode.entry_no).all()

            self.table.blockSignals(True)
            for sc in rows:
                row = sc.entry_no

                # Entry No — read only, grey background
                hex_item = QTableWidgetItem(format(sc.entry_no, 'X'))
                hex_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                hex_item.setFlags(
                    Qt.ItemFlag.ItemIsSelectable |
                    Qt.ItemFlag.ItemIsEnabled
                )
                hex_item.setBackground(QColor("#d4d0c8"))
                self.table.setItem(row, 0, hex_item)

                # Name — editable
                name_item = QTableWidgetItem(sc.name or "")
                name_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft |
                    Qt.AlignmentFlag.AlignVCenter
                )
                self.table.setItem(row, 1, name_item)

            self.table.blockSignals(False)
        finally:
            session.close()

    def _collect(self) -> list:
        rows = []
        for row in range(NUM_ROWS):
            name_item = self.table.item(row, 1)
            rows.append({
                "entry_no": row,
                "name": name_item.text().strip() if name_item else ""
            })
        return rows

    def _on_save(self):
        rows = self._collect()
        session = get_session()
        try:
            for r in rows:
                sc = session.get(SourceCode, r["entry_no"])
                if sc:
                    sc.name = r["name"]
                else:
                    session.add(SourceCode(
                        entry_no=r["entry_no"], name=r["name"]))
            session.commit()
            QMessageBox.information(self, "Saved",
                "Source codes saved successfully.")
        finally:
            session.close()

    def _on_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Source Codes", "source_codes.json",
            "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            with open(path, "w") as f:
                json.dump({"source_codes": self._collect()}, f, indent=2)
            QMessageBox.information(self, "Exported",
                f"Source codes exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Source Codes", "",
            "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            rows = data.get("source_codes", [])
            if len(rows) != NUM_ROWS:
                QMessageBox.warning(self, "Import Failed",
                    f"Expected {NUM_ROWS} rows, got {len(rows)}.")
                return
            session = get_session()
            try:
                for r in rows:
                    sc = session.get(SourceCode, r["entry_no"])
                    if sc:
                        sc.name = r.get("name", "")
                    else:
                        session.add(SourceCode(
                            entry_no=r["entry_no"],
                            name=r.get("name", "")))
                session.commit()
            finally:
                session.close()
            self._load()
            QMessageBox.information(self, "Imported",
                "Source codes imported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", str(e))