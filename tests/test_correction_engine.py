import unittest

from core.analysis.correction_engine import CorrectionEngine


class CorrectionEngineTests(unittest.TestCase):
    def test_full_pipeline_applies_each_registered_stage(self):
        group_data = {
            "page_04_drift": {
                "rows": [{"name": "Fe", "alpha": "2", "beta": "1", "k_coeff": "0.5"}]
            },
            "page_05_wc": {
                "coefficients": [{"element": "Fe", "a": "0", "b": "0", "c": "2", "d": "0"}]
            },
            "page_06_matrix": {
                "corrections": [
                    {"target_name": "Fe", "interfering_name": "C", "type": "L", "coeff": "1"},
                    {"target_name": "Fe", "interfering_name": "Si", "type": "D", "coeff": "0.1"},
                ]
            },
            "page_07_master": {
                "rows": [{"name": "Fe", "mc": "2", "ac": "1"}]
            },
            "page_09_purity": {
                "calculation": "Y",
                "rows": [{"name": "Fe", "mark": "+"}, {"name": "C", "mark": "-"}],
            },
        }

        result = CorrectionEngine(group_data).apply_all({"Fe": 3, "C": 2, "Si": 1})

        # Fe: drift 3 -> 3.5, WC -> 7, matrix -> 9.9, master -> 20.8,
        # then purity balance replaces Fe with 100 - C.
        self.assertAlmostEqual(result["Fe"], 98.0)
        self.assertEqual(result["C"], 2)
        self.assertEqual(result["Si"], 1)

    def test_display_order_uses_page_eight_when_orders_are_configured(self):
        engine = CorrectionEngine(
            {
                "page_08_display": {
                    "rows": [
                        {"name": "Si", "order": 2, "deci": 2, "magn": 0},
                        {"name": "Fe", "order": 1, "deci": 1, "magn": 0},
                    ]
                }
            }
        )

        ordered = engine.order_for_display({"Fe": 12.34, "Si": 5.678})

        self.assertEqual([row["name"] for row in ordered], ["Fe", "Si"])
        self.assertEqual([row["formatted"] for row in ordered], ["12.3", "5.68"])

    def test_normalized_matrix_rows_override_matching_legacy_rows(self):
        engine = CorrectionEngine(
            {
                "page_06_matrix": {
                    "corrections": [
                        {"target_name": "Fe", "interfering_name": "C", "type": "L", "coeff": 1.0},
                    ]
                },
                "page_06_active_corrections": [
                    {"target_element_key": "FE", "interfering_element_key": "C", "correction_type": "L", "coefficient": 2.0},
                ],
            }
        )

        self.assertEqual(engine.apply_matrix({"Fe": 10.0, "C": 3.0})["Fe"], 16.0)

    def test_normalized_rows_suppress_matching_legacy_rows_and_keep_other_legacy_rows(self):
        engine = CorrectionEngine(
            {
                "page_06_matrix": {
                    "corrections": [
                        {"target_name": "Fe", "interfering_name": "C", "type": "L", "coeff": 1.0},
                        {"target_name": "Fe", "interfering_name": "Si", "type": "D", "coeff": 0.1},
                    ]
                },
                "page_06_active_corrections": [
                    {"target_element_key": "FE", "interfering_element_key": "C", "correction_type": "L", "coefficient": 2.0},
                ],
            }
        )

        result = engine.apply_matrix({"Fe": 10.0, "C": 3.0, "Si": 1.0})
        self.assertAlmostEqual(result["Fe"], 16.0 * 1.1)

    def test_multiple_normalized_rows_apply_l_before_d_using_original_values(self):
        engine = CorrectionEngine(
            {
                "page_06_active_corrections": [
                    {"target_element_key": "FE", "interfering_element_key": "C", "correction_type": "L", "coefficient": 1.0},
                    {"target_element_key": "FE", "interfering_element_key": "SI", "correction_type": "D", "coefficient": 0.1},
                ]
            }
        )

        self.assertAlmostEqual(
            engine.apply_matrix({"Fe": 10.0, "C": 2.0, "Si": 3.0})["Fe"],
            12.0 * 1.3,
        )

    def test_retired_normalized_key_suppresses_matching_legacy_row(self):
        engine = CorrectionEngine(
            {
                "page_06_matrix": {
                    "corrections": [
                        {"target_name": "Fe", "interfering_name": "C", "type": "L", "coeff": 1.0},
                    ]
                },
                "page_06_active_corrections": [],
                "page_06_authoritative_keys": [["FE", "C", "L"]],
            }
        )

        self.assertEqual(engine.apply_matrix({"Fe": 10.0, "C": 3.0})["Fe"], 10.0)

    def test_matrix_uses_page3_ele_when_runtime_uses_display_name(self):
        engine = CorrectionEngine(
            {
                "page_03_channel": [
                    {"name": "Iron", "ele": "FE"},
                    {"name": "Carbon", "ele": "C"},
                ],
                "page_06_active_corrections": [
                    {"target_element_key": "FE", "interfering_element_key": "C", "correction_type": "L", "coefficient": 2.0},
                ],
            }
        )

        self.assertEqual(engine.apply_matrix({"Iron": 10.0, "Carbon": 3.0})["Iron"], 16.0)

    def test_inactive_matrix_candidate_does_not_suppress_legacy_correction(self):
        engine = CorrectionEngine(
            {
                "page_06_matrix": {
                    "corrections": [
                        {"target_element": "FE", "interfering_element": "C", "type": "L", "coeff": 1.0},
                    ]
                },
                "page_06_active_corrections": [],
                "page_06_authoritative_keys": [],
            }
        )

        self.assertEqual(engine.apply_matrix({"FE": 10.0, "C": 3.0})["FE"], 13.0)

    def test_legacy_display_name_is_canonicalized_for_target_grouping(self):
        engine = CorrectionEngine(
            {
                "page_03_channel": [
                    {"name": "Iron", "ele": "FE"},
                    {"name": "Carbon", "ele": "C"},
                ],
                "page_06_matrix": {
                    "corrections": [
                        {"target_name": "Iron", "interfering_name": "Carbon", "type": "L", "coeff": 2.0},
                    ]
                },
            }
        )

        self.assertEqual(engine.apply_matrix({"Iron": 10.0, "Carbon": 3.0})["Iron"], 16.0)


if __name__ == "__main__":
    unittest.main()
