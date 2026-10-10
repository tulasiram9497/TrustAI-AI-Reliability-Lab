from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DatasetCase(BaseModel):
    """A single evaluation case."""

    model_config = ConfigDict(extra="allow")

    case_id: str
    input: Any
    reference_answer: Any | None = None
    context: Any | None = None
    expected_output_schema: dict[str, Any] | None = None
    expected_behavior: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("case_id")
    @classmethod
    def validate_case_id(cls, value: str) -> str:
        value = str(value).strip()
        if not value:
            raise ValueError("case_id is required and cannot be empty")
        return value


class DatasetDefinition(BaseModel):
    """A validated dataset definition."""

    dataset_id: str
    name: str | None = None
    description: str | None = None
    version: str | None = None
    cases: list[DatasetCase] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def case_count(self) -> int:
        return len(self.cases)


def _compute_dataset_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def load_dataset(payload: dict[str, Any] | list[dict[str, Any]]) -> DatasetDefinition:
    """Validate a dataset payload and return a normalized DatasetDefinition."""

    raw_cases: Any
    if isinstance(payload, list):
        raw_cases = payload
    elif isinstance(payload, dict):
        raw_cases = payload.get("cases")
        if raw_cases is None:
            raise ValueError("Dataset payload must include a 'cases' list.")
    else:
        raise ValueError("Dataset payload must be a dict or list of case objects.")

    if not isinstance(raw_cases, list):
        raise ValueError("Dataset 'cases' field must be a list of objects.")

    validated_cases: list[DatasetCase] = []
    for index, case in enumerate(raw_cases):
        try:
            validated_cases.append(DatasetCase.model_validate(case))
        except Exception as exc:  # noqa: BLE001 - keep validation message explicit
            raise ValueError(f"Invalid case at index {index}: {exc}") from exc

    dataset_payload = {
        "name": payload.get("name") if isinstance(payload, dict) else None,
        "description": payload.get("description") if isinstance(payload, dict) else None,
        "version": payload.get("version") if isinstance(payload, dict) else None,
        "cases": [case.model_dump(mode="json") for case in validated_cases],
    }
    dataset_id = _compute_dataset_hash(dataset_payload)
    return DatasetDefinition(
        dataset_id=dataset_id,
        name=dataset_payload["name"],
        description=dataset_payload["description"],
        version=dataset_payload["version"],
        cases=validated_cases,
        metadata={"source": "direct-payload"},
    )
