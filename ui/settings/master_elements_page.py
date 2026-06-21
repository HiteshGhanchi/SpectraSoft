"""
SpectraSoft — Master Elements Settings Page

Editable list of all elements the spectrometer supports.
Loads from DB only — no hardcoded defaults.
Export/Import via JSON file.

Columns:
- ITG No.: Integrator number (primary key, used as hardware channel identifier)
- Ele. Name: Element symbol (e.g., FE, C, SI)
- Chemical Name: Full element name (e.g., Iron, Carbon)
- Wavelength: Wavelength in nm (e.g., 271.4, 193.0)

Rules:
- ITG No. must be unique (primary key)
- Ele. Name is required
- ITG No. is used as the primary key in the database
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


class MasterElementsPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._build_ui()
        self._load()

    # =========================================================================
    # UI Construction
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        bar = QLabel("Master Elements")
        bar.setFixedHeight(24)
        bar.setContentsMargins(12, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(
            "background:#5c9bd5;"
            "color:white;"
            "font:bold 10pt Arial;"
        )
        root.addWidget(bar)

        # ── Outer Frame ──────────────────────────────────────────────────
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:white;")
        root.addWidget(outer, stretch=1)

        ol = QVBoxLayout(outer)
        ol.setContentsMargins(0, 0, 0, 0)

        inner = QWidget()
        inner.setAutoFillBackground(True)
        ip = inner.palette()
        ip.setColor(inner.backgroundRole(), Qt.GlobalColor.lightGray)
        inner.setPalette(ip)

        ml = QVBoxLayout(inner)
        ml.setContentsMargins(20, 16, 20, 12)
        ml.setSpacing(8)

        # ── Info Text ────────────────────────────────────────────────────
        info = QLabel(
            "Define all elements the spectrometer supports.\n"
            "ITG No. is the hardware channel number (primary key)."
        )
        info.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:#666666;"
            "font:9pt Arial;"
            "border:none;"
            "padding:2px 0px;"
            "}"
        )
        ml.addWidget(info)

        # ── Excel-Style Table ───────────────────────────────────────────
        table_frame = QFrame()
        table_frame.setStyleSheet(
            "QFrame{"
            "background:white;"
            "border:1px solid #888888;"
            "}"
        )

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "ITG No.", "Ele. Name", "Chemical Name", "Wavelength"
        ])

        # Excel-style table styling
        self.table.setStyleSheet(
            "QTableWidget{"
            "background:white;"
            "color:black;"
            "border:none;"
            "gridline-color:#888888;"
            "font:9pt Arial;"
            "}"
            "QTableWidget::item{"
            "border:1px solid #888888;"
            "padding:0px 4px;"
            "color:black;"
            "}"
            "QHeaderView::section{"
            "background:#0078d7;"
            "color:white;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:2px 4px;"
            "}"
            "QTableWidget::item:selected{"
            "background:#cce5ff;"
            "color:black;"
            "}"
            "QTableWidget::item:!selected{"
            "color:black;"
            "}"
            "QTableWidget QLineEdit{"
            "background:white;"
            "color:black;"
            "}"
        )

        # Column widths
        self.table.setColumnWidth(0, 80)   # ITG No.
        self.table.setColumnWidth(1, 100)  # Ele. Name
        self.table.setColumnWidth(2, 120)  # Chemical Name
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )

        # Row height - 27px consistent
        self.table.verticalHeader().setDefaultSectionSize(27)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        table_layout.addWidget(self.table)

        ml.addWidget(table_frame)

        # ── Buttons ──────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        btn_style = (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:60px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

        for label, slot in [
            ("Add Row", self._on_add),
            ("Delete Row", self._on_delete),
            ("Save", self._on_save),
            ("Export", self._on_export),
            ("Import", self._on_import),
        ]:
            b = QPushButton(label)
            b.setStyleSheet(btn_style)
            b.clicked.connect(slot)
            btn_row.addWidget(b)

        btn_row.addStretch()
        ml.addLayout(btn_row)

        ol.addWidget(inner)

    # =========================================================================
    # Data
    # =========================================================================

    def _add_row(self, itg_no="", ele_name="", chemical_name="", wavelength=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        # ITG No. column (editable, but must be unique)
        itg_item = QTableWidgetItem(str(itg_no))
        itg_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 0, itg_item)

        # Ele. Name
        ele_item = QTableWidgetItem(ele_name)
        ele_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 1, ele_item)

        # Chemical Name
        chem_item = QTableWidgetItem(chemical_name)
        chem_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 2, chem_item)

        # Wavelength
        wl_item = QTableWidgetItem(wavelength)
        wl_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.table.setItem(row, 3, wl_item)

    def _load(self):
        """Load from DB. If empty, table stays empty."""
        session = get_session()
        try:
            rows = session.query(MasterElement).order_by(
                MasterElement.display_order,
                MasterElement.itg_no).all()
            self.table.setRowCount(0)
            for r in rows:
                self._add_row(
                    r.itg_no,
                    r.ele_name,
                    r.chemical_name,
                    r.wavelength
                )
        finally:
            session.close()

    def _collect(self) -> list:
        rows = []
        for row in range(self.table.rowCount()):
            def cell(col, r=row):
                item = self.table.item(r, col)
                return item.text().strip() if item else ""
            itg_val = cell(0)
            if not itg_val:
                continue  # skip rows without ITG
            rows.append({
                "itg_no": itg_val,
                "ele_name": cell(1),
                "chemical_name": cell(2),
                "wavelength": cell(3),
            })
        return rows

    # =========================================================================
    # Actions
    # =========================================================================

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
            # We'll update or insert based on itg_no.
            # First get all existing ITG numbers from DB.
            existing_itgs = {r.itg_no for r in session.query(MasterElement).all()}
            new_itgs = set()

            for r in rows:
                try:
                    itg = int(r["itg_no"])
                except ValueError:
                    QMessageBox.warning(self, "Invalid ITG",
                        f"ITG No. '{r['itg_no']}' is not a valid integer.")
                    return
                if itg in new_itgs:
                    QMessageBox.warning(self, "Duplicate ITG",
                        f"ITG No. '{itg}' appears more than once.")
                    return
                new_itgs.add(itg)

                # Check if this ITG already exists
                existing = session.query(MasterElement).filter_by(itg_no=itg).first()
                if existing:
                    # Update existing
                    existing.ele_name = r["ele_name"]
                    existing.chemical_name = r["chemical_name"]
                    existing.wavelength = r["wavelength"]
                else:
                    # Insert new
                    session.add(MasterElement(
                        itg_no=itg,
                        ele_name=r["ele_name"],
                        chemical_name=r["chemical_name"],
                        wavelength=r["wavelength"],
                        display_order=len(existing_itgs)  # simplistic; user can reorder later
                    ))

            # Delete rows that are not in the new list
            to_delete = existing_itgs - new_itgs
            for itg in to_delete:
                session.query(MasterElement).filter_by(itg_no=itg).delete()

            session.commit()
            QMessageBox.information(self, "Saved",
                "Master elements saved successfully.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Save Failed", str(e))
        finally:
            session.close()
        self._load()  # refresh

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
                # Clear existing
                session.query(MasterElement).delete()
                for i, r in enumerate(rows):
                    if not r.get("ele_name"):
                        continue
                    try:
                        itg = int(r.get("itg_no", i + 1))
                    except (ValueError, TypeError):
                        itg = i + 1
                    session.add(MasterElement(
                        itg_no=itg,
                        ele_name=r.get("ele_name", ""),
                        chemical_name=r.get("chemical_name", ""),
                        wavelength=r.get("wavelength", ""),
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

    # =========================================================================
    # Fullscreen mode
    # =========================================================================

    def wants_fullscreen(self) -> bool:
        return True