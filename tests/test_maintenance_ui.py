import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.maintenance.models import MaintenanceJournalEntry
from core.maintenance.service import MaintenanceService
from core.persistence.database import Base


class MaintenanceUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine, tables=[MaintenanceJournalEntry.__table__])
        self.session_factory = sessionmaker(bind=self.engine)
        self.temp_dir = TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "live.db"
        self.database.touch()

    def tearDown(self):
        self.temp_dir.cleanup()
        self.engine.dispose()

    def test_unverified_hardware_actions_are_disabled_with_reason(self):
        from ui.maintenance.maintenance_page import MaintenancePage

        service = MaintenanceService(self.session_factory)
        page = MaintenancePage(service, database_path=self.database)

        for operation in service.OPERATIONS:
            button = page.operation_buttons[operation]
            self.assertFalse(button.isEnabled())
            self.assertIn("not available", button.toolTip().lower())

    def test_legacy_clock_is_not_shown_and_portable_package_controls_exist(self):
        from ui.maintenance.maintenance_page import MaintenancePage

        service = MaintenanceService(self.session_factory)
        page = MaintenancePage(service, database_path=self.database)

        self.assertFalse(hasattr(page, "clock_label"))
        self.assertFalse(any(label.text() == "OS clock:" for label in page.findChildren(type(page.status_label))))
        self.assertTrue(hasattr(page, "export_package_path_edit"))
        self.assertTrue(hasattr(page, "import_package_path_edit"))

    def test_restore_requires_confirmation_dialog_before_mutation(self):
        from ui.maintenance.maintenance_page import MaintenancePage

        service = MaintenanceService(self.session_factory)
        page = MaintenancePage(service, database_path=self.database)
        page.restore_path_edit.setText(str(self.database))
        page._restore_source = self.database

        with patch("ui.maintenance.maintenance_page.QMessageBox.question", return_value=page._no_button):
            page._on_restore()

        self.assertIn("confirmation", page.status_label.text().lower())

    def test_manual_completion_action_persists_operator_confirmed_entry(self):
        from ui.maintenance.maintenance_page import MaintenancePage

        service = MaintenanceService(self.session_factory)
        page = MaintenancePage(service, database_path=self.database)
        page.manual_operation_combo.setCurrentText("Waste Discharge")
        page.operator_edit.setText("Operator")
        page.notes_edit.setPlainText("Observed and completed on instrument")

        page._on_record_manual()

        with self.session_factory() as session:
            entry = session.query(MaintenanceJournalEntry).one()
            self.assertEqual(entry.completion_mode, "manual_confirmed")
            self.assertFalse(entry.hardware_performed)
        self.assertIn("recorded", page.status_label.text().lower())


if __name__ == "__main__":
    unittest.main()
