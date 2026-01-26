# tests_metrices/run_all_metrics.py

from tests_metrices.results.failure_explainer import explain_case_failure
print(">>> Starting PC-MLRA Metrics Evaluation <<<")

import json
from pathlib import Path
from datetime import datetime

from tests_metrices.loaders.dataset_loader import load_dataset
from tests_metrices.loaders.response_runner import ResponseRunner

from tests_metrices.metrics.intent_metrics import (
    primary_intent_accuracy,
    secondary_intent_recall,
)
from tests_metrices.metrics.clause_metrics import (
    nhrc_clause_coverage,
    forbidden_clause_violation_rate,
    imc_clause_precision,
)
from tests_metrices.metrics.ethics_metrics import (
    imc_awareness_accuracy,
    misconduct_awareness_accuracy,
)
from tests_metrices.metrics.proof_metrics import proof_completeness_score
from tests_metrices.metrics.safety_metrics import (
    determinism_score,
    pipeline_correctness_index,
)

from tests_metrices.results.case_evaluator import evaluate_case


RESULTS_DIR = Path("tests_metrices/results")
RESULTS_DIR.mkdir(exist_ok=True)

HISTORY_FILE = RESULTS_DIR / "metrics_history.json"


def run_all_metrics(dataset_path: str):
    dataset = load_dataset(dataset_path)
    runner = ResponseRunner()

    per_case_results = []
    pci_inputs = []

    # -------- run system ONCE per query --------
    for case in dataset:
        detected = runner.run_for_metrics(case["user_query"])

        evaluation = evaluate_case(case, detected)
        failure_reasons = explain_case_failure({**case, **detected})

        record = {
            **case,
            **detected,
            **evaluation.__dict__,
            "failure_reasons": failure_reasons,
        }

        per_case_results.append(record)
        pci_inputs.append(evaluation.__dict__)

    # -------- compute metrics --------
    summary = {
        "primary_intent_accuracy": primary_intent_accuracy(per_case_results),
        "secondary_intent_recall": secondary_intent_recall(per_case_results),
        "nhrc_clause_coverage": nhrc_clause_coverage(per_case_results),
        "forbidden_clause_violation_rate": forbidden_clause_violation_rate(per_case_results),
        "imc_clause_precision": imc_clause_precision(per_case_results),
        "imc_awareness_accuracy": imc_awareness_accuracy(per_case_results),
        "misconduct_awareness_accuracy": misconduct_awareness_accuracy(per_case_results),
        "proof_completeness_score": proof_completeness_score(per_case_results),
        "pipeline_correctness_index": pipeline_correctness_index(pci_inputs),
    }

    # -------- determinism check --------
    sample_query = dataset[0]["user_query"]
    responses = [runner.run_for_metrics(sample_query) for _ in range(10)]
    summary["determinism_score"] = determinism_score(responses)

    # -------- save latest results --------
    with open(RESULTS_DIR / "metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with open(RESULTS_DIR / "per_case_results.json", "w", encoding="utf-8") as f:
        json.dump(per_case_results, f, indent=2)

    # -------- append history (IMPORTANT PART) --------
    history_record = {
        "timestamp": datetime.now().isoformat(),
        "dataset": dataset_path,
        "summary": summary,
    }

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(history_record, indent=2))
        f.write("\n" + "=" * 80 + "\n")

    print("\n✅ METRICS GENERATED SUCCESSFULLY\n")
    for k, v in summary.items():
        print(f"{k}: {v:.3f}")


if __name__ == "__main__":
    run_all_metrics("datasets/golden_cases_v6.json")
    print(">>> Entered main block <<<")
