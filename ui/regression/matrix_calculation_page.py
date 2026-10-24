"""
SpectraSoft — Matrix Coefficient Calculation Page

This page calculates Page 6 matrix correction coefficients.

Inputs:
1. Job 7 measured drift-corrected intensities:
       AnalyticalGroup.page_05_wc_measurements

2. Certified chemical standard values:
       AnalyticalGroup.page_05_chemical_standards

3. Page 5 working curve coefficients:
       AnalyticalGroup.page_05_wc

Output:
    AnalyticalGroup.page_06_matrix["corrections"]

Correction types:

L correction:
    C_true ≈ C0 + l * Cj

    l = Σ(Cj * error) / Σ(Cj^2)

D correction:
    C_true ≈ C0 * (1 + d * Cj)

    error = C_true - C0
    d = Σ((C0 * Cj) * error) / Σ((C0 * Cj)^2)

Where:
    C_true = certified target concentration
    C0     = concentration calculated from Page 5 before matrix correction
    Cj     = certified interfering element concentration
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QComboBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt

from core.persistence.database import get_session
from core.persistence.models import AnalyticalGroup
from core.analysis.matrix_correction_service import (
    build_matrix_pairs,
    calculate_matrix_coefficient,
)
from core.persistence.matrix_correction_repository import create_matrix_candidate

import csv


class MatrixCalculationPage(QWidget):
    """
    Regression-side Matrix Coefficient Calculator.

    This page does not run hardware.
    It calculates D/L coefficients and files them into Page 6.
    """

    COL_SAMPLE = 0
    COL_C0 = 1
    COL_TRUE = 2
    COL_INTERF = 3
    COL_ERROR = 4

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        self.element_names = []
        self.ar_lookup = {}

        self.current_result = None

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_elements()
        self._build_ui()
        self._populate_combos()
        self._refresh_table()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        bar = QLabel(f"Matrix Coefficient Calculation - {self.group_name}")
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
        outer.setStyleSheet("background:#d4d0c8;")
        root.addWidget(outer, stretch=1)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(14, 14, 14, 10)
        outer_layout.setSpacing(8)

        # ── Page Title ───────────────────────────────────────────────────
        title = QLabel("MATRIX COEFFICIENT CALCULATION")
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

        # ── Info ─────────────────────────────────────────────────────────
        info = QLabel(
            "Select target element, interfering element, and correction type. "
            "The page compares Page 5 calculated concentration with certified "
            "standard values and files the calculated D/L coefficient into Page 6."
        )
        info.setWordWrap(True)
        info.setFixedHeight(42)
        info.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#555555;"
            "font:9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(info)

        # ── Controls ─────────────────────────────────────────────────────
        controls = QHBoxLayout()
        controls.setSpacing(8)

        lbl_target = QLabel("Target:")
        lbl_target.setStyleSheet("font:9pt Arial;color:black;")
        controls.addWidget(lbl_target)

        self.target_combo = QComboBox()
        self.target_combo.setFixedWidth(150)
        self.target_combo.setStyleSheet(self._combo_style())
        self.target_combo.currentIndexChanged.connect(self._refresh_table)
        controls.addWidget(self.target_combo)

        lbl_type = QLabel("D/L:")
        lbl_type.setStyleSheet("font:9pt Arial;color:black;")
        controls.addWidget(lbl_type)

        self.type_combo = QComboBox()
        self.type_combo.setFixedWidth(70)
        self.type_combo.addItems(["L", "D"])
        self.type_combo.setStyleSheet(self._combo_style())
        self.type_combo.currentIndexChanged.connect(self._refresh_table)
        controls.addWidget(self.type_combo)

        lbl_interf = QLabel("Interfering:")
        lbl_interf.setStyleSheet("font:9pt Arial;color:black;")
        controls.addWidget(lbl_interf)

        self.interf_combo = QComboBox()
        self.interf_combo.setFixedWidth(150)
        self.interf_combo.setStyleSheet(self._combo_style())
        self.interf_combo.currentIndexChanged.connect(self._refresh_table)
        controls.addWidget(self.interf_combo)

        controls.addStretch()

        self.points_label = QLabel("Points: 0")
        self.points_label.setStyleSheet("font:9pt Arial;color:#333333;")
        controls.addWidget(self.points_label)

        outer_layout.addLayout(controls)

        # ── Table ────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Sample",
            "Target C0",
            "Certified Target",
            "Certified Interfering",
            "Error"
        ])

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
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        header = self.table.horizontalHeader()
        header.setSectionsClickable(False)
        header.setHighlightSections(False)
        header.setStretchLastSection(True)

        self.table.setColumnWidth(self.COL_SAMPLE, 140)
        self.table.setColumnWidth(self.COL_C0, 120)
        self.table.setColumnWidth(self.COL_TRUE, 140)
        self.table.setColumnWidth(self.COL_INTERF, 150)
        self.table.setColumnWidth(self.COL_ERROR, 120)

        for col in range(5):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Result Label ─────────────────────────────────────────────────
        self.result_label = QLabel("COEFF. = —")
        self.result_label.setFixedHeight(34)
        self.result_label.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#333333;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.result_label)

        # ── Action Buttons ───────────────────────────────────────────────
        action_row = QHBoxLayout()
        action_row.setSpacing(6)

        btn_calc = QPushButton("Calculate")
        btn_calc.setStyleSheet(self._button_style())
        btn_calc.clicked.connect(self._on_calculate)
        action_row.addWidget(btn_calc)

        btn_file = QPushButton("File to Page 6")
        btn_file.setStyleSheet(self._button_style())
        btn_file.clicked.connect(self._on_file_to_page6)
        action_row.addWidget(btn_file)

        btn_export = QPushButton("Export CSV")
        btn_export.setStyleSheet(self._button_style())
        btn_export.clicked.connect(self._on_export_csv)
        action_row.addWidget(btn_export)

        action_row.addStretch()
        outer_layout.addLayout(action_row)

        # ── Bottom Navigation ────────────────────────────────────────────
        btn_bar = QWidget()
        btn_bar.setAutoFillBackground(True)
        btn_bar.setStyleSheet("background:#d4d0c8;")

        nav = QHBoxLayout(btn_bar)
        nav.setContentsMargins(12, 4, 12, 8)
        nav.setSpacing(4)

        for text, slot in [
            ("Page 6", self._on_page6),
            ("Working Curve Regression", self._on_working_curve_regression),
            ("Chemical Standards", self._on_chemical_standards),
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

    def _combo_style(self) -> str:
        return (
            "QComboBox{"
            "background:white;"
            "color:black;"
            "border:1px solid #888888;"
            "font:9pt Arial;"
            "padding:2px 4px;"
            "}"
            "QComboBox QAbstractItemView{"
            "background:white;"
            "color:black;"
            "selection-background-color:#0078d7;"
            "selection-color:white;"
            "}"
        )

    # =========================================================================
    # Load Element / Data
    # =========================================================================

    def _load_elements(self):
        self.element_names = []
        self.ar_lookup = {}

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and isinstance(group.page_03_channel, list):
                for idx, entry in enumerate(group.page_03_channel):
                    ar_no = str(idx + 1)

                    name = str(entry.get("name", "")).strip()
                    ele = str(entry.get("ele", "")).strip()
                    itg = str(entry.get("itg", "")).strip()

                    display_name = name or ele or (f"ITG{itg}" if itg else "")

                    if display_name:
                        self.element_names.append(display_name)
                        self.ar_lookup[ele.upper() or display_name.upper()] = {
                            "ar_no": ar_no,
                            "name": display_name,
                            "element": ele or display_name,
                        }

        finally:
            session.close()

    def _populate_combos(self):
        self.target_combo.clear()
        self.interf_combo.clear()

        for elem in self.element_names:
            info = next(
                (value for value in self.ar_lookup.values() if value.get("name") == elem),
                {},
            )
            element_key = info.get("element", elem)
            self.target_combo.addItem(elem, element_key)
            self.interf_combo.addItem(elem, element_key)

        if len(self.element_names) > 1:
            self.interf_combo.setCurrentIndex(1)

    def _load_group_data(self):
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return {}, {}, {}

            return (
                group.page_05_wc_measurements or {},
                group.page_05_chemical_standards or {},
                group.page_05_wc or {},
            )

        finally:
            session.close()

    # =========================================================================
    # Current Selections
    # =========================================================================

    def _target_element(self) -> str:
        return str(self.target_combo.currentData() or "").strip()

    def _interfering_element(self) -> str:
        return str(self.interf_combo.currentData() or "").strip()

    def _correction_type(self) -> str:
        value = str(self.type_combo.currentText() or "").strip().upper()
        return value if value in ["D", "L"] else "L"

    # =========================================================================
    # Data Pairing
    # =========================================================================

    def _refresh_table(self):
        self.current_result = None
        self.result_label.setText("COEFF. = —")

        target = self._target_element()
        interfering = self._interfering_element()

        if not target or not interfering:
            self.table.setRowCount(0)
            self.points_label.setText("Points: 0")
            return

        try:
            pairs = self._build_pairs(target, interfering)
        except ValueError as error:
            self._show_msg(
                "Calculation Failed",
                str(error),
                QMessageBox.Icon.Warning,
            )
            return

        self.table.setRowCount(len(pairs))

        for row_idx, pair in enumerate(pairs):
            sample_item = QTableWidgetItem(pair["sample"])
            sample_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, self.COL_SAMPLE, sample_item)

            c0_item = QTableWidgetItem(f"{pair['c0']:.6f}")
            c0_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, self.COL_C0, c0_item)

            true_item = QTableWidgetItem(f"{pair['true']:.6f}")
            true_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, self.COL_TRUE, true_item)

            interf_item = QTableWidgetItem(f"{pair['interfering']:.6f}")
            interf_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, self.COL_INTERF, interf_item)

            error_item = QTableWidgetItem(f"{pair['error']:.6f}")
            error_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, self.COL_ERROR, error_item)

        self.table.resizeRowsToContents()
        self.points_label.setText(f"Points: {len(pairs)}")

    def _build_pairs(self, target: str, interfering: str) -> list:
        session = get_session()
        try:
            return build_matrix_pairs(
                session,
                self.group_id,
                target,
                interfering,
            )
        finally:
            session.close()

    def _dict_get_case_insensitive(self, data: dict, key: str):
        target = str(key).strip().upper()

        for k, v in data.items():
            if str(k).strip().upper() == target:
                return v

        return None

    def _page5_coeff_lookup(self, page5_data: dict) -> dict:
        lookup = {}

        if not isinstance(page5_data, dict):
            return lookup

        rows = page5_data.get("coefficients", [])

        if not isinstance(rows, list):
            return lookup

        for row in rows:
            for key in ["element", "name", "ele"]:
                value = str(row.get(key, "")).strip().upper()

                if value:
                    lookup[value] = row

        return lookup

    def _apply_working_curve_for_element(self, intensity: float, coeff: dict) -> float:
        a = self._to_float(coeff.get("a", 0.0), 0.0)
        b = self._to_float(coeff.get("b", 0.0), 0.0)
        c = self._to_float(coeff.get("c", 1.0), 1.0)
        d = self._to_float(coeff.get("d", 0.0), 0.0)

        return (
            a * (intensity ** 3) +
            b * (intensity ** 2) +
            c * intensity +
            d
        )

    # =========================================================================
    # Calculation
    # =========================================================================

    def _on_calculate(self):
        target = self._target_element()
        interfering = self._interfering_element()
        corr_type = self._correction_type()

        if not target or not interfering:
            self._show_msg(
                "Missing Selection",
                "Please select target and interfering elements.",
                QMessageBox.Icon.Warning
            )
            return

        if target.upper() == interfering.upper():
            self._show_msg(
                "Invalid Selection",
                "Target and interfering element cannot be the same.",
                QMessageBox.Icon.Warning
            )
            return

        try:
            pairs = self._build_pairs(target, interfering)
        except ValueError as error:
            self.table.setRowCount(0)
            self.points_label.setText("Points: 0")
            self.result_label.setText(str(error))
            return

        if not pairs:
            self._show_msg(
                "No Valid Data",
                "No valid paired data found.\n\n"
                "Check Job 7 measurements, Chemical Standards, and Page 5 coefficients.",
                QMessageBox.Icon.Warning
            )
            return

        try:
            result = calculate_matrix_coefficient(pairs, corr_type)
        except Exception as e:
            self._show_msg(
                "Calculation Failed",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        self.current_result = {
            "target": target,
            "interfering": interfering,
            "type": corr_type,
            "coeff": result["coefficient"],
            "point_count": result["point_count"],
            "r2": result["r2"],
            "rmse": result["rmse"],
            "working_curve_id": next(
                (pair.get("working_curve_id") for pair in pairs if pair.get("working_curve_id")),
                None,
            ),
        }

        self.result_label.setText(
            f"COEFF. = {result['coefficient']:.6f}     "
            f"Type = {corr_type}     "
            f"Target = {target}     "
            f"Interfering = {interfering}     "
            f"Points = {result['point_count']}     "
            f"Working Curve ID = {self.current_result['working_curve_id'] or 'legacy'}     "
            f"R² = {result['r2'] if result['r2'] is not None else '—'}     "
            f"RMSE = {result['rmse']:.6f}"
        )

    def _on_file_to_page6(self):
        if not self.current_result:
            self._on_calculate()

            if not self.current_result:
                return

        self._file_current_result_to_page6()

        self._show_msg("Filed", "Matrix coefficient filed as an inactive Page 6 candidate.")

    def _file_current_result_to_page6(self):
        result = self.current_result

        target = result["target"]
        interfering = result["interfering"]
        corr_type = result["type"]
        coeff = result["coeff"]

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return

            create_matrix_candidate(
                session,
                self.group_id,
                target,
                interfering,
                corr_type,
                coeff,
                source_working_curve_id=result.get("working_curve_id"),
                point_count=result.get("point_count", 0),
                fit_stats={"r2": result.get("r2"), "rmse": result.get("rmse")},
            )

            # The candidate remains inactive. Do not write it to legacy Page 6
            # JSON because legacy consumers treat every stored row as active.
            # Page 6 synchronizes the compatibility JSON when the candidate is
            # explicitly activated.

        finally:
            session.close()

    # =========================================================================
    # Helpers
    # =========================================================================

    def _to_float(self, value, default: float = 0.0) -> float:
        try:
            text = str(value).strip()

            if text == "":
                return default

            return float(text)

        except (TypeError, ValueError):
            return default

    # =========================================================================
    # Navigation / Export
    # =========================================================================

    def _on_page6(self):
        from ui.anainf.page_06_matrix import CorrectionPage

        self.main_window.set_right_widget(
            CorrectionPage(
                self.main_window,
                self.group_id,
                self.group_name
            )
        )

    def _on_working_curve_regression(self):
        from ui.regression.regression_calculation_page import RegressionCalculationPage

        self.main_window.set_right_widget(
            RegressionCalculationPage(
                self.main_window,
                self.group_id,
                self.group_name
            )
        )

    def _on_chemical_standards(self):
        from ui.regression.chemical_standards_page import ChemicalStandardsPage

        self.main_window.set_right_widget(
            ChemicalStandardsPage(
                self.main_window,
                self.group_id,
                self.group_name
            )
        )

    def _on_export_csv(self):
        target = self._target_element()
        interfering = self._interfering_element()

        if not target or not interfering:
            self._show_msg(
                "Missing Selection",
                "Please select target and interfering elements.",
                QMessageBox.Icon.Warning
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Matrix Calculation Data",
            f"matrix_{target}_{interfering}.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            pairs = self._build_pairs(target, interfering)

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                writer.writerow([
                    "Sample",
                    "Target C0",
                    "Certified Target",
                    "Certified Interfering",
                    "Error"
                ])

                for pair in pairs:
                    writer.writerow([
                        pair["sample"],
                        f"{pair['c0']:.6f}",
                        f"{pair['true']:.6f}",
                        f"{pair['interfering']:.6f}",
                        f"{pair['error']:.6f}",
                    ])

                if self.current_result:
                    writer.writerow([])
                    writer.writerow(["Type", self.current_result["type"]])
                    writer.writerow(["Coefficient", self.current_result["coeff"]])

            self._show_msg(
                "Exported",
                f"Matrix calculation data exported to:\n{path}"
            )

        except Exception as e:
            self._show_msg(
                "Export Failed",
                str(e),
                QMessageBox.Icon.Critical
            )

    def _on_print(self):
        self._show_msg("Print", "Print coming soon.")

    def _on_cancel(self):
        self.main_window._show_home_content()

    # =========================================================================
    # Message
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
