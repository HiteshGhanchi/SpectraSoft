"""
SpectraSoft — Correction Engine

Applies drift correction, working curve, matrix, master, and purity.

Drift correction uses Page 4 row-wise coefficients:

    I_DC = k * (α * I + β)

Where:
    I    = pre-correction intensity from Job 5/8/2/3 pipeline
    α    = alpha from Page 4 for that element
    β    = beta from Page 4 for that element
    k    = k_coeff from Page 4 for that element
    I_DC = drift-corrected intensity
"""


class CorrectionEngine:
    def __init__(self, group_data: dict):
        self.group_data = group_data or {}

    # =========================================================================
    # Drift Correction
    # =========================================================================

    def apply_drift(self, intensities: dict) -> dict:
        """
        Apply Page 4 drift correction per element.

        Formula:
            I_DC = k * (alpha * I + beta)

        Args:
            intensities:
                Dict of pre-correction intensities:
                {
                    "C": 95.911,
                    "Si": 85.398,
                    ...
                }

        Returns:
            Dict of drift-corrected intensities:
                {
                    "C": corrected_value,
                    "Si": corrected_value,
                    ...
                }

        Notes:
        - If an element has no Page 4 row, neutral correction is used.
        - If alpha/beta/k are blank or invalid, neutral defaults are used.
        - Rows marked H/L/K="*" still apply neutral coefficients if those
          coefficients are saved as default.
        """
        drift_rows = self._get_page4_drift_rows()

        corrected = {}

        for elem_name, intensity in intensities.items():
            row = drift_rows.get(elem_name)

            try:
                i_value = float(intensity)
            except (TypeError, ValueError):
                i_value = 0.0

            if not row:
                # No Page 4 row found. Use no correction.
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
            element_name -> Page 4 row
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
                lookup[name] = row

        return lookup

    def _to_float(self, value, default: float = 0.0) -> float:
        try:
            text = str(value).strip()

            if text == "":
                return default

            return float(text)

        except (TypeError, ValueError):
            return default

    # =========================================================================
    # Working Curve
    # =========================================================================

    def apply_working_curve(self, intensities: dict) -> dict:
        """
        Apply working curve:

            C = a*I³ + b*I² + c*I + d

        This should be used after drift correction.
        """
        wc = self.group_data.get("page_05_wc", {})

        if not isinstance(wc, dict):
            return intensities

        coeffs = {}

        for entry in wc.get("coefficients", []):
            element = str(entry.get("element", "")).strip()

            if element:
                coeffs[element] = entry

        results = {}

        for elem_name, intensity in intensities.items():
            coeff = coeffs.get(elem_name, {})

            a = self._to_float(coeff.get("a", 0.0), 0.0)
            b = self._to_float(coeff.get("b", 0.0), 0.0)
            c = self._to_float(coeff.get("c", 1.0), 1.0)
            d = self._to_float(coeff.get("d", 0.0), 0.0)

            try:
                i_value = float(intensity)
            except (TypeError, ValueError):
                i_value = 0.0

            results[elem_name] = (
                a * (i_value ** 3) +
                b * (i_value ** 2) +
                c * i_value +
                d
            )

        return results

    # =========================================================================
    # Future Corrections
    # =========================================================================

    def apply_matrix(self, concentrations: dict) -> dict:
        """
        Apply matrix corrections.

        TODO:
        Use future page_06_matrix data.
        """
        return concentrations

    def apply_master(self, concentrations: dict) -> dict:
        """
        Apply master curve correction.

        TODO:
        Use future page_07_master data.
        """
        return concentrations

    def apply_purity(self, concentrations: dict) -> dict:
        """
        Calculate purity.

        TODO:
        Use future page_09_purity data.
        """
        return concentrations