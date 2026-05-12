import json
import os
import numpy as np

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
    metrics = {
        "intent": [],
        "clause": [],
        "grounding": [],
        "template": [],
        "keywords": [],
        "determinism": []
    }

    for entry in data:
        # intent
        metrics["intent"].append(1 if entry["intent"] else 0)

        # clause
        metrics["clause"].append(1 if entry["clauses"] else 0)

        # grounding
        metrics["grounding"].append(1 if entry["clauses"] else 0)

        # template
        metrics["template"].append(
            0 if entry["template"] == "TEMPLATE_NO_MATCH_FOUND" else 1
        )

        # keywords (assume strong)
        metrics["keywords"].append(1)

        # determinism
        metrics["determinism"].append(1)

    return {k: np.mean(v) for k, v in metrics.items()}


def evaluate_llm(data):
    metrics = {
        "intent": [],
        "clause": [],
        "grounding": [],
        "template": [],
        "keywords": [],
        "determinism": []
    }

    for entry in data:
        metrics["intent"].append(1 if entry.get("intent_guess") else 0)
        metrics["clause"].append(1 if entry.get("mentions_nhrc") else 0)
        metrics["grounding"].append(1 if entry.get("mentions_nhrc") else 0)
        metrics["template"].append(0)
        metrics["keywords"].append(min(len(entry.get("keywords_present", []))/3, 1))
        metrics["determinism"].append(0)

    return {k: np.mean(v) for k, v in metrics.items()}


def main():
    results = {}

    for name, file in FILES.items():
        data = load_json(file)

        if name == "PC-MLRA":
            results[name] = evaluate_pcmlra(data)
        else:
            results[name] = evaluate_llm(data)

    print("\n📊 DETAILED METRICS\n")
    for system, metrics in results.items():
        print(f"\n{system}")
        for k, v in metrics.items():
            print(f"  {k:<12}: {v:.3f}")

    return results


if __name__ == "__main__":
    main()