import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.maintenance.models import MaintenanceJournalEntry
from core.maintenance.service import MaintenanceCapabilityUnavailable, MaintenanceService
from core.persistence.database import Base


class FakeController:
    def connect(self):
        return True

    def reset(self):
        return True

    def argon_purge(self, purge_sec):
        return True

    def prespark(self, source_code, preburn_ms):
        return True

    def integrate(self, integ_ms, elements):
        return {}

    def clean(self, clean_ms):
        return True

    def shutdown(self):
        return True

    def set_attenuator(self, itg_no, att_value):
        return True

    def close(self):
        return None


class MaintenanceServiceTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine, tables=[MaintenanceJournalEntry.__table__])
        self.session_factory = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_generic_controller_does_not_claim_maintenance_capabilities(self):
        service = MaintenanceService(self.session_factory, controller=FakeController())

        for operation in service.OPERATIONS:
            capability = service.capability(operation)
            self.assertFalse(capability.available)
            self.assertIn("no verified", capability.reason.lower())

        with self.assertRaises(MaintenanceCapabilityUnavailable):
            service.perform("tan_clear", operator="operator")

    def test_manual_completion_is_persisted_as_operator_confirmed_not_hardware_work(self):
        service = MaintenanceService(self.session_factory)

        entry = service.record_manual_completion(
            "waste_discharge",
            operator="A. Operator",
            notes="Completed using the instrument's local maintenance controls.",
        )

        self.assertFalse(entry.hardware_performed)
        self.assertEqual(entry.completion_mode, "manual_confirmed")
        self.assertEqual(entry.operation, "waste_discharge")
        with self.session_factory() as session:
            saved = session.get(MaintenanceJournalEntry, entry.id)
            self.assertEqual(saved.operator, "A. Operator")
            self.assertIn("local maintenance", saved.notes)

    def test_explicit_verified_callback_is_available_and_recorded_as_hardware_work(self):
        calls = []

        def waste_discharge():
            calls.append("waste_discharge")
            return True

        service = MaintenanceService(
            self.session_factory,
            controller=FakeController(),
            verified_operations={"waste_discharge": waste_discharge},
        )

        self.assertTrue(service.capability("waste_discharge").available)
        entry = service.perform("waste_discharge", operator="Engineer", notes="Verified test callback")

        self.assertEqual(calls, ["waste_discharge"])
        self.assertTrue(entry.hardware_performed)
        self.assertEqual(entry.completion_mode, "hardware_performed")

if __name__ == "__main__":
    unittest.main()
