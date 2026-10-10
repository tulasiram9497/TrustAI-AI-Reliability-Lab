from app.metrics.core import exact_match, normalized_exact_match, token_f1
from app.providers.mock import MockProvider
from app.schemas.dataset import DatasetCase, DatasetDefinition
from app.evaluation.runner import EvaluationRunner


def test_exact_match_and_token_f1_score_examples():
    assert exact_match("4", "4").score == 1.0
    assert normalized_exact_match("  Paris!  ", "paris").score == 1.0
    assert token_f1("the quick brown fox", "quick brown").score > 0.5


def test_evaluation_runner_aggregates_case_metrics():
    dataset = DatasetDefinition(
        dataset_id="demo-dataset",
        name="demo",
        cases=[
            DatasetCase(case_id="a1", input="What is 2 + 2?", reference_answer="4"),
            DatasetCase(case_id="a2", input="What is the capital of France?", reference_answer="Paris"),
        ],
    )
    runner = EvaluationRunner(provider=MockProvider())
    report = runner.run(dataset)

    assert report["total_cases"] == 2
    assert report["metrics"]["exact_match"] >= 0.0
    assert "case_results" in report
