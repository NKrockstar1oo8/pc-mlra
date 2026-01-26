#!/usr/bin/env python3
"""
Test the corrected service architecture
"""
import re
import sys
import os

# Add project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.services.pc_mlra_correct import PCMLRAServiceCorrect

def run_architecture_test():
    print("="*70)
    print("TESTING CORRECTED ARCHITECTURE")
    print("="*70)
    
    service = PCMLRAServiceCorrect(debug=False)
    
    # Test cases
    test_cases = [
        # (Query, Should have proof?, Expected intent category)
        ("Doctor refused to give my medical reports", True, "access_medical_records"),
        ("Hospital asked for advance payment in emergency", True, "emergency_care"),
        ("Surgery done without my permission", True, "informed_consent"),
        ("Doctor shared my information with others", True, "privacy_confidentiality"),
        ("What are cricket rules?", False, "non_medical"),
        ("Stock market investment tips", False, "non_medical"),
        ("Recipe for chocolate cake", False, "non_medical"),
        ("Medical negligence complaint", True, "medical_negligence"),
        ("Second opinion rights", True, "second_opinion"),
        ("Overcharged for treatment", True, "transparent_pricing"),
    ]
    
    print("\n🧪 Running tests...")
    print("-" * 70)
    
    results = []
    
    for query, should_have_proof, expected_intent in test_cases:
        print(f"\n📝 Query: '{query}'")
        print(f"   Expected: {'Proof' if should_have_proof else 'No proof'}, Intent: {expected_intent}")
        
        result = service.process_query(query)
        
        has_proof = bool(result['proof'])
        intent = result['intent']
        
        # Check correctness
        proof_correct = (has_proof == should_have_proof)
        
        if proof_correct:
            print(f"   ✅ PROOF: {'Has proof' if has_proof else 'No proof'} (correct)")
        else:
            print(f"   ❌ PROOF: {'Has proof' if has_proof else 'No proof'} (WRONG)")
        
        print(f"   Intent: {intent}")
        if has_proof:
            print(f"   Proof text: '{result['proof']}'")
        print(f"   Confidence: {result['confidence']:.2f}")
        
        results.append({
            'query': query,
            'proof_correct': proof_correct,
            'has_proof': has_proof,
            'intent': intent,
            'confidence': result['confidence']
        })
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    proof_correct_count = sum(1 for r in results if r['proof_correct'])
    proof_accuracy = proof_correct_count / total * 100
    
    medical_queries = [r for r in results if r['has_proof']]
    non_medical_queries = [r for r in results if not r['has_proof']]
    
    print(f"\nOverall Proof Accuracy: {proof_accuracy:.1f}% ({proof_correct_count}/{total})")
    print(f"Medical queries with proofs: {len(medical_queries)}")
    print(f"Non-medical queries without proofs: {len(non_medical_queries)}")
    
    # Check architecture
    print(f"\n🔧 ARCHITECTURE VALIDATION:")
    
    # Test direct ResponseAssembler access
    from src.response_assembler import ResponseAssembler
    assembler = ResponseAssembler()
    
    test_query = "informed consent"
    response, proof_trace = assembler.generate_response(test_query, show_proof=False)
    
    print(f"   ✅ ResponseAssembler accessible")
    print(f"   ✅ ProofTrace object available with {len(proof_trace.matched_clauses)} clauses")
    print(f"   ✅ Citation format: {proof_trace.matched_clauses[0].get('citation_format', 'N/A')}")
    
    if proof_accuracy >= 80:
        print(f"\n🎉 SUCCESS: Correct architecture working!")
    else:
        print(f"\n⚠️  Needs improvement: Proof accuracy {proof_accuracy:.1f}%")

if __name__ == "__main__":
    run_architecture_test()
