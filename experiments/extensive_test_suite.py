#!/usr/bin/env python3
"""
EXTENSIVE TEST SUITE for PC-MLRA - 100+ Test Cases
Covers: Patient Rights, Doctor Obligations, Edge Cases, Non-Legal Queries
"""

import time
import json
import random
from datetime import datetime
from app.services.pc_mlra_service import PCMLRAService

def create_extensive_test_cases():
    """Create 100+ comprehensive test cases"""
    
    # CATEGORY 1: PATIENT RIGHTS (40 test cases)
    patient_rights = [
        # Informed Consent (10 cases)
        ("What is informed consent?", "informed_consent"),
        ("Do I need to give consent for surgery?", "informed_consent"),
        ("Can doctors operate without my permission?", "informed_consent"),
        ("What information must doctors provide before treatment?", "informed_consent"),
        ("Is verbal consent enough for major procedures?", "informed_consent"),
        ("Can family members give consent for me?", "informed_consent"),
        ("What if I'm unconscious in emergency?", "informed_consent"),
        ("Do I have right to refuse treatment?", "informed_consent"),
        ("What risks must doctors disclose?", "informed_consent"),
        ("Can I withdraw consent after giving it?", "informed_consent"),
        
        # Medical Records (10 cases)
        ("Can I access my medical records?", "access_medical_records"),
        ("How to get copy of medical reports?", "access_medical_records"),
        ("Are hospital records confidential?", "access_medical_records"),
        ("Who can see my medical history?", "access_medical_records"),
        ("How long are records kept?", "access_medical_records"),
        ("Can I correct errors in my records?", "access_medical_records"),
        ("Do I need to pay for medical records?", "access_medical_records"),
        ("Electronic vs paper records access?", "access_medical_records"),
        ("Can insurance companies access records?", "access_medical_records"),
        ("What if hospital denies record access?", "access_medical_records"),
        
        # Emergency Care (10 cases)
        ("Do hospitals have to treat emergencies?", "emergency_care"),
        ("What is emergency medical care?", "emergency_care"),
        ("Can ER turn away patients?", "emergency_care"),
        ("What if I can't pay for emergency?", "emergency_care"),
        ("Are private hospitals required for emergencies?", "emergency_care"),
        ("What qualifies as emergency?", "emergency_care"),
        ("Time limits for emergency treatment?", "emergency_care"),
        ("Can hospitals transfer emergency patients?", "emergency_care"),
        ("Emergency care for foreigners?", "emergency_care"),
        ("Emergency vs non-emergency treatment?", "emergency_care"),
        
        # Privacy & Confidentiality (10 cases)
        ("Are my medical details private?", "privacy_confidentiality"),
        ("Can doctors share my information?", "privacy_confidentiality"),
        ("What is doctor-patient confidentiality?", "privacy_confidentiality"),
        ("Exceptions to medical confidentiality?", "privacy_confidentiality"),
        ("Can police access medical records?", "privacy_confidentiality"),
        ("Privacy in shared hospital rooms?", "privacy_confidentiality"),
        ("Electronic records security?", "privacy_confidentiality"),
        ("Can employers access medical info?", "privacy_confidentiality"),
        ("Mental health records privacy?", "privacy_confidentiality"),
        ("HIV status confidentiality?", "privacy_confidentiality"),
    ]
    
    # CATEGORY 2: DOCTOR OBLIGATIONS (30 test cases)
    doctor_obligations = [
        # Professional Conduct (15 cases)
        ("What ethical rules do doctors follow?", "professional_conduct"),
        ("Can doctors refuse treatment?", "professional_conduct"),
        ("Doctor's duty to explain treatment?", "professional_conduct"),
        ("Are doctors required to update knowledge?", "professional_conduct"),
        ("Can doctors advertise services?", "professional_conduct"),
        ("Doctor's duty in epidemics?", "professional_conduct"),
        ("Are doctors required to maintain records?", "professional_conduct"),
        ("Can doctors accept gifts from patients?", "professional_conduct"),
        ("Doctor's duty to report errors?", "professional_conduct"),
        ("Are doctors required to wear ID?", "professional_conduct"),
        ("Can doctors practice alternative medicine?", "professional_conduct"),
        ("Doctor's working hours limits?", "professional_conduct"),
        ("Are doctors required to have insurance?", "professional_conduct"),
        ("Can doctors refuse HIV patients?", "professional_conduct"),
        ("Doctor's duty to refer specialists?", "professional_conduct"),
        
        # Patient Relationship (15 cases)
        ("Can doctors treat family members?", "patient_relationship"),
        ("Doctor's duty to respect patients?", "patient_relationship"),
        ("Are doctors allowed to date patients?", "patient_relationship"),
        ("Can doctors disclose patient info to family?", "patient_relationship"),
        ("Doctor's duty in terminal illness?", "patient_relationship"),
        ("Are doctors required to speak local language?", "patient_relationship"),
        ("Can doctors prescribe over phone?", "patient_relationship"),
        ("Doctor's duty in medical research?", "patient_relationship"),
        ("Are doctors required to give second opinion?", "patient_relationship"),
        ("Can doctors charge extra fees?", "patient_relationship"),
        ("Doctor's duty in organ donation?", "patient_relationship"),
        ("Are doctors required to explain costs?", "patient_relationship"),
        ("Can doctors practice outside specialty?", "patient_relationship"),
        ("Doctor's duty in medical negligence?", "patient_relationship"),
        ("Are doctors required to provide receipts?", "patient_relationship"),
    ]
    
    # CATEGORY 3: GENERAL MEDICAL-LEGAL (20 test cases)
    general_medical = [
        ("What are patient rights in India?", "general_rights"),
        ("Medical Council of India regulations?", "general_regulations"),
        ("How to file medical complaint?", "complaint_procedure"),
        ("What is medical negligence?", "medical_negligence"),
        ("Hospital accreditation requirements?", "hospital_standards"),
        ("Medical insurance rights?", "insurance_rights"),
        ("Clinical trial participant rights?", "clinical_trials"),
        ("Mental healthcare rights?", "mental_health"),
        ("Women's healthcare rights?", "womens_health"),
        ("Child patient rights?", "child_rights"),
        ("Elderly patient rights?", "elderly_rights"),
        ("Disabled patient rights?", "disabled_rights"),
        ("Transgender healthcare rights?", "lgbtq_health"),
        ("Rural healthcare rights?", "rural_health"),
        ("Medical education rights?", "medical_education"),
        ("Telemedicine regulations?", "telemedicine"),
        ("Ayush system regulations?", "ayush"),
        ("Blood donation regulations?", "blood_donation"),
        ("Transplant regulations?", "organ_transplant"),
        ("End of life care rights?", "end_of_life"),
    ]
    
    # CATEGORY 4: NON-LEGAL / OUT-OF-SCOPE (20 test cases)
    non_legal = [
        ("What are cricket rules?", "sports"),
        ("How to invest in stock market?", "finance"),
        ("Recipe for biryani?", "cooking"),
        ("Weather forecast tomorrow?", "weather"),
        ("Best movies on Netflix?", "entertainment"),
        ("How to learn Python?", "education"),
        ("Car maintenance tips?", "automotive"),
        ("Gardening advice?", "hobbies"),
        ("Travel destinations in India?", "travel"),
        ("Cooking tips for beginners?", "cooking"),
        ("Fitness exercise routine?", "fitness"),
        ("Stock market trends?", "finance"),
        ("Mobile phone recommendations?", "technology"),
        ("Study tips for exams?", "education"),
        ("Home decoration ideas?", "lifestyle"),
        ("Pet care advice?", "pets"),
        ("Cooking chicken recipes?", "cooking"),
        ("Video game recommendations?", "gaming"),
        ("Book reading suggestions?", "reading"),
        ("Music playlist suggestions?", "music"),
    ]
    
    # CATEGORY 5: EDGE CASES & AMBIGUOUS (10 test cases)
    edge_cases = [
        ("What about consent?", "ambiguous"),  # Very short
        ("Records?", "ambiguous"),  # Single word
        ("Emergency?", "ambiguous"),  # Single word
        ("", "empty_query"),  # Empty query
        ("   ", "empty_query"),  # Whitespace only
        ("12345", "non_text"),  # Numbers only
        ("@#$%^&*", "non_text"),  # Symbols only
        ("consent records emergency privacy", "multiple_keywords"),
        ("medical and legal rights", "compound_query"),
        ("what can you help me with?", "meta_query"),
    ]
    
    # Combine all test cases
    all_tests = []
    
    # Add category labels
    for query, intent in patient_rights:
        all_tests.append({
            "query": query,
            "category": "patient_rights",
            "subcategory": intent,
            "should_have_proof": True,
            "expected_intent": intent
        })
    
    for query, intent in doctor_obligations:
        all_tests.append({
            "query": query,
            "category": "doctor_obligations", 
            "subcategory": intent,
            "should_have_proof": True,
            "expected_intent": intent
        })
    
    for query, intent in general_medical:
        all_tests.append({
            "query": query,
            "category": "general_medical",
            "subcategory": intent,
            "should_have_proof": True,
            "expected_intent": intent
        })
    
    for query, intent in non_legal:
        all_tests.append({
            "query": query,
            "category": "non_legal",
            "subcategory": intent,
            "should_have_proof": False,
            "expected_intent": "general_query"
        })
    
    for query, intent in edge_cases:
        all_tests.append({
            "query": query,
            "category": "edge_cases",
            "subcategory": intent,
            "should_have_proof": False,
            "expected_intent": "general_query"
        })
    
    return all_tests

