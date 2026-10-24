import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from import_data.constants import ELEMENT_CHANNEL_COUNT, SOURCE_CODE_COUNT
from core.persistence.database import Base
from core.persistence.models import MasterElement, SourceCode
from core.persistence.reference_data import seed_reference_data


class ReferenceDataTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_seed_loads_bundled_master_and_source_data(self):
        self.assertTrue(seed_reference_data(self.session))

        self.assertEqual(self.session.query(MasterElement).count(), ELEMENT_CHANNEL_COUNT)
        self.assertEqual(self.session.query(SourceCode).count(), SOURCE_CODE_COUNT)
        self.assertEqual(self.session.get(MasterElement, 1).ele_name, "FE")
        self.assertEqual(self.session.get(SourceCode, 1).name, "Normal Spark")
        self.assertEqual(self.session.get(SourceCode, 11).name, "")

    def test_seed_does_not_overwrite_existing_configuration(self):
        seed_reference_data(self.session)
        self.session.get(MasterElement, 1).ele_name = "CUSTOM"
        self.session.get(SourceCode, 1).name = "Custom Source"
        self.session.commit()

        self.assertFalse(seed_reference_data(self.session))
        self.assertEqual(self.session.get(MasterElement, 1).ele_name, "CUSTOM")
        self.assertEqual(self.session.get(SourceCode, 1).name, "Custom Source")


if __name__ == "__main__":
    unittest.main()
