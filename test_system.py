"""
Quick test script for PC-MLRA system
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.response_assembler import ResponseAssembler

def run_quick_tests():
    """Run quick tests of the system"""
    print("PC-MLRA Quick System Test")
    print("=" * 70)
    
    assembler = ResponseAssembler()
    
    # Test cases with expected outcomes
    test_cases = [
        {
            "query": "hospital won't give my medical reports",
            "description": "Medical records access",
            "expected_intent": "access_medical_records",
            "expected_clause": "NHRC-2"
        },
        {
            "query": "doctor did surgery without asking me",
            "description": "Informed consent violation",
            "expected_intent": "informed_consent",
            "expected_clause": "NHRC-4"
        },
        {
            "query": "emergency room asked for payment first",
            "description": "Emergency care rights",
            "expected_intent": "emergency_care",
            "expected_clause": "NHRC-3"
        },
        {
            "query": "doctor told others about my illness",
            "description": "Privacy breach",
            "expected_intent": "privacy_confidentiality",
            "expected_clause": "NHRC-5"
        },
        {
            "query": "hospital overcharged me",
            "description": "Transparent pricing",
            "expected_intent": "transparent_pricing",
            "expected_clause": "NHRC-7"
        }
    ]
    
    print("\nRunning test cases...\n")
    
    all_passed = True
    for i, test in enumerate(test_cases):
        print(f"Test {i+1}: {test['description']}")
        print(f"Query: '{test['query']}'")
        
        response, proof_trace = assembler.generate_response(test['query'], show_proof=False)
        
        # Check if expected intent was matched
        matched_intents = [intent for intent, _ in proof_trace.matched_intents]
        intent_found = test['expected_intent'] in matched_intents
        
        # Check if expected clause was found
        matched_clauses = [c['id'] for c in proof_trace.matched_clauses]
        clause_found = test['expected_clause'] in matched_clauses
        
        if intent_found:
            print(f"  ✓ Found intent: {test['expected_intent']}")
        else:
            print(f"  ✗ Missing intent: {test['expected_intent']}")
            print(f"    Found intents: {matched_intents}")
            all_passed = False
        
        if clause_found:
            print(f"  ✓ Found clause: {test['expected_clause']}")
        else:
            print(f"  ✗ Missing clause: {test['expected_clause']}")
            print(f"    Found clauses: {matched_clauses}")
            all_passed = False
        
        if intent_found or clause_found:
            # Show first 2 lines of response
            lines = response.split('\n')[:2]
            preview = ' '.join(lines)[:100]
            print(f"  Response: {preview}...")
        else:
            print(f"  Response: No relevant rights found")
        
        print()
    
    # Test edge cases
    print("\nTesting edge cases...\n")
    
    edge_cases = [
        "what are my rights",
        "doctor was rude",
        "hospital is dirty",
        "can't afford medicine"
    ]
    
    for query in edge_cases:
        print(f"Query: '{query}'")
        response, _ = assembler.generate_response(query, show_proof=False)
        lines = response.split('\n')
        first_line = lines[0] if lines else "No response"
        print(f"Response: {first_line[:80]}...")
        print()
    
    print("=" * 70)
    if all_passed:
        print("✅ All tests passed!")
        print("\nTo run the full system:")
        print("  python src/main.py")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)