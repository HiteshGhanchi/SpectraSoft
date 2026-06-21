from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIntValidator

from core.database import get_session
from core.models import AnalyticalGroup, MasterElement


class AttenuatorPage(QWidget):

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()
        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

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
        bar = QLabel(f"Attenuator Settings - {self.group_name}")
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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        ol.addWidget(scroll)

        inner = QWidget()
        inner.setAutoFillBackground(True)
        ip = inner.palette()
        ip.setColor(inner.backgroundRole(), Qt.GlobalColor.lightGray)
        inner.setPalette(ip)
        scroll.setWidget(inner)

        ml = QVBoxLayout(inner)
        ml.setContentsMargins(20, 16, 20, 12)
        ml.setSpacing(8)

        # ── Table Title ──────────────────────────────────────────────────
        title = QLabel("ATTENUATOR SETTINGS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "QLabel{"
            "background:#d4d0c8;"
            "color:black;"
            "font:bold 10pt Arial;"
            "border:1px solid #888888;"
            "padding:3px 0px;"
            "}"
        )
        ml.addWidget(title)

        # ── Get Elements ──────────────────────────────────────────────────
        session = get_session()
        try:
            elements = session.query(MasterElement).order_by(
                MasterElement.display_order).all()
            element_count = len(elements)
        finally:
            session.close()

        if element_count == 0:
            # Create a default list if no elements exist
            default_elements = [
                {"ele_name": "SI", "wavelength": "212.4"},
                {"ele_name": "MN", "wavelength": "293.3"},
                {"ele_name": "P", "wavelength": "178.3"},
                {"ele_name": "S", "wavelength": "180.7"},
                {"ele_name": "V", "wavelength": "311.0"},
                {"ele_name": "CR", "wavelength": "267.7"},
                {"ele_name": "CR", "wavelength": "298.9"},
                {"ele_name": "MO", "wavelength": "202.0"},
                {"ele_name": "MO", "wavelength": "277.5"},
                {"ele_name": "NI", "wavelength": "231.6"},
                {"ele_name": "NI", "wavelength": "227.7"},
                {"ele_name": "AL", "wavelength": "394.4"},
                {"ele_name": "CU", "wavelength": "224.2"},
                {"ele_name": "TI", "wavelength": "337.2"},
                {"ele_name": "W", "wavelength": "220.4"},
                {"ele_name": "B", "wavelength": "182.6"},
                {"ele_name": "NB", "wavelength": "319.5"},
                {"ele_name": "CA", "wavelength": "396.8"},
                {"ele_name": "CO", "wavelength": "258.0"},
                {"ele_name": "SN", "wavelength": "189.9"},
                {"ele_name": "N", "wavelength": "174.5*2"},
                {"ele_name": "PB", "wavelength": "405.7"},
                {"ele_name": "RH", "wavelength": "421.8"},
                {"ele_name": "CE", "wavelength": ""},
            ]
            elements = default_elements
            element_count = len(elements)

        # Split into two halves
        half = (element_count + 1) // 2
        left_elements = elements[:half]
        right_elements = elements[half:]

        # Pad to ensure both tables have same number of rows
        max_rows = max(len(left_elements), len(right_elements))
        if len(left_elements) < max_rows:
            left_elements = left_elements + [None] * (max_rows - len(left_elements))
        if len(right_elements) < max_rows:
            right_elements = right_elements + [None] * (max_rows - len(right_elements))

        # ── Tables Container ─────────────────────────────────────────────
        tables_container = QHBoxLayout()
        tables_container.setSpacing(20)
        tables_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create left table with correct height
        self._left_table = self._create_table(max_rows)
        self._populate_table(self._left_table, left_elements)

        # Create right table with same height
        self._right_table = self._create_table(max_rows)
        self._populate_table(self._right_table, right_elements)

        tables_container.addWidget(self._left_table)
        tables_container.addWidget(self._right_table)

        # Wrap in a container with stretch for centering
        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addLayout(tables_container)
        wrapper.addStretch()

        ml.addLayout(wrapper)
        ml.addStretch()

        # ── Bottom Nav ──────────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        bbp = btn_bar.palette()
        bbp.setColor(btn_bar.backgroundRole(), Qt.GlobalColor.lightGray)
        btn_bar.setPalette(bbp)

        bbl = QHBoxLayout(btn_bar)
        bbl.setContentsMargins(12, 4, 12, 8)
        bbl.setSpacing(4)

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

        for txt, slot in [
            ("1:OK", self._on_ok),
            ("2:Next", self._on_next),
            ("3:Pre.", self._on_pre),
            ("4:Print", self._on_print),
        ]:
            b = QPushButton(txt)
            b.setStyleSheet(btn_style)
            b.clicked.connect(slot)
            bbl.addWidget(b)

        bbl.addStretch()

        canc = QPushButton("9:Cancel")
        canc.setStyleSheet(btn_style)
        canc.clicked.connect(self._on_cancel)
        bbl.addWidget(canc)

        root.addWidget(btn_bar)

    # =========================================================================
    # Table Creation
    # =========================================================================

    def _create_table(self, row_count: int) -> QTableWidget:
        """Create a single Excel-style table with 3 columns."""
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Element", "W.L.", "ATT"])

        # Excel-style table styling
        table.setStyleSheet(
            "QTableWidget{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
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
            # FIX: Force editor line edit to be black on white
            "QLineEdit{"
            "background:white;"
            "color:black;"
            "}"
        )

        # Column widths
        table.setColumnWidth(0, 70)   # Element
        table.setColumnWidth(1, 80)   # Wavelength
        table.setColumnWidth(2, 70)   # ATT

        # FIX: Turn off scrollbars to avoid layout shifting
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )

        # Row height - 27px consistent
        table.verticalHeader().setDefaultSectionSize(27)

        # Set row count
        table.setRowCount(row_count)

        # FIX: Calculate exact table dimensions to remove empty space on the right
        # Width: 70 + 80 + 70 + 2 (for 1px left/right borders) = 222
        table.setFixedWidth(222)
        
        # Height: rows × 27 + header (27) + borders
        table_height = (row_count * 27) + 27 + 3
        table.setFixedHeight(table_height)

        return table

    def _populate_table(self, table, elements):
        """Populate a table with element data."""
        session = get_session()
        try:
            saved_values = {}
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_02_attenuator and g.page_02_attenuator.get("rows"):
                for r in g.page_02_attenuator["rows"]:
                    saved_values[(r["element"], r["wavelength"])] = r.get("att_value", 0)
        finally:
            session.close()

        for row, me in enumerate(elements):
            if me is None:
                # Empty row (padding)
                for col in range(3):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                    # FIX: Color the empty padding rows so the columns look uniformly gray
                    if col < 2:
                        item.setBackground(QColor("#e8e8e8"))
                    else:
                        item.setBackground(QColor("white"))
                    table.setItem(row, col, item)
                continue

            # Handle both model objects and dicts
            if hasattr(me, 'ele_name'):
                ele = me.ele_name or ""
                wl = me.wavelength or ""
            else:
                ele = me.get("ele_name", "")
                wl = me.get("wavelength", "")

            # Element (read-only, grayish)
            ele_item = QTableWidgetItem(ele)
            ele_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ele_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            ele_item.setBackground(QColor("#e8e8e8"))
            ele_item.setForeground(QColor("black"))
            table.setItem(row, 0, ele_item)

            # Wavelength (read-only, grayish)
            wl_item = QTableWidgetItem(wl)
            wl_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            wl_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            wl_item.setBackground(QColor("#e8e8e8"))
            wl_item.setForeground(QColor("black"))
            table.setItem(row, 1, wl_item)

            # ATT value (editable, white)
            att = saved_values.get((ele, wl), 0)
            att_item = QTableWidgetItem(str(att))
            att_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            att_item.setForeground(QColor("black"))
            table.setItem(row, 2, att_item)

    # =========================================================================
    # Data
    # =========================================================================

    def _collect(self) -> dict:
        rows = []
        # Collect from both tables
        for table in [self._left_table, self._right_table]:
            for row in range(table.rowCount()):
                ele_item = table.item(row, 0)
                wl_item = table.item(row, 1)
                att_item = table.item(row, 2)

                if ele_item and wl_item and att_item:
                    ele = ele_item.text().strip()
                    wl = wl_item.text().strip()
                    if ele:  # only save non-empty
                        try:
                            att_val = int(att_item.text()) if att_item.text() else 0
                        except ValueError:
                            att_val = 0
                        rows.append({
                            "element": ele,
                            "wavelength": wl,
                            "att_value": att_val,
                        })

        return {"rows": rows}

    def _save(self):
        session = get_session()
        try:
            g = session.get(AnalyticalGroup, self.group_id)
            if g:
                g.page_02_attenuator = self._collect()
                session.commit()
        finally:
            session.close()

    def _load(self):
        """Reload both tables with current data."""
        session = get_session()
        try:
            elements = session.query(MasterElement).order_by(
                MasterElement.display_order).all()

            if not elements:
                return

            half = (len(elements) + 1) // 2
            left_elements = elements[:half]
            right_elements = elements[half:]

            # Pad to same length
            max_rows = max(len(left_elements), len(right_elements))
            if len(left_elements) < max_rows:
                left_elements = left_elements + [None] * (max_rows - len(left_elements))
            if len(right_elements) < max_rows:
                right_elements = right_elements + [None] * (max_rows - len(right_elements))

            # Save current ATT values
            saved_values = {}
            g = session.get(AnalyticalGroup, self.group_id)
            if g and g.page_02_attenuator and g.page_02_attenuator.get("rows"):
                for r in g.page_02_attenuator["rows"]:
                    saved_values[(r["element"], r["wavelength"])] = r.get("att_value", 0)

            # Update table heights based on new row count
            self._left_table.setRowCount(max_rows)
            self._right_table.setRowCount(max_rows)

            # Recalculate table height
            table_height = (max_rows * 27) + 27 + 3
            self._left_table.setFixedHeight(table_height)
            self._right_table.setFixedHeight(table_height)

            # Repopulate
            self._repopulate_table(self._left_table, left_elements, saved_values)
            self._repopulate_table(self._right_table, right_elements, saved_values)

        finally:
            session.close()

    def _repopulate_table(self, table, elements, saved_values):
        """Repopulate a table with saved data."""
        for row, me in enumerate(elements):
            if me is None:
                for col in range(3):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                    # FIX: Empty rows also get gray background for col 0 and 1
                    if col < 2:
                        item.setBackground(QColor("#e8e8e8"))
                    else:
                        item.setBackground(QColor("white"))
                    table.setItem(row, col, item)
                continue

            if hasattr(me, 'ele_name'):
                ele = me.ele_name or ""
                wl = me.wavelength or ""
            else:
                ele = me.get("ele_name", "")
                wl = me.get("wavelength", "")

            # Element (read-only, grayish)
            ele_item = QTableWidgetItem(ele)
            ele_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            ele_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            ele_item.setBackground(QColor("#e8e8e8"))
            ele_item.setForeground(QColor("black"))
            table.setItem(row, 0, ele_item)

            # Wavelength (read-only, grayish)
            wl_item = QTableWidgetItem(wl)
            wl_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            wl_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            wl_item.setBackground(QColor("#e8e8e8"))
            wl_item.setForeground(QColor("black"))
            table.setItem(row, 1, wl_item)

            # ATT value (editable, white)
            att = saved_values.get((ele, wl), 0)
            att_item = QTableWidgetItem(str(att))
            att_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            att_item.setForeground(QColor("black"))
            table.setItem(row, 2, att_item)

    # =========================================================================
    # Message Box Helper
    # =========================================================================

    def _show_msg(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
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
        msg.exec()

    def _show_question(self, title, text):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet(
            "QLabel{color:black;font:9pt Arial;}"
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
        return msg.exec()

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_ok(self):
        self._save()
        self._show_msg("Saved", "Attenuator settings saved successfully.")

    def _on_next(self):
        self._save()
        from ui.anainf.page_03_element import ElementPage
        self.main_window.set_right_widget(
            ElementPage(self.main_window, self.group_id, self.group_name)
        )

    def _on_pre(self):
        self._save()
        from ui.anainf.page_01_condition import AnalyticalConditionPage
        self.main_window.set_right_widget(
            AnalyticalConditionPage(self.main_window, self.group_id, self.group_name)
        )

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        if self._show_question("Cancel", "Discard changes?") == QMessageBox.StandardButton.Yes:
            from ui.anainf.page_01_condition import AnalyticalConditionPage
            self.main_window.set_right_widget(
                AnalyticalConditionPage(self.main_window, self.group_id, self.group_name)
            )