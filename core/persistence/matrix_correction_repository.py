"""Repository and migration helpers for normalized matrix corrections."""

from __future__ import annotations

from datetime import datetime, timezone
import math
from sqlalchemy import case

from core.persistence.models import AnalyticalGroup, MatrixCorrection, WorkingCurve


def _key(value) -> str:
    return str(value or "").strip().upper()


def _correction_type(value) -> str:
    value = str(value or "").strip().upper()
    if value not in {"L", "D"}:
        raise ValueError("Matrix correction type must be L or D")
    return value


def create_matrix_candidate(
    session,
    group_id: int,
    target_element: str,
    interfering_element: str,
    correction_type: str,
    coefficient: float,
    *,
    source_working_curve_id: int | None = None,
    point_count: int = 0,
    fit_stats: dict | None = None,
    version_name: str | None = None,
) -> MatrixCorrection:
    target_key = _key(target_element)
    interfering_key = _key(interfering_element)
    if not target_key or not interfering_key:
        raise ValueError("Target and interfering elements are required")
    if target_key == interfering_key:
        raise ValueError("Target and interfering elements must be different")

    if not math.isfinite(float(coefficient)):
        raise ValueError("Matrix coefficient must be finite")
    if source_working_curve_id is not None:
        curve = session.get(WorkingCurve, source_working_curve_id)
        if curve is None:
            raise ValueError("Source working curve does not exist")
        if curve.analytical_group_id != group_id:
            raise ValueError("Source working curve belongs to another group")
        if _key(curve.element_key) != target_key:
            raise ValueError("Source working curve does not match target element")

    correction_key = _correction_type(correction_type)
    stats = fit_stats or {}
    r2 = stats.get("r2")
    rmse = stats.get("rmse")
    if r2 is not None and not math.isfinite(float(r2)):
        raise ValueError("Matrix fit statistics must be finite")
    if rmse is not None and not math.isfinite(float(rmse)):
        raise ValueError("Matrix fit statistics must be finite")
    candidate = MatrixCorrection(
        analytical_group_id=group_id,
        target_element_key=target_key,
        interfering_element_key=interfering_key,
        correction_type=correction_key,
        coefficient=float(coefficient),
        status="inactive",
        version_name=version_name or f"{target_key}-{interfering_key} {correction_key}",
        source_working_curve_id=source_working_curve_id,
        point_count=int(point_count),
        r2=r2,
        rmse=rmse,
    )
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return candidate


def list_matrix_corrections(
    session, group_id: int, target_element: str | None = None
) -> list[MatrixCorrection]:
    query = session.query(MatrixCorrection).filter(
        MatrixCorrection.analytical_group_id == group_id
    )
    if target_element:
        query = query.filter(
            MatrixCorrection.target_element_key == _key(target_element)
        )
    return query.order_by(
        case(
            (MatrixCorrection.status == "active", 0),
            (MatrixCorrection.status == "inactive", 1),
            else_=2,
        ),
        MatrixCorrection.target_element_key,
        MatrixCorrection.interfering_element_key,
        MatrixCorrection.correction_type,
        MatrixCorrection.created_at.desc(),
        MatrixCorrection.id.desc(),
    ).all()


def get_active_matrix_corrections(
    session, group_id: int, target_element: str | None = None
) -> list[MatrixCorrection]:
    query = session.query(MatrixCorrection).filter(
        MatrixCorrection.analytical_group_id == group_id,
        MatrixCorrection.status == "active",
    )
    if target_element:
        query = query.filter(
            MatrixCorrection.target_element_key == _key(target_element)
        )
    return query.order_by(
        MatrixCorrection.target_element_key,
        MatrixCorrection.interfering_element_key,
        MatrixCorrection.correction_type,
    ).all()


