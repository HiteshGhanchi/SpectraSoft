"""Maintenance capability truthfulness and journal service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping, Optional

from .models import MaintenanceJournalEntry


class MaintenanceCapabilityUnavailable(RuntimeError):
    """Raised when an operation has no verified hardware implementation."""


class MaintenanceOperationFailed(RuntimeError):
    """Raised when a verified hardware operation reports failure."""


@dataclass(frozen=True)
class MaintenanceCapability:
    operation: str
    label: str
    available: bool
    reason: str


class MaintenanceService:
    """Persist maintenance records without guessing instrument semantics."""

    OPERATIONS = (
        "waste_discharge",
        "lamp_test",
        "manual_scanning",
        "telemetry",
        "tan_clear",
    )
    LABELS = {
        "waste_discharge": "Waste Discharge",
        "lamp_test": "Lamp Test",
        "manual_scanning": "Manual Scanning",
        "telemetry": "Temperature / Voltage / Vacuum",
        "tan_clear": "TAN Clear",
    }
    _UNVERIFIED_REASON = (
        "Not available: no verified maintenance capability is supplied by the "
        "current SpectrometerController integration."
    )

    def __init__(
        self,
        session_factory,
        *,
        controller=None,
        verified_operations: Optional[Mapping[str, Callable[[], object]]] = None,
    ):
        self.session_factory = session_factory
        self.controller = controller
        self.verified_operations = dict(verified_operations or {})
        unknown = set(self.verified_operations) - set(self.OPERATIONS)
        if unknown:
            raise ValueError(f"Unknown maintenance operations: {sorted(unknown)}")

    def capability(self, operation: str) -> MaintenanceCapability:
        self._validate_operation(operation)
        callback = self.verified_operations.get(operation)
        if callable(callback):
            return MaintenanceCapability(
                operation,
                self.LABELS[operation],
                True,
                "Available through an explicitly supplied verified integration callback.",
            )
        return MaintenanceCapability(operation, self.LABELS[operation], False, self._UNVERIFIED_REASON)

    def record_manual_completion(self, operation: str, *, operator: str, notes: str = ""):
        """Record what an operator says they did on the instrument locally."""
        return self._record(
            operation,
            operator=operator,
            notes=notes,
            completion_mode="manual_confirmed",
            hardware_performed=False,
        )

    def perform(self, operation: str, *, operator: str, notes: str = ""):
        """Run only an explicitly supplied verified callback and journal it."""
        self._validate_operation(operation)
        callback = self.verified_operations.get(operation)
        if not callable(callback):
            raise MaintenanceCapabilityUnavailable(self.capability(operation).reason)
        result = callback()
        if result is False:
            raise MaintenanceOperationFailed(f"Verified maintenance operation failed: {operation}")
        return self._record(
            operation,
            operator=operator,
            notes=notes,
            completion_mode="hardware_performed",
            hardware_performed=True,
        )

    def recent_entries(self, limit: int = 25):
        if limit < 1:
            raise ValueError("limit must be positive")
        with self.session_factory() as session:
            return (
                session.query(MaintenanceJournalEntry)
                .order_by(MaintenanceJournalEntry.performed_at.desc())
                .limit(limit)
                .all()
            )

    def _record(self, operation, *, operator, notes, completion_mode, hardware_performed):
        self._validate_operation(operation)
        operator = str(operator).strip()
        if not operator:
            raise ValueError("operator is required")
        with self.session_factory() as session:
            entry = MaintenanceJournalEntry(
                operation=operation,
                completion_mode=completion_mode,
                hardware_performed=hardware_performed,
                operator=operator,
                notes=str(notes or "").strip(),
            )
            session.add(entry)
            session.commit()
            session.refresh(entry)
            return entry

    def _validate_operation(self, operation: str) -> None:
        if operation not in self.OPERATIONS:
            raise ValueError(f"Unknown maintenance operation: {operation}")
