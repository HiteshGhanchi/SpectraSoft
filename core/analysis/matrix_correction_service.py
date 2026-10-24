"""Matrix-correction pairing and regression calculations."""

from __future__ import annotations

import math

from core.persistence.models import (
    AnalyticalGroup,
    WorkingCurve,
    WorkingCurveMeasurement,
    WorkingStandard,
)
from core.persistence.working_curve_repository import get_active_coefficients


def _key(value) -> str:
    return str(value or "").strip().upper()


def _float(value, default=None):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if number == number and abs(number) != float("inf") else default


def _apply_curve(intensity: float, coefficients: dict) -> float:
    a = _float(coefficients.get("a"), None)
    b = _float(coefficients.get("b"), None)
    c = _float(coefficients.get("c"), None)
    d = _float(coefficients.get("d"), None)
    if any(value is None for value in (a, b, c, d)):
        raise ValueError("Working-curve coefficients must be finite")
    if a is None or b is None or c is None or d is None:
        raise ValueError("Working-curve coefficients must be finite")
    a, b, c, d = float(a), float(b), float(c), float(d)
    try:
        result = a * intensity**3 + b * intensity**2 + c * intensity + d
    except OverflowError as error:
        raise ValueError("Working-curve result must be finite") from error
    if not math.isfinite(result):
        raise ValueError("Working-curve result must be finite")
    return result


def _legacy_coefficients(group: AnalyticalGroup, element: str) -> dict | None:
    data = group.page_05_wc or {}
    rows = data.get("coefficients", []) if isinstance(data, dict) else []
    for row in rows if isinstance(rows, list) else []:
        keys = [row.get("element"), row.get("name"), row.get("ele")]
        if any(_key(value) == _key(element) for value in keys):
            return row
    return None


def build_matrix_pairs(
    session,
    group_id: int,
    target_element: str,
    interfering_element: str,
    working_curve_id: int | None = None,
) -> list[dict]:
    """Build certified target/interfering pairs from normalized calibration data."""
    target_key = _key(target_element)
    interfering_key = _key(interfering_element)
    if not target_key or not interfering_key or target_key == interfering_key:
        return []

    group = session.get(AnalyticalGroup, group_id)
    if group is None:
        return []

    curve = None
    coefficients = None
    source_curve_id = working_curve_id
    if working_curve_id is not None:
        curve = session.get(WorkingCurve, working_curve_id)
        if curve is None or curve.analytical_group_id != group_id:
            raise ValueError("Selected working curve does not belong to this group")
        if _key(curve.element_key) != target_key:
            raise ValueError("Selected working curve does not match target element")
        if not curve.coefficients:
            raise ValueError("Selected working curve has no coefficients")
        coefficient = curve.coefficients[0]
        coefficients = {"a": coefficient.a, "b": coefficient.b, "c": coefficient.c, "d": coefficient.d}
    else:
        active = get_active_coefficients(session, group_id, target_key)
        if active is not None:
            coefficients = active["coefficients"]
            source_curve_id = active["curve_id"]
        else:
            normalized_curve_exists = (
                session.query(WorkingCurve)
                .filter_by(analytical_group_id=group_id, element_key=target_key)
                .count()
                > 0
            )
            if normalized_curve_exists:
                raise ValueError("No active normalized working curve exists for target element")
            coefficients = _legacy_coefficients(group, target_key)

    if coefficients is None:
        return []

    standards = {
        standard.id: standard
        for standard in session.query(WorkingStandard)
        .filter_by(analytical_group_id=group_id, active=True)
        .all()
    }
    measurements = (
        session.query(WorkingCurveMeasurement)
        .filter_by(analytical_group_id=group_id)
        .all()
    )
    pairs = []
    for measurement in measurements:
        standard = standards.get(measurement.standard_id)
        if standard is None or _key(measurement.element_key) != target_key:
            continue
        values = {_key(value.element_key): value.known_value for value in standard.values}
        target_true = _float(values.get(target_key))
        interfering_true = _float(values.get(interfering_key))
        intensity = _float(measurement.corrected_intensity)
        if target_true is None or interfering_true is None or intensity is None:
            if (
                (target_key in values and target_true is None)
                or (interfering_key in values and interfering_true is None)
                or intensity is None
            ):
                raise ValueError("Matrix calibration values must be finite")
            continue
        c0 = _apply_curve(intensity, coefficients)
        pairs.append({
            "sample": standard.sample_name,
            "c0": c0,
            "true": target_true,
            "interfering": interfering_true,
            "error": target_true - c0,
            "working_curve_id": source_curve_id,
        })
    return sorted(pairs, key=lambda pair: pair["sample"])


def predict_matrix_corrected(pair: dict, coefficient: float, correction_type: str) -> float:
    c0 = _float(pair.get("c0"))
    interfering = _float(pair.get("interfering"))
    coefficient_value = _float(coefficient)
    if c0 is None or interfering is None or coefficient_value is None:
        raise ValueError("Matrix prediction values must be finite")
    kind = str(correction_type or "").strip().upper()
    if kind == "L":
        result = c0 + coefficient_value * interfering
    elif kind == "D":
        result = c0 * (1.0 + coefficient_value * interfering)
    else:
        raise ValueError("Matrix correction type must be L or D")
    if not math.isfinite(result):
        raise ValueError("Matrix prediction values must be finite")
    return result


def calculate_matrix_coefficient(pairs: list[dict], correction_type: str) -> dict:
    kind = str(correction_type or "").strip().upper()
    if kind not in {"L", "D"}:
        raise ValueError("Matrix correction type must be L or D")
    if not pairs:
        raise ValueError("No valid matrix pairs")

    for pair in pairs:
        for field in ("c0", "true", "interfering"):
            if _float(pair.get(field)) is None:
                raise ValueError("Matrix pair values must be finite")

    numerator = 0.0
    denominator = 0.0
    for pair in pairs:
        c0 = float(pair["c0"])
        cj = float(pair["interfering"])
        error_value = pair.get("error")
        error = float(pair["true"]) - c0 if error_value is None else _float(error_value)
        if error is None:
            raise ValueError("Matrix pair values must be finite")
        x = cj if kind == "L" else c0 * cj
        numerator += x * error
        denominator += x * x
        if not math.isfinite(numerator) or not math.isfinite(denominator):
            raise ValueError("Matrix coefficient values must be finite")
    if abs(denominator) < 1e-12:
        raise ValueError("Matrix coefficient denominator is zero")

    coefficient = numerator / denominator
    if not math.isfinite(coefficient):
        raise ValueError("Matrix coefficient must be finite")
    points = []
    for pair in pairs:
        predicted = predict_matrix_corrected(pair, coefficient, kind)
        residual = float(pair["true"]) - predicted
        if not math.isfinite(predicted) or not math.isfinite(residual):
            raise ValueError("Matrix fit values must be finite")
        points.append({**pair, "predicted": predicted, "residual": residual})

    mean_true = sum(float(pair["true"]) for pair in pairs) / len(pairs)
    ss_res = sum(point["residual"] ** 2 for point in points)
    ss_tot = sum((float(pair["true"]) - mean_true) ** 2 for pair in pairs)
    r2 = None if ss_tot < 1e-12 else 1.0 - (ss_res / ss_tot)
    rmse = (ss_res / len(points)) ** 0.5
    if r2 is not None and not math.isfinite(r2):
        raise ValueError("Matrix fit statistics must be finite")
    if not math.isfinite(rmse):
        raise ValueError("Matrix fit statistics must be finite")
    return {
        "coefficient": coefficient,
        "point_count": len(points),
        "r2": r2,
        "rmse": rmse,
        "points": points,
    }
