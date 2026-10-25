import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication


class WorkingCurveRegressionUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_chart_keeps_observed_predicted_and_residual_data(self):
        from ui.regression.working_curve_chart import WorkingCurveChart

        chart = WorkingCurveChart()
        chart.set_points(
            [{"chemical": 1.0, "predicted": 1.1, "residual": -0.1}],
            {"a": 0, "b": 0, "c": 1, "d": 0},
        )

        self.assertEqual(chart.target_line, [(1.0, 1.1)])
        self.assertEqual(chart.residuals, [-0.1])

    def test_page5_has_curve_version_management_controls(self):
        from ui.anainf.page_05_working_curve import WorkingCurvePage

        self.assertTrue(hasattr(WorkingCurvePage, "_load_curve_versions"))
        self.assertTrue(hasattr(WorkingCurvePage, "_activate_selected_curve"))
        self.assertTrue(hasattr(WorkingCurvePage, "_retire_selected_curve"))

    def test_master_curve_page_has_validated_numeric_settings(self):
        from ui.anainf.page_07_master import MasterCurvePage

        self.assertTrue(hasattr(MasterCurvePage, "_validate_rows"))
        self.assertTrue(hasattr(MasterCurvePage, "_normalize_float_text"))


if __name__ == "__main__":
    unittest.main()
