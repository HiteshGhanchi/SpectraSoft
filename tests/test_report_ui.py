import os
import unittest
from datetime import datetime

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup
from core.persistence.result_repository import file_analysis_result


class ReportPageUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.factory = sessionmaker(bind=self.engine)
        session = self.factory()
        group = AnalyticalGroup(name="STEEL")
        session.add(group)
        session.commit()
        self.group_id = group.id
        result = file_analysis_result(
            session,
            self.group_id,
            "X",
            "SAMPLE-1",
            [{"FE": 10.0}],
            {"FE": 10.0},
            {"FE": 10.0},
            {"FE": "OK"},
            {"product_name": "P-1", "method": "v1"},
        )
        result.occurred_at = datetime(2026, 1, 1, 8)
        session.commit()
        session.close()

        import ui.report.result_report_page as page_module
        self.page_module = page_module
        self.original_session = page_module.get_session
        page_module.get_session = lambda: self.factory()

    def tearDown(self):
        self.page_module.get_session = self.original_session
        self.engine.dispose()

    def test_page_loads_real_rows_and_exposes_all_report_modes(self):
        page = self.page_module.ResultReportPage(None, self.group_id, "STEEL")
        self.assertEqual(page.table.rowCount(), 1)
        self.assertIn("Daily by group", [page.mode_combo.itemText(i) for i in range(page.mode_combo.count())])
        self.assertIn("Long-term X-R", [page.mode_combo.itemText(i) for i in range(page.mode_combo.count())])
        self.assertIn("Histogram", [page.mode_combo.itemText(i) for i in range(page.mode_combo.count())])
        self.assertIn("SAMPLE-1", page.table.item(0, 2).text())

    def test_filters_and_detail_show_stored_burns_method_and_flags(self):
        page = self.page_module.ResultReportPage(None, self.group_id, "STEEL")
        page.sample_edit.setText("SAMPLE-1")
        page.refresh_button.click()
        self.assertEqual(page.table.rowCount(), 1)
        page.table.selectRow(0)
        self.assertIn("Burns", page.detail_label.text())
        self.assertIn("method", page.detail_label.text())
        self.assertIn("OK", page.detail_label.text())

    def test_csv_and_print_actions_are_wired(self):
        page = self.page_module.ResultReportPage(None, self.group_id, "STEEL")
        self.assertTrue(page.export_button.isEnabled())
        self.assertTrue(page.print_button.isEnabled())
        self.assertTrue(hasattr(page, "_on_print_preview"))
        self.assertIn("correction", page.modification_note.text().lower())

    def test_histogram_mode_accepts_limits_and_exposes_capability_statistics(self):
        page = self.page_module.ResultReportPage(None, self.group_id, "STEEL")
        page.lower_limit_edit.setText("0")
        page.upper_limit_edit.setText("20")
        page.mode_combo.setCurrentText("Histogram")
        self.assertIn("Cp=", page.table.item(0, 4).text())
        self.assertIn("Cpk=", page.table.item(0, 4).text())


if __name__ == "__main__":
    unittest.main()
