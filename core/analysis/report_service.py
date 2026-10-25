"""Read-only reporting calculations for filed analytical results.

The report layer deliberately works on ``AnalysisResult`` objects rather than
re-running analysis.  This keeps reports traceable to the stored burn data and
method snapshot and makes the calculations usable by both Qt and tests.
"""

from __future__ import annotations

import csv
import io
import json
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from statistics import mean, stdev
from typing import Iterable


@dataclass(frozen=True)
class ReportFilters:
    """Dates are inclusive reporting days (07:00 UTC to next 07:00 UTC).

    Explicit datetimes instead denote exact inclusive instants. SQLite stores
    the existing server-generated timestamps as naive UTC.
    """

    start: date | datetime | None = None
    end: date | datetime | None = None
    sample_name: str = ""
    job: str = ""
    product_name: str = ""


def _as_datetime(value: date | datetime | None, *, end: bool = False) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return _utc_naive(value)
    boundary = datetime.combine(value, time(7))
    return boundary + timedelta(days=1) - timedelta(microseconds=1) if end else boundary


def _utc_naive(value):
    return value.astimezone(timezone.utc).replace(tzinfo=None) if value.tzinfo else value


def _result_datetime(result) -> datetime:
    value = getattr(result, "occurred_at", None)
    return _utc_naive(value) if isinstance(value, datetime) else datetime.min


def reporting_day(result):
    occurred = _result_datetime(result)
    return (occurred - timedelta(hours=7)).date().isoformat() if occurred != datetime.min else "(date not recorded)"


def _normal_text(value) -> str:
    return str(value or "").strip()


def product_name(result) -> str:
    """Return a product/specification name when it was captured in the snapshot.

    Existing filed results have no dedicated product column.  The current
    filing path must capture ``method_snapshot['product_name']``. Master/type
    standard configuration does not identify the unknown sample's product.
    """

    snapshot = getattr(result, "method_snapshot", None) or {}
    if not isinstance(snapshot, dict):
        return ""
    value = snapshot.get("product_name")
    return value.strip() if isinstance(value, str) else ""


def filter_results(results: Iterable, filters: ReportFilters | None = None) -> list:
    """Apply date, sample, job, and product filters and return newest first."""

    filters = filters or ReportFilters()
    start = _as_datetime(filters.start)
    end = _as_datetime(filters.end, end=True)
    if start and end and start > end:
        raise ValueError("Start date must not be after end date.")
    sample = filters.sample_name.strip().casefold()
    job = filters.job.strip().upper()
    product = filters.product_name.strip().casefold()
    selected = []
    for result in results:
        occurred = _result_datetime(result)
        if start and occurred < start:
            continue
        if end and occurred > end:
            continue
        if sample and sample not in _normal_text(getattr(result, "sample_name", "")).casefold():
            continue
        if job and job != _normal_text(getattr(result, "job", "")).upper():
            continue
        if product and product not in product_name(result).casefold():
            continue
        selected.append(result)
    return sorted(selected, key=lambda item: (_result_datetime(item), getattr(item, "id", 0)), reverse=True)


