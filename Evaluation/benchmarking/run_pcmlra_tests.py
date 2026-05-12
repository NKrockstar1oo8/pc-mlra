#!/usr/bin/env python3
"""
Run PC-MLRA on all 90 test cases and save responses
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath('.'))

from src.response_assembler import ResponseAssembler


# ============================================================
# COMPLETE TEST SUITE (90 Queries)
# ============================================================

TEST_QUERIES = [
    # === NHRC RIGHT 1: RIGHT TO INFORMATION ===
    {"id": "T001", "category": "right_to_information", "query": "Doctor did not explain my diagnosis to me"},
    {"id": "T002", "category": "right_to_information", "query": "What is wrong with my health condition the doctor is not telling me"},
    {"id": "T003", "category": "right_to_information", "query": "Nurse refused to clarify my treatment options"},
    
    # === NHRC RIGHT 2: ACCESS TO MEDICAL RECORDS ===
    {"id": "T004", "category": "access_medical_records", "query": "Hospital is not giving me my medical reports"},
    {"id": "T005", "category": "access_medical_records", "query": "I need my discharge summary but they refused to provide it"},
    {"id": "T006", "category": "access_medical_records", "query": "Doctor shouted at me when I asked for my test results"},
    {"id": "T007", "category": "access_medical_records", "query": "They denied access to my case papers and medical file"},
    
    # === NHRC RIGHT 3: EMERGENCY CARE ===
    {"id": "T008", "category": "emergency_care", "query": "Doctor not admitting my friend who met with an accident"},
    {"id": "T009", "category": "emergency_care", "query": "Hospital asked for advance payment for my father's heart attack treatment"},
    {"id": "T010", "category": "emergency_care", "query": "They refused emergency care to my brother who was bleeding heavily after an accident"},
    {"id": "T011", "category": "emergency_care", "query": "My mother was unconscious and hospital turned her away"},
    {"id": "T012", "category": "emergency_care", "query": "Critical patient denied treatment because no money was given in advance"},
    
    # === NHRC RIGHT 4: INFORMED CONSENT ===
    {"id": "T013", "category": "informed_consent", "query": "Surgery was performed on me without my permission"},
    {"id": "T014", "category": "informed_consent", "query": "Doctor forced me to sign consent form without explaining the risks"},
    {"id": "T015", "category": "informed_consent", "query": "They did the operation without telling me what could go wrong"},
    {"id": "T016", "category": "informed_consent", "query": "My consent was taken but they did a different procedure than what was explained"},
    
    # === NHRC RIGHT 5: PRIVACY & CONFIDENTIALITY ===
    {"id": "T017", "category": "privacy_confidentiality", "query": "Doctor told my relatives about my HIV status without asking me"},
    {"id": "T018", "category": "privacy_confidentiality", "query": "Hospital staff discussed my abortion in the corridor where everyone could hear"},
    {"id": "T019", "category": "privacy_confidentiality", "query": "My medical condition was leaked to my employer by the hospital"},
    {"id": "T020", "category": "privacy_confidentiality", "query": "Nurse shared my confidential health details with other patients"},
    
    # === NHRC RIGHT 6: SECOND OPINION ===
    {"id": "T021", "category": "second_opinion", "query": "Doctor refused to let me consult another specialist for second opinion"},
    {"id": "T022", "category": "second_opinion", "query": "Hospital is not providing my records to another doctor for second opinion"},
    {"id": "T023", "category": "second_opinion", "query": "They threatened me when I said I want to get a different doctor's opinion"},
    
    # === NHRC RIGHT 7: TRANSPARENT PRICING ===
    {"id": "T024", "category": "transparent_pricing", "query": "Hospital overcharged me for treatment and added hidden costs to my bill"},
    {"id": "T025", "category": "transparent_pricing", "query": "They are charging too much money and the rates are not transparent"},
    {"id": "T026", "category": "transparent_pricing", "query": "Doctor is scamming me with expensive unnecessary tests"},
    {"id": "T027", "category": "transparent_pricing", "query": "I paid more than expected because they did not give itemized bill"},
    
    # === NHRC RIGHT 8: NON-DISCRIMINATION ===
    {"id": "T028", "category": "non_discrimination", "query": "Hospital refused treatment because I am HIV positive"},
    {"id": "T029", "category": "non_discrimination", "query": "Doctor said he won't treat Muslims in his clinic"},
    {"id": "T030", "category": "non_discrimination", "query": "They discriminated against my father because of his caste"},
    {"id": "T031", "category": "non_discrimination", "query": "Patient was denied care due to AIDS and treated differently because of disease"},
    {"id": "T032", "category": "non_discrimination", "query": "Hospital won't treat poor patients and only admits rich people"},
    
    # === NHRC RIGHT 9: PATIENT SAFETY ===
    {"id": "T033", "category": "patient_safety", "query": "I caught infection in hospital because of dirty ward and poor hygiene"},
    {"id": "T034", "category": "patient_safety", "query": "Unsafe care provided to my mother with unclean equipment"},
    {"id": "T035", "category": "patient_safety", "query": "Medical error caused harm to my child during treatment"},
    {"id": "T036", "category": "patient_safety", "query": "Hospital negligence led to complications in my surgery"},
    
    # === NHRC RIGHT 10: TREATMENT CHOICE ===
    {"id": "T037", "category": "treatment_choice", "query": "Doctor forced me to take allopathy and did not allow ayurveda option"},
    {"id": "T038", "category": "treatment_choice", "query": "I want to choose alternative treatment but they are not offering other options"},
    {"id": "T039", "category": "treatment_choice", "query": "Patient was not allowed to choose between available treatment options"},
    
    # === NHRC RIGHT 11: CHOICE OF SOURCE ===
    {"id": "T040", "category": "choice_of_source", "query": "Hospital forced me to buy medicines from their pharmacy only"},
    {"id": "T041", "category": "choice_of_source", "query": "Doctor insisted I get tests done only at their recommended lab"},
    {"id": "T042", "category": "choice_of_source", "query": "They refused to let me purchase medicines from outside chemist"},
    
    # === NHRC RIGHT 12: PROPER REFERRAL ===
    {"id": "T043", "category": "proper_referral", "query": "Doctor referred me to another hospital for commission money"},
    {"id": "T044", "category": "proper_referral", "query": "They forced referral to a specialist who pays them kickback"},
    {"id": "T045", "category": "proper_referral", "query": "Unnecessary referral was made to higher center for money"},
    
    # === NHRC RIGHT 13: CLINICAL TRIAL RIGHTS ===
    {"id": "T046", "category": "clinical_trial_rights", "query": "I was forced into a clinical trial without proper explanation"},
    {"id": "T047", "category": "clinical_trial_rights", "query": "Research experiment conducted on me without my consent"},
    {"id": "T048", "category": "clinical_trial_rights", "query": "Study participant was misled about the risks of the trial"},
    
    # === NHRC RIGHT 14: BIOMEDICAL RESEARCH ===
    {"id": "T049", "category": "biomedical_research", "query": "Biomedical research was conducted on patients without ethics committee approval"},
    {"id": "T050", "category": "biomedical_research", "query": "Human research involved vulnerable people without informed consent"},
    {"id": "T051", "category": "biomedical_research", "query": "Health research participant was not compensated for injuries"},
    
    # === NHRC RIGHT 15: DETENTION FOR PAYMENT / BODY WITHHELD ===
    {"id": "T052", "category": "detained_for_payment", "query": "Hospital is not discharging my father because bill payment is pending"},
    {"id": "T053", "category": "detained_for_payment", "query": "They detained my mother in hospital due to payment dispute"},
    {"id": "T054", "category": "body_withheld", "query": "Hospital is not releasing my brother's dead body until we pay"},
    {"id": "T055", "category": "body_withheld", "query": "They refused to hand over my father's body because of pending bill"},
    
    # === NHRC RIGHT 16: PATIENT EDUCATION ===
    {"id": "T056", "category": "patient_education", "query": "Hospital never educated me about my health insurance scheme options"},
    {"id": "T057", "category": "patient_education", "query": "They did not explain my rights and responsibilities as a patient"},
    {"id": "T058", "category": "patient_education", "query": "No health education was provided about ayushman bharat scheme"},
    
    # === NHRC RIGHT 17: GRIEVANCE REDRESSAL ===
    {"id": "T059", "category": "grievance_redressal", "query": "Hospital ignored my complaint and there is no grievance mechanism"},
    {"id": "T060", "category": "grievance_redressal", "query": "They refused to accept my feedback and dismissed my complaint"},
    {"id": "T061", "category": "grievance_redressal", "query": "No response to my lodged complaint about hospital services"},
    
    # === IMC ETHICS: DOCTOR MISBEHAVIOR ===
    {"id": "T062", "category": "doctor_misbehavior", "query": "Doctor shouted at my mother and called her names during checkup"},
    {"id": "T063", "category": "doctor_misbehavior", "query": "Surgeon was drunk during operation and under influence of alcohol"},
    {"id": "T064", "category": "doctor_misbehavior", "query": "Doctor insulted and humiliated me in front of other patients"},
    {"id": "T065", "category": "doctor_misbehavior", "query": "Medical professional was rude and arrogant during consultation"},
    
    # === IMC ETHICS: DOCTOR ABSENTEEISM ===
    {"id": "T066", "category": "doctor_absenteeism", "query": "Doctor was absent during duty hours when my father needed emergency care"},
    {"id": "T067", "category": "doctor_absenteeism", "query": "Physician not available during scheduled appointment time"},
    
    # === IMC ETHICS: ADVERTISING ISSUES ===
    {"id": "T068", "category": "advertising_issues", "query": "Doctor is making false claims and exaggerated advertisement on sign board"},
    {"id": "T069", "category": "advertising_issues", "query": "Medical practitioner boasting about guaranteed cure in publicity"},
    
    # === IMC ETHICS: KICKBACK/COMMISSION ===
    {"id": "T070", "category": "kickback_commission", "query": "Doctor received illegal commission for referring patients to diagnostic center"},
    {"id": "T071", "category": "kickback_commission", "query": "They are taking kickback money for sending patients to specific hospital"},
    
    # === IMC ETHICS: PRESCRIPTION ISSUES ===
    {"id": "T072", "category": "prescription_issues", "query": "Doctor wrote wrong prescription with incorrect drug dosage"},
    {"id": "T073", "category": "prescription_issues", "query": "Illegal prescription was given for banned medicine"},
    
    # === IMC ETHICS: SEX DETERMINATION ===
    {"id": "T074", "category": "sex_determination", "query": "Doctor performed sex determination test on my pregnant wife"},
    {"id": "T075", "category": "sex_determination", "query": "Clinic is doing female foeticide and gender selection of fetus"},
    
    # === IMC ETHICS: EUTHANASIA ===
    {"id": "T076", "category": "euthanasia", "query": "Doctor practiced mercy killing on my brain dead father"},
    {"id": "T077", "category": "euthanasia", "query": "They want to withdraw life support from my brain death patient"},
    
    # === EDGE CASES: AMBIGUOUS / COMPOUND / OUT-OF-SCOPE ===
    {"id": "T078", "category": "ambiguous", "query": "Doctor was rude and also refused to give my medical records"},
    {"id": "T079", "category": "ambiguous", "query": "Hospital discriminated against my accident victim friend and asked for payment"},
    {"id": "T080", "category": "out_of_scope", "query": "Can you recommend a good hospital in Delhi for heart surgery"},
    {"id": "T081", "category": "out_of_scope", "query": "What should I eat after my surgery for fast recovery"},
    {"id": "T082", "category": "out_of_scope", "query": "Tell me the phone number of the nearest government hospital"},
    {"id": "T083", "category": "vague", "query": "I am not happy with the hospital"},
    {"id": "T084", "category": "vague", "query": "Something bad happened at the clinic"},
    {"id": "T085", "category": "dignity_respect", "query": "Male doctor examined me without female attendant present"},
    {"id": "T086", "category": "dignity_respect", "query": "Doctor humiliated me during examination without maintaining dignity"},
    {"id": "T087", "category": "medical_negligence", "query": "Wrong treatment was given causing severe complications and infection"},
    {"id": "T088", "category": "medical_negligence", "query": "Doctor was intoxicated and made mistake during procedure"},
    {"id": "T089", "category": "trial_compensation", "query": "My relative died during clinical trial and we got no compensation"},
    {"id": "T090", "category": "trial_compensation", "query": "Patient suffered adverse effects during research but was denied compensation and care"},
]


def main():
    print("="*70)
    print("PC-MLRA COMPREHENSIVE TEST SUITE - 90 QUERIES")
    print("="*70)
    
    assembler = ResponseAssembler()
    results = []
    
    os.makedirs('test_results', exist_ok=True)
    
    for i, test in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i:2d}/90] {test['id']}: {test['query'][:55]}...")
        
        try:
            response, proof_trace = assembler.generate_response(test['query'], show_proof=True)
            
            results.append({
                "test_id": test['id'],
                "category": test['category'],
                "query": test['query'],
                "system_response": response,
                "matched_intents": [
                    {"intent": intent, "confidence": round(confidence, 3)}
                    for intent, confidence in proof_trace.matched_intents
                ],
                "matched_clauses": [
                    {
                        "id": c["id"],
                        "title": c["title"],
                        "citation": c.get("citation_format", "")
                    }
                    for c in proof_trace.matched_clauses
                ],
                "template_used": proof_trace.template_used,
                "variables_filled": len(proof_trace.variables_used),
                "timestamp": datetime.now().isoformat()
            })
            
            # Print compact summary
            intents = [m['intent'] for m in results[-1]['matched_intents']]
            clauses = [c['id'] for c in results[-1]['matched_clauses']]
            print(f"    Intents: {intents[:2]} | Clauses: {clauses} | Template: {proof_trace.template_used}")
            
        except Exception as e:
            print(f"    ✗ ERROR: {str(e)[:60]}")
            results.append({
                "test_id": test['id'],
                "category": test['category'],
                "query": test['query'],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # Save results
    output_path = 'test_results/pcmlra_test_results.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "metadata": {
                "system": "PC-MLRA",
                "version": "1.0.0",
                "total_tests": len(TEST_QUERIES),
                "completed": len([r for r in results if "error" not in r]),
                "failed": len([r for r in results if "error" in r]),
                "timestamp": datetime.now().isoformat()
            },
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    # Print final summary
    successful = len([r for r in results if "error" not in r])
    failed = len([r for r in results if "error" in r])
    
    print("\n" + "="*70)
    print("TEST RUN COMPLETE")
    print("="*70)
    print(f"Total tests:     {len(results)}")
    print(f"Successful:      {successful}")
    print(f"Failed:          {failed}")
    print(f"Output file:     {output_path}")
    print(f"File size:       {os.path.getsize(output_path) / 1024:.1f} KB")
    print("="*70)
    
    # Show template distribution
    from collections import Counter
    templates = Counter(r.get('template_used', 'ERROR') for r in results if 'error' not in r)
    print("\nTemplate usage:")
    for tmpl, count in templates.most_common():
        print(f"  {count:2d}x  {tmpl}")
    
    # Show intent distribution
    all_intents = []
    for r in results:
        if 'error' not in r and r.get('matched_intents'):
            all_intents.extend([m['intent'] for m in r['matched_intents']])
    intent_counts = Counter(all_intents)
    print("\nTop matched intents:")
    for intent, count in intent_counts.most_common(10):
        print(f"  {count:2d}x  {intent}")


if __name__ == "__main__":
    main()