"""
SpectraSoft — Correction Engine

Applies the full SpectraSoft correction chain:

1. Page 4 Drift Correction
       I_DC = k * (alpha * I + beta)

2. Page 5 Working Curve
       C0 = a*I_DC^3 + b*I_DC^2 + c*I_DC + d

3. Page 6 Matrix Correction
       L type:
           C = C0 + sum(lj * Cj)

       D type:
           C = C0 * (1 + sum(dj * Cj))

4. Page 7 Master Curve Correction
       C = (C * MC) + AC

5. Page 9 Purity Calculation
       C_base = 100 - sum(C_impurities)

All data is read from the selected Analytical Group.
"""


class CorrectionEngine:
    def __init__(self, group_data: dict):
        self.group_data = group_data or {}

    # =========================================================================
    # Full Pipeline
    # =========================================================================

    def apply_all(self, intensities: dict) -> dict:
        """
        Apply full content-analysis correction chain.

        Input:
            pre-correction intensities

        Output:
            final corrected concentrations
        """
        drifted = self.apply_drift(intensities)
        content = self.apply_working_curve(drifted)
        matrix_corrected = self.apply_matrix(content)
        master_corrected = self.apply_master(matrix_corrected)
        purity_corrected = self.apply_purity(master_corrected)

        return purity_corrected

    # =========================================================================
    # Page 4: Drift Correction
    # =========================================================================

    def apply_drift(self, intensities: dict) -> dict:
        """
        Apply Page 4 drift correction per element.

        Formula:
            I_DC = k * (alpha * I + beta)

        If an element has no Page 4 row, neutral correction is used.
        """
        drift_rows = self._get_page4_drift_rows()
        corrected = {}

        for elem_name, intensity in intensities.items():
            lookup_key = self._key(elem_name)
            row = drift_rows.get(lookup_key)

            i_value = self._to_float(intensity, 0.0)

            if not row:
                corrected[elem_name] = i_value
                continue

            alpha = self._to_float(row.get("alpha", ""), 1.0)
            beta = self._to_float(row.get("beta", ""), 0.0)
            k_coeff = self._to_float(row.get("k_coeff", ""), 1.0)

            corrected[elem_name] = k_coeff * ((alpha * i_value) + beta)

        return corrected

    def _get_page4_drift_rows(self) -> dict:
        """
        Build lookup:
            ELEMENT_NAME_UPPER -> Page 4 row
        """
        page4 = self.group_data.get("page_04_drift", {})

        if not isinstance(page4, dict):
            return {}

        rows = page4.get("rows", [])

        if not isinstance(rows, list):
            return {}

        lookup = {}

        for row in rows:
            name = str(row.get("name", "")).strip()

            if name:
                lookup[self._key(name)] = row

        return lookup

    # =========================================================================
    # Page 5: Working Curve
    # =========================================================================

    def apply_working_curve(self, intensities: dict) -> dict:
        """
        Apply Page 5 working curve.

        Formula:
            C = a*I^3 + b*I^2 + c*I + d

        This should be used after drift correction.
        """
        coeffs = self._get_page5_coefficients()
        results = {}

        for elem_name, intensity in intensities.items():
            lookup_key = self._key(elem_name)
            coeff = coeffs.get(lookup_key, {})

            a = self._to_float(coeff.get("a", 0.0), 0.0)
            b = self._to_float(coeff.get("b", 0.0), 0.0)
            c = self._to_float(coeff.get("c", 1.0), 1.0)
            d = self._to_float(coeff.get("d", 0.0), 0.0)

            i_value = self._to_float(intensity, 0.0)

            results[elem_name] = (
                a * (i_value ** 3) +
                b * (i_value ** 2) +
                c * i_value +
                d
            )

        return results

    def _get_page5_coefficients(self) -> dict:
        """
        Build lookup:
            ELEMENT_NAME_UPPER -> Page 5 coefficient row
        """
        page5 = self.group_data.get("page_05_wc", {})

        if not isinstance(page5, dict):
            return {}

        rows = page5.get("coefficients", [])

        if not isinstance(rows, list):
            return {}

        lookup = {}

        for row in rows:
            for key in ["element", "name", "ele"]:
                value = str(row.get(key, "")).strip()

                if value:
                    lookup[self._key(value)] = row

        return lookup

    # =========================================================================
    # Page 6: Matrix Correction
    # =========================================================================

    def apply_matrix(self, concentrations: dict) -> dict:
        """
        Apply Page 6 matrix correction.

        L = additive / overlap correction:
            C = C0 + Σ(lj * Cj)

        D = multiplicative / matrix correction:
            C = C0 * (1 + Σ(dj * Cj))
        """

        corrections = self._get_page6_corrections()

        if not corrections:
            return dict(concentrations)

        original = dict(concentrations)
        corrected = dict(concentrations)

        # Group correction rows by target element
        grouped = {}

        for row in corrections:
            target = self._key(
                row.get("target_name")
                or row.get("target_element")
                or ""
            )

            if not target:
                continue

            grouped.setdefault(target, []).append(row)

        # Apply corrections
        for elem_name, c0 in original.items():
            target_key = self._key(elem_name)

            if target_key not in grouped:
                corrected[elem_name] = c0
                continue

            base_value = self._to_float(c0, 0.0)

            l_sum = 0.0
            d_sum = 0.0

            # Iterate through all correction rows for this target
            for row in grouped[target_key]:
                corr_type = str(row.get("type", "")).strip().upper()
                coeff = self._to_float(row.get("coeff", 0.0), 0.0)

                interfering_key = self._key(
                    row.get("interfering_name")
                    or row.get("interfering_element")
                    or ""
                )

                if not interfering_key:
                    continue

                interfering_value = self._get_value_case_insensitive(
                    original,
                    interfering_key,
                    0.0
                )

                if corr_type == "L":
                    l_sum += coeff * interfering_value

                elif corr_type == "D":
                    d_sum += coeff * interfering_value

            # Apply L correction first, then D correction
            after_l = base_value + l_sum
            after_d = after_l * (1.0 + d_sum)

            corrected[elem_name] = after_d

        return corrected

    def _get_page6_corrections(self) -> list:
        page6 = self.group_data.get("page_06_matrix", {})

        if not isinstance(page6, dict):
            return []

        corrections = page6.get("corrections", [])

        if not isinstance(corrections, list):
            return []

        return corrections

    # =========================================================================
    # Page 7: Master Curve Correction
    # =========================================================================

    def apply_master(self, concentrations: dict) -> dict:
        """
        Apply Page 7 master curve / y-correction.

        Formula:
            C_master = (C * MC) + AC

        Defaults:
            MC = 1.0000
            AC = 0.00000
        """
        master_rows = self._get_page7_master_rows()

        if not master_rows:
            return dict(concentrations)

        corrected = {}

        for elem_name, value in concentrations.items():
            row = master_rows.get(self._key(elem_name))

            c_value = self._to_float(value, 0.0)

            if not row:
                corrected[elem_name] = c_value
                continue

            ac = self._to_float(row.get("ac", ""), 0.0)
            mc = self._to_float(row.get("mc", ""), 1.0)

            corrected[elem_name] = (c_value * mc) + ac

        return corrected

    def _get_page7_master_rows(self) -> dict:
        """
        Build lookup:
            ELEMENT_NAME_UPPER -> Page 7 row
        """
        page7 = self.group_data.get("page_07_master", {})

        if not isinstance(page7, dict):
            return {}

        rows = page7.get("rows", [])

        if not isinstance(rows, list):
            return {}

        lookup = {}

        for row in rows:
            name = str(row.get("name", "")).strip()

            if name:
                lookup[self._key(name)] = row

        return lookup

    # =========================================================================
    # Page 9: Purity Calculation
    # =========================================================================

    def apply_purity(self, concentrations: dict) -> dict:
        """
        Apply purity / balance calculation.

        Schema:
            AnalyticalGroup.page_09_purity

        Logic:
            calculation = "Y" enables purity calculation.

            mark:
                "+" = base element to calculate by balance
                "-" = impurity element to subtract from 100
                ""  = ignored

        Formula:
            C_base = 100 - sum(C_impurities)

        If calculation is N or setup is invalid, concentrations are returned unchanged.
        """
        purity = self.group_data.get("page_09_purity", {})

        if not isinstance(purity, dict):
            return dict(concentrations)

        calculation = str(purity.get("calculation", "N")).strip().upper()

        if calculation != "Y":
            return dict(concentrations)

        rows = purity.get("rows", [])

        if not isinstance(rows, list):
            return dict(concentrations)

        base_elements = []
        impurity_elements = []

        for row in rows:
            name = str(row.get("name", "")).strip()
            mark = str(row.get("mark", "")).strip()

            if not name:
                continue

            if mark == "+":
                base_elements.append(name)

            elif mark == "-":
                impurity_elements.append(name)

        # Require exactly one base element.
        if len(base_elements) != 1:
            return dict(concentrations)

        base_name = base_elements[0]

        impurity_sum = 0.0

        for elem in impurity_elements:
            impurity_sum += self._get_value_case_insensitive(
                concentrations,
                self._key(elem),
                0.0
            )

        base_value = 100.0 - impurity_sum

        corrected = dict(concentrations)

        # Preserve original key style if base already exists.
        base_existing_key = self._find_existing_key(
            corrected,
            self._key(base_name)
        )

        if base_existing_key:
            corrected[base_existing_key] = base_value
        else:
            corrected[base_name] = base_value

        return corrected

    # =========================================================================
    # Formatting Helpers for Page 8
    # =========================================================================

    def get_display_order_rows(self) -> list:
        """
        Return Page 8 display rows.

        Job X can use this to decide final element order/format.

        If no Page 8 rows exist, returns [].
        """
        page8 = self.group_data.get("page_08_display", {})

        if not isinstance(page8, dict):
            return []

        rows = page8.get("rows", [])

        if not isinstance(rows, list):
            return []

        return rows

    def order_for_display(self, concentrations: dict) -> list:
        """
        Return ordered list of:
            [
                {
                    "name": element_name,
                    "value": concentration,
                    "formatted": text,
                    "order": order,
                    "fig": fig,
                    "deci": deci,
                    "magn": magn
                }
            ]

        Rule:
        - If any Page 8 ORDER > 0:
            show only ORDER > 0, sorted by ORDER.
        - If all ORDER values are 0 or Page 8 missing:
            show all concentrations in input order.
        """
        rows = self.get_display_order_rows()

        if not rows:
            return [
                {
                    "name": elem,
                    "value": value,
                    "formatted": self.format_value(value),
                    "order": 0,
                    "fig": 0,
                    "deci": 0,
                    "magn": 0,
                }
                for elem, value in concentrations.items()
            ]

        page8_lookup = {}

        for row in rows:
            name = str(row.get("name", "")).strip()

            if name:
                page8_lookup[self._key(name)] = row

        any_order = False

        for row in rows:
            order = self._to_int(row.get("order", 0), 0)

            if order > 0:
                any_order = True
                break

        output = []

        for elem, value in concentrations.items():
            row = page8_lookup.get(self._key(elem), {})

            order = self._to_int(row.get("order", 0), 0)
            fig = self._to_int(row.get("fig", 0), 0)
            deci = self._to_int(row.get("deci", 0), 0)
            magn = self._to_int(row.get("magn", 0), 0)

            if any_order and order <= 0:
                continue

            output.append({
                "name": elem,
                "value": value,
                "formatted": self.format_value(value, deci=deci, magn=magn),
                "order": order,
                "fig": fig,
                "deci": deci,
                "magn": magn,
            })

        if any_order:
            output.sort(key=lambda x: x["order"])

        return output

    @staticmethod
    def format_value(value, deci: int = 0, magn: int = 0) -> str:
        """
        Format analytical result using Page 8 rules.

        - Apply display multiplier:
              displayed = value * (10 ** magn)

        - If deci > 0:
              fixed decimal places

        - If deci == 0:
              default floating precision
        """
        try:
            val = float(value)
        except (TypeError, ValueError):
            val = 0.0

        try:
            d = int(deci)
        except (TypeError, ValueError):
            d = 0

        try:
            m = int(magn)
        except (TypeError, ValueError):
            m = 0

        displayed = val * (10 ** m)

        if d > 0:
            return f"{displayed:.{d}f}"

        return f"{displayed:.6g}"

    # =========================================================================
    # Shared Helpers
    # =========================================================================

    def _key(self, value) -> str:
        return str(value or "").strip().upper()

    def _to_float(self, value, default: float = 0.0) -> float:
        try:
            text = str(value).strip()

            if text == "":
                return default

            return float(text)

        except (TypeError, ValueError):
            return default

    def _to_int(self, value, default: int = 0) -> int:
        try:
            text = str(value).strip()

            if text == "":
                return default

            return int(float(text))

        except (TypeError, ValueError):
            return default

    def _find_existing_key(self, data: dict, lookup_key: str):
        for key in data.keys():
            if self._key(key) == lookup_key:
                return key

        return None

    def _get_value_case_insensitive(
        self,
        data: dict,
        lookup_key: str,
        default: float = 0.0
    ) -> float:
        existing_key = self._find_existing_key(data, lookup_key)

        if existing_key is None:
            return default

        return self._to_float(data.get(existing_key), default)