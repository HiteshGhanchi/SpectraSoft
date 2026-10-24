"""Domain services for instrument attenuator adjustment."""

from dataclasses import dataclass
import time

from import_data.constants import (
    ADC_MAX_VALUE,
    ATT_ADJUSTMENT_TARGET_MAX,
    ATT_ADJUSTMENT_TARGET_MIN,
    ATTENUATOR_MAX_VALUE,
    ATTENUATOR_MIN_VALUE,
    EMISSION_UNIT_HPSG_300,
    EMISSION_UNIT_HVS,
    HPSG_300_ADJUSTMENT_GRADUATION_MAX,
    HPSG_300_ADJUSTMENT_GRADUATION_MIN,
    HPSG_300_ADJUSTMENT_INTEGRATION_MS,
    HPSG_300_ADJUSTMENT_SCALE,
    HVS_ADJUSTMENT_GRADUATION_MAX,
    HVS_ADJUSTMENT_GRADUATION_MIN,
    HVS_ADJUSTMENT_INTEGRATION_MS,
    HVS_ADJUSTMENT_SCALE,
)
from core.hardware.sequence_engine import SequenceEngine
from core.persistence.models import AnalyticalGroup


@dataclass(frozen=True)
class AdjustmentPreset:
    emission_unit_type: str
    scale: int
    graduation_min: int
    graduation_max: int
    integration_ms: int
    target_min: float = ATT_ADJUSTMENT_TARGET_MIN
    target_max: float = ATT_ADJUSTMENT_TARGET_MAX


@dataclass(frozen=True)
class AdjustmentReading:
    timestamp: float
    itg_no: int
    att_value: int
    intensity: float


class AdjustmentHistory:
    """In-memory readings and the points where the operator changed ATT."""

    def __init__(self):
        self.readings: list[AdjustmentReading] = []
        self.att_markers: list[tuple[float, int]] = []

    def add(self, timestamp: float, att_value: int, intensity: float) -> AdjustmentReading:
        value = validate_att_value(att_value)
        reading = AdjustmentReading(timestamp, 0, value, float(intensity))
        if not self.readings or self.readings[-1].att_value != value:
            self.att_markers.append((timestamp, value))
        self.readings.append(reading)
        return reading


def get_adjustment_preset(emission_unit_type: str) -> AdjustmentPreset:
    """Return manual-defined adjustment guidance for an emission unit."""
    value = str(emission_unit_type).strip().upper()
    if value == EMISSION_UNIT_HPSG_300:
        return AdjustmentPreset(
            emission_unit_type=value,
            scale=HPSG_300_ADJUSTMENT_SCALE,
            graduation_min=HPSG_300_ADJUSTMENT_GRADUATION_MIN,
            graduation_max=HPSG_300_ADJUSTMENT_GRADUATION_MAX,
            integration_ms=HPSG_300_ADJUSTMENT_INTEGRATION_MS,
        )
    if value == EMISSION_UNIT_HVS:
        return AdjustmentPreset(
            emission_unit_type=value,
            scale=HVS_ADJUSTMENT_SCALE,
            graduation_min=HVS_ADJUSTMENT_GRADUATION_MIN,
            graduation_max=HVS_ADJUSTMENT_GRADUATION_MAX,
            integration_ms=HVS_ADJUSTMENT_INTEGRATION_MS,
        )
    raise ValueError(f"Unsupported emission unit '{emission_unit_type}'")


def validate_att_value(att_value: int) -> int:
    """Return a validated ATT value in the inclusive 0-63 range."""
    try:
        value = int(att_value)
    except (TypeError, ValueError) as exc:
        raise ValueError("ATT must be an integer between 0 and 63") from exc
    if not ATTENUATOR_MIN_VALUE <= value <= ATTENUATOR_MAX_VALUE:
        raise ValueError("ATT must be an integer between 0 and 63")
    return value


