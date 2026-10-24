import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.analysis.matrix_correction_service import (
    build_matrix_pairs,
    calculate_matrix_coefficient,
    predict_matrix_corrected,
)
from core.persistence.database import Base
from core.persistence.models import (
    AnalyticalGroup,
    WorkingCurve,
    WorkingCurveCoefficient,
    WorkingCurveMeasurement,
    WorkingStandard,
    WorkingStandardValue,
)


class MatrixCorrectionServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        group = AnalyticalGroup(name="STEEL")
        self.session.add(group)
        self.session.flush()

        curve = WorkingCurve(
            analytical_group_id=group.id,
            element_key="FE",
            name="Fe linear",
            curve_type="linear",
            status="active",
        )
        curve.coefficients.append(WorkingCurveCoefficient(c=2.0, d=0.0))
        self.session.add(curve)

        for sample, fe, c, intensity in [
            ("STD1", 10.0, 2.0, 4.0),
            ("STD2", 20.0, 4.0, 9.0),
            ("STD3", 30.0, 6.0, 14.0),
        ]:
            standard = WorkingStandard(
                analytical_group_id=group.id, sample_name=sample
            )
            standard.values.extend([
                WorkingStandardValue(element_key="FE", known_value=fe),
                WorkingStandardValue(element_key="C", known_value=c),
            ])
            self.session.add(standard)
            self.session.flush()
            self.session.add(
                WorkingCurveMeasurement(
                    analytical_group_id=group.id,
                    standard_id=standard.id,
                    element_key="FE",
                    corrected_intensity=intensity,
                    burn_count=3,
                )
            )

        self.session.commit()
        self.group_id = group.id
        self.curve_id = curve.id

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_build_pairs_uses_active_curve_and_normalized_standard_ids(self):
        pairs = build_matrix_pairs(self.session, self.group_id, "fe", "c")

        self.assertEqual([pair["sample"] for pair in pairs], ["STD1", "STD2", "STD3"])
        self.assertEqual([pair["c0"] for pair in pairs], [8.0, 18.0, 28.0])
        self.assertEqual(pairs[0]["interfering"], 2.0)
        self.assertEqual(pairs[0]["working_curve_id"], self.curve_id)

    def test_calculate_l_and_d_reports_fit_statistics(self):
        pairs = [
            {"sample": "A", "c0": 8.0, "true": 10.0, "interfering": 2.0},
            {"sample": "B", "c0": 18.0, "true": 22.0, "interfering": 4.0},
        ]

        l_result = calculate_matrix_coefficient(pairs, "L")
        d_result = calculate_matrix_coefficient(pairs, "D")

        self.assertAlmostEqual(l_result["coefficient"], 1.0)
        self.assertAlmostEqual(d_result["coefficient"], 0.0588235294117647)
        self.assertEqual(l_result["point_count"], 2)
        self.assertIn("r2", l_result)
        self.assertIn("rmse", l_result)
        self.assertEqual(len(l_result["points"]), 2)

    def test_prediction_applies_l_or_d_formula(self):
        pair = {"c0": 10.0, "interfering": 2.0}
        self.assertAlmostEqual(predict_matrix_corrected(pair, 0.5, "L"), 11.0)
        self.assertAlmostEqual(predict_matrix_corrected(pair, 0.5, "D"), 20.0)

    def test_empty_and_zero_denominator_pairs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "No valid matrix pairs"):
            calculate_matrix_coefficient([], "L")
        with self.assertRaisesRegex(ValueError, "denominator is zero"):
            calculate_matrix_coefficient(
                [{"c0": 1.0, "true": 2.0, "interfering": 0.0}], "L"
            )

        with self.assertRaisesRegex(ValueError, "finite"):
            calculate_matrix_coefficient(
                [{"c0": float("nan"), "true": 2.0, "interfering": 1.0}], "L"
            )
        with self.assertRaisesRegex(ValueError, "finite"):
            calculate_matrix_coefficient(
                [{"c0": 1.0, "true": 2.0, "interfering": 1.0, "error": float("nan")}], "L"
            )
        with self.assertRaisesRegex(ValueError, "finite"):
            predict_matrix_corrected(
                {"c0": float("inf"), "interfering": 1.0}, 0.1, "L"
            )
        with self.assertRaisesRegex(ValueError, "finite"):
            calculate_matrix_coefficient(
                [{"c0": 1e308, "true": 1e308, "interfering": 1e308}], "L"
            )

    def test_explicit_curve_must_match_target_element(self):
        with self.assertRaisesRegex(ValueError, "target element"):
            build_matrix_pairs(self.session, self.group_id, "C", "FE", self.curve_id)

    def test_inactive_normalized_curve_does_not_fall_back_to_legacy_coefficients(self):
        from core.persistence.models import WorkingCurve

        session_curve = WorkingCurve(
            analytical_group_id=self.group_id,
            element_key="C",
            name="C inactive",
            curve_type="linear",
            status="inactive",
        )
        self.session.add(session_curve)
        group = self.session.get(AnalyticalGroup, self.group_id)
        group.page_05_wc = {
            "coefficients": [{"element": "C", "a": 0, "b": 0, "c": 2, "d": 0}]
        }
        self.session.commit()

        with self.assertRaisesRegex(ValueError, "No active normalized working curve"):
            build_matrix_pairs(self.session, self.group_id, "C", "FE")


if __name__ == "__main__":
    unittest.main()
