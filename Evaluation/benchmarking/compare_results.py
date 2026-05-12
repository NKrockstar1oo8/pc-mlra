import json
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_results"))

FILES = {
    "pcmlra": "pcmlra_results.json",
    "gpt4": "chatgpt_responses.json",
    "gemini": "gemini_responses.json",
    "claude": "claude_responses.json",
    "deepseek": "deepseek_responses.json"
}


def load_json(filename):
    path = os.path.join(BASE_PATH, filename)
    with open(path, "r") as f:
        return json.load(f)


def normalize_text(text):
    return text.lower().strip()


def score_pcmlra(pc_entry):
    # PC-MLRA always structured → full score
    intent_score = 1 if pc_entry["intent"] else 0
    clause_score = 1 if pc_entry["clauses"] else 0
    template_score = 1 if pc_entry["template"] else 0

    return (intent_score + clause_score + template_score) / 3


def score_llm(llm_entry):
    text_intent = normalize_text(llm_entry.get("intent_guess", ""))
    keywords = [normalize_text(k) for k in llm_entry.get("keywords_present", [])]

    # Intent match (simple heuristic)
    intent_score = 1 if len(text_intent) > 0 else 0

    # Clause detection (NHRC mention)
    clause_score = 1 if llm_entry.get("mentions_nhrc", False) else 0

    # Keyword richness
    keyword_score = min(len(keywords) / 3, 1)

    return (intent_score + clause_score + keyword_score) / 3


def evaluate():
    pcmlra_data = load_json(FILES["pcmlra"])

    llm_data = {
        name: load_json(file)
        for name, file in FILES.items()
        if name != "pcmlra"
    }

    results = {}

    # PC-MLRA score
    pc_scores = [score_pcmlra(x) for x in pcmlra_data]
    results["PC-MLRA"] = sum(pc_scores) / len(pc_scores)

    # LLM scores
    for name, data in llm_data.items():
        scores = []
        for entry in data:
            scores.append(score_llm(entry))

        results[name.upper()] = sum(scores) / len(scores)

    return results


def print_results(results):
    print("\n" + "="*50)
    print(" FINAL COMPARISON RESULTS ")
    print("="*50)

    for system, score in results.items():
        print(f"{system:<15} : {score:.3f}")

    print("="*50)

    # Ranking
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    print("\n🏆 RANKING:")
    for i, (system, score) in enumerate(sorted_results, 1):
        print(f"{i}. {system} ({score:.3f})")


if __name__ == "__main__":
    results = evaluate()
    print_results(results)