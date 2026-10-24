import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup, MatrixCorrection, WorkingCurve
from core.persistence.matrix_correction_repository import (
    activate_matrix_correction,
    create_matrix_candidate,
    get_active_matrix_corrections,
    list_matrix_corrections,
    migrate_matrix_json,
    retire_matrix_correction,
    update_active_matrix_coefficient,
)


class MatrixCorrectionRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.group = AnalyticalGroup(
            name="STEEL",
            page_06_matrix={
                "corrections": [
                    {
                        "target_element": "FE",
                        "target_name": "Fe",
                        "interfering_element": "C",
                        "interfering_name": "C",
                        "type": "L",
                        "coeff": 0.25,
                    }
                ]
            },
        )
        self.session.add(self.group)
        self.session.commit()
        self.session.refresh(self.group)
        self.curve1 = WorkingCurve(
            analytical_group_id=self.group.id,
            element_key="FE",
            name="Fe curve 1",
            curve_type="linear",
        )
        self.curve2 = WorkingCurve(
            analytical_group_id=self.group.id,
            element_key="FE",
            name="Fe curve 2",
            curve_type="linear",
        )
        self.session.add_all([self.curve1, self.curve2])
        self.session.commit()
        self.session.refresh(self.curve1)
        self.session.refresh(self.curve2)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_candidates_can_coexist_and_activation_is_unique_per_pair(self):
        first = create_matrix_candidate(
            self.session,
            self.group.id,
            "Fe",
            "C",
            "L",
            0.25,
            source_working_curve_id=self.curve1.id,
            point_count=4,
            fit_stats={"r2": 0.91, "rmse": 0.12},
            version_name="Fe-C L v1",
        )
        second = create_matrix_candidate(
            self.session,
            self.group.id,
            "FE",
            "C",
            "L",
            0.31,
            source_working_curve_id=self.curve2.id,
            point_count=5,
            fit_stats={"r2": 0.95, "rmse": 0.08},
            version_name="Fe-C L v2",
        )

        self.assertEqual(first.status, "inactive")
        self.assertEqual(second.source_working_curve_id, self.curve2.id)
        activate_matrix_correction(self.session, first.id)
        activate_matrix_correction(self.session, second.id)

        active = get_active_matrix_corrections(self.session, self.group.id)
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].id, second.id)
        self.assertEqual(active[0].coefficient, 0.31)

    def test_retire_and_update_active_coefficient(self):
        candidate = create_matrix_candidate(
            self.session, self.group.id, "Fe", "Si", "D", 0.1
        )
        activate_matrix_correction(self.session, candidate.id)
        update_active_matrix_coefficient(self.session, candidate.id, 0.2)

        self.session.refresh(candidate)
        self.assertEqual(candidate.coefficient, 0.2)
        retire_matrix_correction(self.session, candidate.id)
        self.assertEqual(candidate.status, "retired")
        self.assertEqual(get_active_matrix_corrections(self.session, self.group.id), [])

    def test_migration_is_idempotent_and_preserves_legacy_json(self):
        first = migrate_matrix_json(self.session)
        second = migrate_matrix_json(self.session)

        self.assertEqual(first, {"corrections": 1})
        self.assertEqual(second, {"corrections": 0})
        rows = list_matrix_corrections(self.session, self.group.id)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].status, "active")
        self.assertEqual(rows[0].target_element_key, "FE")
        self.assertEqual(self.group.page_06_matrix["corrections"][0]["coeff"], 0.25)

    def test_active_lookup_can_filter_by_target(self):
        fe = create_matrix_candidate(self.session, self.group.id, "Fe", "C", "L", 0.2)
        si = create_matrix_candidate(self.session, self.group.id, "Si", "C", "L", 0.3)
        activate_matrix_correction(self.session, fe.id)
        activate_matrix_correction(self.session, si.id)

        active = get_active_matrix_corrections(self.session, self.group.id, "FE")
        self.assertEqual([row.target_element_key for row in active], ["FE"])

    def test_candidate_rejects_non_finite_fit_statistics(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            create_matrix_candidate(
                self.session,
                self.group.id,
                "FE",
                "C",
                "L",
                0.2,
                fit_stats={"r2": float("nan"), "rmse": 0.1},
            )


if __name__ == "__main__":
    unittest.main()
