from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from app.errors import DatasetValidationError
from app.schemas.dataset import DatasetDefinition, load_dataset as validate_dataset


def load_dataset(payload: dict[str, Any] | list[dict[str, Any]] | str | Path) -> DatasetDefinition:
    """Load a dataset from a direct payload or a JSON/JSONL/CSV file."""

    if isinstance(payload, (str, Path)):
        file_path = Path(payload)
        if not file_path.exists():
            raise DatasetValidationError(f"Dataset file does not exist: {file_path}")

        suffix = file_path.suffix.lower()
        if suffix == ".json":
            with file_path.open("r", encoding="utf-8") as handle:
                document = json.load(handle)
            return validate_dataset(document)
        if suffix == ".jsonl":
            cases: list[dict[str, Any]] = []
            with file_path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        cases.append(json.loads(stripped))
                    except json.JSONDecodeError as exc:
                        raise DatasetValidationError(
                            f"Invalid JSONL line {line_number} in {file_path}: {exc}"
                        ) from exc
            return validate_dataset(cases)
        if suffix == ".csv":
            with file_path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
            return validate_dataset(rows)

        raise DatasetValidationError(f"Unsupported dataset format: {file_path.suffix}")

    return validate_dataset(payload)
