import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication


class DriftJobTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_job8_table_displays_element_average(self):
        from ui.analysis.analysis_run_job8 import Job8RunPage

        page = Job8RunPage.__new__(Job8RunPage)
        page.element_names = ["Fe"]
        page.results = [{"Fe": 0.75}]
        page.table = __import__("PyQt6.QtWidgets", fromlist=["QTableWidget"]).QTableWidget()

        page._update_table()

        self.assertEqual(page.table.item(0, 1).text(), "0.75000")

    def test_job3_table_displays_element_average(self):
        from ui.analysis.analysis_run_job3 import Job3RecalPage

        page = Job3RecalPage.__new__(Job3RecalPage)
        page.element_names = ["Fe"]
        page.results = [{"Fe": 0.75}]
        page.table = __import__("PyQt6.QtWidgets", fromlist=["QTableWidget"]).QTableWidget()

        page._update_table()

        self.assertEqual(page.table.item(0, 1).text(), "0.75000")

    def test_job2_table_displays_element_average(self):
        from ui.analysis.analysis_run_job2 import Job2RecalPage

        page = Job2RecalPage.__new__(Job2RecalPage)
        page.element_names = ["Fe"]
        page.results = [{"Fe": 0.75}]
        page.table = __import__("PyQt6.QtWidgets", fromlist=["QTableWidget"]).QTableWidget()

        page._update_table()

        self.assertEqual(page.table.item(0, 1).text(), "0.75000")


if __name__ == "__main__":
    unittest.main()
