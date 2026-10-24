import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.matrix_correction_repository import (
    activate_matrix_correction,
    create_matrix_candidate,
    get_active_matrix_corrections,
)
from core.persistence.models import AnalyticalGroup


class MatrixPageUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.factory = sessionmaker(bind=self.engine)
        session = self.factory()
        group = AnalyticalGroup(
            name="STEEL",
            page_03_channel=[
                {"name": "Fe", "ele": "FE"},
                {"name": "C", "ele": "C"},
            ],
        )
        session.add(group)
        session.commit()
        self.group_id = group.id
        session.close()

        import ui.anainf.page_06_matrix as page_module
        self.page_module = page_module
        self.original_session = page_module.get_session
        page_module.get_session = lambda: self.factory()

    def tearDown(self):
        self.page_module.get_session = self.original_session
        self.engine.dispose()

    def test_page6_exposes_version_management_actions(self):
        from ui.anainf.page_06_matrix import CorrectionPage

        self.assertTrue(hasattr(CorrectionPage, "_load_matrix_versions"))
        self.assertTrue(hasattr(CorrectionPage, "_activate_selected_matrix"))
        self.assertTrue(hasattr(CorrectionPage, "_retire_selected_matrix"))

    def test_page6_renders_version_table_and_controls(self):
        from ui.anainf.page_06_matrix import CorrectionPage

        page = CorrectionPage(None, self.group_id, "STEEL")
        self.assertTrue(hasattr(page, "version_table"))
        self.assertTrue(hasattr(page, "activate_button"))
        self.assertTrue(hasattr(page, "retire_button"))

    def test_page6_version_table_shows_point_count_with_fit_statistics(self):
        session = self.factory()
        candidate = create_matrix_candidate(
            session,
            self.group_id,
            "FE",
            "C",
            "L",
            0.2,
            point_count=4,
            fit_stats={"r2": 0.95, "rmse": 0.1},
            version_name="Fe-C L v1",
        )
        activate_matrix_correction(session, candidate.id)
        session.close()

        from ui.anainf.page_06_matrix import CorrectionPage

        page = CorrectionPage(None, self.group_id, "STEEL")
        row_values = [
            page.version_table.item(0, column).text()
            for column in range(page.version_table.columnCount())
        ]
        self.assertIn("4", " ".join(row_values))
        self.assertIn("Fe-C L v1", row_values)

    def test_activation_updates_normalized_status(self):
        session = self.factory()
        first = create_matrix_candidate(session, self.group_id, "FE", "C", "L", 0.1)
        second = create_matrix_candidate(session, self.group_id, "FE", "C", "L", 0.2)
        second_id = second.id
        activate_matrix_correction(session, first.id)
        session.close()

        from ui.anainf.page_06_matrix import CorrectionPage

        page = CorrectionPage(None, self.group_id, "STEEL")
        page._selected_matrix_id = second_id
        page._activate_selected_matrix()

        session = self.factory()
        active = get_active_matrix_corrections(session, self.group_id, "FE")
        self.assertEqual([row.id for row in active], [second_id])
        session.close()

    def test_activation_is_not_undone_by_saving_stale_blank_table(self):
        session = self.factory()
        candidate = create_matrix_candidate(session, self.group_id, "FE", "C", "L", 0.2)
        candidate_id = candidate.id
        session.close()

        from ui.anainf.page_06_matrix import CorrectionPage

        page = CorrectionPage(None, self.group_id, "STEEL")
        page._selected_matrix_id = candidate_id
        page._activate_selected_matrix()
        page._save()

        session = self.factory()
        active = get_active_matrix_corrections(session, self.group_id, "FE")
        self.assertEqual([row.id for row in active], [candidate_id])
        session.close()

    def test_inactive_candidate_does_not_remove_legacy_row_during_sync(self):
        session = self.factory()
        group = session.get(__import__("core.persistence.models", fromlist=["AnalyticalGroup"]).AnalyticalGroup, self.group_id)
        group.page_06_matrix = {
            "corrections": [
                {
                    "target_ar_no": "1",
                    "target_element": "FE",
                    "target_name": "Fe",
                    "type": "L",
                    "interfering_ar_no": "2",
                    "interfering_element": "C",
                    "interfering_name": "C",
                    "coeff": 1.0,
                }
            ]
        }
        candidate = create_matrix_candidate(session, self.group_id, "FE", "C", "L", 0.2)
        candidate_id = candidate.id
        session.commit()
        session.close()

        from ui.anainf.page_06_matrix import CorrectionPage

        page = CorrectionPage(None, self.group_id, "STEEL")
        page._sync_active_json(self.factory())

        session = self.factory()
        group = session.get(__import__("core.persistence.models", fromlist=["AnalyticalGroup"]).AnalyticalGroup, self.group_id)
        self.assertEqual(len(group.page_06_matrix["corrections"]), 1)
        self.assertEqual(group.page_06_matrix["corrections"][0]["coeff"], 1.0)
        self.assertEqual(get_active_matrix_corrections(session, self.group_id), [])
        self.assertEqual(candidate_id, 1)
        session.close()

if __name__ == "__main__":
    unittest.main()