def validate_adjustment_channel(channel: dict) -> tuple[bool, str]:
    """Validate the selected ITG/channel before hardware work begins."""
    try:
        itg_no = int(channel.get("itg"))
    except (AttributeError, TypeError, ValueError):
        return False, "A valid ITG channel is required."
    if itg_no <= 0:
        return False, "A valid ITG channel is required."
    if not str(channel.get("ele", "")).strip():
        return False, "An analytical element is required."
    if str(channel.get("seq", "")).strip() not in {"1", "2", "3"}:
        return False, "A valid SEQ (1, 2, or 3) is required."
    return True, ""


def update_group_att_rows(page_data: dict, element: dict, att_value: int) -> dict:
    """Replace or append one selected channel's ATT row without losing others."""
    value = validate_att_value(att_value)
    try:
        itg_no = int(element.get("itg_no", element.get("itg")))
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("A valid ITG channel is required") from exc

    rows = list((page_data or {}).get("rows", []))
    replacement = {
        "itg_no": itg_no,
        "element": str(element.get("element", element.get("ele", ""))),
        "wavelength": str(element.get("wavelength", "")),
        "att_value": value,
    }
    replaced = False
    updated_rows = []
    for row in rows:
        try:
            row_itg = int(row.get("itg_no"))
        except (AttributeError, TypeError, ValueError):
            row_itg = None
        if row_itg == itg_no:
            updated_rows.append(replacement)
            replaced = True
        else:
            updated_rows.append(dict(row))
    if not replaced:
        updated_rows.append(replacement)
    return {"rows": updated_rows}


def save_group_att(session, group_id: int, element: dict, att_value: int) -> None:
    """Persist one accepted ATT value under an Analytical Group."""
    group = session.get(AnalyticalGroup, group_id)
    if group is None:
        raise ValueError(f"Analytical Group {group_id} does not exist")
    group.page_02_attenuator = update_group_att_rows(
        group.page_02_attenuator or {}, element, att_value
    )
    session.commit()


class AttenuatorAdjustmentRunner:
    """Execute one adjustment measurement through semantic controller methods."""

    def __init__(self, controller):
        self.controller = controller

    def measure_once(
        self,
        group_condition: dict,
        channel: dict,
        preset: AdjustmentPreset,
        att_value: int,
    ) -> AdjustmentReading:
        valid, message = validate_adjustment_channel(channel)
        if not valid:
            raise ValueError(message)
        value = validate_att_value(att_value)
        itg_no = int(channel["itg"])
        element_name = str(channel["ele"])
        seq = str(channel["seq"])

        try:
            if not self.controller.set_attenuator(itg_no, value):
                raise RuntimeError("Unable to set the attenuator")
            if not self.controller.reset():
                raise RuntimeError("Instrument reset failed")

            purge_sec = float(group_condition.get("purge_seq1", 0) or 0)
            source_selection = group_condition.get(f"source_seq{seq}", "1: Normal Spark")
            source_code = SequenceEngine._source_code_from_selection(source_selection)
            preburn_ms = int(group_condition.get(f"preburn_seq{seq}", 0) or 0)

            if not self.controller.argon_purge(purge_sec):
                raise RuntimeError("Argon purge failed")
            if not self.controller.prespark(source_code, preburn_ms):
                raise RuntimeError("Prespark failed")

            results = self.controller.integrate(
                preset.integration_ms,
                [{"itg": itg_no, "ele": element_name}],
            )
            raw_value = results.get(element_name)
            if raw_value is None:
                raise RuntimeError("No intensity was returned for the selected channel")

            return AdjustmentReading(
                timestamp=time.time(),
                itg_no=itg_no,
                att_value=value,
                intensity=float(raw_value) / ADC_MAX_VALUE,
            )
        except Exception:
            self.shutdown()
            raise

    def shutdown(self) -> None:
        """Put the instrument in standby, ignoring cleanup return values."""
        try:
            self.controller.shutdown()
        except Exception:
            pass
