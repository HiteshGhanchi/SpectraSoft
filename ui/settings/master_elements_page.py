"""
SpectraSoft — Master Elements Settings Page

Editable list of all elements the spectrometer supports.
Loads from DB only — no hardcoded defaults.
Export/Import via JSON file.
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
from core.models import MasterElement
from ui.ui_theme import Colors, Stylesheets, Spacing, Fonts, get_font, get_color


class MasterElementsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), get_color(Colors.BG_MAIN))
        self.setPalette(p)
        self._build_ui()
        self._load()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        bar = QLabel("Master Elements")
        bar.setFixedHeight(22)
        bar.setContentsMargins(8, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(Stylesheets.HEADER_BAR)
        root.addWidget(bar)

        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet(Stylesheets.PANEL_WHITE)
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(16, 16, 16, 8)
        ol.setSpacing(10)

        info = QLabel(
            "Define all elements the spectrometer supports.\n"
            "These populate the Attenuator page and element pickers."
        )
        info.setStyleSheet(f"color:{Colors.TEXT_MEDIUM_GRAY};font:{Fonts.SIZE_NORMAL}pt {Fonts.FAMILY_DEFAULT};")
        ol.addWidget(info)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "ITG No.", "Ele. Name", "Chemical Name", "Wavelength"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 120)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet(Stylesheets.TABLE_NORMAL)
        ol.addWidget(self.table)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        for label, slot in [
            ("Add Row",    self._on_add),
            ("Delete Row", self._on_delete),
            ("Save",       self._on_save),
            ("Export",     self._on_export),
            ("Import",     self._on_import),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(Stylesheets.BUTTON_NORMAL)
            b.clicked.connect(slot)
            btn_row.addWidget(b)
        btn_row.addStretch()
        ol.addLayout(btn_row)

    def _add_row(self, itg_no="", ele_name="",
                 chemical_name="", wavelength=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate([
            str(itg_no), ele_name, chemical_name, wavelength
        ]):
            item = QTableWidgetItem(val)
            item.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft |
                Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, col, item)

    def _load(self):
        """Load from DB only. If empty, table stays empty."""
        session = get_session()
        try:
            rows = session.query(MasterElement).order_by(
                MasterElement.display_order,
                MasterElement.id).all()
            self.table.setRowCount(0)
            for r in rows:
                self._add_row(r.itg_no, r.ele_name,
                              r.chemical_name, r.wavelength)
        finally:
            session.close()
            
    def wants_fullscreen(self) -> bool:
        return True

    def _collect(self) -> list:
        rows = []
        for row in range(self.table.rowCount()):
            def cell(col, r=row):
                item = self.table.item(r, col)
                return item.text().strip() if item else ""
            rows.append({
                "itg_no":        cell(0),
                "ele_name":      cell(1),
                "chemical_name": cell(2),
                "wavelength":    cell(3),
            })
        return rows

    def _on_add(self):
        self._add_row()

    def _on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning",
                "Please select a row to delete.")
            return
        self.table.removeRow(row)

    def _on_save(self):
        rows = self._collect()
        session = get_session()
        try:
            session.query(MasterElement).delete()
            for i, r in enumerate(rows):
                if not r["ele_name"]:
                    continue
                try:
                    itg = int(r["itg_no"]) if r["itg_no"] else i + 1
                except ValueError:
                    itg = i + 1
                session.add(MasterElement(
                    ele_name=r["ele_name"],
                    chemical_name=r["chemical_name"],
                    wavelength=r["wavelength"],
                    itg_no=itg,
                    display_order=i
                ))
            session.commit()
            QMessageBox.information(self, "Saved",
                "Master elements saved successfully.")
        finally:
            session.close()

    def _on_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Master Elements",
            "master_elements.json", "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "w") as f:
                json.dump({"master_elements": self._collect()}, f, indent=2)
            QMessageBox.information(self, "Exported",
                f"Master elements exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import Master Elements", "",
            "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "r") as f:
                data = json.load(f)
            rows = data.get("master_elements", [])
            if not rows:
                QMessageBox.warning(self, "Import Failed",
                    "No master_elements found in file.")
                return
            session = get_session()
            try:
                session.query(MasterElement).delete()
                for i, r in enumerate(rows):
                    if not r.get("ele_name"):
                        continue
                    try:
                        itg = int(r.get("itg_no", i + 1))
                    except (ValueError, TypeError):
                        itg = i + 1
                    session.add(MasterElement(
                        ele_name=r.get("ele_name", ""),
                        chemical_name=r.get("chemical_name", ""),
                        wavelength=r.get("wavelength", ""),
                        itg_no=itg,
                        display_order=i
                    ))
                session.commit()
            finally:
                session.close()
            self._load()
            QMessageBox.information(self, "Imported",
                "Master elements imported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", str(e))