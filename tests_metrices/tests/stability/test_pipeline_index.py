from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner
from tests_metrices.results.case_evaluator import evaluate_case
from tests_metrices.metrics.safety_metrics import pipeline_correctness_index


def test_pipeline_index_real():
    dataset = load_dataset(
        "tests_metrices/datasets/golden_cases_v3.json"
    )

    runner = ResponseRunner()
    evaluations = []

    for case in dataset:
        detected = runner.run_for_metrics(case["user_query"])
        evaluation = evaluate_case(case, detected)
        evaluations.append(evaluation.__dict__)

    pci = pipeline_correctness_index(evaluations)
    print(f"Pipeline Correctness Index (REAL): {pci:.3f}")

    assert 0.0 <= pci <= 1.0
