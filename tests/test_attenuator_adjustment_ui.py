import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup, MasterElement


class AttenuatorAdjustmentUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(
            self.engine,
            tables=[AnalyticalGroup.__table__, MasterElement.__table__],
        )
        self.session = sessionmaker(bind=self.engine)()
        group = AnalyticalGroup(
            name="LOW_ALLOY_STEEL",
            page_01_source={
                "purge_seq1": "1",
                "source_seq1": "B: Normal Spark",
                "preburn_seq1": "25",
                "integ_seq1": "300",
            },
            page_03_channel=[{"itg": "3", "ele": "C", "seq": "1", "ise_ref": 0}],
            page_02_attenuator={"rows": [{"itg_no": 3, "element": "C", "wavelength": "193.0", "att_value": 7}]},
        )
        self.session.add(group)
        self.session.add(MasterElement(itg_no=3, ele_name="C", wavelength="193.0"))
        self.session.commit()
        self.group_id = group.id

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_context_loads_only_selected_group_channels(self):
        from ui.adjustment.attenuator_adjustment_page import load_adjustment_context

        context = load_adjustment_context(self.session, self.group_id, "HVS")

        self.assertEqual([channel["itg"] for channel in context["channels"]], [3])
        self.assertEqual(context["channels"][0]["att_value"], 7)
        self.assertEqual(context["channels"][0]["group_integration_ms"], 300)
        self.assertEqual(context["channels"][0]["source"], "B: Normal Spark")
        self.assertEqual(context["preset"].integration_ms, 15000)

    def test_adjustment_page_explains_unit_is_changed_in_instrument_settings(self):
        from ui.adjustment.attenuator_adjustment_page import AttenuatorAdjustmentPage

        with patch(
            "ui.adjustment.attenuator_adjustment_page.get_or_create_instrument_configuration",
            return_value=Mock(emission_unit_type="HVS"),
        ):
            page = AttenuatorAdjustmentPage(Mock(), self.group_id, "LOW_ALLOY_STEEL")

        self.assertEqual(page._unit_label.text(), "HVS")
        self.assertEqual(
            page.change_unit_button.text(),
            "Change emission unit in Instrument Configuration",
        )

    def test_graph_stores_target_band_and_history_for_rendering(self):
        from ui.adjustment.adjustment_graph import (
            AdjustmentGraphWidget,
            normalized_time_positions,
        )

        graph = AdjustmentGraphWidget()
        graph.set_target_band(0.5, 0.6)
        graph.set_history([(1.0, 0.4), (2.0, 0.55)])

        self.assertEqual(graph.target_band, (0.5, 0.6))
        self.assertEqual(graph.history, [(1.0, 0.4), (2.0, 0.55)])
        self.assertEqual(normalized_time_positions([(1.0, 0.4), (3.0, 0.55)]), [0.0, 1.0])

    def test_adjustment_worker_rejects_out_of_range_att(self):
        from ui.adjustment.attenuator_adjustment_page import AdjustmentWorker

        worker = AdjustmentWorker({}, {"itg": 3, "ele": "C", "seq": "1"}, Mock(), 10)

        with self.assertRaises(ValueError):
            worker.update_att(64)

    def test_adjustment_worker_cleans_up_when_connection_fails(self):
        from ui.adjustment.attenuator_adjustment_page import AdjustmentWorker

        controller = Mock()
        controller.connect.return_value = False
        worker = AdjustmentWorker({}, {"itg": 3, "ele": "C", "seq": "1"}, Mock(), 10)

        with patch(
            "ui.adjustment.attenuator_adjustment_page.create_spectrometer_controller",
            return_value=controller,
        ):
            worker.run()

        controller.shutdown.assert_called_once_with()
        controller.close.assert_called_once_with()

    def test_navigation_shutdown_waits_for_adjustment_worker(self):
        from ui.adjustment.attenuator_adjustment_page import AttenuatorAdjustmentPage

        page = Mock()
        page._worker = Mock()
        page._thread = Mock()

        AttenuatorAdjustmentPage.shutdown_for_navigation(page)

        page._worker.stop.assert_called_once_with()
        page._thread.quit.assert_called_once_with()
        page._thread.wait.assert_called_once_with(2000)

    def test_main_window_requires_group_for_adjustment(self):
        from ui.main_window import MainWindow

        main_window = MainWindow.__new__(MainWindow)
        main_window.action_attenuator_adjustment = Mock()
        main_window._set_active_menu = Mock()
        main_window._get_current_group = Mock(return_value=(None, None))
        main_window._warn_no_group = Mock()

        MainWindow._open_attenuator_adjustment(main_window)

        main_window._warn_no_group.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