def run_extensive_test():
    """Run comprehensive test suite"""
    
    print("\n" + "="*80)
    print("PC-MLRA EXTENSIVE TEST SUITE - 100+ TEST CASES")
    print("="*80)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load service
    service = PCMLRAService()
    test_cases = create_extensive_test_cases()
    
    print(f"📊 Total test cases: {len(test_cases)}")
    print(f"   • Patient Rights: {len([t for t in test_cases if t['category'] == 'patient_rights'])}")
    print(f"   • Doctor Obligations: {len([t for t in test_cases if t['category'] == 'doctor_obligations'])}")
    print(f"   • General Medical: {len([t for t in test_cases if t['category'] == 'general_medical'])}")
    print(f"   • Non-Legal: {len([t for t in test_cases if t['category'] == 'non_legal'])}")
    print(f"   • Edge Cases: {len([t for t in test_cases if t['category'] == 'edge_cases'])}")
    print()
    
    # Run tests
    results = []
    category_results = {
        'patient_rights': {'total': 0, 'correct': 0, 'proofs': 0},
        'doctor_obligations': {'total': 0, 'correct': 0, 'proofs': 0},
        'general_medical': {'total': 0, 'correct': 0, 'proofs': 0},
        'non_legal': {'total': 0, 'correct': 0, 'proofs': 0},
        'edge_cases': {'total': 0, 'correct': 0, 'proofs': 0}
    }
    
    subcategory_results = {}
    response_times = []
    
    print("🧪 Running tests... (This may take a minute)")
    print("-" * 80)
    
    for i, test in enumerate(test_cases):
        if (i + 1) % 20 == 0:
            print(f"   Processed {i + 1}/{len(test_cases)} tests...")
        
        # Run query
        start_time = time.time()
        result = service.process_query(test['query'])
        elapsed = time.time() - start_time
        response_times.append(elapsed)
        
        # Analyze result
        proof = result.get('proof', '')
        has_proof = bool(proof)
        has_citation = 'NHRC' in proof or 'IMC' in proof
        intent = result.get('intent', 'unknown')
        
        # Determine correctness
        if test['should_have_proof']:
            correct = has_proof and has_citation
        else:
            correct = not has_proof
        
        # Record results
        test_result = {
            'id': i + 1,
            'query': test['query'],
            'category': test['category'],
            'subcategory': test['subcategory'],
            'expected_proof': test['should_have_proof'],
            'actual_proof': has_proof,
            'actual_intent': intent,
            'expected_intent': test['expected_intent'],
            'has_citation': has_citation,
            'correct': correct,
            'response_time': elapsed,
            'proof_text': proof[:100] + "..." if len(proof) > 100 else proof
        }
        
        results.append(test_result)
        
        # Update category stats
        cat = test['category']
        category_results[cat]['total'] += 1
        if correct:
            category_results[cat]['correct'] += 1
        if has_proof:
            category_results[cat]['proofs'] += 1
        
        # Update subcategory stats
        subcat = test['subcategory']
        if subcat not in subcategory_results:
            subcategory_results[subcat] = {'total': 0, 'correct': 0}
        subcategory_results[subcat]['total'] += 1
        if correct:
            subcategory_results[subcat]['correct'] += 1
    
    print()
    print("-" * 80)
    print("📊 COMPREHENSIVE RESULTS ANALYSIS")
    print("-" * 80)
    
    # Calculate overall metrics
    total_tests = len(test_cases)
    correct_tests = sum(1 for r in results if r['correct'])
    overall_accuracy = (correct_tests / total_tests) * 100
    
    # Legal vs Non-legal accuracy
    legal_tests = [r for r in results if r['category'] in ['patient_rights', 'doctor_obligations', 'general_medical']]
    non_legal_tests = [r for r in results if r['category'] in ['non_legal', 'edge_cases']]
    
    legal_correct = sum(1 for r in legal_tests if r['correct'])
    non_legal_correct = sum(1 for r in non_legal_tests if r['correct'])
    
    legal_accuracy = (legal_correct / len(legal_tests) * 100) if legal_tests else 0
    non_legal_accuracy = (non_legal_correct / len(non_legal_tests) * 100) if non_legal_tests else 0
    
    # Proof generation stats
    total_proofs_generated = sum(1 for r in results if r['actual_proof'])
    proof_citations = sum(1 for r in results if r['has_citation'])
    
    # Response time stats
    avg_response_time = sum(response_times) / len(response_times)
    max_response_time = max(response_times)
    min_response_time = min(response_times)
    
    print(f"\n🎯 OVERALL SYSTEM PERFORMANCE:")
    print(f"   Total tests: {total_tests}")
    print(f"   Correct responses: {correct_tests}")
    print(f"   Overall Accuracy: {overall_accuracy:.2f}%")
    print()
    
    print(f"⚖️  LEGAL QUERY PERFORMANCE:")
    print(f"   Legal queries: {len(legal_tests)}")
    print(f"   Correct legal responses: {legal_correct}")
    print(f"   Legal Accuracy: {legal_accuracy:.2f}%")
    print(f"   Proofs generated: {sum(1 for r in legal_tests if r['actual_proof'])}/{len(legal_tests)}")
    print(f"   Valid citations: {sum(1 for r in legal_tests if r['has_citation'])}/{len(legal_tests)}")
    print()
    
    print(f"🚫 NON-LEGAL QUERY PERFORMANCE:")
    print(f"   Non-legal queries: {len(non_legal_tests)}")
    print(f"   Correct non-legal responses: {non_legal_correct}")
    print(f"   Non-legal Accuracy: {non_legal_accuracy:.2f}%")
    print(f"   False positives (proofs): {sum(1 for r in non_legal_tests if r['actual_proof'])}")
    print()
    
    print(f"⏱️  PERFORMANCE METRICS:")
    print(f"   Average response time: {avg_response_time:.4f} seconds")
    print(f"   Minimum response time: {min_response_time:.4f} seconds")
    print(f"   Maximum response time: {max_response_time:.4f} seconds")
    print(f"   Queries per second: {1/avg_response_time:.1f}")
    print()
    
    print("-" * 80)
    print("📈 CATEGORY-WISE ANALYSIS")
    print("-" * 80)
    
    for category, stats in category_results.items():
        if stats['total'] > 0:
            accuracy = (stats['correct'] / stats['total']) * 100
            proof_rate = (stats['proofs'] / stats['total']) * 100
            
            category_name = category.replace('_', ' ').title()
            print(f"\n{category_name}:")
            print(f"   Tests: {stats['total']}")
            print(f"   Accuracy: {accuracy:.1f}%")
            print(f"   Proof generation: {proof_rate:.1f}% ({stats['proofs']}/{stats['total']})")
    
    print()
    print("-" * 80)
    print("🎯 TOP PERFORMING SUBCATEGORIES")
    print("-" * 80)
    
    # Sort subcategories by accuracy
    sorted_subcats = sorted(
        [(sc, data['correct']/data['total']*100, data['total']) 
         for sc, data in subcategory_results.items() if data['total'] >= 3],
        key=lambda x: x[1],
        reverse=True
    )
    
    print("\n🏆 Best performing (accuracy):")
    for i, (subcat, accuracy, total) in enumerate(sorted_subcats[:5]):
        subcat_name = subcat.replace('_', ' ').title()
        print(f"   {i+1}. {subcat_name}: {accuracy:.1f}% ({total} tests)")
    
    print("\n⚠️  Needs improvement:")
    for i, (subcat, accuracy, total) in enumerate(sorted_subcats[-5:]):
        subcat_name = subcat.replace('_', ' ').title()
        print(f"   {i+1}. {subcat_name}: {accuracy:.1f}% ({total} tests)")
    
    print()
    print("-" * 80)
    print("🔍 ERROR ANALYSIS")
    print("-" * 80)
    
    # Find common error patterns
    errors = [r for r in results if not r['correct']]
    
    print(f"\nTotal errors: {len(errors)}")
    
    if errors:
        error_types = {
            'false_positive': [e for e in errors if e['actual_proof'] and not e['expected_proof']],
            'false_negative': [e for e in errors if not e['actual_proof'] and e['expected_proof']],
            'wrong_intent': [e for e in errors if e['actual_intent'] != e['expected_intent']],
        }
        
        for error_type, error_list in error_types.items():
            if error_list:
                percentage = (len(error_list) / len(errors)) * 100
                type_name = error_type.replace('_', ' ').title()
                print(f"   {type_name}: {len(error_list)} errors ({percentage:.1f}%)")
                
                # Show examples
                if len(error_list) > 0:
                    example = error_list[0]
                    print(f"      Example: \"{example['query']}\"")
                    print(f"      Expected: {'Proof' if example['expected_proof'] else 'No proof'}")
                    print(f"      Got: {'Proof' if example['actual_proof'] else 'No proof'}")
                    if example['actual_proof']:
                        print(f"      Proof: {example['proof_text']}")
    
    print()
    print("-" * 80)
    print("📋 RECOMMENDATIONS FOR IMPROVEMENT")
    print("-" * 80)
    
    recommendations = []
    
    # Analyze patterns
    if non_legal_accuracy < 90:
        recommendations.append(f"1. Improve intent classifier for non-legal queries (current: {non_legal_accuracy:.1f}%)")
    
    if legal_accuracy < 80:
        recommendations.append(f"2. Expand knowledge base for legal queries (current: {legal_accuracy:.1f}%)")
    
    false_positives = sum(1 for r in non_legal_tests if r['actual_proof'])
    if false_positives > 0:
        recommendations.append(f"3. Reduce false positives (current: {false_positives} on {len(non_legal_tests)} tests)")
    
    # Check response time
    if avg_response_time > 0.1:
        recommendations.append(f"4. Optimize response time (current: {avg_response_time:.3f}s)")
    
    # Check proof citation rate
    proof_citation_rate = (proof_citations / total_proofs_generated * 100) if total_proofs_generated > 0 else 0
    if proof_citation_rate < 90:
        recommendations.append(f"5. Improve citation accuracy (current: {proof_citation_rate:.1f}%)")
    
    if recommendations:
        print("\nBased on test results:")
        for rec in recommendations:
            print(f"   • {rec}")
    else:
        print("\n✅ System performing well across all metrics!")
    
    # Save detailed results
    output_file = f"extensive_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_data = {
        'test_summary': {
            'total_tests': total_tests,
            'overall_accuracy': overall_accuracy,
            'legal_accuracy': legal_accuracy,
            'non_legal_accuracy': non_legal_accuracy,
            'avg_response_time': avg_response_time,
            'test_timestamp': datetime.now().isoformat()
        },
        'category_results': category_results,
        'subcategory_results': subcategory_results,
        'error_analysis': {
            'total_errors': len(errors),
            'error_types': {k: len(v) for k, v in error_types.items()}
        },
        'detailed_results': results[:50]  # First 50 for brevity
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    print(f"\n⏱️  Total test duration: {sum(response_times):.2f} seconds")
    print(f"🏁 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*80)

if __name__ == "__main__":
    run_extensive_test()
