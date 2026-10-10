from app.datasets.loader import load_dataset


def test_load_dataset_validates_example_rows():
    dataset = load_dataset(
        {
            "cases": [
                {
                    "case_id": "case-1",
                    "input": "What is 2 + 2?",
                    "reference_answer": "4",
                    "expected_behavior": "Provide the numeric answer",
                    "tags": ["math"],
                }
            ]
        }
    )

    assert dataset.case_count == 1
    assert dataset.cases[0].case_id == "case-1"
    assert dataset.cases[0].reference_answer == "4"


def test_load_dataset_rejects_missing_case_id():
    try:
        load_dataset({"cases": [{"input": "No case id"}]})
        raise AssertionError("Expected validation error")
    except ValueError as exc:
        assert "case_id" in str(exc)
