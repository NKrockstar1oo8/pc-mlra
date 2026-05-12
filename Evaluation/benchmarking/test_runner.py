#!/usr/bin/env python3
"""
PC-MLRA Comprehensive Test Suite Runner
========================================
Runs 90 test queries through the PC-MLRA system and collects:
1. System responses
2. Proof traces
3. Intent classification results
4. Matched clauses

Outputs structured data for LLM comparison and scoring.

Usage:
    python test_runner.py --output-dir ./test_results
    python test_runner.py --format json --output-dir ./test_results
    python test_runner.py --format csv --output-dir ./test_results
"""

import sys
import os
import json
import csv
import argparse
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.response_assembler import ResponseAssembler
from src.intent_classifier import IntentClassifier
from src.knowledge_loader import KnowledgeBase


# ============================================================
# TEST SUITE (90 Queries)
# ============================================================

TEST_QUERIES = [
    # === NHRC RIGHT 1: RIGHT TO INFORMATION ===
    {"id": "T001", "category": "right_to_information", "expected_intent": "right_to_information", "priority": "low", 
     "query": "Doctor did not explain my diagnosis to me", "notes": "Basic information denial"},
    {"id": "T002", "category": "right_to_information", "expected_intent": "right_to_information", "priority": "low",
     "query": "What is wrong with my health condition the doctor is not telling me", "notes": "Information withholding"},
    {"id": "T003", "category": "right_to_information", "expected_intent": "right_to_information", "priority": "low",
     "query": "Nurse refused to clarify my treatment options", "notes": "Treatment options information"},

    # === NHRC RIGHT 2: ACCESS TO MEDICAL RECORDS ===
    {"id": "T004", "category": "access_medical_records", "expected_intent": "access_medical_records", "priority": "medium",
     "query": "Hospital is not giving me my medical reports", "notes": "Records denial"},
    {"id": "T005", "category": "access_medical_records", "expected_intent": "access_medical_records", "priority": "medium",
     "query": "I need my discharge summary but they refused to provide it", "notes": "Discharge summary"},
    {"id": "T006", "category": "access_medical_records", "expected_intent": "access_medical_records", "priority": "medium",
     "query": "Doctor shouted at me when I asked for my test results", "notes": "Aggressive refusal"},
    {"id": "T007", "category": "access_medical_records", "expected_intent": "access_medical_records", "priority": "medium",
     "query": "They denied access to my case papers and medical file", "notes": "Complete denial"},

    # === NHRC RIGHT 3: EMERGENCY CARE ===
    {"id": "T008", "category": "emergency_care", "expected_intent": "emergency_care", "priority": "critical",
     "query": "Doctor not admitting my friend who met with an accident", "notes": "Accident emergency"},
    {"id": "T009", "category": "emergency_care", "expected_intent": "emergency_care", "priority": "critical",
     "query": "Hospital asked for advance payment for my father's heart attack treatment", "notes": "Payment demand in emergency"},
    {"id": "T010", "category": "emergency_care", "expected_intent": "emergency_care", "priority": "critical",
     "query": "They refused emergency care to my brother who was bleeding heavily after an accident", "notes": "Severe bleeding"},
    {"id": "T011", "category": "emergency_care", "expected_intent": "emergency_care", "priority": "critical",
     "query": "My mother was unconscious and hospital turned her away", "notes": "Unconscious patient"},
    {"id": "T012", "category": "emergency_care", "expected_intent": "emergency_care", "priority": "critical",
     "query": "Critical patient denied treatment because no money was given in advance", "notes": "Critical + payment"},

    # === NHRC RIGHT 4: INFORMED CONSENT ===
    {"id": "T013", "category": "informed_consent", "expected_intent": "informed_consent", "priority": "high",
     "query": "Surgery was performed on me without my permission", "notes": "No consent surgery"},
    {"id": "T014", "category": "informed_consent", "expected_intent": "informed_consent", "priority": "high",
     "query": "Doctor forced me to sign consent form without explaining the risks", "notes": "Forced consent"},
    {"id": "T015", "category": "informed_consent", "expected_intent": "informed_consent", "priority": "high",
     "query": "They did the operation without telling me what could go wrong", "notes": "Risk not explained"},
    {"id": "T016", "category": "informed_consent", "expected_intent": "informed_consent", "priority": "high",
     "query": "My consent was taken but they did a different procedure than what was explained", "notes": "Consent mismatch"},

    # === NHRC RIGHT 5: PRIVACY & CONFIDENTIALITY ===
    {"id": "T017", "category": "privacy_confidentiality", "expected_intent": "privacy_confidentiality", "priority": "high",
     "query": "Doctor told my relatives about my HIV status without asking me", "notes": "HIV disclosure"},
    {"id": "T018", "category": "privacy_confidentiality", "expected_intent": "privacy_confidentiality", "priority": "high",
     "query": "Hospital staff discussed my abortion in the corridor where everyone could hear", "notes": "Public discussion"},
    {"id": "T019", "category": "privacy_confidentiality", "expected_intent": "privacy_confidentiality", "priority": "high",
     "query": "My medical condition was leaked to my employer by the hospital", "notes": "Leak to third party"},
    {"id": "T020", "category": "privacy_confidentiality", "expected_intent": "privacy_confidentiality", "priority": "high",
     "query": "Nurse shared my confidential health details with other patients", "notes": "Patient-to-patient leak"},

    # === NHRC RIGHT 6: SECOND OPINION ===
    {"id": "T021", "category": "second_opinion", "expected_intent": "second_opinion", "priority": "medium",
     "query": "Doctor refused to let me consult another specialist for second opinion", "notes": "Denied second opinion"},
    {"id": "T022", "category": "second_opinion", "expected_intent": "second_opinion", "priority": "medium",
     "query": "Hospital is not providing my records to another doctor for second opinion", "notes": "Records blocking"},
    {"id": "T023", "category": "second_opinion", "expected_intent": "second_opinion", "priority": "medium",
     "query": "They threatened me when I said I want to get a different doctor's opinion", "notes": "Threat for second opinion"},

    # === NHRC RIGHT 7: TRANSPARENT PRICING ===
    {"id": "T024", "category": "transparent_pricing", "expected_intent": "transparent_pricing", "priority": "medium",
     "query": "Hospital overcharged me for treatment and added hidden costs to my bill", "notes": "Overcharging + hidden costs"},
    {"id": "T025", "category": "transparent_pricing", "expected_intent": "transparent_pricing", "priority": "medium",
     "query": "They are charging too much money and the rates are not transparent", "notes": "Non-transparent rates"},
    {"id": "T026", "category": "transparent_pricing", "expected_intent": "transparent_pricing", "priority": "medium",
     "query": "Doctor is scamming me with expensive unnecessary tests", "notes": "Unnecessary tests"},
    {"id": "T027", "category": "transparent_pricing", "expected_intent": "transparent_pricing", "priority": "medium",
     "query": "I paid more than expected because they did not give itemized bill", "notes": "No itemized bill"},

    # === NHRC RIGHT 8: NON-DISCRIMINATION ===
    {"id": "T028", "category": "non_discrimination", "expected_intent": "non_discrimination", "priority": "high",
     "query": "Hospital refused treatment because I am HIV positive", "notes": "HIV discrimination"},
    {"id": "T029", "category": "non_discrimination", "expected_intent": "non_discrimination", "priority": "high",
     "query": "Doctor said he won't treat Muslims in his clinic", "notes": "Religious discrimination"},
    {"id": "T030", "category": "non_discrimination", "expected_intent": "non_discrimination", "priority": "high",
     "query": "They discriminated against my father because of his caste", "notes": "Caste discrimination"},
    {"id": "T031", "category": "non_discrimination", "expected_intent": "non_discrimination", "priority": "high",
     "query": "Patient was denied care due to AIDS and treated differently because of disease", "notes": "Disease-based discrimination"},
    {"id": "T032", "category": "non_discrimination", "expected_intent": "non_discrimination", "priority": "high",
     "query": "Hospital won't treat poor patients and only admits rich people", "notes": "Economic discrimination"},

    # === NHRC RIGHT 9: PATIENT SAFETY ===
    {"id": "T033", "category": "patient_safety", "expected_intent": "patient_safety", "priority": "high",
     "query": "I caught infection in hospital because of dirty ward and poor hygiene", "notes": "Hospital-acquired infection"},
    {"id": "T034", "category": "patient_safety", "expected_intent": "patient_safety", "priority": "high",
     "query": "Unsafe care provided to my mother with unclean equipment", "notes": "Unclean equipment"},
    {"id": "T035", "category": "patient_safety", "expected_intent": "patient_safety", "priority": "high",
     "query": "Medical error caused harm to my child during treatment", "notes": "Medical error"},
    {"id": "T036", "category": "patient_safety", "expected_intent": "patient_safety", "priority": "high",
     "query": "Hospital negligence led to complications in my surgery", "notes": "Negligence + safety"},

    # === NHRC RIGHT 10: TREATMENT CHOICE ===
    {"id": "T037", "category": "treatment_choice", "expected_intent": "treatment_choice", "priority": "medium",
     "query": "Doctor forced me to take allopathy and did not allow ayurveda option", "notes": "Forced allopathy"},
    {"id": "T038", "category": "treatment_choice", "expected_intent": "treatment_choice", "priority": "medium",
     "query": "I want to choose alternative treatment but they are not offering other options", "notes": "No alternative offered"},
    {"id": "T039", "category": "treatment_choice", "expected_intent": "treatment_choice", "priority": "medium",
     "query": "Patient was not allowed to choose between available treatment options", "notes": "Choice denied"},

    # === NHRC RIGHT 11: CHOICE OF SOURCE ===
    {"id": "T040", "category": "choice_of_source", "expected_intent": "choice_of_source", "priority": "medium",
     "query": "Hospital forced me to buy medicines from their pharmacy only", "notes": "Forced pharmacy"},
    {"id": "T041", "category": "choice_of_source", "expected_intent": "choice_of_source", "priority": "medium",
     "query": "Doctor insisted I get tests done only at their recommended lab", "notes": "Restricted lab choice"},
    {"id": "T042", "category": "choice_of_source", "expected_intent": "choice_of_source", "priority": "medium",
     "query": "They refused to let me purchase medicines from outside chemist", "notes": "Outside purchase blocked"},

    # === NHRC RIGHT 12: PROPER REFERRAL ===
    {"id": "T043", "category": "proper_referral", "expected_intent": "proper_referral", "priority": "high",
     "query": "Doctor referred me to another hospital for commission money", "notes": "Commercial referral"},
    {"id": "T044", "category": "proper_referral", "expected_intent": "proper_referral", "priority": "high",
     "query": "They forced referral to a specialist who pays them kickback", "notes": "Kickback referral"},
    {"id": "T045", "category": "proper_referral", "expected_intent": "proper_referral", "priority": "high",
     "query": "Unnecessary referral was made to higher center for money", "notes": "Unnecessary referral"},

    # === NHRC RIGHT 13: CLINICAL TRIAL RIGHTS ===
    {"id": "T046", "category": "clinical_trial_rights", "expected_intent": "clinical_trial_rights", "priority": "high",
     "query": "I was forced into a clinical trial without proper explanation", "notes": "Forced trial"},
    {"id": "T047", "category": "clinical_trial_rights", "expected_intent": "clinical_trial_rights", "priority": "high",
     "query": "Research experiment conducted on me without my consent", "notes": "No consent trial"},
    {"id": "T048", "category": "clinical_trial_rights", "expected_intent": "clinical_trial_rights", "priority": "high",
     "query": "Study participant was misled about the risks of the trial", "notes": "Misled participant"},

    # === NHRC RIGHT 14: BIOMEDICAL RESEARCH ===
    {"id": "T049", "category": "biomedical_research", "expected_intent": "biomedical_research", "priority": "high",
     "query": "Biomedical research was conducted on patients without ethics committee approval", "notes": "No ethics approval"},
    {"id": "T050", "category": "biomedical_research", "expected_intent": "biomedical_research", "priority": "high",
     "query": "Human research involved vulnerable people without informed consent", "notes": "Vulnerable subjects"},
    {"id": "T051", "category": "biomedical_research", "expected_intent": "biomedical_research", "priority": "high",
     "query": "Health research participant was not compensated for injuries", "notes": "No compensation"},

    # === NHRC RIGHT 15: DETENTION FOR PAYMENT / BODY WITHHELD ===
    {"id": "T052", "category": "detained_for_payment", "expected_intent": "detained_for_payment", "priority": "absolute",
     "query": "Hospital is not discharging my father because bill payment is pending", "notes": "Detained for bill"},
    {"id": "T053", "category": "detained_for_payment", "expected_intent": "detained_for_payment", "priority": "absolute",
     "query": "They detained my mother in hospital due to payment dispute", "notes": "Detention dispute"},
    {"id": "T054", "category": "body_withheld", "expected_intent": "body_withheld", "priority": "absolute",
     "query": "Hospital is not releasing my brother's dead body until we pay", "notes": "Body withheld for payment"},
    {"id": "T055", "category": "body_withheld", "expected_intent": "body_withheld", "priority": "absolute",
     "query": "They refused to hand over my father's body because of pending bill", "notes": "Body + bill"},

    # === NHRC RIGHT 16: PATIENT EDUCATION ===
    {"id": "T056", "category": "patient_education", "expected_intent": "patient_education", "priority": "low",
     "query": "Hospital never educated me about my health insurance scheme options", "notes": "No insurance education"},
    {"id": "T057", "category": "patient_education", "expected_intent": "patient_education", "priority": "low",
     "query": "They did not explain my rights and responsibilities as a patient", "notes": "Rights not explained"},
    {"id": "T058", "category": "patient_education", "expected_intent": "patient_education", "priority": "low",
     "query": "No health education was provided about ayushman bharat scheme", "notes": "Scheme education"},

    # === NHRC RIGHT 17: GRIEVANCE REDRESSAL ===
    {"id": "T059", "category": "grievance_redressal", "expected_intent": "grievance_redressal", "priority": "medium",
     "query": "Hospital ignored my complaint and there is no grievance mechanism", "notes": "No grievance mechanism"},
    {"id": "T060", "category": "grievance_redressal", "expected_intent": "grievance_redressal", "priority": "medium",
     "query": "They refused to accept my feedback and dismissed my complaint", "notes": "Complaint dismissed"},
    {"id": "T061", "category": "grievance_redressal", "expected_intent": "grievance_redressal", "priority": "medium",
     "query": "No response to my lodged complaint about hospital services", "notes": "No response"},

    # === IMC ETHICS: DOCTOR MISBEHAVIOR ===
    {"id": "T062", "category": "doctor_misbehavior", "expected_intent": "doctor_misbehavior", "priority": "ethics",
     "query": "Doctor shouted at my mother and called her names during checkup", "notes": "Verbal abuse"},
    {"id": "T063", "category": "doctor_misbehavior", "expected_intent": "doctor_misbehavior", "priority": "ethics",
     "query": "Surgeon was drunk during operation and under influence of alcohol", "notes": "Intoxication"},
    {"id": "T064", "category": "doctor_misbehavior", "expected_intent": "doctor_misbehavior", "priority": "ethics",
     "query": "Doctor insulted and humiliated me in front of other patients", "notes": "Public humiliation"},
    {"id": "T065", "category": "doctor_misbehavior", "expected_intent": "doctor_misbehavior", "priority": "ethics",
     "query": "Medical professional was rude and arrogant during consultation", "notes": "Unprofessional behavior"},

    # === IMC ETHICS: DOCTOR ABSENTEEISM ===
    {"id": "T066", "category": "doctor_absenteeism", "expected_intent": "doctor_absenteeism", "priority": "ethics",
     "query": "Doctor was absent during duty hours when my father needed emergency care", "notes": "Absent in emergency"},
    {"id": "T067", "category": "doctor_absenteeism", "expected_intent": "doctor_absenteeism", "priority": "ethics",
     "query": "Physician not available during scheduled appointment time", "notes": "Missed appointment"},

    # === IMC ETHICS: ADVERTISING ISSUES ===
    {"id": "T068", "category": "advertising_issues", "expected_intent": "advertising_issues", "priority": "ethics",
     "query": "Doctor is making false claims and exaggerated advertisement on sign board", "notes": "False advertising"},
    {"id": "T069", "category": "advertising_issues", "expected_intent": "advertising_issues", "priority": "ethics",
     "query": "Medical practitioner boasting about guaranteed cure in publicity", "notes": "Boasting cure"},

    # === IMC ETHICS: KICKBACK/COMMISSION ===
    {"id": "T070", "category": "kickback_commission", "expected_intent": "kickback_commission", "priority": "ethics",
     "query": "Doctor received illegal commission for referring patients to diagnostic center", "notes": "Referral commission"},
    {"id": "T071", "category": "kickback_commission", "expected_intent": "kickback_commission", "priority": "ethics",
     "query": "They are taking kickback money for sending patients to specific hospital", "notes": "Kickback money"},

    # === IMC ETHICS: PRESCRIPTION ISSUES ===
    {"id": "T072", "category": "prescription_issues", "expected_intent": "prescription_issues", "priority": "ethics",
     "query": "Doctor wrote wrong prescription with incorrect drug dosage", "notes": "Wrong prescription"},
    {"id": "T073", "category": "prescription_issues", "expected_intent": "prescription_issues", "priority": "ethics",
     "query": "Illegal prescription was given for banned medicine", "notes": "Illegal prescription"},

    # === IMC ETHICS: SEX DETERMINATION ===
    {"id": "T074", "category": "sex_determination", "expected_intent": "sex_determination", "priority": "ethics",
     "query": "Doctor performed sex determination test on my pregnant wife", "notes": "Sex determination"},
    {"id": "T075", "category": "sex_determination", "expected_intent": "sex_determination", "priority": "ethics",
     "query": "Clinic is doing female foeticide and gender selection of fetus", "notes": "Female foeticide"},

    # === IMC ETHICS: EUTHANASIA ===
    {"id": "T076", "category": "euthanasia", "expected_intent": "euthanasia", "priority": "ethics",
     "query": "Doctor practiced mercy killing on my brain dead father", "notes": "Mercy killing"},
    {"id": "T077", "category": "euthanasia", "expected_intent": "euthanasia", "priority": "ethics",
     "query": "They want to withdraw life support from my brain death patient", "notes": "Life support withdrawal"},

    # === EDGE CASES: AMBIGUOUS / COMPOUND / OUT-OF-SCOPE ===
    {"id": "T078", "category": "ambiguous", "expected_intent": "multiple", "priority": "mixed",
     "query": "Doctor was rude and also refused to give my medical records", "notes": "Compound: misbehavior + records"},
    {"id": "T079", "category": "ambiguous", "expected_intent": "emergency_care", "priority": "mixed",
     "query": "Hospital discriminated against my accident victim friend and asked for payment", "notes": "Compound: emergency + discrimination + payment"},
    {"id": "T080", "category": "out_of_scope", "expected_intent": "none", "priority": "none",
     "query": "Can you recommend a good hospital in Delhi for heart surgery", "notes": "Out of scope: recommendation"},
    {"id": "T081", "category": "out_of_scope", "expected_intent": "none", "priority": "none",
     "query": "What should I eat after my surgery for fast recovery", "notes": "Out of scope: medical advice"},
    {"id": "T082", "category": "out_of_scope", "expected_intent": "none", "priority": "none",
     "query": "Tell me the phone number of the nearest government hospital", "notes": "Out of scope: directory"},
    {"id": "T083", "category": "vague", "expected_intent": "none", "priority": "none",
     "query": "I am not happy with the hospital", "notes": "Vague: no specific issue"},
    {"id": "T084", "category": "vague", "expected_intent": "none", "priority": "none",
     "query": "Something bad happened at the clinic", "notes": "Vague: no indicators"},
    {"id": "T085", "category": "dignity_respect", "expected_intent": "dignity_respect", "priority": "high",
     "query": "Male doctor examined me without female attendant present", "notes": "Dignity during examination"},
    {"id": "T086", "category": "dignity_respect", "expected_intent": "dignity_respect", "priority": "high",
     "query": "Doctor humiliated me during examination without maintaining dignity", "notes": "Humiliation"},
    {"id": "T087", "category": "medical_negligence", "expected_intent": "medical_negligence", "priority": "high",
     "query": "Wrong treatment was given causing severe complications and infection", "notes": "Wrong treatment"},
    {"id": "T088", "category": "medical_negligence", "expected_intent": "medical_negligence", "priority": "high",
     "query": "Doctor was intoxicated and made mistake during procedure", "notes": "Drunk + error"},
    {"id": "T089", "category": "trial_compensation", "expected_intent": "trial_compensation", "priority": "high",
     "query": "My relative died during clinical trial and we got no compensation", "notes": "Death during trial"},
    {"id": "T090", "category": "trial_compensation", "expected_intent": "trial_compensation", "priority": "high",
     "query": "Patient suffered adverse effects during research but was denied compensation and care", "notes": "Adverse effects"},
]


