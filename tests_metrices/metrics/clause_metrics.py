# tests_metrices/metrics/clause_metrics.py

from typing import List, Dict, Set


def nhrc_clause_coverage(results: List[Dict]) -> float:
    """
    Metric — NHRC Clause Coverage Accuracy
    """
    correct = 0
    total = 0

    for item in results:
        required = {
            c.replace("-", "_") for c in item.get("required_nhrc_clauses", [])
        }
        detected = {
            c.replace("-", "_") for c in item.get("detected_nhrc_clauses", [])
        }

        if not required:
            continue

        total += 1
        if required.issubset(detected):
            correct += 1

    return correct / total if total else 1.0


def forbidden_clause_violation_rate(results: List[Dict]) -> float:
    """
    Metric — Forbidden Clause Violation Rate
    """
    violations = 0
    total = 0

    for item in results:
        forbidden = {
            c.replace("-", "_") for c in item.get("forbidden_nhrc_clauses", [])
        }
        detected = {
            c.replace("-", "_") for c in item.get("detected_nhrc_clauses", [])
        }

        if not forbidden:
            continue

        total += 1
        if forbidden & detected:
            violations += 1

    return violations / total if total else 0.0


def imc_clause_precision(results: List[Dict]) -> float:
    """
    Metric — IMC Clause Precision
    """
    correct = 0
    total = 0

    for item in results:
        required = set(item.get("required_imc_clauses", []))
        detected = set(item.get("detected_imc_clauses", []))

        if not detected:
            continue

        total += len(detected)
        correct += len(required & detected)

    return correct / total if total else 1.0
