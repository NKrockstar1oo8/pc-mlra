# tests_metrices/loaders/response_runner.py

from typing import Dict, Any, List

from src.intent_classifier import IntentClassifier
from src.response_assembler import ResponseAssembler


class ResponseRunner:
    """
    Executes the REAL PC-MLRA pipeline for evaluation.
    This file MUST mirror production behavior exactly.
    """

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.response_assembler = ResponseAssembler()

    # -------------------------------------------------
    # Intent-only run (optional diagnostic)
    # -------------------------------------------------
    def run_intent_only(self, query: str) -> Dict[str, Any]:
        result = self.intent_classifier.classify(query)

        if not isinstance(result, dict):
            raise TypeError("IntentClassifier.classify must return dict")

        if "intents" not in result or not isinstance(result["intents"], list):
            raise KeyError("Intent output must contain list 'intents'")

        return result

    # -------------------------------------------------
    # Full pipeline run (canonical, USED BY METRICS)
    # -------------------------------------------------
    def run_for_metrics(self, query: str) -> dict:
        intent_result = self.intent_classifier.classify(query)

        if not isinstance(intent_result, list):
            raise TypeError("IntentClassifier must return list")

        response_text, proof_trace = self.response_assembler.generate_response(
            query,
            show_proof=True
        )
        
        #print("PROOF TRACE TYPE:", type(proof_trace))
        #print("PROOF TRACE DIR:", dir(proof_trace))
        #print("PROOF TRACE DICT (if any):", getattr(proof_trace, "__dict__", None))

        intents_sorted = sorted(
            intent_result,
            key=lambda x: x[1],   # (name, confidence)
            reverse=True,
        )

        detected_nhrc = []
        detected_imc = []

        matched_clauses = getattr(proof_trace, "matched_clauses", [])

        for clause in matched_clauses:
            clause_id = clause.get("id")
            document = clause.get("document")

            if document == "NHRC":
                detected_nhrc.append(clause_id)
            elif document == "IMC":
                detected_imc.append(clause_id)

        imc_awareness = bool(detected_imc)

        return {
            "detected_primary_intents": (
                [intents_sorted[0][0]] if intents_sorted else []
            ),
            "detected_secondary_intents": [
                i[0] for i in intents_sorted[1:]
            ],
            "detected_nhrc_clauses": detected_nhrc,
            "detected_imc_clauses": detected_imc,
            "imc_awareness_detected": imc_awareness,
            "misconduct_awareness_detected": imc_awareness,  # 👈 THIS LINE
            "proof_present": bool(proof_trace),
            "template_id": getattr(proof_trace, "template_id", None),
        }