def finite_number(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def numeric_values(values):
    return [number for value in values if (number := finite_number(value)) is not None]


def _numeric_values(results: Iterable, element: str) -> list[float]:
    return numeric_values((result.final_concentrations or {}).get(element) for result in results)


def validate_limits(lower, upper):
    if lower is None and upper is None:
        return None
    low, high = finite_number(lower), finite_number(upper)
    if low is None or high is None or low >= high:
        raise ValueError("Supply both finite specification limits with lower < upper, or leave both blank.")
    return low, high


def summarize_values(
    values: Iterable[float],
    lower_limit: float | None = None,
    upper_limit: float | None = None,
) -> dict:
    """Calculate manual-defined statistics and capability indices.

    Cp/Cpk are intentionally unavailable unless both finite, ordered limits
    are supplied and the sample standard deviation is non-zero.
    """

    numbers = numeric_values(values)
    limits = validate_limits(lower_limit, upper_limit)
    if not numbers:
        return {
            "count": 0, "average": None, "range": None, "stddev": None,
            "cp": None, "cpk": None, "lower_limit": lower_limit,
            "upper_limit": upper_limit, "over_limit": 0 if limits else None,
            "under_limit": 0 if limits else None,
        }
    average = mean(numbers)
    deviation = stdev(numbers) if len(numbers) > 1 else None
    cp = cpk = None
    if limits and deviation is not None and deviation > 0:
        lower, upper = limits
        cp = (upper - lower) / (6.0 * deviation)
        if average < lower or average > upper:
            cpk = 0.0
        else:
            cpk = min((upper - average) / (3.0 * deviation), (average - lower) / (3.0 * deviation))
    return {
        "count": len(numbers),
        "average": average,
        "range": max(numbers) - min(numbers),
        "stddev": deviation,
        "cp": cp,
        "cpk": cpk,
        "lower_limit": limits[0] if limits else None,
        "upper_limit": limits[1] if limits else None,
        "over_limit": sum(value > limits[1] for value in numbers) if limits else None,
        "under_limit": sum(value < limits[0] for value in numbers) if limits else None,
    }


def summarize_results(results: Iterable, element: str, lower_limit=None, upper_limit=None) -> dict:
    return summarize_values(_numeric_values(results, element), lower_limit, upper_limit)


def build_histogram(
    values: Iterable[float],
    lower_limit: float | None = None,
    upper_limit: float | None = None,
    bins: int = 10,
) -> dict:
    """Build counts and bin labels for a native Qt histogram widget."""

    numbers = numeric_values(values)
    bins = max(1, min(int(bins), 15))
    limits = validate_limits(lower_limit, upper_limit)
    bounds = numbers + list(limits or ())
    lower, upper = (min(bounds), max(bounds)) if bounds else (0.0, 1.0)
    if upper <= lower:
        pad = max(abs(lower) * 0.05, 0.5)
        lower -= pad
        upper += pad
    width = (upper - lower) / bins
    counts = [0] * bins
    for value in numbers:
        index = bins - 1 if value >= upper else int((value - lower) / width)
        counts[max(0, min(bins - 1, index))] += 1
    summary = summarize_values(numbers, lower_limit, upper_limit)
    return {
        "lower": lower,
        "upper": upper,
        "edges": [lower + width * index for index in range(bins + 1)],
        "counts": counts,
        "under_limit": summary["under_limit"],
        "over_limit": summary["over_limit"],
        "summary": summary,
    }


def _group_key(result, mode: str) -> str:
    mode = mode.lower().replace("_", "-")
    if mode in {"product", "standard", "specification"}:
        return product_name(result) or "(product not recorded)"
    if mode in {"sample", "sample-index", "sample index"}:
        return _normal_text(getattr(result, "sample_name", "")) or "(sample not recorded)"
    return reporting_day(result)


def daily_report(results: Iterable, mode: str = "group") -> list[dict]:
    """Return daily report rows grouped by day, product, or sample."""

    grouped = {}
    normalized_mode = mode.lower().replace("_", "-")
    for result in results:
        key = _group_key(result, mode)
        grouping_key = (reporting_day(result), key) if normalized_mode in {"group", "day", "daily"} else ("", key)
        grouped.setdefault(grouping_key, []).append(result)
    rows = []
    for (day, key), group in sorted(grouped.items()):
        elements = sorted({
            str(element)
            for result in group
            for element in (getattr(result, "final_concentrations", None) or {})
        })
        rows.append({
            "key": key,
            "day": day,
            "count": len(group),
            "jobs": sorted({_normal_text(getattr(result, "job", "")) for result in group}),
            "samples": sorted({_normal_text(getattr(result, "sample_name", "")) for result in group}),
            "elements": elements,
            "results": sorted(group, key=lambda item: (_result_datetime(item), getattr(item, "id", 0))),
        })
    return rows


def _trend_points(results, element):
    points = []
    for result in sorted(results, key=lambda item: (_result_datetime(item), item.id)):
        value = finite_number((result.final_concentrations or {}).get(element))
        burns = numeric_values(burn.get(element) for burn in result.burns or [] if isinstance(burn, dict))
        if value is None and not burns:
            continue
        points.append({
            "result": result, "occurred_at": _result_datetime(result),
            "sample_name": result.sample_name, "value": value,
            "xbar": mean(burns) if burns else None,
            "count": len(burns),
            "range": max(burns) - min(burns) if len(burns) > 1 else None,
            # Do not join different jobs, samples, products or historical methods.
            "series": (result.analytical_group_id, result.job, result.sample_name,
                       product_name(result), _json_value(result.method_snapshot)),
        })
    return points


def x_r_report(results: Iterable, element: str) -> dict:
    """One X-bar/R point per filed result, calculated from its actual burns.

    No inferred subgroups or statistical control limits: the manual only
    specifies product specification limits for the plotted concentration.
    """
    points = _trend_points(results, element)
    xbars = numeric_values(point["xbar"] for point in points)
    ranges = numeric_values(point["range"] for point in points)
    return {
        "points": points,
        "average_xbar": mean(xbars) if xbars else None,
        "average_range": mean(ranges) if ranges else None,
        "maximum": max(xbars) if xbars else None,
        "minimum": min(xbars) if xbars else None,
    }


def stability_report(results: Iterable, element: str) -> dict:
    points = [point for point in _trend_points(results, element) if point["value"] is not None]
    values = [point["value"] for point in points]
    summary = summarize_values(values)
    return {
        **summary,
        "points": points,
        "variance": summary["stddev"] ** 2 if summary["stddev"] is not None else None,
        "maximum": max(values) if values else None,
        "minimum": min(values) if values else None,
    }


def analytical_frequency(results: Iterable) -> dict:
    by_job: dict[str, int] = {}
    by_sample: dict[str, int] = {}
    by_product: dict[str, int] = {}
    by_day: dict[str, int] = {}
    result_list = list(results)
    for result in result_list:
        job = _normal_text(getattr(result, "job", "")) or "(unknown)"
        sample = _normal_text(getattr(result, "sample_name", "")) or "(unknown)"
        product = product_name(result) or "(not recorded)"
        day = reporting_day(result)
        for mapping, key in ((by_job, job), (by_sample, sample), (by_product, product), (by_day, day)):
            mapping[key] = mapping.get(key, 0) + 1
    return {"total": len(result_list), "burn_count": sum(len(result.burns or []) for result in result_list), "by_job": dict(sorted(by_job.items())), "by_sample": dict(sorted(by_sample.items())), "by_product": dict(sorted(by_product.items())), "by_day": dict(sorted(by_day.items()))}


def result_detail(result) -> dict:
    return {
        "id": getattr(result, "id", None),
        "analytical_group_id": getattr(result, "analytical_group_id", None),
        "occurred_at": getattr(result, "occurred_at", None),
        "job": getattr(result, "job", ""),
        "sample_name": getattr(result, "sample_name", ""),
        "product_name": product_name(result),
        "burns": getattr(result, "burns", None) or [],
        "averages": getattr(result, "averages", None) or {},
        "final_concentrations": getattr(result, "final_concentrations", None) or {},
        "flags": getattr(result, "flags", None) or {},
        "method_snapshot": getattr(result, "method_snapshot", None) or {},
    }


def _json_value(value) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def export_results_csv(results: Iterable, include_details: bool = True) -> str:
    """Return a CSV export suitable for saving or handing to a print view."""

    fields = ["id", "analytical_group_id", "occurred_at", "job", "sample_name", "product_name", "burns", "averages", "final_concentrations", "flags", "method_snapshot"]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for result in sorted(results, key=lambda item: (_result_datetime(item), getattr(item, "id", 0))):
        detail = result_detail(result)
        row = {key: detail.get(key, "") for key in fields}
        for key in ("burns", "averages", "final_concentrations", "flags", "method_snapshot"):
            row[key] = _json_value(row[key]) if include_details else ""
        row["occurred_at"] = str(row["occurred_at"] or "")
        writer.writerow(row)
    return output.getvalue()


CORRECTION_SCHEMA_NOTE = (
    "Stored-result modification is read-only until an immutable result correction "
    "table is integrated; the original AnalysisResult must remain unchanged."
)
