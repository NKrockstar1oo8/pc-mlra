# tests_metrices/metrics/safety_metrics.py

import hashlib
from typing import List, Dict


def _hash_response(response: dict) -> str:
    """
    Deterministic hash of response dict.
    """
    normalized = str(sorted(response.items())).encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def determinism_score(responses: List[dict]) -> float:
    """
    Metric 9 — Determinism Score
    """
    if not responses:
        return 1.0

    hashes = [_hash_response(r) for r in responses]
    first = hashes[0]

    identical = sum(1 for h in hashes if h == first)

    return identical / len(hashes)

def pipeline_correctness_index(results: List[Dict]) -> float:
    """
    Metric 10 — Pipeline Correctness Index (PCI)

    Each step is binary:
    intent_ok, clauses_ok, ethics_ok, template_ok, proof_ok
    """
    total = 0
    score = 0

    for r in results:
        steps = [
            r["intent_ok"],
            r["clauses_ok"],
            r["ethics_ok"],
            r["template_ok"],
            r["proof_ok"],
        ]

        score += sum(1 for s in steps if s)
        total += len(steps)

    return score / total if total else 1.0

