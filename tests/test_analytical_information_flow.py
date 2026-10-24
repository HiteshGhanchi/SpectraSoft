import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from ui.anainf.page_02_attenuator import ordered_selected_elements
from ui.anainf.page_03_channel import (
    selected_itg_numbers,
    validate_channel_data,
)


class AnalyticalInformationFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_empty_channel_selection_is_invalid(self):
        valid, message = validate_channel_data([])

        self.assertFalse(valid)
        self.assertIn("at least one", message.lower())

    def test_selected_channel_requires_a_valid_sequence(self):
        valid, message = validate_channel_data([{"itg": "4", "seq": ""}])

        self.assertFalse(valid)
        self.assertIn("seq", message.lower())

    def test_duplicate_channels_are_invalid(self):
        valid, message = validate_channel_data(
            [
                {"itg": "4", "seq": "1"},
                {"itg": "4", "seq": "2"},
            ]
        )

        self.assertFalse(valid)
        self.assertIn("more than once", message.lower())

    def test_valid_channels_preserve_order(self):
        data = [
            {"itg": "8", "seq": "2"},
            {"itg": "3", "seq": "1"},
        ]

        self.assertEqual(validate_channel_data(data), (True, ""))
        self.assertEqual(selected_itg_numbers(data), [8, 3])

    def test_selected_itg_numbers_excludes_malformed_values(self):
        data = [
            {"itg": "8", "seq": "2"},
            {"itg": "not-a-number", "seq": "1"},
            {"itg": None, "seq": "3"},
        ]

        self.assertEqual(selected_itg_numbers(data), [8])

    def test_att_elements_follow_page_three_order_and_exclude_unselected(self):
        selected = [
            {"itg": "3", "seq": "1"},
            {"itg": "1", "seq": "2"},
        ]
        master = [
            {"itg_no": 1, "ele_name": "FE", "wavelength": "271.4"},
            {"itg_no": 2, "ele_name": "C", "wavelength": "193.0"},
            {"itg_no": 3, "ele_name": "SI", "wavelength": "212.4"},
        ]

        rows = ordered_selected_elements(selected, master)

        self.assertEqual([row["itg_no"] for row in rows], [3, 1])

    def test_att_elements_are_empty_for_no_or_stale_selection(self):
        master = [{"itg_no": 1, "ele_name": "FE", "wavelength": "271.4"}]

        self.assertEqual(ordered_selected_elements([], master), [])
        self.assertEqual(
            ordered_selected_elements([{"itg": "99", "seq": "1"}], master),
            [],
        )

    def test_condition_next_opens_order_and_ise_page(self):
        from ui.anainf.page_01_source import SourceConditionPage

        class MainWindow:
            def __init__(self):
                self.widget = None

            def set_right_widget(self, widget):
                self.widget = widget

        main_window = MainWindow()
        page = SourceConditionPage.__new__(SourceConditionPage)
        page.main_window = main_window
        page.group_id = 1
        page.group_name = "TEST"
        page._save = lambda: None

        with patch("ui.anainf.page_03_channel.ChannelPage") as channel_page:
            page._on_next()

        channel_page.assert_called_once_with(main_window, 1, "TEST")
        self.assertIs(main_window.widget, channel_page.return_value)

    def test_order_and_ise_next_opens_att_page(self):
        from ui.anainf.page_03_channel import ChannelPage

        class MainWindow:
            def __init__(self):
                self.widget = None

            def set_right_widget(self, widget):
                self.widget = widget

        main_window = MainWindow()
        page = ChannelPage.__new__(ChannelPage)
        page.main_window = main_window
        page.group_id = 1
        page.group_name = "TEST"
        page._validate_rows = lambda: True
        page._save_data = lambda: None

        with patch("ui.anainf.page_02_attenuator.AttenuatorPage") as att_page:
            page._on_next()

        att_page.assert_called_once_with(main_window, 1, "TEST")
        self.assertIs(main_window.widget, att_page.return_value)

    def test_order_and_ise_next_blocks_when_no_channel_is_selected(self):
        from PyQt6.QtWidgets import QComboBox
        from ui.anainf.page_03_channel import ChannelPage

        class MainWindow:
            def set_right_widget(self, widget):
                self.widget = widget

        itg = QComboBox()
        itg.addItem("", "")
        seq = QComboBox()
        seq.addItems(["", "1", "2", "3"])
        page = ChannelPage.__new__(ChannelPage)
        page.main_window = MainWindow()
        page.group_id = 1
        page.group_name = "TEST"
        page._rows = [{"itg": itg, "seq": seq}]
        page._save_data = unittest.mock.Mock()
        page._show_msg = unittest.mock.Mock()

        with patch("ui.anainf.page_02_attenuator.AttenuatorPage") as att_page:
            page._on_next()

        att_page.assert_not_called()
        page._save_data.assert_not_called()
        page._show_msg.assert_called_once()

    def test_order_and_ise_next_blocks_when_sequence_is_missing(self):
        from PyQt6.QtWidgets import QComboBox
        from ui.anainf.page_03_channel import ChannelPage

        class MainWindow:
            def set_right_widget(self, widget):
                self.widget = widget

        itg = QComboBox()
        itg.addItem("3: SI", 3)
        seq = QComboBox()
        seq.addItems(["", "1", "2", "3"])
        page = ChannelPage.__new__(ChannelPage)
        page.main_window = MainWindow()
        page.group_id = 1
        page.group_name = "TEST"
        page._rows = [{"itg": itg, "seq": seq}]
        page._save_data = unittest.mock.Mock()
        page._show_msg = unittest.mock.Mock()

        with patch("ui.anainf.page_02_attenuator.AttenuatorPage") as att_page:
            page._on_next()

        att_page.assert_not_called()
        page._save_data.assert_not_called()
        page._show_msg.assert_called_once()

    def test_order_and_ise_previous_opens_condition_page(self):
        from ui.anainf.page_03_channel import ChannelPage

        class MainWindow:
            def __init__(self):
                self.widget = None

            def set_right_widget(self, widget):
                self.widget = widget

        main_window = MainWindow()
        page = ChannelPage.__new__(ChannelPage)
        page.main_window = main_window
        page.group_id = 1
        page.group_name = "TEST"
        page._validate_rows = lambda: True
        page._save_data = lambda: None

        with patch("ui.anainf.page_01_source.SourceConditionPage") as condition_page:
            page._on_pre()

        condition_page.assert_called_once_with(main_window, 1, "TEST")
        self.assertIs(main_window.widget, condition_page.return_value)


    def test_att_next_opens_drift_correction_page(self):
        from ui.anainf.page_02_attenuator import AttenuatorPage

        class MainWindow:
            def __init__(self):
                self.widget = None

            def set_right_widget(self, widget):
                self.widget = widget

        main_window = MainWindow()
        page = AttenuatorPage.__new__(AttenuatorPage)
        page.main_window = main_window
        page.group_id = 1
        page.group_name = "TEST"
        page._validate_att_values = lambda: True
        page._save = lambda: None

        with patch("ui.anainf.page_03_channel.ChannelPage") as channel_page, \
                patch("ui.anainf.page_04_drift.DriftCorrectionPage") as drift_page:
            page._on_next()

        channel_page.assert_not_called()
        drift_page.assert_called_once_with(main_window, 1, "TEST")
        self.assertIs(main_window.widget, drift_page.return_value)


    def test_saved_string_itg_restores_integer_combo_data(self):
        from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit
        from PyQt6.QtCore import QSignalBlocker
        from ui.anainf.page_03_channel import ChannelPage

        page = ChannelPage.__new__(ChannelPage)
        page._itg_to_ele = {"3": "SI"}
        page.group_name = "TEST"
        page.title_bar = QLabel()

        itg = QComboBox()
        itg.addItem("", "")
        itg.addItem("3: SI", 3)
        seq = QComboBox()
        seq.addItems(["", "1", "2", "3"])
        ise = QComboBox()
        ise.addItem("0 (none)", 0)
        row = {
            "ar": QLabel("1"),
            "itg": itg,
            "ele": QLabel(),
            "name": QLineEdit(),
            "seq": seq,
            "ise": ise,
        }
        page._rows = [row]

        page._populate_table_from_data(
            [{"itg": "3", "ele": "SI", "name": "S", "seq": "1", "ise_ref": 0}]
        )

        self.assertEqual(row["itg"].currentData(), 3)
        self.assertEqual(row["ele"].text(), "SI")

    def test_drift_previous_opens_att_page(self):
        from ui.anainf.page_04_drift import DriftCorrectionPage

        class MainWindow:
            def __init__(self):
                self.widget = None

            def set_right_widget(self, widget):
                self.widget = widget

        main_window = MainWindow()
        page = DriftCorrectionPage.__new__(DriftCorrectionPage)
        page.main_window = main_window
        page.group_id = 1
        page.group_name = "TEST"
        page._save = lambda: None

        with patch("ui.anainf.page_03_channel.ChannelPage") as channel_page, \
                patch("ui.anainf.page_02_attenuator.AttenuatorPage") as att_page:
            page._on_pre()

        channel_page.assert_not_called()
        att_page.assert_called_once_with(main_window, 1, "TEST")
        self.assertIs(main_window.widget, att_page.return_value)


if __name__ == "__main__":
    unittest.main()
