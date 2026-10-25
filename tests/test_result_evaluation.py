import unittest

from core.analysis.result_evaluation import evaluate_element_flags, evaluate_r_control


class ResultEvaluationTests(unittest.TestCase):
    def test_product_limits_create_high_low_trace_and_ok_flags(self):
        specs = {
            "FE": {"lower": 8.0, "upper": 12.0, "trace": 0.5},
            "C": {"lower": 0.0, "upper": 2.0, "trace": 0.1},
        }
        flags = evaluate_element_flags({"FE": 13.0, "C": 0.05}, specs)
        self.assertEqual(flags, {"FE": "H", "C": "Tr"})

    def test_r_control_uses_quadratic_width_and_reports_out_of_control(self):
        settings = {"FE": {"a": 0.0, "b": 0.1, "c": 0.1}}
        self.assertEqual(evaluate_r_control({"FE": [10.0, 10.2]}, settings)["FE"], "OK")
        self.assertEqual(evaluate_r_control({"FE": [10.0, 12.0]}, settings)["FE"], "R")


if __name__ == "__main__":
    unittest.main()
