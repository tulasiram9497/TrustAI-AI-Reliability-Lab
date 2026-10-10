from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricResult:
    name: str
    score: float | None
    applicable: bool = True
    details: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
