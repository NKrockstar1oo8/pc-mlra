# tests_metrices/metrics/ethics_metrics.py

from typing import List, Dict


def imc_awareness_accuracy(results: List[Dict]) -> float:
    """
    Metric 5 — IMC Ethics Awareness Accuracy

    Checks whether IMC awareness is shown when expected.
    """
    correct = 0
    total = 0

    for item in results:
        expected = item["imc_awareness_expected"]
        detected = item["imc_awareness_detected"]

        total += 1
        if expected == detected:
            correct += 1

    return correct / total if total else 1.0


def misconduct_awareness_accuracy(results: List[Dict]) -> float:
    """
    Metric 7 — Misconduct Awareness Accuracy

    Binary check: awareness surfaced or not.
    """
    correct = 0
    total = 0

    for item in results:
        expected = item["misconduct_awareness_expected"]
        detected = item["misconduct_awareness_detected"]

        total += 1
        if expected == detected:
            correct += 1

    return correct / total if total else 1.0
