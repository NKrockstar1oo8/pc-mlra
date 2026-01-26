# tests_metrices/tests/ethics/test_ethics_metrics.py

from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner
from tests_metrices.metrics.ethics_metrics import (
    imc_awareness_accuracy,
    misconduct_awareness_accuracy,
)


def test_ethics_metrics():
    dataset = load_dataset(
        "tests_metrices/datasets/golden_cases_v3.json"
    )

    runner = ResponseRunner()
    results = []

    for case in dataset:
        response = runner.run_full_pipeline(case["user_query"])

        results.append(
            {
                "test_id": case["test_id"],
                "imc_awareness_expected": case["imc_awareness_expected"],
                "misconduct_awareness_expected": case[
                    "misconduct_awareness_expected"
                ],
                "imc_awareness_detected": runner._detect_imc_awareness(
                    response
                ),
                "misconduct_awareness_detected": runner._detect_misconduct_awareness(
                    response
                ),
            }
        )

    imc_score = imc_awareness_accuracy(results)
    misconduct_score = misconduct_awareness_accuracy(results)

    print(f"IMC Awareness Accuracy: {imc_score:.3f}")
    print(f"Misconduct Awareness Accuracy: {misconduct_score:.3f}")

    assert 0.0 <= imc_score <= 1.0
    assert 0.0 <= misconduct_score <= 1.0
