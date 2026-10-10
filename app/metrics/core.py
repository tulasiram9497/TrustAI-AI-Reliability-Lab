from __future__ import annotations

import re
from collections import Counter
from typing import Any

from app.metrics.base import MetricResult


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value).strip().lower()).strip(" .,!?:;'\"()[]{}")


def exact_match(prediction: Any, reference: Any) -> MetricResult:
    score = 1.0 if str(prediction) == str(reference) else 0.0
    return MetricResult(
        name="exact_match",
        score=score,
        applicable=True,
        details={"prediction": str(prediction), "reference": str(reference)},
    )


def normalized_exact_match(prediction: Any, reference: Any) -> MetricResult:
    pred_norm = _normalize_text(prediction)
    ref_norm = _normalize_text(reference)
    score = 1.0 if pred_norm == ref_norm else 0.0
    return MetricResult(
        name="normalized_exact_match",
        score=score,
        applicable=True,
        details={"prediction": pred_norm, "reference": ref_norm},
    )


def token_f1(prediction: Any, reference: Any) -> MetricResult:
    pred_tokens = _normalize_text(prediction).split()
    ref_tokens = _normalize_text(reference).split()
    if not pred_tokens and not ref_tokens:
        score = 1.0
    elif not pred_tokens or not ref_tokens:
        score = 0.0
    else:
        common = Counter(pred_tokens) & Counter(ref_tokens)
        overlap = sum(common.values())
        precision = overlap / len(pred_tokens)
        recall = overlap / len(ref_tokens)
        score = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return MetricResult(
        name="token_f1",
        score=score,
        applicable=True,
        details={"prediction_tokens": pred_tokens, "reference_tokens": ref_tokens},
    )


def schema_compliance(prediction: Any, reference: Any, *, expected_schema: dict[str, Any] | None = None) -> MetricResult:
    if expected_schema is None:
        return MetricResult(name="schema_compliance", score=1.0, applicable=False, details={"reason": "No schema provided"})

    if not isinstance(prediction, dict):
        return MetricResult(name="schema_compliance", score=0.0, applicable=True, details={"reason": "Prediction is not an object"})

    required = expected_schema.get("required", [])
    missing = [key for key in required if key not in prediction]
    if missing:
        return MetricResult(name="schema_compliance", score=0.0, applicable=True, details={"missing_fields": missing})

    properties = expected_schema.get("properties", {})
    violations: list[str] = []
    for key, schema_definition in properties.items():
        if key not in prediction:
            continue
        value = prediction[key]
        expected_type = schema_definition.get("type")
        if expected_type == "string" and not isinstance(value, str):
            violations.append(f"{key} should be a string")
        elif expected_type == "number" and not isinstance(value, (int, float)):
            violations.append(f"{key} should be a number")
        elif expected_type == "object" and not isinstance(value, dict):
            violations.append(f"{key} should be an object")
    score = 0.0 if violations else 1.0
    return MetricResult(name="schema_compliance", score=score, applicable=True, details={"violations": violations})
