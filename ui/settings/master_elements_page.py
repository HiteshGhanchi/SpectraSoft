"""
SpectraSoft — Master Elements Settings Page

Fixed table of 45 hardware channels (ITG 1-45).
User can edit Element Name and Wavelength for each channel.
ITG No. is read-only and serves as the primary key.

Columns:
- ITG No.: Integrator number (1-45, fixed, read-only)
- Ele. Name: Element symbol/name (editable, may be empty)
- Wavelength: Wavelength in nm (editable)

Rules:
- Exactly 45 rows, ITG No. cannot be changed
- Ele. Name may be empty for unused channels
- The same Ele. Name may appear on multiple ITG channels
  because one element can have multiple physical analytical lines
  for different concentration ranges.

Example:
- ITG 2  -> C at 193.0 nm
- ITG 37 -> C at 165.8 nm

This is valid because both are different physical detector channels.
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


NUM_ROWS = 45  # ITG 1 to 45


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

        # ── Table Frame ──────────────────────────────────────────────────
        table_frame = QFrame()
        table_frame.setStyleSheet(
            "QFrame{"
            "background:white;"
            "border:1px solid #888888;"
            "}"
        )
        table_frame.setFixedHeight(465)

        self.table = QTableWidget(NUM_ROWS, 3)
        self.table.setHorizontalHeaderLabels(
            ["ITG No.", "Ele. Name", "Wavelength"]
        )

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
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "}"
        )

        # Column widths
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)

        # Disable column resizing
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )

        self.table.verticalHeader().setDefaultSectionSize(27)
        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # ── Fill rows with fixed ITG numbers ─────────────────────────────
        for row in range(NUM_ROWS):
            itg_no = row + 1

            # ITG No. column: read-only
            itg_item = QTableWidgetItem(str(itg_no))
            itg_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            itg_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled
            )
            itg_item.setBackground(QColor("#e8e8e8"))
            itg_item.setForeground(QColor("black"))
            self.table.setItem(row, 0, itg_item)

            # Ele. Name column: editable
            name_item = QTableWidgetItem("")
            name_item.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft |
                Qt.AlignmentFlag.AlignVCenter
            )
            name_item.setForeground(QColor("black"))
            self.table.setItem(row, 1, name_item)

            # Wavelength column: editable
            wl_item = QTableWidgetItem("")
            wl_item.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft |
                Qt.AlignmentFlag.AlignVCenter
            )
            wl_item.setForeground(QColor("black"))
            self.table.setItem(row, 2, wl_item)

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

    def _load(self):
        """Load element names and wavelengths from DB into the table."""
        session = get_session()
        try:
            rows = session.query(MasterElement).order_by(
                MasterElement.itg_no
            ).all()

            # Clear existing editable cells
            for row in range(NUM_ROWS):
                self.table.item(row, 1).setText("")
                self.table.item(row, 2).setText("")

            # Fill from DB
            for r in rows:
                if 1 <= r.itg_no <= NUM_ROWS:
                    row = r.itg_no - 1
                    self.table.item(row, 1).setText(r.ele_name or "")
                    self.table.item(row, 2).setText(r.wavelength or "")

        finally:
            session.close()

    def _collect(self) -> list:
        """Collect data from table into a list of dictionaries."""
        rows = []

        for row in range(NUM_ROWS):
            name_item = self.table.item(row, 1)
            wl_item = self.table.item(row, 2)

            name = name_item.text().strip() if name_item else ""
            wavelength = wl_item.text().strip() if wl_item else ""

            rows.append({
                "itg_no": row + 1,
                "ele_name": name,
                "wavelength": wavelength,
            })

        return rows

    def _validate_rows(self, rows) -> bool:
        """
        Validate master element rows.

        Empty element names are allowed.
        Duplicate element names are allowed.
        Only fixed ITG range and duplicate ITG safety are checked.
        """
        seen_itg = set()

        for r in rows:
            itg = r.get("itg_no")

            if not isinstance(itg, int):
                QMessageBox.warning(
                    self,
                    "Invalid ITG",
                    "Invalid ITG number found."
                )
                return False

            if itg < 1 or itg > NUM_ROWS:
                QMessageBox.warning(
                    self,
                    "Invalid ITG",
                    f"ITG number {itg} must be between 1 and {NUM_ROWS}."
                )
                return False

            if itg in seen_itg:
                QMessageBox.warning(
                    self,
                    "Duplicate ITG",
                    f"Duplicate ITG number {itg} found."
                )
                return False

            seen_itg.add(itg)

        return True

    # =========================================================================
    # Actions
    # =========================================================================

    def _on_save(self):
        rows = self._collect()

        if not self._validate_rows(rows):
            return

        session = get_session()
        try:
            # Clear all existing entries
            session.query(MasterElement).delete()

            # Insert all 45 rows
            for r in rows:
                session.add(MasterElement(
                    itg_no=r["itg_no"],
                    ele_name=r["ele_name"],
                    wavelength=r["wavelength"],
                ))

            session.commit()

            QMessageBox.information(
                self,
                "Saved",
                f"Master elements saved successfully.\n"
                f"{len(rows)} channels configured."
            )

        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Save Failed", str(e))

        finally:
            session.close()

    def _on_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Master Elements",
            "master_elements.json",
            "JSON Files (*.json)"
        )

        if not path:
            return

        try:
            with open(path, "w") as f:
                json.dump(
                    {"master_elements": self._collect()},
                    f,
                    indent=2
                )

            QMessageBox.information(
                self,
                "Exported",
                f"Master elements exported to:\n{path}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Master Elements",
            "",
            "JSON Files (*.json)"
        )

        if not path:
            return

        try:
            with open(path, "r") as f:
                data = json.load(f)

            rows = data.get("master_elements", [])

            if not rows:
                QMessageBox.warning(
                    self,
                    "Import Failed",
                    "No master_elements found in file."
                )
                return

            itg_map = {}

            for r in rows:
                try:
                    itg = int(r.get("itg_no", 0))
                except (ValueError, TypeError):
                    itg = 0

                if itg < 1 or itg > NUM_ROWS:
                    QMessageBox.warning(
                        self,
                        "Import Failed",
                        f"Invalid ITG No. '{itg}' – must be between 1 and {NUM_ROWS}."
                    )
                    return

                if itg in itg_map:
                    QMessageBox.warning(
                        self,
                        "Import Failed",
                        f"Duplicate ITG No. '{itg}' found in import file."
                    )
                    return

                name = r.get("ele_name", "")
                wavelength = r.get("wavelength", "")

                if name is None:
                    name = ""
                if wavelength is None:
                    wavelength = ""

                name = str(name).strip()
                wavelength = str(wavelength).strip()

                # Empty names are allowed.
                # Duplicate names are allowed.
                itg_map[itg] = (name, wavelength)

            # Clear all editable cells first
            for row in range(NUM_ROWS):
                self.table.item(row, 1).setText("")
                self.table.item(row, 2).setText("")

            # Apply imported rows
            for itg, (name, wavelength) in itg_map.items():
                row = itg - 1
                self.table.item(row, 1).setText(name)
                self.table.item(row, 2).setText(wavelength)

            QMessageBox.information(
                self,
                "Imported",
                f"Imported {len(itg_map)} element entries.\n\n"
                "Click Save to store them in the database."
            )

        except Exception as e:
            QMessageBox.critical(self, "Import Failed", str(e))

    # =========================================================================
    # Fullscreen mode
    # =========================================================================

    def wants_fullscreen(self) -> bool:
        return True