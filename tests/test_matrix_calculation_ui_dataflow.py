import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import (
    AnalyticalGroup,
    WorkingCurve,
    WorkingCurveCoefficient,
    WorkingCurveMeasurement,
    WorkingStandard,
    WorkingStandardValue,
)
from core.persistence.matrix_correction_repository import (
    activate_matrix_correction,
    get_active_matrix_corrections,
)


class MatrixCalculationUIDataflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        session = self.session_factory()
        group = AnalyticalGroup(
            name="STEEL",
            page_03_channel=[
                {"name": "Fe", "ele": "FE", "itg": "1"},
                {"name": "C", "ele": "C", "itg": "2"},
            ],
        )
        session.add(group)
        session.flush()
        curve = WorkingCurve(
            analytical_group_id=group.id,
            element_key="FE",
            name="Fe linear",
            curve_type="linear",
            status="active",
        )
        curve.coefficients.append(WorkingCurveCoefficient(c=2.0))
        session.add(curve)
        for sample, true_fe, true_c, intensity in [
            ("STD1", 10.0, 2.0, 4.0),
            ("STD2", 20.0, 4.0, 9.0),
        ]:
            standard = WorkingStandard(
                analytical_group_id=group.id, sample_name=sample
            )
            standard.values.extend([
                WorkingStandardValue(element_key="FE", known_value=true_fe),
                WorkingStandardValue(element_key="C", known_value=true_c),
            ])
            session.add(standard)
            session.flush()
            session.add(WorkingCurveMeasurement(
                analytical_group_id=group.id,
                standard_id=standard.id,
                element_key="FE",
                corrected_intensity=intensity,
                burn_count=3,
            ))
        session.commit()
        self.group_id = group.id
        session.close()

        import ui.regression.matrix_calculation_page as matrix_page
        self.matrix_page = matrix_page
        self.original_session = matrix_page.get_session
        matrix_page.get_session = lambda: self.session_factory()

    def tearDown(self):
        self.matrix_page.get_session = self.original_session
        self.engine.dispose()

    def test_matrix_page_builds_pairs_from_active_normalized_working_curve(self):
        from ui.regression.matrix_calculation_page import MatrixCalculationPage

        page = MatrixCalculationPage(object(), self.group_id, "STEEL")
        pairs = page._build_pairs("Fe", "C")

        self.assertEqual([pair["c0"] for pair in pairs], [8.0, 18.0])
        self.assertEqual(pairs[0]["working_curve_id"] > 0, True)

    def test_filing_creates_inactive_candidate_without_replacing_active(self):
        from ui.regression.matrix_calculation_page import MatrixCalculationPage

        page = MatrixCalculationPage(object(), self.group_id, "STEEL")
        page.current_result = {
            "target": "Fe",
            "interfering": "C",
            "type": "L",
            "coeff": 0.25,
            "point_count": 2,
            "r2": 0.9,
            "rmse": 0.1,
            "working_curve_id": 1,
        }
        page._file_current_result_to_page6()

        session = self.session_factory()
        rows = session.query(__import__("core.persistence.models", fromlist=["MatrixCorrection"]).MatrixCorrection).all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].status, "inactive")
        self.assertEqual(rows[0].source_working_curve_id, 1)
        self.assertEqual(get_active_matrix_corrections(session, self.group_id), [])
        session.close()

    def test_combo_data_uses_page3_element_keys_not_display_names(self):
        from ui.regression.matrix_calculation_page import MatrixCalculationPage

        page = MatrixCalculationPage(object(), self.group_id, "STEEL")
        self.assertEqual(page.target_combo.itemData(0), "FE")
        self.assertEqual(page.target_combo.itemText(0), "Fe")

    def test_invalid_matrix_pair_data_is_reported_as_calculation_failure(self):
        from ui.regression.matrix_calculation_page import MatrixCalculationPage

        page = MatrixCalculationPage(object(), self.group_id, "STEEL")
        page._build_pairs = lambda target, interfering: [
            {"sample": "STD1", "c0": float("nan"), "true": 10.0, "interfering": 2.0}
        ]
        page._show_msg = lambda *args, **kwargs: setattr(page, "validation_message", args[1])
        page._on_calculate()

        self.assertIn("finite", page.validation_message)


if __name__ == "__main__":
    unittest.main()
