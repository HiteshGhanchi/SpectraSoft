import unittest

from core.analysis.drift_service import (
    DEFAULT_DRIFT_ROW,
    calculate_alpha_beta,
    calculate_k,
    file_target_values,
    normalize_drift_row,
)


class DriftServiceTests(unittest.TestCase):
    def test_default_row_matches_manual_initial_state(self):
        row = normalize_drift_row({"name": "Fe"})

        self.assertEqual(row["name"], "Fe")
        self.assertEqual(row["h_sample"], "")
        self.assertEqual(row["l_sample"], "")
        self.assertEqual(row["k_sample"], "")
        self.assertEqual(row["h_target"], DEFAULT_DRIFT_ROW["h_target"])
        self.assertEqual(row["l_target"], "0.00000")
        self.assertEqual(row["k_target"], "0.00000")
        self.assertEqual(row["alpha"], "1.0000")
        self.assertEqual(row["beta"], "0.00000")
        self.assertEqual(row["k_coeff"], "1.0000")

    def test_file_target_values_updates_only_matching_h_l_k_roles(self):
        rows = [
            {"name": "Fe", "h_sample": "HIGH", "l_sample": "LOW", "k_sample": "CHECK"},
            {"name": "C", "h_sample": "HIGH", "l_sample": "*", "k_sample": ""},
        ]

        updated = file_target_values(rows, "high", {"Fe": 0.75, "C": 0.25})

        self.assertEqual(updated, 2)
        self.assertEqual(rows[0]["h_target"], "0.75000")
        self.assertEqual(rows[1]["h_target"], "0.25000")
        self.assertNotIn("l_target", rows[0])

    def test_alpha_beta_follow_two_point_formula(self):
        alpha, beta = calculate_alpha_beta(
            h_target=0.9,
            l_target=0.3,
            h_intensity=0.8,
            l_intensity=0.2,
        )

        self.assertAlmostEqual(alpha, 1.0)
        self.assertAlmostEqual(beta, 0.1)

    def test_alpha_beta_reject_equal_measurements(self):
        with self.assertRaises(ValueError):
            calculate_alpha_beta(0.9, 0.3, 0.5, 0.5)

    def test_k_follows_one_point_formula(self):
        self.assertAlmostEqual(calculate_k(0.8, 0.5, 1.0, 0.1), 1.3333333333)

    def test_k_rejects_zero_corrected_intensity(self):
        with self.assertRaises(ValueError):
            calculate_k(0.8, 0.0, 1.0, 0.0)


if __name__ == "__main__":
    unittest.main()
