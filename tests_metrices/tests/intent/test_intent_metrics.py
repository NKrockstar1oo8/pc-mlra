# tests_metrices/tests/intent/test_intent_metrics.py

from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner
from tests_metrices.metrics.intent_metrics import (
    primary_intent_accuracy,
    secondary_intent_recall,
)


def test_intent_metrics():
    dataset = load_dataset(
        "tests_metrices/datasets/golden_cases_v3.json"
    )

    runner = ResponseRunner()
    results = []

    for case in dataset:
        output = runner.run_intent_only(case["user_query"])

        intents_sorted = sorted(
            output["intents"],
            key=lambda x: x["confidence"],
            reverse=True,
        )

        results.append(
            {
                "test_id": case["test_id"],
                "expected_primary_legal_triggers": case.get(
                    "expected_primary_legal_triggers", []
                ),
                "expected_secondary_legal_triggers": case.get(
                    "expected_secondary_legal_triggers", []
                ),
                "detected_primary_intents": [
                    intents_sorted[0]["name"]
                ]
                if intents_sorted
                else [],
                "detected_secondary_intents": [
                    i["name"] for i in intents_sorted[1:]
                ],
            }
        )

    pa = primary_intent_accuracy(results)
    sr = secondary_intent_recall(results)

    print(f"Primary Intent Accuracy: {pa:.3f}")
    print(f"Secondary Intent Recall: {sr:.3f}")

    assert 0.0 <= pa <= 1.0
    assert 0.0 <= sr <= 1.0
