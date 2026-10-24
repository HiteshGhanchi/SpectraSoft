"""Load and seed the reference data shipped with the application."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from import_data.constants import (
    ELEMENT_CHANNEL_COUNT,
    ELEMENT_NAME_MAX_LENGTH,
    SOURCE_CODE_COUNT,
    SOURCE_CODE_MAX,
    SOURCE_CODE_MIN,
    SOURCE_CODE_NAME_MAX_LENGTH,
    WAVELENGTH_MAX_LENGTH,
)


def _import_data_dir() -> Path:
    """Return the import-data directory next to the application source."""
    return Path(__file__).resolve().parents[2] / "import_data"


def _load_rows(filename: str, key: str) -> list[dict[str, Any]]:
    path = _import_data_dir() / filename
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    rows = payload.get(key)
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a '{key}' list.")
    return rows


def load_master_element_rows() -> list[dict[str, Any]]:
    """Load and validate the shipped master-element rows."""
    rows = _load_rows("master_elements.json", "master_elements")
    expected = set(range(1, ELEMENT_CHANNEL_COUNT + 1))
    actual = {int(row.get("itg_no", -1)) for row in rows}
    if len(rows) != ELEMENT_CHANNEL_COUNT or actual != expected:
        raise ValueError(
            "master_elements.json must contain exactly one row for every "
            f"ITG number 1-{ELEMENT_CHANNEL_COUNT}."
        )

    validated = []
    for row in rows:
        name = str(row.get("ele_name") or "").strip()
        wavelength = str(row.get("wavelength") or "").strip()
        if len(name) > ELEMENT_NAME_MAX_LENGTH:
            raise ValueError(f"Element name is longer than {ELEMENT_NAME_MAX_LENGTH} characters.")
        if len(wavelength) > WAVELENGTH_MAX_LENGTH:
            raise ValueError(f"Wavelength is longer than {WAVELENGTH_MAX_LENGTH} characters.")
        validated.append({
            "itg_no": int(row["itg_no"]),
            "ele_name": name,
            "wavelength": wavelength,
        })
    return sorted(validated, key=lambda row: row["itg_no"])


def load_source_code_rows() -> list[dict[str, Any]]:
    """Load and validate the shipped hexadecimal source-code rows."""
    rows = _load_rows("source_codes.json", "source_codes")
    expected = set(range(SOURCE_CODE_MIN, SOURCE_CODE_MAX + 1))
    actual = {int(row.get("entry_no", -1)) for row in rows}
    if len(rows) != SOURCE_CODE_COUNT or actual != expected:
        raise ValueError(
            "source_codes.json must contain exactly one row for every "
            f"source code 0x{SOURCE_CODE_MIN:X}-0x{SOURCE_CODE_MAX:X}."
        )

    validated = []
    for row in rows:
        entry_no = int(row["entry_no"])
        name = str(row.get("name") or "").strip()
        if len(name) > SOURCE_CODE_NAME_MAX_LENGTH:
            raise ValueError(
                f"Source-code name is longer than {SOURCE_CODE_NAME_MAX_LENGTH} characters."
            )
        validated.append({"entry_no": entry_no, "name": name})
    return sorted(validated, key=lambda row: row["entry_no"])


def _master_elements_are_uninitialized(rows: Iterable[Any]) -> bool:
    rows = list(rows)
    return not rows or all(
        not (row.ele_name or "").strip() and not (row.wavelength or "").strip()
        for row in rows
    )


def _source_codes_are_uninitialized(rows: Iterable[Any]) -> bool:
    rows = list(rows)
    return not rows or all(not (row.name or "").strip() for row in rows)


def seed_reference_data(session) -> bool:
    """Seed shipped reference data without overwriting configured data.

    A table is seeded only when it is empty or contains only blank placeholder
    rows left by an older application version. Existing nonblank user edits are
    preserved.
    """
    from core.persistence.models import MasterElement, SourceCode

    changed = False
    master_rows = session.query(MasterElement).order_by(MasterElement.itg_no).all()
    if _master_elements_are_uninitialized(master_rows):
        session.query(MasterElement).delete()
        session.add_all(MasterElement(**row) for row in load_master_element_rows())
        changed = True

    source_rows = session.query(SourceCode).order_by(SourceCode.entry_no).all()
    if _source_codes_are_uninitialized(source_rows):
        session.query(SourceCode).delete()
        session.add_all(SourceCode(**row) for row in load_source_code_rows())
        changed = True

    if changed:
        session.commit()
    return changed