def get_active_matrix_correction_dicts(session, group_id: int) -> list[dict]:
    """Return active normalized rows in the shape consumed by CorrectionEngine."""
    return [
        {
            "target_element_key": row.target_element_key,
            "interfering_element_key": row.interfering_element_key,
            "correction_type": row.correction_type,
            "coefficient": row.coefficient,
            "matrix_correction_id": row.id,
        }
        for row in get_active_matrix_corrections(session, group_id)
    ]


def get_authoritative_matrix_correction_keys(session, group_id: int) -> list[list[str]]:
    """Return every normalized pair/type key, including inactive and retired rows."""
    return [
        [row.target_element_key, row.interfering_element_key, row.correction_type]
        for row in list_matrix_corrections(session, group_id)
        if row.status in {"active", "retired"}
    ]


def activate_matrix_correction(session, correction_id: int) -> MatrixCorrection:
    correction = session.get(MatrixCorrection, correction_id)
    if correction is None:
        raise ValueError(f"Matrix correction {correction_id} does not exist")

    session.query(MatrixCorrection).filter(
        MatrixCorrection.analytical_group_id == correction.analytical_group_id,
        MatrixCorrection.target_element_key == correction.target_element_key,
        MatrixCorrection.interfering_element_key == correction.interfering_element_key,
        MatrixCorrection.correction_type == correction.correction_type,
        MatrixCorrection.id != correction.id,
        MatrixCorrection.status == "active",
    ).update({"status": "inactive"}, synchronize_session=False)

    correction.status = "active"
    correction.retired_at = None
    session.commit()
    session.refresh(correction)
    return correction


def retire_matrix_correction(session, correction_id: int) -> MatrixCorrection:
    correction = session.get(MatrixCorrection, correction_id)
    if correction is None:
        raise ValueError(f"Matrix correction {correction_id} does not exist")
    correction.status = "retired"
    correction.retired_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(correction)
    return correction


def update_active_matrix_coefficient(
    session, correction_id: int, coefficient: float
) -> MatrixCorrection:
    correction = session.get(MatrixCorrection, correction_id)
    if correction is None:
        raise ValueError(f"Matrix correction {correction_id} does not exist")
    if correction.status != "active":
        raise ValueError("Only an active matrix correction can be edited")
    value = float(coefficient)
    if not math.isfinite(value):
        raise ValueError("Matrix coefficient must be finite")
    correction.coefficient = value
    session.commit()
    session.refresh(correction)
    return correction


def _legacy_row_key(row: dict) -> tuple[str, str, str] | None:
    target = _key(row.get("target_element") or row.get("target_name"))
    interfering = _key(
        row.get("interfering_element") or row.get("interfering_name")
    )
    correction_type = str(row.get("type", "")).strip().upper()
    if not target or not interfering or correction_type not in {"L", "D"}:
        return None
    return target, interfering, correction_type


def migrate_matrix_json(session) -> dict:
    """Import legacy Page 6 rows into normalized active records once."""
    counts = {"corrections": 0}
    for group in session.query(AnalyticalGroup).all():
        data = group.page_06_matrix or {}
        rows = data.get("corrections", []) if isinstance(data, dict) else []
        if not isinstance(rows, list):
            continue

        for row in rows:
            if not isinstance(row, dict):
                continue
            identity = _legacy_row_key(row)
            if identity is None:
                continue
            target, interfering, correction_type = identity
            exists = session.query(MatrixCorrection).filter_by(
                analytical_group_id=group.id,
                target_element_key=target,
                interfering_element_key=interfering,
                correction_type=correction_type,
            ).first()
            if exists is not None:
                continue

            create_matrix_candidate(
                session,
                group.id,
                target,
                interfering,
                correction_type,
                float(row.get("coeff", 0.0)),
                point_count=0,
                version_name="Imported Page 6",
            )
            imported = session.query(MatrixCorrection).filter_by(
                analytical_group_id=group.id,
                target_element_key=target,
                interfering_element_key=interfering,
                correction_type=correction_type,
            ).order_by(MatrixCorrection.id.desc()).first()
            activate_matrix_correction(session, imported.id)
            counts["corrections"] += 1

    return counts
