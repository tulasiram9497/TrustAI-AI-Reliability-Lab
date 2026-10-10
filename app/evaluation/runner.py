from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.metrics.core import exact_match, normalized_exact_match, schema_compliance, token_f1
from app.providers.mock import MockProvider
from app.schemas.dataset import DatasetDefinition


class EvaluationRunner:
    """Run a deterministic evaluation over a dataset with a model provider and simple metrics."""

    def __init__(
        self,
        provider: MockProvider | None = None,
        metrics: list[str] | None = None,
    ) -> None:
        self.provider = provider or MockProvider()
        self.metrics = metrics or ["exact_match", "normalized_exact_match", "token_f1"]

    def run(self, dataset: DatasetDefinition) -> dict[str, Any]:
        case_results: list[dict[str, Any]] = []
        metric_scores: dict[str, list[float]] = defaultdict(list)

        for case in dataset.cases:
            response = self.provider.generate(str(case.input))
            metric_values: dict[str, Any] = {}

            for metric_name in self.metrics:
                if metric_name == "exact_match":
                    result = exact_match(response.output, case.reference_answer)
                elif metric_name == "normalized_exact_match":
                    result = normalized_exact_match(response.output, case.reference_answer)
                elif metric_name == "token_f1":
                    result = token_f1(response.output, case.reference_answer)
                elif metric_name == "schema_compliance":
                    result = schema_compliance(
                        response.output if isinstance(response.output, dict) else {},
                        case.reference_answer,
                        expected_schema=case.expected_output_schema,
                    )
                else:
                    continue

                metric_values[metric_name] = {"score": result.score, "applicable": result.applicable}
                if result.score is not None:
                    metric_scores[metric_name].append(float(result.score))

            case_result = {
                "case_id": case.case_id,
                "input": case.input,
                "reference_answer": case.reference_answer,
                "prediction": response.output,
                "metrics": metric_values,
            }
            case_results.append(case_result)

        summary = {
            metric_name: (sum(values) / len(values) if values else 0.0)
            for metric_name, values in metric_scores.items()
        }

        return {
            "total_cases": len(dataset.cases),
            "successful_cases": len(dataset.cases),
            "failed_cases": 0,
            "metrics": summary,
            "case_results": case_results,
        }
