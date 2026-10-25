"""Product-limit and repeated-burn R-control evaluation."""

from __future__ import annotations

import math


def evaluate_element_flags(concentrations: dict, specifications: dict) -> dict:
    flags = {}
    for element, value in concentrations.items():
        try:
            number = float(value)
        except (TypeError, ValueError):
            flags[element] = "WARN"
            continue
        spec = specifications.get(element) or specifications.get(str(element).upper()) or {}
        try:
            lower = float(spec.get("lower")) if spec.get("lower") is not None else None
            upper = float(spec.get("upper")) if spec.get("upper") is not None else None
            trace = float(spec.get("trace")) if spec.get("trace") is not None else None
        except (TypeError, ValueError):
            flags[element] = "OK"
            continue
        if trace is not None and number <= trace:
            flags[element] = "Tr"
        elif upper is not None and number > upper:
            flags[element] = "H"
        elif lower is not None and number < lower:
            flags[element] = "L"
        else:
            flags[element] = "OK"
    return flags


def evaluate_r_control(burns_by_element: dict, settings: dict) -> dict:
    flags = {}
    for element, burns in burns_by_element.items():
        values = []
        for value in burns or []:
            try:
                number = float(value)
            except (TypeError, ValueError):
                continue
            if math.isfinite(number):
                values.append(number)
        if len(values) < 2:
            flags[element] = "OK"
            continue
        width = max(values) - min(values)
        setting = settings.get(element) or settings.get(str(element).upper()) or {}
        try:
            average = sum(values) / len(values)
            allowed = (
                float(setting.get("a", 0.0)) * average * average
                + float(setting.get("b", 0.0)) * average
                + float(setting.get("c", 0.0))
            )
        except (TypeError, ValueError):
            flags[element] = "WARN"
            continue
        flags[element] = "OK" if width <= max(0.0, allowed) else "R"
    return flags
