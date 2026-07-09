"""
SpectraSoft — Regression Calculation Page

This page calculates Page 5 working curve coefficients a, b, c, d.

Inputs:
1. Job 7 measured drift-corrected intensities:
       AnalyticalGroup.page_05_wc_measurements

2. Certified chemical values:
       AnalyticalGroup.page_05_chemical_standards

Output:
    AnalyticalGroup.page_05_wc["coefficients"]

Working curve formula:
    C = a*I^3 + b*I^2 + c*I + d

Degree mapping:
    Degree 1:
        C = c*I + d
        a = 0
        b = 0

    Degree 2:
        C = b*I^2 + c*I + d
        a = 0

    Degree 3:
        C = a*I^3 + b*I^2 + c*I + d

Important:
- This page does not run hardware.
- This page uses measured IDC values already stored by Job 7.
- This page preserves Page 5 Y/N, SKIP, and POINT fields while filing a,b,c,d.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QComboBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt

from core.database import get_session
from core.models import AnalyticalGroup

import csv


class RegressionCalculationPage(QWidget):

    COL_SAMPLE = 0
    COL_INTENSITY = 1
    COL_CHEMICAL = 2

    def __init__(self, main_window, group_id: int, group_name: str):
        super().__init__()

        self.main_window = main_window
        self.group_id = group_id
        self.group_name = group_name

        self.element_names = []
        self.calculated_coeffs = {}

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.lightGray)
        self.setPalette(p)

        self._load_elements()
        self._build_ui()
        self._populate_element_combo()
        self._refresh_current_element_table()

    # =========================================================================
    # UI
    # =========================================================================

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title Bar ──────────────────────────────────────────────────────
        bar = QLabel(f"Regression Calculation - {self.group_name}")
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
        title = QLabel("WORKING CURVE REGRESSION CALCULATION")
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
            "Regression pairs Job 7 drift-corrected intensities with certified "
            "chemical values, then calculates Page 5 coefficients a, b, c, and d."
        )
        info.setWordWrap(True)
        info.setFixedHeight(38)
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

        # ── Controls Row ─────────────────────────────────────────────────
        controls = QHBoxLayout()
        controls.setSpacing(8)

        lbl_elem = QLabel("Element:")
        lbl_elem.setStyleSheet("font:9pt Arial;color:black;")
        controls.addWidget(lbl_elem)

        self.element_combo = QComboBox()
        self.element_combo.setFixedWidth(180)
        self.element_combo.setStyleSheet(self._combo_style())
        self.element_combo.currentIndexChanged.connect(
            self._refresh_current_element_table
        )
        controls.addWidget(self.element_combo)

        lbl_degree = QLabel("Degree:")
        lbl_degree.setStyleSheet("font:9pt Arial;color:black;")
        controls.addWidget(lbl_degree)

        self.degree_combo = QComboBox()
        self.degree_combo.setFixedWidth(80)
        self.degree_combo.addItems(["1", "2", "3"])
        self.degree_combo.setCurrentText("1")
        self.degree_combo.setStyleSheet(self._combo_style())
        self.degree_combo.currentIndexChanged.connect(
            self._refresh_current_element_table
        )
        controls.addWidget(self.degree_combo)

        controls.addStretch()

        self.points_label = QLabel("Points: 0")
        self.points_label.setStyleSheet("font:9pt Arial;color:#333333;")
        controls.addWidget(self.points_label)

        outer_layout.addLayout(controls)

        # ── Pair Table ───────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Sample",
            "IDC from Job 7",
            "Certified Value"
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

        self.table.setColumnWidth(self.COL_SAMPLE, 160)
        self.table.setColumnWidth(self.COL_INTENSITY, 140)
        self.table.setColumnWidth(self.COL_CHEMICAL, 140)

        for col in range(3):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        outer_layout.addWidget(self.table, stretch=1)

        # ── Coefficient Result Label ─────────────────────────────────────
        self.coeff_label = QLabel("a = —     b = —     c = —     d = —")
        self.coeff_label.setFixedHeight(34)
        self.coeff_label.setStyleSheet(
            "QLabel{"
            "background:#f0ece4;"
            "color:#333333;"
            "font:bold 9pt Arial;"
            "border:1px solid #888888;"
            "padding:4px 6px;"
            "}"
        )
        outer_layout.addWidget(self.coeff_label)

        # ── Action Buttons ───────────────────────────────────────────────
        action_row = QHBoxLayout()
        action_row.setSpacing(6)

        btn_calc = QPushButton("Calculate")
        btn_calc.setStyleSheet(self._button_style())
        btn_calc.clicked.connect(self._on_calculate_current)
        action_row.addWidget(btn_calc)

        btn_file = QPushButton("File to Page 5")
        btn_file.setStyleSheet(self._button_style())
        btn_file.clicked.connect(self._on_file_current)
        action_row.addWidget(btn_file)

        btn_calc_all = QPushButton("Calculate All")
        btn_calc_all.setStyleSheet(self._button_style())
        btn_calc_all.clicked.connect(self._on_calculate_all)
        action_row.addWidget(btn_calc_all)

        btn_file_all = QPushButton("File All to Page 5")
        btn_file_all.setStyleSheet(self._button_style())
        btn_file_all.clicked.connect(self._on_file_all)
        action_row.addWidget(btn_file_all)

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
            ("Chemical Standards", self._on_chemical_standards),
            ("Page 5", self._on_page5),
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
    # Data Loading
    # =========================================================================

    def _load_elements(self):
        """
        Load active element/display names from Page 3.

        Uses same display key as analysis pages:
            NAME if present, else ELE, else ITG fallback.
        """
        self.element_names = []

        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if group and group.page_03_channel:
                for entry in group.page_03_channel:
                    name = str(entry.get("name", "")).strip()
                    ele = str(entry.get("ele", "")).strip()
                    itg = str(entry.get("itg", "")).strip()

                    display_name = name or ele or (f"ITG{itg}" if itg else "")

                    if display_name:
                        self.element_names.append(display_name)

        finally:
            session.close()

    def _populate_element_combo(self):
        self.element_combo.clear()

        for elem in self.element_names:
            self.element_combo.addItem(elem, elem)

    def _load_measurements_and_standards(self):
        """
        Load:
        - Job 7 IDC measurements
        - Certified chemical standards
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return [], []

            meas_data = group.page_05_wc_measurements or {}
            chem_data = group.page_05_chemical_standards or {}

            measurements = []
            standards = []

            if isinstance(meas_data, dict):
                measurements = meas_data.get("measurements", [])

                if not isinstance(measurements, list):
                    measurements = []

            if isinstance(chem_data, dict):
                standards = chem_data.get("standards", [])

                if not isinstance(standards, list):
                    standards = []

            return measurements, standards

        finally:
            session.close()

    # =========================================================================
    # Pair Building
    # =========================================================================

    def _current_element(self) -> str:
        return str(self.element_combo.currentData() or "").strip()

    def _current_degree(self) -> int:
        try:
            return int(self.degree_combo.currentText())
        except ValueError:
            return 1

    def _refresh_current_element_table(self):
        elem = self._current_element()

        if not elem:
            self.table.setRowCount(0)
            self.points_label.setText("Points: 0")
            self.coeff_label.setText("a = —     b = —     c = —     d = —")
            return

        pairs = self._build_pairs_for_element(elem)
        self.table.setRowCount(len(pairs))

        for row_idx, pair in enumerate(pairs):
            sample_item = QTableWidgetItem(pair["sample"])
            sample_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_idx, self.COL_SAMPLE, sample_item)

            intensity_item = QTableWidgetItem(f"{pair['intensity']:.5f}")
            intensity_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight |
                Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, self.COL_INTENSITY, intensity_item)

            chemical_item = QTableWidgetItem(f"{pair['chemical']:.5f}")
            chemical_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight |
                Qt.AlignmentFlag.AlignVCenter
            )
            self.table.setItem(row_idx, self.COL_CHEMICAL, chemical_item)

        self.table.resizeRowsToContents()

        degree = self._current_degree()
        needed = degree + 1

        self.points_label.setText(
            f"Points: {len(pairs)} / required {needed}"
        )

        if elem in self.calculated_coeffs:
            self._show_coefficients(self.calculated_coeffs[elem])
        else:
            self.coeff_label.setText("a = —     b = —     c = —     d = —")

    def _build_pairs_for_element(self, elem: str) -> list:
        """
        Pair:
            IDC intensity from Job 7
        with:
            Certified chemical value from Chemical Standards page

        Matching is by sample name.
        """
        measurements, standards = self._load_measurements_and_standards()

        intensity_by_sample = {}
        chemical_by_sample = {}

        for entry in measurements:
            sample = str(entry.get("sample", "")).strip().upper()
            intensities = entry.get("intensities", {})

            if not sample or not isinstance(intensities, dict):
                continue

            value = self._dict_get_case_insensitive(intensities, elem)

            if value is None:
                continue

            try:
                intensity_by_sample[sample] = float(value)
            except (TypeError, ValueError):
                pass

        for entry in standards:
            sample = str(entry.get("sample", "")).strip().upper()
            values = entry.get("values", {})

            if not sample or not isinstance(values, dict):
                continue

            value = self._dict_get_case_insensitive(values, elem)

            if value is None:
                continue

            try:
                chemical_by_sample[sample] = float(value)
            except (TypeError, ValueError):
                pass

        pairs = []

        for sample in sorted(intensity_by_sample.keys()):
            if sample not in chemical_by_sample:
                continue

            pairs.append({
                "sample": sample,
                "intensity": intensity_by_sample[sample],
                "chemical": chemical_by_sample[sample],
            })

        return pairs

    def _dict_get_case_insensitive(self, data: dict, key: str):
        target = str(key).strip().upper()

        for k, v in data.items():
            if str(k).strip().upper() == target:
                return v

        return None

    # =========================================================================
    # Regression Math
    # =========================================================================

    def _fit_element(self, elem: str, degree: int):
        pairs = self._build_pairs_for_element(elem)

        if len(pairs) < degree + 1:
            raise ValueError(
                f"Element {elem}: degree {degree} requires at least "
                f"{degree + 1} valid point(s). Found {len(pairs)}."
            )

        x = [p["intensity"] for p in pairs]
        y = [p["chemical"] for p in pairs]

        coeff = self._polyfit(x, y, degree)

        return coeff, pairs

    def _polyfit(self, x_values: list, y_values: list, degree: int) -> dict:
        """
        Fit polynomial using least squares.

        Preferred:
            numpy.polyfit

        Fallback:
            normal equations solved by Gaussian elimination.

        Returns Page 5 coefficients:
            a, b, c, d
        """
        try:
            import numpy as np

            raw = np.polyfit(x_values, y_values, degree)

            if degree == 1:
                # y = c*x + d
                a = 0.0
                b = 0.0
                c = float(raw[0])
                d = float(raw[1])

            elif degree == 2:
                # y = b*x^2 + c*x + d
                a = 0.0
                b = float(raw[0])
                c = float(raw[1])
                d = float(raw[2])

            else:
                # y = a*x^3 + b*x^2 + c*x + d
                a = float(raw[0])
                b = float(raw[1])
                c = float(raw[2])
                d = float(raw[3])

            return {
                "a": a,
                "b": b,
                "c": c,
                "d": d,
            }

        except Exception:
            return self._polyfit_fallback(x_values, y_values, degree)

    def _polyfit_fallback(self, x_values: list, y_values: list, degree: int) -> dict:
        """
        Least-squares polynomial fit using normal equations.

        Fits:
            y = q0 + q1*x + q2*x^2 + q3*x^3

        Maps:
            d = q0
            c = q1
            b = q2
            a = q3
        """
        n = degree + 1

        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        vector = [0.0 for _ in range(n)]

        for x, y in zip(x_values, y_values):
            powers = [1.0]

            for _ in range(1, (2 * degree) + 1):
                powers.append(powers[-1] * x)

            for row in range(n):
                for col in range(n):
                    matrix[row][col] += powers[row + col]

                vector[row] += y * powers[row]

        q = self._solve_linear_system(matrix, vector)

        d = q[0] if len(q) > 0 else 0.0
        c = q[1] if len(q) > 1 else 0.0
        b = q[2] if len(q) > 2 else 0.0
        a = q[3] if len(q) > 3 else 0.0

        return {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
        }

    def _solve_linear_system(self, matrix: list, vector: list) -> list:
        """
        Solve Ax=b by Gaussian elimination with partial pivoting.
        """
        n = len(vector)
        a = [row[:] + [vector[i]] for i, row in enumerate(matrix)]

        for i in range(n):
            pivot = i

            for r in range(i + 1, n):
                if abs(a[r][i]) > abs(a[pivot][i]):
                    pivot = r

            if abs(a[pivot][i]) < 1e-12:
                raise ValueError(
                    "Regression matrix is singular. "
                    "Check standard points or lower the degree."
                )

            if pivot != i:
                a[i], a[pivot] = a[pivot], a[i]

            pivot_value = a[i][i]

            for col in range(i, n + 1):
                a[i][col] /= pivot_value

            for r in range(n):
                if r == i:
                    continue

                factor = a[r][i]

                for col in range(i, n + 1):
                    a[r][col] -= factor * a[i][col]

        return [a[i][n] for i in range(n)]

    # =========================================================================
    # Calculate / File
    # =========================================================================

    def _on_calculate_current(self):
        elem = self._current_element()
        degree = self._current_degree()

        if not elem:
            self._show_msg(
                "No Element",
                "Please select an element.",
                QMessageBox.Icon.Warning
            )
            return

        try:
            coeff, pairs = self._fit_element(elem, degree)
        except Exception as e:
            self._show_msg(
                "Regression Failed",
                str(e),
                QMessageBox.Icon.Warning
            )
            return

        self.calculated_coeffs[elem] = {
            **coeff,
            "degree": degree,
            "points": len(pairs),
        }

        self._show_coefficients(self.calculated_coeffs[elem])

    def _on_file_current(self):
        elem = self._current_element()

        if not elem:
            self._show_msg(
                "No Element",
                "Please select an element.",
                QMessageBox.Icon.Warning
            )
            return

        if elem not in self.calculated_coeffs:
            self._on_calculate_current()

            if elem not in self.calculated_coeffs:
                return

        self._file_coefficients_to_page5({
            elem: self.calculated_coeffs[elem]
        })

        self._show_msg(
            "Filed",
            f"Regression coefficients for {elem} filed into Page 5."
        )

    def _on_calculate_all(self):
        degree = self._current_degree()

        calculated = 0
        skipped = 0
        messages = []

        for elem in self.element_names:
            try:
                coeff, pairs = self._fit_element(elem, degree)

                self.calculated_coeffs[elem] = {
                    **coeff,
                    "degree": degree,
                    "points": len(pairs),
                }

                calculated += 1

            except Exception as e:
                skipped += 1
                messages.append(f"{elem}: {e}")

        self._refresh_current_element_table()

        summary = (
            f"Calculated: {calculated}\n"
            f"Skipped: {skipped}"
        )

        if messages:
            summary += "\n\nSkipped details:\n" + "\n".join(messages[:12])

            if len(messages) > 12:
                summary += f"\n... and {len(messages) - 12} more."

        self._show_msg("Calculate All", summary)

    def _on_file_all(self):
        if not self.calculated_coeffs:
            self._on_calculate_all()

        if not self.calculated_coeffs:
            self._show_msg(
                "No Coefficients",
                "No coefficients are calculated.",
                QMessageBox.Icon.Warning
            )
            return

        self._file_coefficients_to_page5(self.calculated_coeffs)

        self._show_msg(
            "Filed",
            f"Filed coefficients for {len(self.calculated_coeffs)} element(s) into Page 5."
        )

    def _show_coefficients(self, coeff: dict):
        self.coeff_label.setText(
            f"a = {coeff.get('a', 0.0):.10f}     "
            f"b = {coeff.get('b', 0.0):.10f}     "
            f"c = {coeff.get('c', 0.0):.10f}     "
            f"d = {coeff.get('d', 0.0):.10f}     "
            f"(degree {coeff.get('degree', '-')}, points {coeff.get('points', '-')})"
        )

    def _file_coefficients_to_page5(self, coefficient_map: dict):
        """
        File regression coefficients into AnalyticalGroup.page_05_wc.

        Preserves existing:
        - Y/N
        - norm
        - SKIP
        - POINT

        Also backs up previous coefficients as backup_coefficients.
        """
        session = get_session()

        try:
            group = session.get(AnalyticalGroup, self.group_id)

            if not group:
                return

            old_data = group.page_05_wc or {}

            old_coefficients = []

            if isinstance(old_data, dict):
                old_coefficients = old_data.get("coefficients", [])

                if not isinstance(old_coefficients, list):
                    old_coefficients = []

            page5_rows = self._build_page5_rows_with_coefficients(
                old_coefficients,
                coefficient_map
            )

            group.page_05_wc = {
                "coefficients": page5_rows,
                "backup_coefficients": old_coefficients,
            }

            session.commit()

        finally:
            session.close()

    def _build_page5_rows_with_coefficients(
        self,
        old_coefficients: list,
        coefficient_map: dict
    ) -> list:
        old_lookup = {}

        for row in old_coefficients:
            for key in ["element", "name", "ele"]:
                value = str(row.get(key, "")).strip().upper()

                if value:
                    old_lookup[value] = row

        rows = []

        for elem in self.element_names:
            old = old_lookup.get(elem.upper(), {})

            coeff = coefficient_map.get(elem, None)

            if coeff:
                a = float(coeff.get("a", 0.0))
                b = float(coeff.get("b", 0.0))
                c = float(coeff.get("c", 1.0))
                d = float(coeff.get("d", 0.0))
            else:
                a = self._to_float(old.get("a", 0.0), 0.0)
                b = self._to_float(old.get("b", 0.0), 0.0)
                c = self._to_float(old.get("c", 1.0), 1.0)
                d = self._to_float(old.get("d", 0.0), 0.0)

            yn = str(
                old.get(
                    "yn",
                    old.get("norm", "Y")
                )
            ).strip().upper()

            if yn not in ["", "I", "Y", "N"]:
                yn = "Y"

            skip = str(old.get("skip", "")).strip().upper()

            if skip not in ["", "+"]:
                skip = ""

            point = self._to_float(old.get("point", 0.0), 0.0)

            rows.append({
                "element": elem,
                "ele": str(old.get("ele", elem)).strip() or elem,
                "name": str(old.get("name", elem)).strip() or elem,
                "a": a,
                "b": b,
                "c": c,
                "d": d,

                # Updated Page 5 manual-style fields.
                "yn": yn,
                "norm": yn,
                "skip": skip,
                "point": point,
            })

        return rows

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

    def _on_chemical_standards(self):
        from ui.regression.chemical_standards_page import ChemicalStandardsPage

        self.main_window.set_right_widget(
            ChemicalStandardsPage(
                self.main_window,
                self.group_id,
                self.group_name
            )
        )

    def _on_page5(self):
        from ui.anainf.page_05_working_curve import WorkingCurvePage

        self.main_window.set_right_widget(
            WorkingCurvePage(
                self.main_window,
                self.group_id,
                self.group_name
            )
        )

    def _on_export_csv(self):
        elem = self._current_element()

        if not elem:
            self._show_msg(
                "No Element",
                "Please select an element.",
                QMessageBox.Icon.Warning
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Regression Data",
            f"regression_{elem}.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            pairs = self._build_pairs_for_element(elem)

            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Sample", "IDC", "Certified"])

                for pair in pairs:
                    writer.writerow([
                        pair["sample"],
                        f"{pair['intensity']:.5f}",
                        f"{pair['chemical']:.5f}",
                    ])

                if elem in self.calculated_coeffs:
                    coeff = self.calculated_coeffs[elem]
                    writer.writerow([])
                    writer.writerow(["a", coeff.get("a", 0.0)])
                    writer.writerow(["b", coeff.get("b", 0.0)])
                    writer.writerow(["c", coeff.get("c", 0.0)])
                    writer.writerow(["d", coeff.get("d", 0.0)])

            self._show_msg("Exported", f"Regression data exported to:\n{path}")

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
    # Messages
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