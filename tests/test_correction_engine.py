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


if __name__ == "__main__":
    unittest.main()
