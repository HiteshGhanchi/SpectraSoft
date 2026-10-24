"""
SpectraSoft — Page 6: Matrix Element Correction Coefficients

Manual-style Page 6 table:

Target AR-No. | Target NAME | D/L | Interfering AR-No. | Interfering NAME | COEFF.

Purpose:
- Stores inter-element matrix correction coefficients.
- These coefficients are used after Page 5 working curve conversion.
- Page 6 is normally filed by Regression Matrix Coefficient Calculation.
- User can also manually enter / override rows.

Correction meaning:
- L = additive / overlap correction
      C = C0 + sum(lj * Cj)

- D = multiplicative / matrix effect correction
      C = C0 * (1 + sum(dj * Cj))

Default:
- No matrix corrections active.
- Empty rows are ignored.
- COEFF. defaults to 0.000000.

Saved JSON example:
{
    "corrections": [
        {
            "target_ar_no": "4",
            "target_element": "MN",
            "target_name": "Mn",
            "type": "L",
            "interfering_ar_no": "10",
            "interfering_element": "CR",
            "interfering_name": "Cr",
            "coeff": 0.000000
        }
    ]
}
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView
)
from PyQt6.QtCore import Qt
import math

from core.persistence.database import get_session
from core.persistence.models import AnalyticalGroup
from core.persistence.matrix_correction_repository import (
    activate_matrix_correction,
    get_active_matrix_corrections,
    list_matrix_corrections,
    retire_matrix_correction,
    update_active_matrix_coefficient,
)


class CorrectionPage(QWidget):
    """
    Page 6: Matrix Element Correction Coefficients.
    """

    COL_TARGET_AR = 0
    COL_TARGET_NAME = 1
    COL_TYPE = 2
    COL_INTERF_AR = 3
    COL_INTERF_NAME = 4
    COL_COEFF = 5

    HEADERS = [
        "AR-No.",
        "NAME",
        "D/L",
        "AR-No.",
        "NAME",
        "COEFF.",
    ]

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        self._updating_table = False
        self._selected_matrix_id = None

        # Page 3 lookup:
        # {
        #   "1": {"name": "Fe", "element": "FE"},
        #   "2": {"name": "C", "element": "C"}
        # }
        self._ar_lookup = {}

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_page3_lookup()
        self._build_ui()
        self._load()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Title Bar
        bar = QLabel(f"Matrix Correction Coefficients - {self.group_name}")
        bar.setFixedHeight(24)
        bar.setContentsMargins(12, 0, 0, 0)
        bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        bar.setStyleSheet(
            "background:#5c9bd5;"
            "color:white;"
            "font:bold 10pt Arial;"
        )
        root.addWidget(bar)

        # Outer Frame
        outer = QFrame()
        outer.setFrameShape(QFrame.Shape.Box)
        outer.setFrameShadow(QFrame.Shadow.Sunken)
        outer.setLineWidth(2)
        outer.setStyleSheet("background:#d4d0c8;")
        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(14, 14, 14, 10)
        outer_layout.setSpacing(8)

        # Page Title
        title = QLabel("MATRIX ELEMENT CORRECTION COEFFICIENTS")
        title.setFixedHeight(24)
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
        outer_layout.addWidget(title)

        # Help note
        note = QLabel(
            "Register inter-element corrections. D/L may be blank, D, or L. "
            "D = multiplicative matrix correction; L = additive overlap correction. "
            "Rows with blank AR-No. fields are ignored."
        )
        note.setFixedHeight(42)
        note.setWordWrap(True)
        note.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#555555;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(note)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.table.setStyleSheet(
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
            "background:white;"
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
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked |
            QAbstractItemView.EditTrigger.SelectedClicked |
            QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.table.verticalHeader().setDefaultSectionSize(27)

        header = self.table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setHighlightSections(False)
        header.setStretchLastSection(True)

        self.table.setColumnWidth(self.COL_TARGET_AR, 70)
        self.table.setColumnWidth(self.COL_TARGET_NAME, 130)
        self.table.setColumnWidth(self.COL_TYPE, 60)
        self.table.setColumnWidth(self.COL_INTERF_AR, 70)
        self.table.setColumnWidth(self.COL_INTERF_NAME, 130)
        self.table.setColumnWidth(self.COL_COEFF, 110)

        for col in range(len(self.HEADERS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.table.itemChanged.connect(self._on_item_changed)

        outer_layout.addWidget(self.table, stretch=1)

        versions_title = QLabel("MATRIX CORRECTION VERSIONS")
        versions_title.setStyleSheet("font:bold 9pt Arial;color:black;background:#d4d0c8;")
        outer_layout.addWidget(versions_title)

        self.version_table = QTableWidget()
        self.version_table.setColumnCount(8)
        self.version_table.setHorizontalHeaderLabels([
            "Target", "D/L", "Interfering", "Coeff.",
            "Status", "Version", "Curve ID", "Points / R² / RMSE",
        ])
        self.version_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.version_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.version_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.version_table.verticalHeader().setVisible(False)
        self.version_table.itemSelectionChanged.connect(self._on_version_selected)
        outer_layout.addWidget(self.version_table, stretch=1)

        version_buttons = QHBoxLayout()
        self.activate_button = QPushButton("Activate Selected Version")
        self.activate_button.setStyleSheet(self._button_style())
        self.activate_button.clicked.connect(self._on_activate_version)
        version_buttons.addWidget(self.activate_button)
        self.retire_button = QPushButton("Retire Selected Version")
        self.retire_button.setStyleSheet(self._button_style())
        self.retire_button.clicked.connect(self._on_retire_version)
        version_buttons.addWidget(self.retire_button)
        version_buttons.addStretch()
        outer_layout.addLayout(version_buttons)

        # Control row
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(6)

        btn_add = QPushButton("Add Correction")
        btn_add.setStyleSheet(self._button_style())
        btn_add.clicked.connect(self._on_add_row)
        ctrl_layout.addWidget(btn_add)

        btn_delete = QPushButton("Delete Selected")
        btn_delete.setStyleSheet(self._button_style())
        btn_delete.clicked.connect(self._on_delete_selected)
        ctrl_layout.addWidget(btn_delete)

        btn_clear = QPushButton("Clear All")
        btn_clear.setStyleSheet(self._button_style())
        btn_clear.clicked.connect(self._on_clear_all)
        ctrl_layout.addWidget(btn_clear)

        ctrl_layout.addStretch()

        info_lbl = QLabel(
            "No correction is applied when this table is empty or coefficients are 0.000000."
        )
        info_lbl.setStyleSheet(
            "QLabel{"
            "color:#555555;"
            "font:9pt Arial;"
            "border:none;"
            "background:#d4d0c8;"
            "}"
        )
        ctrl_layout.addWidget(info_lbl)

        outer_layout.addLayout(ctrl_layout)

        # Bottom Navigation
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        btn_bar.setStyleSheet("background:#d4d0c8;")

        nav = QHBoxLayout(btn_bar)
        nav.setContentsMargins(12, 4, 12, 8)
        nav.setSpacing(4)

        for text, slot in [
            ("OK", self._on_ok),
            ("Next", self._on_next),
            ("Previous", self._on_pre),
            ("Print", self._on_print),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(self._button_style())
            btn.clicked.connect(slot)
            nav.addWidget(btn)

        nav.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(self._button_style())
        cancel_btn.clicked.connect(self._on_cancel)
        nav.addWidget(cancel_btn)

        root.addWidget(btn_bar)

    # =========================================================================
    # Styles
    # =========================================================================

    def _button_style(self) -> str:
        return (
            "QPushButton{"
            "background:#d4d0c8;"
            "color:black;"
            "border:2px outset #aaaaaa;"
            "font:9pt Arial;"
            "padding:4px 12px;"
            "min-width:70px;"
            "}"
            "QPushButton:pressed{"
            "border:2px inset #888888;"
            "}"
        )

    # =========================================================================
    # Page 3 Lookup
    # =========================================================================

    def _load_page3_lookup(self):
        """
        Load AR-No. -> element/name mapping from Page 3.
        """
        self._ar_lookup = {}

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group or not group.page_03_channel:
                return

            if not isinstance(group.page_03_channel, list):
                return

            for idx, entry in enumerate(group.page_03_channel):
                ar_no = str(idx + 1)

                name = str(entry.get("name", "")).strip()
                ele = str(entry.get("ele", "")).strip()
                itg = str(entry.get("itg", "")).strip()

                display_name = name or ele or (f"ITG{itg}" if itg else "")

                if not display_name:
                    continue

                self._ar_lookup[ar_no] = {
                    "name": display_name,
                    "element": ele or display_name,
                }

        finally:
            session.close()

    def _name_for_ar(self, ar_no: str) -> str:
        ar_no = str(ar_no or "").strip()

        if ar_no in self._ar_lookup:
            return self._ar_lookup[ar_no]["name"]

        return ""

    def _element_for_ar(self, ar_no: str) -> str:
        ar_no = str(ar_no or "").strip()

        if ar_no in self._ar_lookup:
            return self._ar_lookup[ar_no]["element"]

        return ""

    # =========================================================================
    # Table Helpers
    # =========================================================================

    def _on_item_changed(self, item: QTableWidgetItem):
        """
        Normalize D/L and auto-fill names from AR-No.
        """
        if self._updating_table:
            return

        row = item.row()
        col = item.column()
        text = item.text().strip()

        if col == self.COL_TYPE:
            value = text.upper()

            if value not in ["", "D", "L"]:
                self._updating_table = True
                item.setText("")
                self._updating_table = False
                self._show_msg(
                    "Invalid D/L",
                    "D/L must be blank, D, or L.",
                    QMessageBox.Icon.Warning
                )
                return

            if value != text:
                self._updating_table = True
                item.setText(value)
                self._updating_table = False

        elif col == self.COL_TARGET_AR:
            target_name = self._name_for_ar(text)

            self._updating_table = True
            self._set_cell_text(row, self.COL_TARGET_NAME, target_name, editable=False)
            self._updating_table = False

        elif col == self.COL_INTERF_AR:
            interf_name = self._name_for_ar(text)

            self._updating_table = True
            self._set_cell_text(row, self.COL_INTERF_NAME, interf_name, editable=False)
            self._updating_table = False

    def _set_cell_text(self, row: int, col: int, text: str, editable: bool = True):
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

        if editable:
            flags |= Qt.ItemFlag.ItemIsEditable
        else:
            item.setBackground(Qt.GlobalColor.lightGray)

        item.setFlags(flags)
        self.table.setItem(row, col, item)

    def _add_row(self, data: dict = None):
        data = data or {}

        row = self.table.rowCount()
        self.table.insertRow(row)

        target_ar = str(data.get("target_ar_no", "")).strip()
        interf_ar = str(data.get("interfering_ar_no", "")).strip()

        target_name = str(data.get("target_name", "")).strip() or self._name_for_ar(target_ar)
        interf_name = str(data.get("interfering_name", "")).strip() or self._name_for_ar(interf_ar)

        corr_type = str(data.get("type", "")).strip().upper()

        if corr_type not in ["", "D", "L"]:
            corr_type = ""

        coeff = self._normalize_float_text(data.get("coeff", ""), "0.000000", 6)

        self._set_cell_text(row, self.COL_TARGET_AR, target_ar)
        self._set_cell_text(row, self.COL_TARGET_NAME, target_name, editable=False)
        self._set_cell_text(row, self.COL_TYPE, corr_type)
        self._set_cell_text(row, self.COL_INTERF_AR, interf_ar)
        self._set_cell_text(row, self.COL_INTERF_NAME, interf_name, editable=False)
        self._set_cell_text(row, self.COL_COEFF, coeff)

    def _cell_text(self, row: int, col: int) -> str:
        item = self.table.item(row, col)

        if not item:
            return ""

        return item.text().strip()

    # =========================================================================
    # Data Operations
    # =========================================================================

    def _load(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)
            data = group.page_06_matrix if group else {}

            corrections = []

            if isinstance(data, dict):
                corrections = data.get("corrections", [])

                if not isinstance(corrections, list):
                    corrections = []

        finally:
            session.close()

        self._updating_table = True
        self.table.setRowCount(0)

        for correction in corrections:
            if isinstance(correction, dict):
                self._add_row(correction)

        self._updating_table = False

        if self.table.rowCount() == 0:
            self._add_row()

        self._load_matrix_versions()

    def _load_matrix_versions(self):
        """Load normalized Page 6 candidates for version-management actions."""
        session = get_session()
        try:
            rows = list_matrix_corrections(session, self.group_id)
            self.matrix_versions = [
                {
                    "id": row.id,
                    "target": row.target_element_key,
                    "interfering": row.interfering_element_key,
                    "type": row.correction_type,
                    "coefficient": row.coefficient,
                    "status": row.status,
                    "version_name": row.version_name,
                    "source_working_curve_id": row.source_working_curve_id,
                    "point_count": row.point_count,
                    "r2": row.r2,
                    "rmse": row.rmse,
                }
                for row in rows
            ]
            if hasattr(self, "version_table"):
                self.version_table.setRowCount(0)
                for row in self.matrix_versions:
                    row_index = self.version_table.rowCount()
                    self.version_table.insertRow(row_index)
                    values = [
                        row["target"], row["type"], row["interfering"],
                        f"{row['coefficient']:.6f}", row["status"],
                        row["version_name"],
                        str(row["source_working_curve_id"] or "—"),
                        f"{row['point_count']} / {row['r2']:.4f} / {row['rmse']:.6f}"
                        if row["r2"] is not None and row["rmse"] is not None
                        else str(row["point_count"]),
                    ]
                    for column, value in enumerate(values):
                        item = QTableWidgetItem(value)
                        item.setData(Qt.ItemDataRole.UserRole, row["id"])
                        self.version_table.setItem(row_index, column, item)
            return self.matrix_versions
        finally:
            session.close()

    def _activate_selected_matrix(self):
        correction_id = getattr(self, "_selected_matrix_id", None)
        if correction_id is None:
            return None
        session = get_session()
        try:
            row = activate_matrix_correction(session, correction_id)
            self._sync_active_json(session)
            self._reload_manual_table(session)
            self._load_matrix_versions()
            return row
        finally:
            session.close()

    def _retire_selected_matrix(self):
        correction_id = getattr(self, "_selected_matrix_id", None)
        if correction_id is None:
            return None
        session = get_session()
        try:
            row = retire_matrix_correction(session, correction_id)
            self._sync_active_json(session)
            self._reload_manual_table(session)
            self._load_matrix_versions()
            return row
        finally:
            session.close()

    def _on_version_selected(self):
        selected = self.version_table.selectionModel().selectedRows()
        self._selected_matrix_id = None
        if selected:
            item = self.version_table.item(selected[0].row(), 0)
            if item is not None:
                self._selected_matrix_id = item.data(Qt.ItemDataRole.UserRole)

    def _on_activate_version(self):
        try:
            if self._activate_selected_matrix() is not None:
                self._show_msg("Activated", "Matrix correction version activated.")
        except ValueError as error:
            self._show_msg("Activation Failed", str(error), QMessageBox.Icon.Warning)

    def _on_retire_version(self):
        try:
            if self._selected_matrix_id is None:
                return
            if not self._show_question(
                "Retire Matrix Version",
                "Retire the selected matrix correction version?",
            ):
                return
            if self._retire_selected_matrix() is not None:
                self._show_msg("Retired", "Matrix correction version retired.")
        except ValueError as error:
            self._show_msg("Retirement Failed", str(error), QMessageBox.Icon.Warning)

    def _sync_active_json(self, session):
        """Keep legacy Page 6 JSON limited to active normalized corrections."""
        group = session.get(AnalyticalGroup, self.group_id)
        if group is None:
            return
        rows = get_active_matrix_corrections(session, self.group_id)
        by_element = {
            str(info.get("element", "")).strip().upper(): (ar_no, info)
            for ar_no, info in self._ar_lookup.items()
        }
        existing_data = group.page_06_matrix if isinstance(group.page_06_matrix, dict) else {}
        existing_rows = existing_data.get("corrections", [])
        normalized_keys = {
            (
                row.target_element_key,
                row.interfering_element_key,
                row.correction_type,
            )
            for row in list_matrix_corrections(session, self.group_id)
            if row.status in {"active", "retired"}
        }
        compatibility_rows = []
        for legacy in existing_rows if isinstance(existing_rows, list) else []:
            target = str(
                legacy.get("target_element") or legacy.get("target_name") or ""
            ).strip().upper()
            interfering = str(
                legacy.get("interfering_element")
                or legacy.get("interfering_name")
                or ""
            ).strip().upper()
            correction_type = str(legacy.get("type", "")).strip().upper()
            if (target, interfering, correction_type) not in normalized_keys:
                compatibility_rows.append(legacy)
        group.page_06_matrix = {
            "corrections": [
                self._compatibility_row(row, by_element)
                for row in rows
            ] + compatibility_rows
        }
        session.commit()

    def _compatibility_row(self, row, by_element: dict) -> dict:
        target_ar, target_info = by_element.get(row.target_element_key, ("", {}))
        interfering_ar, interfering_info = by_element.get(
            row.interfering_element_key, ("", {})
        )
        return {
            "target_ar_no": target_ar,
            "target_element": row.target_element_key,
            "target_name": target_info.get("name", row.target_element_key),
            "type": row.correction_type,
            "interfering_ar_no": interfering_ar,
            "interfering_element": row.interfering_element_key,
            "interfering_name": interfering_info.get(
                "name", row.interfering_element_key
            ),
            "coeff": row.coefficient,
        }

    def _reload_manual_table(self, session):
        group = session.get(AnalyticalGroup, self.group_id)
        data = group.page_06_matrix if group else {}
        rows = data.get("corrections", []) if isinstance(data, dict) else []
        self._updating_table = True
        self.table.setRowCount(0)
        for row in rows if isinstance(rows, list) else []:
            if isinstance(row, dict):
                self._add_row(row)
        if self.table.rowCount() == 0:
            self._add_row()
        self._updating_table = False

    def _collect(self) -> dict:
        corrections = []

        for row in range(self.table.rowCount()):
            target_ar = self._cell_text(row, self.COL_TARGET_AR)
            target_name = self._cell_text(row, self.COL_TARGET_NAME)
            corr_type = self._cell_text(row, self.COL_TYPE).upper()
            interf_ar = self._cell_text(row, self.COL_INTERF_AR)
            interf_name = self._cell_text(row, self.COL_INTERF_NAME)
            coeff_text = self._cell_text(row, self.COL_COEFF)

            # Completely blank row is ignored.
            if (
                not target_ar and
                not target_name and
                not corr_type and
                not interf_ar and
                not interf_name and
                not coeff_text
            ):
                continue

            # Row with only default coeff and no AR fields is ignored.
            if not target_ar and not interf_ar:
                continue

            if corr_type not in ["D", "L"]:
                raise ValueError(
                    f"Row {row + 1}: D/L must be D or L."
                )

            if not target_ar:
                raise ValueError(
                    f"Row {row + 1}: Target AR-No. is required."
                )

            if not interf_ar:
                raise ValueError(
                    f"Row {row + 1}: Interfering AR-No. is required."
                )

            if target_ar == interf_ar:
                raise ValueError(
                    f"Row {row + 1}: Target and interfering element cannot be the same."
                )

            target_element = self._element_for_ar(target_ar)
            interfering_element = self._element_for_ar(interf_ar)

            if not target_element:
                raise ValueError(
                    f"Row {row + 1}: Target AR-No. {target_ar} is not found in Page 3."
                )

            if not interfering_element:
                raise ValueError(
                    f"Row {row + 1}: Interfering AR-No. {interf_ar} is not found in Page 3."
                )

            coeff = self._to_float(coeff_text, 0.0)

            corrections.append({
                "target_ar_no": target_ar,
                "target_element": target_element,
                "target_name": target_name or target_element,
                "type": corr_type,
                "interfering_ar_no": interf_ar,
                "interfering_element": interfering_element,
                "interfering_name": interf_name or interfering_element,
                "coeff": coeff,
            })

        return {
            "corrections": corrections
        }

    def _save(self):
        data = self._collect()

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group:
                group.page_06_matrix = data
                active_rows = get_active_matrix_corrections(session, self.group_id)
                desired_keys = set()
                for correction in data["corrections"]:
                    target_key = str(correction.get("target_element", "")).strip().upper()
                    interfering_key = str(correction.get("interfering_element", "")).strip().upper()
                    correction_type = str(correction.get("type", "")).strip().upper()
                    key = (target_key, interfering_key, correction_type)
                    desired_keys.add(key)
                    for normalized in active_rows:
                        normalized_key = (
                            normalized.target_element_key,
                            normalized.interfering_element_key,
                            normalized.correction_type,
                        )
                        if normalized_key == key:
                            update_active_matrix_coefficient(
                                session, normalized.id, correction["coeff"]
                            )
                            break

                for normalized in active_rows:
                    normalized_key = (
                        normalized.target_element_key,
                        normalized.interfering_element_key,
                        normalized.correction_type,
                    )
                    if normalized_key not in desired_keys:
                        retire_matrix_correction(session, normalized.id)
                self._sync_active_json(session)
                session.commit()

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _to_float(self, text, default: float = 0.0) -> float:
        try:
            value = str(text or "").strip()

            if value == "":
                return default

            result = float(value)
            if not math.isfinite(result):
                raise ValueError
            return result

        except (TypeError, ValueError):
            raise ValueError(f"Invalid numeric coefficient: {text}")

    def _normalize_float_text(self, value, default: str, decimals: int) -> str:
        raw = str(value or "").strip()

        if raw == "":
            raw = default

        try:
            return f"{float(raw):.{decimals}f}"

        except (TypeError, ValueError):
            return default

    # =========================================================================
    # Buttons
    # =========================================================================

    def _on_add_row(self):
        self._add_row()

    def _on_delete_selected(self):
        selected = self.table.selectionModel().selectedRows()

        if not selected:
            self._show_msg(
                "Delete",
                "Please select a correction row to delete.",
                QMessageBox.Icon.Warning
            )
            return

        row = selected[0].row()

        if QMessageBox.question(
            self,
            "Delete Correction",
            "Delete selected matrix correction row?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self.table.removeRow(row)

        if self.table.rowCount() == 0:
            self._add_row()

    def _on_clear_all(self):
        if QMessageBox.question(
            self,
            "Clear All",
            "Clear all matrix correction rows?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        self.table.setRowCount(0)
        self._add_row()

    def _on_ok(self):
        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Matrix Correction",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        self._show_msg("Saved", "Matrix correction data saved successfully.")

    def _on_next(self):
        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Matrix Correction",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        try:
            from ui.anainf.page_07_master import MasterCurvePage

            self.main_window.set_right_widget(
                MasterCurvePage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            self._show_msg("Next Page", "Page 7 is not built yet.")

    def _on_pre(self):
        try:
            self._save()
        except ValueError as e:
            self._show_msg(
                "Invalid Matrix Correction",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        try:
            from ui.anainf.page_05_working_curve import WorkingCurvePage

            self.main_window.set_right_widget(
                WorkingCurvePage(
                    self.main_window,
                    self.group_id,
                    self.group_name
                )
            )

        except ImportError:
            pass

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        if self._show_question("Cancel", "Discard changes?"):
            self._load()
            self.main_window._show_home_content()

    # =========================================================================
    # Message Helpers
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
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
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
        return msg.exec() == QMessageBox.StandardButton.Yes
