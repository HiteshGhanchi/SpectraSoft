import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup, WorkingCurveMeasurement, WorkingStandard
from core.persistence.working_curve_repository import (
    activate_curve,
    create_curve_version,
    get_active_coefficients,
    list_standards,
    migrate_working_curve_json,
    retire_curve,
    upsert_measurement,
    upsert_standard,
    sync_standards,
    update_active_curve_coefficients,
)


class WorkingCurveRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.group = AnalyticalGroup(
            name="STEEL",
            page_05_chemical_standards={
                "standards": [
                    {"sample": "STD_1", "values": {"C": 0.1, "SI": 0.2}},
                    {"sample": "STD_2", "values": {"C": 0.3}},
                ]
            },
            page_05_wc_measurements={
                "measurements": [
                    {"sample": "STD_1", "burns": 3, "intensities": {"C": 0.11}}
                ]
            },
            page_05_wc={
                "coefficients": [
                    {"element": "C", "a": 0, "b": 0, "c": 2, "d": 0}
                ]
            },
        )
        self.session.add(self.group)
        self.session.commit()
        self.session.refresh(self.group)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_migration_is_idempotent_and_imports_all_json_layers(self):
        first = migrate_working_curve_json(self.session)
        second = migrate_working_curve_json(self.session)

        self.assertGreaterEqual(first["standards"], 2)
        self.assertGreaterEqual(first["measurements"], 1)
        self.assertGreaterEqual(first["curves"], 1)
        self.assertEqual(second, {"standards": 0, "measurements": 0, "curves": 0})
        self.assertEqual(len(list_standards(self.session, self.group.id)), 2)

    def test_standard_and_measurement_upserts_replace_existing_records(self):
        standard = upsert_standard(
            self.session, self.group.id, "std_3", {"C": 0.5, "SI": 0.6}
        )
        same = upsert_standard(self.session, self.group.id, "STD_3", {"C": 0.7})

        self.assertEqual(standard.id, same.id)
        self.assertEqual(same.values[0].known_value, 0.7)

        upsert_measurement(self.session, self.group.id, "STD_3", {"C": 0.51}, 3)
        upsert_measurement(
            self.session, self.group.id, "STD_3", {"C": 0.71}, 4
        )
        measurement = self.session.query(WorkingCurveMeasurement).one()
        self.assertEqual(measurement.burn_count, 4)
        self.assertEqual(measurement.corrected_intensity, 0.71)

    def test_curve_versions_can_coexist_and_activation_is_per_group_element(self):
        first = create_curve_version(
            self.session,
            self.group.id,
            "C",
            "linear",
            {"a": 0, "b": 0, "c": 2, "d": 0},
            {"r2": 0.9, "rmse": 0.1},
            3,
        )
        second = create_curve_version(
            self.session,
            self.group.id,
            "C",
            "quadratic",
            {"a": 0, "b": 1, "c": 1, "d": 0},
            {"r2": 0.95, "rmse": 0.05},
            4,
        )

        activate_curve(self.session, first.id)
        activate_curve(self.session, second.id)
        active = get_active_coefficients(self.session, self.group.id, "c")

        self.assertEqual(active["curve_id"], second.id)
        self.assertEqual(active["curve_type"], "quadratic")
        self.assertEqual(active["coefficients"]["b"], 1.0)

        retire_curve(self.session, second.id)
        self.assertIsNone(get_active_coefficients(self.session, self.group.id, "C"))

    def test_sync_standards_removes_deleted_normalized_values(self):
        upsert_standard(self.session, self.group.id, "STD_X", {"C": 0.1, "SI": 0.2})
        sync_standards(self.session, self.group.id, [{"sample": "STD_X", "values": {"C": 0.3}}])

        standard = self.session.query(WorkingStandard).filter_by(sample_name="STD_X").one()
        self.assertEqual([(value.element_key, value.known_value) for value in standard.values], [("C", 0.3)])

    def test_manual_update_changes_active_normalized_coefficients(self):
        curve = create_curve_version(
            self.session, self.group.id, "C", "linear", {"a": 0, "b": 0, "c": 2, "d": 0}, {}, 2
        )
        activate_curve(self.session, curve.id)
        update_active_curve_coefficients(
            self.session, self.group.id, "C", {"a": 0, "b": 0, "c": 4, "d": 1}
        )

        active = get_active_coefficients(self.session, self.group.id, "C")
        self.assertEqual(active["coefficients"]["c"], 4.0)


if __name__ == "__main__":
    unittest.main()
