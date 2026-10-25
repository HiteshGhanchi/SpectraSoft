import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup


class ResultSettingsUITests(unittest.TestCase):
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
        session.close()

        import ui.anainf.page_10_result_settings as module
        self.module = module
        self.original_session = module.get_session
        module.get_session = lambda: self.factory()

    def tearDown(self):
        self.module.get_session = self.original_session
        self.engine.dispose()

    def test_page_exposes_product_r_control_and_optional_tabs(self):
        page = self.module.ResultSettingsPage(None, self.group_id, "STEEL")
        labels = [page.tabs.tabText(i) for i in range(page.tabs.count())]
        self.assertEqual(labels, ["Product Specifications", "R Control", "Optional Calculations"])


if __name__ == "__main__":
    unittest.main()
