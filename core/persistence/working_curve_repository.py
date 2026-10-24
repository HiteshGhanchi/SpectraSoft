"""Repository and migration helpers for normalized working-curve data."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func

from core.persistence.models import (
    AnalyticalGroup,
    WorkingCurve,
    WorkingCurveCoefficient,
    WorkingCurveMeasurement,
    WorkingStandard,
    WorkingStandardValue,
)


def _key(value) -> str:
    return str(value or "").strip().upper()


def list_standards(session, group_id: int) -> list[WorkingStandard]:
    return (
        session.query(WorkingStandard)
        .filter(WorkingStandard.analytical_group_id == group_id)
        .order_by(WorkingStandard.sample_name)
        .all()
    )


def upsert_standard(
    session, group_id: int, sample_name: str, values: dict
) -> WorkingStandard:
    sample = _key(sample_name)
    if not sample:
        raise ValueError("Working-curve standard name is required")

    standard = (
        session.query(WorkingStandard)
        .filter_by(analytical_group_id=group_id, sample_name=sample)
        .one_or_none()
    )
    if standard is None:
        standard = WorkingStandard(analytical_group_id=group_id, sample_name=sample)
        session.add(standard)
        session.flush()

    normalized_values = {
        _key(element): float(value)
        for element, value in (values or {}).items()
        if _key(element)
    }
    existing = {value.element_key: value for value in standard.values}
    for element, value in normalized_values.items():
        row = existing.get(element)
        if row is None:
            standard.values.append(
                WorkingStandardValue(element_key=element, known_value=value)
            )
        else:
            row.known_value = value

    session.commit()
    session.refresh(standard)
    return standard


def sync_standards(session, group_id: int, entries: list[dict]) -> list[WorkingStandard]:
    """Make normalized standards exactly match the current editor contents."""
    desired = {}
    for entry in entries or []:
        sample = _key(entry.get("sample"))
        if sample:
            desired[sample] = entry.get("values", {})

    existing = {
        standard.sample_name: standard
        for standard in list_standards(session, group_id)
    }
    for sample, values in desired.items():
        standard = upsert_standard(session, group_id, sample, values)
        desired_keys = {_key(element) for element in (values or {})}
        for value in list(standard.values):
            if value.element_key not in desired_keys:
                session.delete(value)

    for sample, standard in existing.items():
        if sample not in desired:
            session.delete(standard)
    session.commit()
    return list_standards(session, group_id)


def _get_standard(session, group_id: int, sample_name: str) -> WorkingStandard:
    sample = _key(sample_name)
    standard = (
        session.query(WorkingStandard)
        .filter_by(analytical_group_id=group_id, sample_name=sample)
        .one_or_none()
    )
    if standard is None:
        standard = upsert_standard(session, group_id, sample, {})
    return standard


def upsert_measurement(
    session,
    group_id: int,
    sample_name: str,
    intensities: dict,
    burn_count: int,
) -> list[WorkingCurveMeasurement]:
    """Store the latest Job 7 corrected intensity for each standard element."""
    standard = _get_standard(session, group_id, sample_name)
    existing = {
        row.element_key: row
        for row in session.query(WorkingCurveMeasurement)
        .filter_by(standard_id=standard.id)
        .all()
    }
    updated_rows = []
    for element, value in (intensities or {}).items():
        element_key = _key(element)
        if not element_key:
            continue
        row = existing.get(element_key)
        if row is None:
            row = WorkingCurveMeasurement(
                analytical_group_id=group_id,
                standard_id=standard.id,
                element_key=element_key,
            )
            session.add(row)
        row.corrected_intensity = float(value)
        row.burn_count = int(burn_count)
        row.measured_at = datetime.now(timezone.utc)
        updated_rows.append(row)

    session.commit()
    return updated_rows


def create_curve_version(
    session,
    group_id: int,
    element: str,
    curve_type: str,
    coefficients: dict,
    fit_stats: dict,
    source_point_count: int,
    name: str | None = None,
) -> WorkingCurve:
    element_key = _key(element)
    if not element_key:
        raise ValueError("Working-curve element is required")
    curve = WorkingCurve(
        analytical_group_id=group_id,
        element_key=element_key,
        name=name or f"{element_key} {curve_type} curve",
        curve_type=str(curve_type).strip().lower(),
        status="inactive",
        point_count=int(source_point_count),
        r2=fit_stats.get("r2"),
        rmse=fit_stats.get("rmse"),
    )
    curve.coefficients.append(
        WorkingCurveCoefficient(
            a=float(coefficients.get("a", 0.0)),
            b=float(coefficients.get("b", 0.0)),
            c=float(coefficients.get("c", 1.0)),
            d=float(coefficients.get("d", 0.0)),
        )
    )
    session.add(curve)
    session.commit()
    session.refresh(curve)
    return curve


def activate_curve(session, curve_id: int) -> WorkingCurve:
    curve = session.get(WorkingCurve, curve_id)
    if curve is None:
        raise ValueError(f"Working curve {curve_id} does not exist")
    (
        session.query(WorkingCurve)
        .filter(
            WorkingCurve.analytical_group_id == curve.analytical_group_id,
            func.upper(WorkingCurve.element_key) == curve.element_key.upper(),
            WorkingCurve.id != curve.id,
            WorkingCurve.status == "active",
        )
        .update({"status": "inactive"}, synchronize_session=False)
    )
    curve.status = "active"
    curve.retired_at = None
    session.commit()
    session.refresh(curve)
    return curve


def retire_curve(session, curve_id: int) -> WorkingCurve:
    curve = session.get(WorkingCurve, curve_id)
    if curve is None:
        raise ValueError(f"Working curve {curve_id} does not exist")
    curve.status = "retired"
    curve.retired_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(curve)
    return curve


def update_active_curve_coefficients(
    session, group_id: int, element: str, coefficients: dict
) -> WorkingCurve | None:
    curve = (
        session.query(WorkingCurve)
        .filter_by(
            analytical_group_id=group_id,
            element_key=_key(element),
            status="active",
        )
        .first()
    )
    if curve is None or not curve.coefficients:
        return None
    coefficient = curve.coefficients[0]
    coefficient.a = float(coefficients.get("a", coefficient.a))
    coefficient.b = float(coefficients.get("b", coefficient.b))
    coefficient.c = float(coefficients.get("c", coefficient.c))
    coefficient.d = float(coefficients.get("d", coefficient.d))
    session.commit()
    session.refresh(curve)
    return curve


def get_active_coefficients(session, group_id: int, element: str) -> dict | None:
    curve = (
        session.query(WorkingCurve)
        .filter(
            WorkingCurve.analytical_group_id == group_id,
            func.upper(WorkingCurve.element_key) == _key(element),
            WorkingCurve.status == "active",
        )
        .order_by(WorkingCurve.created_at.desc(), WorkingCurve.id.desc())
        .first()
    )
    if curve is None or not curve.coefficients:
        return None
    coefficient = curve.coefficients[0]
    return {
        "curve_id": curve.id,
        "curve_type": curve.curve_type,
        "name": curve.name,
        "r2": curve.r2,
        "rmse": curve.rmse,
        "point_count": curve.point_count,
        "coefficients": {
            "a": coefficient.a,
            "b": coefficient.b,
            "c": coefficient.c,
            "d": coefficient.d,
        },
    }


def list_curves(session, group_id: int, element: str | None = None) -> list[WorkingCurve]:
    query = session.query(WorkingCurve).filter(WorkingCurve.analytical_group_id == group_id)
    if element:
        query = query.filter(func.upper(WorkingCurve.element_key) == _key(element))
    return query.order_by(WorkingCurve.element_key, WorkingCurve.created_at.desc()).all()


def _legacy_curve_type(row: dict) -> str:
    try:
        if float(row.get("a", 0)) != 0:
            return "cubic"
        if float(row.get("b", 0)) != 0:
            return "quadratic"
    except (TypeError, ValueError):
        pass
    return "linear"


def migrate_working_curve_json(session) -> dict:
    """Import legacy group JSON into normalized records once."""
    counts = {"standards": 0, "measurements": 0, "curves": 0}
    for group in session.query(AnalyticalGroup).all():
        standards_data = group.page_05_chemical_standards or {}
        for entry in standards_data.get("standards", []) if isinstance(standards_data, dict) else []:
            sample = _key(entry.get("sample"))
            if not sample:
                continue
            exists = (
                session.query(WorkingStandard)
                .filter_by(analytical_group_id=group.id, sample_name=sample)
                .one_or_none()
            )
            if exists is None:
                upsert_standard(session, group.id, sample, entry.get("values", {}))
                counts["standards"] += 1

        measurements_data = group.page_05_wc_measurements or {}
        for entry in measurements_data.get("measurements", []) if isinstance(measurements_data, dict) else []:
            sample = _key(entry.get("sample"))
            if not sample:
                continue
            standard = _get_standard(session, group.id, sample)
            existing = (
                session.query(WorkingCurveMeasurement)
                .filter_by(standard_id=standard.id)
                .count()
            )
            if existing == 0:
                upsert_measurement(
                    session,
                    group.id,
                    sample,
                    entry.get("intensities", {}),
                    entry.get("burns", 0),
                )
                counts["measurements"] += 1

        page5 = group.page_05_wc or {}
        legacy_rows = page5.get("coefficients", []) if isinstance(page5, dict) else []
        for row in legacy_rows if isinstance(legacy_rows, list) else []:
            element = _key(row.get("element") or row.get("name") or row.get("ele"))
            if not element:
                continue
            existing = (
                session.query(WorkingCurve)
                .filter_by(analytical_group_id=group.id, element_key=element)
                .count()
            )
            if existing:
                continue
            curve = create_curve_version(
                session,
                group.id,
                element,
                _legacy_curve_type(row),
                row,
                {},
                0,
                name="Imported Page 5",
            )
            activate_curve(session, curve.id)
            counts["curves"] += 1

    return counts