class PCMLRATestRunner:
    """Test runner for PC-MLRA system"""

    def __init__(self):
        self.assembler = ResponseAssembler()
        self.classifier = IntentClassifier()
        self.kb = KnowledgeBase()
        self.results = []

    def run_single_test(self, test_case: Dict) -> Dict:
        """Run a single test query through the system"""
        query = test_case["query"]
        test_id = test_case["id"]

        print(f"\n[{'='*60}]")
        print(f"Running Test {test_id}: {test_case['category']}")
        print(f"Query: {query}")
        print(f"[{'='*60}]")

        # Run through response assembler
        response, proof_trace = self.assembler.generate_response(query, show_proof=True)

        # Also run intent classification separately for detailed analysis
        intents, matched_indicators = self.classifier.classify(query)

        # Build result record
        result = {
            "test_id": test_id,
            "category": test_case["category"],
            "expected_intent": test_case["expected_intent"],
            "priority": test_case["priority"],
            "query": query,
            "notes": test_case.get("notes", ""),
            "system_response": response,
            "matched_intents": [
                {"intent": intent, "confidence": round(confidence, 3)}
                for intent, confidence in intents[:5]  # Top 5
            ],
            "matched_clauses": [
                {
                    "id": clause["id"],
                    "title": clause["title"],
                    "citation": clause.get("citation_format", "")
                }
                for clause in proof_trace.matched_clauses
            ],
            "template_used": proof_trace.template_used,
            "variables_filled": len(proof_trace.variables_used),
            "proof_trace": proof_trace.to_dict(),
            "matched_indicators": matched_indicators,
            "timestamp": datetime.now().isoformat()
        }

        # Print summary
        print(f"\nMatched Intents: {[i['intent'] for i in result['matched_intents']]}")
        print(f"Matched Clauses: {[c['id'] for c in result['matched_clauses']]}")
        print(f"Template: {result['template_used']}")
        print(f"Response length: {len(response)} chars")

        return result

    def run_all_tests(self) -> List[Dict]:
        """Run all test queries"""
        print("\n" + "="*70)
        print("PC-MLRA COMPREHENSIVE TEST SUITE")
        print(f"Total Tests: {len(TEST_QUERIES)}")
        print("="*70 + "\n")

        for i, test_case in enumerate(TEST_QUERIES, 1):
            print(f"\n\n{'#'*70}")
            print(f"PROGRESS: {i}/{len(TEST_QUERIES)} ({i/len(TEST_QUERIES)*100:.1f}%)")
            print(f"{'#'*70}")

            try:
                result = self.run_single_test(test_case)
                self.results.append(result)
            except Exception as e:
                print(f"ERROR in test {test_case['id']}: {str(e)}")
                self.results.append({
                    "test_id": test_case["id"],
                    "category": test_case["category"],
                    "query": test_case["query"],
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        return self.results

    def export_json(self, filepath: str):
        """Export results to JSON"""
        output = {
            "metadata": {
                "system": "PC-MLRA",
                "version": "1.0.0",
                "total_tests": len(TEST_QUERIES),
                "completed_tests": len(self.results),
                "timestamp": datetime.now().isoformat(),
                "test_categories": list(set(t["category"] for t in TEST_QUERIES))
            },
            "test_cases": TEST_QUERIES,
            "results": self.results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nJSON exported to: {filepath}")

    def export_csv(self, filepath: str):
        """Export results to CSV (summary only)"""
        rows = []
        for result in self.results:
            rows.append({
                "test_id": result.get("test_id", ""),
                "category": result.get("category", ""),
                "query": result.get("query", ""),
                "expected_intent": result.get("expected_intent", ""),
                "top_matched_intent": result.get("matched_intents", [{}])[0].get("intent", "NONE") if result.get("matched_intents") else "NONE",
                "top_confidence": result.get("matched_intents", [{}])[0].get("confidence", 0) if result.get("matched_intents") else 0,
                "matched_clauses": ", ".join([c["id"] for c in result.get("matched_clauses", [])]),
                "template_used": result.get("template_used", "ERROR"),
                "response_length": len(result.get("system_response", "")),
                "has_ethics_notice": "IMC Ethics" in result.get("system_response", ""),
                "has_disclaimer": "disclaimer" in result.get("system_response", "").lower(),
                "error": result.get("error", "")
            })

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV exported to: {filepath}")

    def export_llm_prompts(self, filepath: str):
        """Export queries formatted for LLM testing"""
        llm_prompts = []
        for test in TEST_QUERIES:
            llm_prompts.append({
                "test_id": test["id"],
                "category": test["category"],
                "system_prompt": """You are a medical-legal rights advisor. A user has described a situation involving healthcare. 
Your task is to identify the relevant patient rights under the NHRC Charter of Patients' Rights (India, 2019) 
and applicable professional ethics under the IMC Ethics Regulations (2002). 

IMPORTANT RULES:
- Only state the rights and duties. Do NOT advise what to do or what not to do.
- Cite specific NHRC rights (e.g., Right 3: Emergency Care) and IMC sections where applicable.
- If the query is vague or out of scope, state that clearly.
- Do not hallucinate rights that are not in the NHRC Charter or IMC Regulations.
- Keep responses factual and grounded in the actual legal documents.""",
                "user_query": test["query"],
                "expected_category": test["category"]
            })

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(llm_prompts, f, indent=2, ensure_ascii=False)
        print(f"LLM prompts exported to: {filepath}")

    def generate_summary_report(self) -> Dict:
        """Generate summary statistics"""
        total = len(self.results)
        successful = len([r for r in self.results if "error" not in r])
        with_ethics = len([r for r in self.results if r.get("has_ethics_notice", False)])

        intent_distribution = {}
        for r in self.results:
            if "matched_intents" in r and r["matched_intents"]:
                top_intent = r["matched_intents"][0]["intent"]
                intent_distribution[top_intent] = intent_distribution.get(top_intent, 0) + 1

        template_distribution = {}
        for r in self.results:
            tmpl = r.get("template_used", "ERROR")
            template_distribution[tmpl] = template_distribution.get(tmpl, 0) + 1

        return {
            "total_tests": total,
            "successful_tests": successful,
            "failed_tests": total - successful,
            "tests_with_ethics_notice": with_ethics,
            "intent_distribution": intent_distribution,
            "template_distribution": template_distribution,
            "avg_response_length": sum(len(r.get("system_response", "")) for r in self.results) / max(successful, 1)
        }


def main():
    parser = argparse.ArgumentParser(description="PC-MLRA Test Suite Runner")
    parser.add_argument("--output-dir", default="./test_results", help="Output directory")
    parser.add_argument("--format", choices=["json", "csv", "both"], default="both", help="Export format")
    parser.add_argument("--llm-prompts", action="store_true", help="Also export LLM testing prompts")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Run tests
    runner = PCMLRATestRunner()
    results = runner.run_all_tests()

    # Export results
    if args.format in ["json", "both"]:
        runner.export_json(os.path.join(args.output_dir, "pcmlra_test_results.json"))
    if args.format in ["csv", "both"]:
        runner.export_csv(os.path.join(args.output_dir, "pcmlra_test_summary.csv"))
    if args.llm_prompts:
        runner.export_llm_prompts(os.path.join(args.output_dir, "llm_test_prompts.json"))

    # Print summary
    summary = runner.generate_summary_report()
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"With Ethics Notice: {summary['tests_with_ethics_notice']}")
    print(f"Avg Response Length: {summary['avg_response_length']:.0f} chars")
    print("\nTop Matched Intents:")
    for intent, count in sorted(summary['intent_distribution'].items(), key=lambda x: -x[1])[:10]:
        print(f"  {intent}: {count}")
    print("\nTemplates Used:")
    for tmpl, count in sorted(summary['template_distribution'].items(), key=lambda x: -x[1]):
        print(f"  {tmpl}: {count}")

    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print(f"Results saved to: {args.output_dir}")
    print("="*70)


if __name__ == "__main__":
    main()