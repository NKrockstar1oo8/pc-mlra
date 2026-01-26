# tests_metrices/tests/clauses/test_clause_metrics.py

from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner
from tests_metrices.metrics.clause_metrics import (
    nhrc_clause_coverage,
    forbidden_clause_violation_rate,
    imc_clause_precision,
    _extract_clauses,
)


def test_clause_metrics():
    dataset = load_dataset(
        "tests_metrices/datasets/golden_cases_v3.json"
    )

    runner = ResponseRunner()
    results = []

    for case in dataset:
        response = runner.run_full_pipeline(case["user_query"])
        detected = _extract_clauses(response)

        results.append(
            {
                "test_id": case["test_id"],
                "required_nhrc_clauses": case["required_nhrc_clauses"],
                "forbidden_nhrc_clauses": case["forbidden_nhrc_clauses"],
                "required_imc_clauses": case["required_imc_clauses"],
                "detected_nhrc_clauses": {
                    c for c in detected if c.startswith("NHRC")
                },
                "detected_imc_clauses": {
                    c for c in detected if c.startswith("IMC")
                },
            }
        )

    coverage = nhrc_clause_coverage(results)
    violation = forbidden_clause_violation_rate(results)
    imc_precision = imc_clause_precision(results)

    print(f"NHRC Clause Coverage: {coverage:.3f}")
    print(f"Forbidden Clause Violation Rate: {violation:.3f}")
    print(f"IMC Clause Precision: {imc_precision:.3f}")

    assert 0.0 <= coverage <= 1.0
    assert 0.0 <= violation <= 1.0
    assert 0.0 <= imc_precision <= 1.0
