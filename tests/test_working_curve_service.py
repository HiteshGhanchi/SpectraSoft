import unittest

from core.analysis.working_curve_service import (
    build_calibration_pairs,
    fit_polynomial,
)
from core.analysis.correction_engine import CorrectionEngine


class WorkingCurveServiceTests(unittest.TestCase):
    def test_build_pairs_matches_measurements_to_known_values(self):
        pairs = build_calibration_pairs(
            [{"sample": "STD_1", "intensities": {"C": 0.1}}],
            [{"sample": "STD_1", "values": {"C": 0.2}}],
            "C",
        )

        self.assertEqual(pairs, [{"sample": "STD_1", "intensity": 0.1, "chemical": 0.2}])

    def test_linear_fit_returns_coefficients_and_quality(self):
        result = fit_polynomial(
            [{"intensity": 0.0, "chemical": 1.0}, {"intensity": 1.0, "chemical": 3.0}],
            1,
        )

        self.assertAlmostEqual(result["coefficients"]["c"], 2.0, places=5)
        self.assertAlmostEqual(result["coefficients"]["d"], 1.0, places=5)
        self.assertAlmostEqual(result["r2"], 1.0, places=5)
        self.assertAlmostEqual(result["rmse"], 0.0, places=5)

    def test_fit_requires_degree_plus_one_points(self):
        with self.assertRaises(ValueError):
            fit_polynomial([{"intensity": 0.0, "chemical": 1.0}], 2)

    def test_correction_prefers_normalized_active_coefficients(self):
        engine = CorrectionEngine(
            {
                "page_05_active_coefficients": {
                    "FE": {"a": 0, "b": 0, "c": 3, "d": 1}
                },
                "page_05_wc": {
                    "coefficients": [{"element": "Fe", "a": 0, "b": 0, "c": 2, "d": 0}]
                },
            }
        )

        self.assertEqual(engine.apply_working_curve({"Fe": 2})["Fe"], 7)

    def test_correction_merges_normalized_and_legacy_coefficients_per_element(self):
        engine = CorrectionEngine(
            {
                "page_05_active_coefficients": {"FE": {"a": 0, "b": 0, "c": 3, "d": 1}},
                "page_05_wc": {"coefficients": [{"element": "SI", "a": 0, "b": 0, "c": 4, "d": 0}]},
            }
        )

        self.assertEqual(engine.apply_working_curve({"Fe": 2, "Si": 2}), {"Fe": 7, "Si": 8})


if __name__ == "__main__":
    unittest.main()
