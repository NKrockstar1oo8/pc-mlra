import json
import os
import matplotlib.pyplot as plt

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_results"))

FILES = {
    "PC-MLRA": "pcmlra_results.json",
    "GPT4": "chatgpt_responses.json",
    "GEMINI": "gemini_responses.json",
    "CLAUDE": "claude_responses.json",
    "DEEPSEEK": "deepseek_responses.json"
}


# ---------------- LOAD ----------------
def load_json(file):
    with open(os.path.join(BASE_PATH, file)) as f:
        return json.load(f)


# ---------------- PC-MLRA ----------------
def evaluate_pcmlra(data):
    scores = {"intent": [], "grounding": [], "coverage": [], "failure": []}

    for entry in data:
        # Intent
        scores["intent"].append(1 if entry["intent"] else 0)

        # Grounding (legal clause present)
        scores["grounding"].append(1 if entry["clauses"] else 0)

        # Coverage (how many clauses covered)
        scores["coverage"].append(min(len(entry["clauses"]) / 2, 1))

        # Failure
        scores["failure"].append(
            1 if entry["template"] == "TEMPLATE_NO_MATCH_FOUND" else 0
        )

    return {k: sum(v)/len(v) for k, v in scores.items()}


# ---------------- LLM ----------------
def evaluate_llm(data):
    scores = {"intent": [], "grounding": [], "coverage": [], "failure": []}

    for entry in data:
        # Intent
        scores["intent"].append(1 if entry.get("intent_guess") else 0)

        # Grounding
        scores["grounding"].append(1 if entry.get("mentions_nhrc") else 0)

        # Coverage (keyword richness)
        scores["coverage"].append(min(len(entry.get("keywords_present", []))/3, 1))

        # Failure
        scores["failure"].append(
            0 if entry.get("intent_guess") else 1
        )

    return {k: sum(v)/len(v) for k, v in scores.items()}


# ---------------- MAIN EVALUATION ----------------
def compute_results():
    results = {}

    for name, file in FILES.items():
        data = load_json(file)

        if name == "PC-MLRA":
            results[name] = evaluate_pcmlra(data)
        else:
            results[name] = evaluate_llm(data)

    return results


# ---------------- FINAL SCORE ----------------
def compute_final_scores(results):
    final_scores = {}

    for system, metrics in results.items():
        final = (
            metrics["intent"]
            + metrics["grounding"]
            + metrics["coverage"]
            + (1 - metrics["failure"])
        ) / 4

        final_scores[system] = final

    return final_scores


# ---------------- PRINT ----------------
def print_results(results, final_scores):
    print("\n📊 DETAILED METRICS\n")

    for system, metrics in results.items():
        print(f"\n{system}")
        for k, v in metrics.items():
            print(f"  {k:<10}: {v:.3f}")

    print("\n🏁 FINAL SCORES\n")
    for system, score in final_scores.items():
        print(f"{system:<10}: {score:.3f}")

    print("\n🏆 RANKING\n")
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (system, score) in enumerate(ranked, 1):
        print(f"{i}. {system} ({score:.3f})")


# ---------------- GRAPH ----------------
def plot_metrics(results):
    systems = list(results.keys())
    metrics = list(next(iter(results.values())).keys())

    for metric in metrics:
        values = [results[s][metric] for s in systems]

        plt.figure()
        plt.bar(systems, values)
        plt.title(f"{metric} comparison")
        plt.ylabel("Score")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(f"{metric}_comparison.png")
        plt.close()

    print("\n✅ Graphs saved")


# ---------------- RUN ----------------
if __name__ == "__main__":
    results = compute_results()
    final_scores = compute_final_scores(results)

    print_results(results, final_scores)
    plot_metrics(results)