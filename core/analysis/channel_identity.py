"""Stable identity helpers for analytical rows and hardware channels."""

from __future__ import annotations

from typing import Iterable


def analytical_row_number(entry: dict, fallback_index: int = 0) -> int:
    """Return the persisted AR number, falling back to its row position."""
    try:
        value = int(entry.get("ar_no", 0))
    except (AttributeError, TypeError, ValueError):
        value = 0

    return value if value > 0 else fallback_index + 1


def channel_result_key(entry: dict, fallback_index: int = 0) -> str:
    """Return the unique software key for one analytical row.

    AR identifies the analytical result. ITG remains the physical channel
    selector and is deliberately not used as the result dictionary key.
    """
    try:
        explicit_ar = int(entry.get("ar_no", 0))
    except (AttributeError, TypeError, ValueError):
        explicit_ar = 0

    if explicit_ar > 0:
        return f"AR:{explicit_ar}"

    return channel_display_name(entry, fallback_index)


def channel_display_name(entry: dict, fallback_index: int = 0) -> str:
    """Return the user-facing label for one analytical row."""
    name = str(entry.get("name", "")).strip()
    element = str(entry.get("ele", "")).strip()
    if name:
        return name
    if element:
        return element

    try:
        itg = int(entry.get("itg", 0))
    except (AttributeError, TypeError, ValueError):
        itg = 0

    return f"ITG{itg}" if itg > 0 else f"Channel {fallback_index + 1}"


def normalized_channel_rows(rows: Iterable[dict] | None) -> list[dict]:
    """Copy channel rows and add backward-compatible explicit AR numbers."""
    normalized = []
    for index, entry in enumerate(rows or []):
        if not isinstance(entry, dict):
            continue
        row = dict(entry)
        row["ar_no"] = analytical_row_number(row, index)
        normalized.append(row)
    return normalized
