import unittest

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from core.persistence.database import Base
from core.persistence.models import InstrumentConfiguration
from core.persistence.configuration import (
    get_or_create_instrument_configuration,
    set_emission_unit_type,
)
from core.adjustment.service import get_adjustment_preset
from import_data.constants import (
    DEFAULT_EMISSION_UNIT_TYPE,
    EMISSION_UNIT_HPSG_300,
    EMISSION_UNIT_HVS,
)


class InstrumentConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine, tables=[InstrumentConfiguration.__table__])
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_configuration_defaults_once_and_preserves_saved_selection(self):
        config = get_or_create_instrument_configuration(self.session)

        self.assertEqual(config.id, 1)
        self.assertEqual(config.emission_unit_type, DEFAULT_EMISSION_UNIT_TYPE)

        set_emission_unit_type(self.session, EMISSION_UNIT_HVS)
        config_again = get_or_create_instrument_configuration(self.session)

        self.assertEqual(config_again.emission_unit_type, EMISSION_UNIT_HVS)
        self.assertEqual(self.session.query(InstrumentConfiguration).count(), 1)

    def test_invalid_emission_unit_is_rejected(self):
        with self.assertRaises(ValueError):
            set_emission_unit_type(self.session, "UNKNOWN")

    def test_invalid_existing_configuration_is_rejected(self):
        self.session.execute(text("PRAGMA ignore_check_constraints = ON"))
        self.session.execute(
            text(
                "INSERT INTO instrument_configuration "
                "(id, emission_unit_type) VALUES (1, 'BROKEN')"
            )
        )
        self.session.commit()

        with self.assertRaises(ValueError):
            get_or_create_instrument_configuration(self.session)

    def test_hpsg_preset_matches_manual_guidance(self):
        preset = get_adjustment_preset(EMISSION_UNIT_HPSG_300)

        self.assertEqual(preset.scale, 2)
        self.assertEqual((preset.graduation_min, preset.graduation_max), (6, 7))
        self.assertEqual(preset.integration_ms, 4000)
        self.assertEqual((preset.target_min, preset.target_max), (0.5, 0.6))

    def test_hvs_preset_matches_manual_guidance(self):
        preset = get_adjustment_preset(EMISSION_UNIT_HVS)

        self.assertEqual(preset.scale, 5)
        self.assertEqual((preset.graduation_min, preset.graduation_max), (4, 5))
        self.assertEqual(preset.integration_ms, 15000)
        self.assertEqual((preset.target_min, preset.target_max), (0.5, 0.6))


if __name__ == "__main__":
    unittest.main()
