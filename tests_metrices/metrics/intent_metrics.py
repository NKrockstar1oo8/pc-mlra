# tests_metrices/metrics/intent_metrics.py

from typing import List, Dict


def primary_intent_accuracy(
    results: List[Dict],
) -> float:
    """
    Metric 1 — Primary Intent Accuracy

    Correct if expected_primary_legal_triggers
    intersects with detected intents.
    """
    correct = 0
    total = 0

    for item in results:
        expected = set(item.get("expected_primary_legal_triggers", []))
        detected = set(item.get("detected_primary_intents", []))

        if not expected:
            continue  # not applicable

        total += 1
        if expected & detected:
            correct += 1

    return correct / total if total else 1.0


def secondary_intent_recall(results: List[Dict]) -> float:
    """
    Metric 2 — Secondary Intent Recall
    """
    found = 0
    expected_total = 0

    for item in results:
        expected = set(item.get("expected_secondary_legal_triggers", []))
        detected = set(item.get("detected_secondary_intents", []))

        expected_total += len(expected)
        found += len(expected & detected)

    return found / expected_total if expected_total else 1.0
