import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.adjustment.service import (
    AdjustmentHistory,
    AttenuatorAdjustmentRunner,
    get_adjustment_preset,
    save_group_att,
    update_group_att_rows,
    validate_adjustment_channel,
)
from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup
from import_data.constants import ADC_MAX_VALUE, EMISSION_UNIT_HPSG_300


class FakeController:
    def __init__(self, readings=None, fail_at=None):
        self.calls = []
        self.readings = readings or {"C": 2048}
        self.fail_at = fail_at

    def _ok(self, name, *args):
        self.calls.append((name, *args))
        return self.fail_at != name

    def reset(self):
        return self._ok("reset")

    def argon_purge(self, purge_sec):
        return self._ok("argon_purge", purge_sec)

    def prespark(self, source_code, preburn_ms):
        return self._ok("prespark", source_code, preburn_ms)

    def integrate(self, integ_ms, elements):
        self.calls.append(("integrate", integ_ms, elements))
        if self.fail_at == "integrate":
            return {}
        return self.readings

    def set_attenuator(self, itg_no, att_value):
        return self._ok("set_attenuator", itg_no, att_value)

    def shutdown(self):
        return self._ok("shutdown")


class AttenuatorAdjustmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine, tables=[AnalyticalGroup.__table__])
        self.session = sessionmaker(bind=self.engine)()
        self.group = AnalyticalGroup(
            name="TEST",
            page_02_attenuator={
                "rows": [
                    {"itg_no": 4, "element": "SI", "wavelength": "212.4", "att_value": 9}
                ]
            },
        )
        self.session.add(self.group)
        self.session.commit()
        self.session.refresh(self.group)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_channel_validation_requires_itg_element_and_sequence(self):
        self.assertEqual(
            validate_adjustment_channel({"itg": "3", "ele": "C", "seq": "1"}),
            (True, ""),
        )
        valid, message = validate_adjustment_channel({"itg": "", "ele": "C", "seq": "1"})
        self.assertFalse(valid)
        self.assertIn("ITG", message)

    def test_att_rows_replace_only_the_selected_itg(self):
        page_data = {
            "rows": [
                {"itg_no": 3, "element": "C", "wavelength": "193.0", "att_value": 7},
                {"itg_no": 4, "element": "SI", "wavelength": "212.4", "att_value": 9},
            ]
        }

        updated = update_group_att_rows(
            page_data,
            {"itg": 3, "ele": "C", "wavelength": "193.0"},
            22,
        )

        self.assertEqual(updated["rows"][0]["att_value"], 22)
        self.assertEqual(updated["rows"][1]["att_value"], 9)

    def test_save_group_att_persists_only_the_accepted_channel_value(self):
        save_group_att(
            self.session,
            self.group.id,
            {"itg": 3, "ele": "C", "wavelength": "193.0"},
            22,
        )

        saved = self.session.get(AnalyticalGroup, self.group.id)
        self.assertEqual(saved.page_02_attenuator["rows"][0]["att_value"], 9)
        self.assertEqual(saved.page_02_attenuator["rows"][1]["att_value"], 22)

    def test_history_records_att_change_markers(self):
        history = AdjustmentHistory()
        history.add(1.0, 10, 0.40)
        history.add(2.0, 10, 0.52)
        history.add(3.0, 12, 0.58)

        self.assertEqual(len(history.readings), 3)
        self.assertEqual(history.att_markers, [(1.0, 10), (3.0, 12)])

    def test_runner_uses_semantic_controller_and_normalizes_adc(self):
        controller = FakeController()
        runner = AttenuatorAdjustmentRunner(controller)

        reading = runner.measure_once(
            {
                "purge_seq1": "1",
                "source_seq1": "B: Normal Spark",
                "preburn_seq1": "25",
            },
            {"itg": 3, "ele": "C", "seq": "1"},
            get_adjustment_preset(EMISSION_UNIT_HPSG_300),
            22,
        )

        self.assertEqual(reading.itg_no, 3)
        self.assertEqual(reading.att_value, 22)
        self.assertAlmostEqual(reading.intensity, 2048 / ADC_MAX_VALUE)
        self.assertEqual(controller.calls[0], ("set_attenuator", 3, 22))
        self.assertIn(("prespark", 0xB, 25), controller.calls)
        self.assertIn(("integrate", 4000, [{"itg": 3, "ele": "C"}]), controller.calls)

    def test_runner_failure_shuts_down_and_does_not_return_reading(self):
        controller = FakeController(fail_at="integrate")
        runner = AttenuatorAdjustmentRunner(controller)

        with self.assertRaises(RuntimeError):
            runner.measure_once(
                {"purge_seq1": "1", "source_seq1": "1: Normal", "preburn_seq1": "25"},
                {"itg": 3, "ele": "C", "seq": "1"},
                get_adjustment_preset(EMISSION_UNIT_HPSG_300),
                22,
            )

        self.assertIn(("shutdown",), controller.calls)


if __name__ == "__main__":
    unittest.main()
