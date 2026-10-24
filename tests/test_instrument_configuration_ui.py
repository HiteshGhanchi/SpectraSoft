import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication


class InstrumentConfigurationUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_configuration_page_exposes_both_emission_units(self):
        from ui.settings.instrument_configuration_page import InstrumentConfigurationPage

        session = Mock()
        session_config = Mock(emission_unit_type="HVS")
        session.get.return_value = session_config

        with patch(
            "ui.settings.instrument_configuration_page.get_session",
            return_value=session,
        ), patch(
            "ui.settings.instrument_configuration_page.get_or_create_instrument_configuration",
            return_value=session_config,
        ):
            page = InstrumentConfigurationPage(Mock())

        self.assertEqual(
            [page.emission_unit_combo.itemData(i) for i in range(page.emission_unit_combo.count())],
            ["HPSG_300", "HVS"],
        )
        self.assertEqual(page.emission_unit_combo.currentData(), "HVS")
        self.assertIn("color:#000000", page.emission_unit_combo.styleSheet())
        self.assertEqual(page.available_units_label.text(), "Available: HPSG-300 and HVS")

    def test_main_window_opens_instrument_configuration_without_group(self):
        from ui.main_window import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.action_instrument_configuration = Mock()
        main_window._set_active_menu = Mock()
        main_window.set_right_widget = Mock()

        with patch("ui.settings.instrument_configuration_page.InstrumentConfigurationPage") as page:
            MainWindow._open_instrument_configuration(main_window)

        page.assert_called_once_with(main_window)
        main_window.set_right_widget.assert_called_once_with(page.return_value)

    def test_configuration_page_saves_selected_emission_unit(self):
        from ui.settings.instrument_configuration_page import InstrumentConfigurationPage

        session = Mock()
        session.get.return_value = Mock(emission_unit_type="HPSG_300")
        saved_config = Mock(emission_unit_type="HVS")

        with patch(
            "ui.settings.instrument_configuration_page.get_session",
            return_value=session,
        ), patch(
            "ui.settings.instrument_configuration_page.get_or_create_instrument_configuration",
            return_value=session.get.return_value,
        ), patch(
            "ui.settings.instrument_configuration_page.set_emission_unit_type",
            return_value=saved_config,
        ) as set_type, patch(
            "ui.settings.instrument_configuration_page.QMessageBox.information"
        ):
            page = InstrumentConfigurationPage(Mock())
            page.emission_unit_combo.setCurrentIndex(1)
            page._on_save()

        set_type.assert_called_once_with(session, "HVS")


if __name__ == "__main__":
    unittest.main()
