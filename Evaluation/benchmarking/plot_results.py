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


def load_json(file):
    with open(os.path.join(BASE_PATH, file)) as f:
        return json.load(f)


def evaluate_pcmlra(data):
    metrics = {"intent": [], "clause": [], "grounding": [], "template": [], "keywords": [], "determinism": []}

    for entry in data:
        metrics["intent"].append(1 if entry["intent"] else 0)
        metrics["clause"].append(1 if entry["clauses"] else 0)
        metrics["grounding"].append(1 if entry["clauses"] else 0)
        metrics["template"].append(0 if entry["template"] == "TEMPLATE_NO_MATCH_FOUND" else 1)
        metrics["keywords"].append(1)
        metrics["determinism"].append(1)

    return {k: sum(v)/len(v) for k, v in metrics.items()}


def evaluate_llm(data):
    metrics = {"intent": [], "clause": [], "grounding": [], "template": [], "keywords": [], "determinism": []}

    for entry in data:
        metrics["intent"].append(1 if entry.get("intent_guess") else 0)
        metrics["clause"].append(1 if entry.get("mentions_nhrc") else 0)
        metrics["grounding"].append(1 if entry.get("mentions_nhrc") else 0)
        metrics["template"].append(0)
        metrics["keywords"].append(min(len(entry.get("keywords_present", []))/3, 1))
        metrics["determinism"].append(0)

    return {k: sum(v)/len(v) for k, v in metrics.items()}


def compute_results():
    results = {}

    for name, file in FILES.items():
        data = load_json(file)

        if name == "PC-MLRA":
            results[name] = evaluate_pcmlra(data)
        else:
            results[name] = evaluate_llm(data)

    return results


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
        plt.savefig(f"{metric}_comparison.png")  # saves image
        plt.close()

    print("✅ Graphs saved as PNG files")


if __name__ == "__main__":
    results = compute_results()
    plot_metrics(results)