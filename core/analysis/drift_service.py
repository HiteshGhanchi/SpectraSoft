"""Pure drift-storage and recalibration calculations."""

from __future__ import annotations


DEFAULT_DRIFT_ROW = {
    "h_sample": "",
    "l_sample": "",
    "k_sample": "",
    "h_target": "0.00000",
    "l_target": "0.00000",
    "k_target": "0.00000",
    "alpha": "1.0000",
    "beta": "0.00000",
    "k_coeff": "1.0000",
}


def normalize_drift_row(row: dict | None) -> dict:
    """Return a row with the manual-defined drift defaults filled in."""
    source = dict(row or {})
    normalized = dict(source)
    for key, default in DEFAULT_DRIFT_ROW.items():
        value = str(source.get(key, "")).strip()
        normalized[key] = value or default
    return normalized


def file_target_values(rows: list[dict], sample: str, averages: dict) -> int:
    """File averaged Job 8 values into matching H/L/K target fields."""
    sample_key = str(sample or "").strip().upper()
    if not sample_key or sample_key == "*":
        return 0

    updated = 0
    for row in rows:
        element = str(row.get("name", "")).strip()
        if not element or element not in averages:
            continue

        value = f"{float(averages[element]):.5f}"
        for sample_key_name, target_key in (
            ("h_sample", "h_target"),
            ("l_sample", "l_target"),
            ("k_sample", "k_target"),
        ):
            configured_sample = str(row.get(sample_key_name, "")).strip().upper()
            if configured_sample and configured_sample != "*" and configured_sample == sample_key:
                row[target_key] = value
                updated += 1
    return updated


def calculate_alpha_beta(
    h_target: float,
    l_target: float,
    h_intensity: float,
    l_intensity: float,
) -> tuple[float, float]:
    """Calculate two-point drift correction coefficients."""
    denominator = float(h_intensity) - float(l_intensity)
    if denominator == 0.0:
        raise ValueError("H and L intensities must be different")
    alpha = (float(h_target) - float(l_target)) / denominator
    beta = float(h_target) - (alpha * float(h_intensity))
    return alpha, beta


def calculate_k(
    k_target: float,
    k_intensity: float,
    alpha: float,
    beta: float,
) -> float:
    """Calculate one-point drift scale k."""
    denominator = (float(alpha) * float(k_intensity)) + float(beta)
    if denominator == 0.0:
        raise ValueError("Corrected K intensity must not be zero")
    return float(k_target) / denominator
