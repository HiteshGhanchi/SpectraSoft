"""Persistence and statistics for filed analytical results."""

from __future__ import annotations

from statistics import mean, pstdev

from core.persistence.models import AnalysisResult


def file_analysis_result(
    session,
    group_id: int,
    job: str,
    sample_name: str,
    burns: list[dict],
    averages: dict,
    final_concentrations: dict,
    flags: dict,
    method_snapshot: dict,
) -> AnalysisResult:
    if not str(sample_name or "").strip():
        raise ValueError("Sample name is required")
    result = AnalysisResult(
        analytical_group_id=group_id,
        job=str(job).strip().upper(),
        sample_name=str(sample_name).strip(),
        burns=burns or [],
        averages=averages or {},
        final_concentrations=final_concentrations or {},
        flags=flags or {},
        method_snapshot=method_snapshot or {},
    )
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def list_analysis_results(
    session,
    group_id: int,
    job: str | None = None,
    sample_name: str | None = None,
) -> list[AnalysisResult]:
    query = session.query(AnalysisResult).filter(
        AnalysisResult.analytical_group_id == group_id
    )
    if job:
        query = query.filter(AnalysisResult.job == str(job).strip().upper())
    if sample_name:
        query = query.filter(AnalysisResult.sample_name == str(sample_name).strip())
    return query.order_by(AnalysisResult.occurred_at.desc(), AnalysisResult.id.desc()).all()


def summarize_results(
    session, group_id: int, element: str, job: str | None = None
) -> dict:
    values = []
    for result in list_analysis_results(session, group_id, job=job):
        value = (result.final_concentrations or {}).get(element)
        try:
            values.append(float(value))
        except (TypeError, ValueError):
            continue
    if not values:
        return {"count": 0, "average": None, "range": None, "stddev": None, "cp": None, "cpk": None}
    return {
        "count": len(values),
        "average": mean(values),
        "range": max(values) - min(values),
        "stddev": pstdev(values) if len(values) > 1 else 0.0,
        "cp": None,
        "cpk": None,
    }
