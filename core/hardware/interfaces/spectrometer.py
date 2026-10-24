"""Instrument-level interface used by analysis workflows."""

from __future__ import annotations

from typing import Dict, List, Protocol


class SpectrometerController(Protocol):
    """Semantic operations required by the burn and calibration workflows."""

    def connect(self) -> bool:
        """Connect to the instrument controller."""
        ...

    def reset(self) -> bool:
        """Reset and enable the instrument source."""
        ...

    def argon_purge(self, purge_sec: float) -> bool:
        """Purge the spark stand with argon."""
        ...

    def prespark(self, source_code: int, preburn_ms: int) -> bool:
        """Run the pre-spark operation for the frontend-selected code."""
        ...

    def integrate(self, integ_ms: int, elements: List[Dict]) -> Dict[str, int]:
        """Measure the requested elements and return ADC values."""
        ...

    def clean(self, clean_ms: int) -> bool:
        """Run the configured cleaning operation."""
        ...

    def shutdown(self) -> bool:
        """Return the controller to its standby state."""
        ...

    def set_attenuator(self, itg_no: int, att_value: int) -> bool:
        """Set an attenuator for one instrument channel."""
        ...

    def close(self) -> None:
        """Release the controller connection."""
        ...
