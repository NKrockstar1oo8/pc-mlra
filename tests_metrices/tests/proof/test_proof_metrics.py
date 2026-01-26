# tests_metrices/tests/proof/test_proof_metrics.py

from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner
from tests_metrices.metrics.proof_metrics import proof_completeness_score


def test_proof_metrics():
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
                "proof_present": runner._detect_proof_presence(response),
            }
        )

    proof_score = proof_completeness_score(results)
    print(f"Proof Completeness Score: {proof_score:.3f}")

    assert 0.0 <= proof_score <= 1.0
