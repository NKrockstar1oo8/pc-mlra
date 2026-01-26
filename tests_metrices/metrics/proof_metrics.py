# tests_metrices/metrics/proof_metrics.py

from typing import List, Dict


def proof_completeness_score(results: List[Dict]) -> float:
    """
    Metric 8 — Proof Completeness Score

    Checks whether proof trace and legal sources are present.
    """
    correct = 0
    total = 0

    for item in results:
        total += 1
        if item["proof_present"]:
            correct += 1

    return correct / total if total else 1.0
