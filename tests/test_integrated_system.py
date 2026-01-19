"""
Integrated system test combining all components
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.intent_classifier import IntentClassifier
from src.knowledge_loader import KnowledgeBase
from src.template_engine import TemplateEngine
from src.response_assembler import ResponseAssembler

def test_integrated_pipeline():
    """Test the complete pipeline from query to knowledge retrieval"""
    
    classifier = IntentClassifier()
    kb = KnowledgeBase()
    
    test_cases = [
        {
            "query": "doctor refused to give my medical reports",
            "expected_intents": ["access_medical_records"],
            "expected_clause_ids": ["NHRC-2"]
        },
        {
            "query": "surgery was done without my permission",
            "expected_intents": ["informed_consent"],
            "expected_clause_ids": ["NHRC-4"]
        },
        {
            "query": "hospital asked for advance payment in emergency",
            "expected_intents": ["emergency_care"],
            "expected_clause_ids": ["NHRC-3"]
        },
        {
            "query": "doctor shared my health information with others",
            "expected_intents": ["privacy_confidentiality", "right_to_information"],
            "expected_clause_ids": ["NHRC-5", "NHRC-1"]
        },
        {
            "query": "they overcharged me for treatment",
            "expected_intents": ["transparent_pricing"],
            "expected_clause_ids": ["NHRC-7"]
        },
        {
            "query": "doctor discriminated against me because of my illness",
            "expected_intents": ["non_discrimination"],
            "expected_clause_ids": ["NHRC-8"]
        }
    ]
    
    print("Integrated System Test: Query → Intent → Knowledge")
    print("=" * 70)
    
    all_passed = True
    for i, test_case in enumerate(test_cases):
        print(f"Test Case {i+1}: '{test_case["query"]}'")
        
        # Step 1: Intent classification
        intents = classifier.classify(test_case["query"])
        matched_intents = [intent for intent, _ in intents]
        
        print(f"  Detected intents: {matched_intents[:3]}")
        
        # Check if expected intent is detected
        intent_found = False
        for expected in test_case["expected_intents"]:
            if expected in matched_intents:
                print(f"  ✓ Found expected intent: '{expected}'")
                intent_found = True
                break
        
        if not intent_found:
            print(f"  ✗ Expected intent not found: {test_case['expected_intents']}")
            print(f"    Found intents: {matched_intents}")
            all_passed = False
            continue
        
        # Step 2: Knowledge retrieval
        for intent in matched_intents[:2]:
            clauses = kb.get_clauses_by_intent(intent)
            clause_ids = [c["id"] for c in clauses]
            
            if clauses:
                print(f"  Clauses found for '{intent}': {clause_ids}")
            
            # Check if expected clauses are found
            clause_found = False
            for expected_id in test_case["expected_clause_ids"]:
                if expected_id in clause_ids:
                    print(f"  ✓ Found expected clause: {expected_id}")
                    
                    # Show clause details
                    clause = kb.get_clause_by_id(expected_id)
                    if clause:
                        print(f"    Title: {clause['title']}")
                        print(f"    Citation: {clause['citation_format']}")
                    
                    clause_found = True
                    break
            
            if clause_found:
                break
        
        if not clause_found and clauses:
            print(f"  ⚠ Found clauses but not expected ones")
            print(f"    Expected: {test_case['expected_clause_ids']}")
            print(f"    Found: {clause_ids}")
    
    print("" + "=" * 70)
    return all_passed

def test_template_integration():
    """Test template engine integration"""
    print("Testing Template Engine Integration")
    print("=" * 70)
    
    engine = TemplateEngine()
    kb = KnowledgeBase()
    
    # Get a clause
    clause = kb.get_clause_by_id("NHRC-2")
    assert clause is not None
    
    # Prepare context
    context = {
        "title": clause["title"],
        "citation_format": clause["citation_format"],
        "paraphrase": clause["paraphrase"],
        "rights_bulleted": clause.get("rights", []),
        "obligations_bulleted": clause.get("obligations", []),
        "exceptions_bulleted": clause.get("exceptions", []),
        "legal_references_bulleted": clause.get("legal_references", []),
        "timeframe_note": clause.get("timeframes", {}),
        "show_exact_text": False,
        "show_proof_trace": True
    }
    
    # Fill template
    response = engine.fill_template("TEMPLATE_SINGLE_CLAUSE", context)
    
    # Verify response contains expected content
    assert clause["title"] in response
    assert clause["citation_format"] in response
    assert "Your Rights:" in response or "In simpler terms:" in response
    
    print("✅ Template integration test passed")
    print(f"Response preview:{response[:300]}...")
    return True

def test_response_assembler():
    """Test complete response assembler"""
    print("Testing Response Assembler")
    print("=" * 70)
    
    assembler = ResponseAssembler()
    
    test_queries = [
        "doctor refused my medical records",
        "emergency treatment was denied",
        "no consent taken for surgery"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        response, proof_trace = assembler.generate_response(query, show_proof=False)
        
        # Check response is generated
        assert len(response) > 0
        assert "Disclaimer" in response
        
        # Check proof trace was created
        assert proof_trace.query == query
        assert len(proof_trace.matched_intents) > 0
        
        print(f"  ✓ Response generated ({len(response)} chars)")
        print(f"  ✓ Matched {len(proof_trace.matched_intents)} intents")
        print(f"  ✓ Found {len(proof_trace.matched_clauses)} clauses")
    
    print("✅ Response assembler test passed")
    return True

def test_complex_queries():
    """Test queries with multiple intents"""
    classifier = IntentClassifier()
    kb = KnowledgeBase()
    
    complex_queries = [
        "doctor refused to give my reports and was shouting at me",
        "hospital overcharged me and shared my information with insurance",
        "no emergency treatment without advance payment and they discriminated against me"
    ]
    
    print("Complex Query Analysis")
    print("=" * 70)
    
    for query in complex_queries:
        print(f"Query: '{query}'")
        intents = classifier.classify(query)
        
        print("  Detected intents:")
        for intent, confidence in intents[:3]:
            details = classifier.get_intent_details(intent)
            print(f"    - {intent}: {confidence:.2f} ({details.get('description', '')[:50]}...)")
            
            # Get relevant clauses
            clauses = kb.get_clauses_by_intent(intent)
            if clauses:
                clause_titles = [c["title"] for c in clauses[:2]]
                print(f"      Relevant: {', '.join(clause_titles)}")
    
    print("✅ Complex query test passed")
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    assembler = ResponseAssembler()
    
    edge_cases = [
        "",  # Empty query
        "what",  # Very short query
        "this is a completely unrelated query about weather",  # Unrelated
        "xyz123",  # Nonsense
    ]
    
    print("Testing Edge Cases")
    print("=" * 70)
    
    for query in edge_cases:
        print(f"Query: '{query}'")
        try:
            response, proof_trace = assembler.generate_response(query, show_proof=False)
            
            # Even edge cases should generate some response
            assert len(response) > 0
            
            # Check for appropriate template
            if len(proof_trace.matched_clauses) == 0:
                assert "TEMPLATE_NO_MATCH_FOUND" in proof_trace.template_used
                print(f"  ✓ Handled with no-match template")
            else:
                print(f"  ✓ Generated response with {len(proof_trace.matched_clauses)} clauses")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return False
    
    print("✅ Edge case test passed")
    return True

def run_all_tests():
    """Run all integrated system tests"""
    print("Running Integrated System Tests")
    print("=" * 70)
    
    tests = [
        test_integrated_pipeline,
        test_template_integration,
        test_response_assembler,
        test_complex_queries,
        test_edge_cases
    ]
    
    results = []
    for test in tests:
        print(f"{'='*70}")
        print(f"Running: {test.__name__}")
        print(f"{'='*70}")
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            results.append(False)
    
    print("" + "=" * 70)
    print("Test Summary:")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print("" + "=" * 70)
    if all(results):
        print("To run the system:")
        print("  python src/main.py")
        print("For quick testing:")
        print("  python test_system.py")
        return True
    else:
        print(f"❌ {sum(1 for r in results if not r)} tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
