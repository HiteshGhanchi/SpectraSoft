"""Pure working-curve pairing, fitting, and fit-quality calculations."""

from __future__ import annotations


def _lookup(data: dict, key: str):
    target = str(key).strip().upper()
    for candidate, value in (data or {}).items():
        if str(candidate).strip().upper() == target:
            return value
    return None


def build_calibration_pairs(measurements: list, standards: list, element: str) -> list[dict]:
    intensity_by_sample = {}
    chemical_by_sample = {}
    for entry in measurements or []:
        sample = str(entry.get("sample", "")).strip().upper()
        intensities = entry.get("intensities", {})
        value = _lookup(intensities, element) if isinstance(intensities, dict) else None
        if sample and value is not None:
            try:
                intensity_by_sample[sample] = float(value)
            except (TypeError, ValueError):
                pass
    for entry in standards or []:
        sample = str(entry.get("sample", "")).strip().upper()
        values = entry.get("values", {})
        value = _lookup(values, element) if isinstance(values, dict) else None
        if sample and value is not None:
            try:
                chemical_by_sample[sample] = float(value)
            except (TypeError, ValueError):
                pass
    return [
        {
            "sample": sample,
            "intensity": intensity_by_sample[sample],
            "chemical": chemical_by_sample[sample],
        }
        for sample in sorted(intensity_by_sample)
        if sample in chemical_by_sample
    ]


def _solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    n = len(vector)
    augmented = [row[:] + [vector[index]] for index, row in enumerate(matrix)]
    for index in range(n):
        pivot = max(range(index, n), key=lambda row: abs(augmented[row][index]))
        if abs(augmented[pivot][index]) < 1e-12:
            raise ValueError("Regression matrix is singular")
        augmented[index], augmented[pivot] = augmented[pivot], augmented[index]
        divisor = augmented[index][index]
        augmented[index] = [value / divisor for value in augmented[index]]
        for row in range(n):
            if row == index:
                continue
            factor = augmented[row][index]
            augmented[row] = [
                left - factor * right
                for left, right in zip(augmented[row], augmented[index])
            ]
    return [augmented[index][n] for index in range(n)]


def _fit_fallback(x_values: list[float], y_values: list[float], degree: int) -> dict:
    size = degree + 1
    matrix = [[0.0] * size for _ in range(size)]
    vector = [0.0] * size
    for x, y in zip(x_values, y_values):
        powers = [1.0]
        for _ in range(2 * degree):
            powers.append(powers[-1] * x)
        for row in range(size):
            vector[row] += y * powers[row]
            for col in range(size):
                matrix[row][col] += powers[row + col]
    q = _solve_linear_system(matrix, vector)
    return {
        "a": q[3] if degree == 3 else 0.0,
        "b": q[2] if degree >= 2 else 0.0,
        "c": q[1] if degree >= 1 else 0.0,
        "d": q[0],
    }


def _predict(coefficients: dict, x: float) -> float:
    return (
        float(coefficients.get("a", 0.0)) * x**3
        + float(coefficients.get("b", 0.0)) * x**2
        + float(coefficients.get("c", 1.0)) * x
        + float(coefficients.get("d", 0.0))
    )


def fit_polynomial(points: list[dict], degree: int) -> dict:
    if degree not in {1, 2, 3}:
        raise ValueError("Working-curve degree must be 1, 2, or 3")
    if len(points) < degree + 1:
        raise ValueError(
            f"Degree {degree} requires at least {degree + 1} calibration points"
        )
    x_values = [float(point["intensity"]) for point in points]
    y_values = [float(point["chemical"]) for point in points]
    try:
        import numpy as np

        raw = np.polyfit(x_values, y_values, degree)
        if degree == 1:
            coefficients = {"a": 0.0, "b": 0.0, "c": float(raw[0]), "d": float(raw[1])}
        elif degree == 2:
            coefficients = {"a": 0.0, "b": float(raw[0]), "c": float(raw[1]), "d": float(raw[2])}
        else:
            coefficients = {"a": float(raw[0]), "b": float(raw[1]), "c": float(raw[2]), "d": float(raw[3])}
    except Exception:
        coefficients = _fit_fallback(x_values, y_values, degree)

    predictions = [_predict(coefficients, value) for value in x_values]
    residuals = [actual - predicted for actual, predicted in zip(y_values, predictions)]
    mean = sum(y_values) / len(y_values)
    total = sum((value - mean) ** 2 for value in y_values)
    residual_sum = sum(value**2 for value in residuals)
    r2 = 1.0 if total == 0 and residual_sum == 0 else (1.0 - residual_sum / total if total else 0.0)
    rmse = (residual_sum / len(residuals)) ** 0.5
    return {
        "coefficients": coefficients,
        "predictions": predictions,
        "residuals": residuals,
        "r2": float(r2),
        "rmse": float(rmse),
        "degree": degree,
        "points": len(points),
    }


def predict_intensity(coefficients: dict, intensity: float) -> float:
    return _predict(coefficients, float(intensity))
