import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import AnalyticalGroup, WorkingCurveMeasurement, WorkingStandard
from core.persistence.working_curve_repository import upsert_measurement, upsert_standard


class WorkingCurveUIDataflowTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        group = AnalyticalGroup(name="STEEL")
        self.session.add(group)
        self.session.commit()
        self.group_id = group.id

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_standard_write_is_normalized_and_replaces_duplicate(self):
        upsert_standard(self.session, self.group_id, "std_1", {"C": 0.1})
        upsert_standard(self.session, self.group_id, "STD_1", {"C": 0.2})

        self.assertEqual(self.session.query(WorkingStandard).count(), 1)
        self.assertEqual(self.session.query(WorkingStandard).one().values[0].known_value, 0.2)

    def test_job7_measurement_write_replaces_latest_element_value(self):
        upsert_measurement(self.session, self.group_id, "STD_1", {"C": 0.1}, 2)
        upsert_measurement(self.session, self.group_id, "STD_1", {"C": 0.3}, 4)

        rows = self.session.query(WorkingCurveMeasurement).all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].corrected_intensity, 0.3)
        self.assertEqual(rows[0].burn_count, 4)


if __name__ == "__main__":
    unittest.main()
