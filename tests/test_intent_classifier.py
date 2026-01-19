"""
Test suite for Intent Classifier
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.intent_classifier import IntentClassifier

def test_basic_classification():
    """Test basic intent classification"""
    classifier = IntentClassifier()
    
    test_cases = [
        {
            "query": "doctor refused to give my medical reports",
            "expected_intents": ["access_medical_records"]
        },
        {
            "query": "surgery was done without my permission",
            "expected_intents": ["informed_consent"]
        },
        {
            "query": "doctor shouted at me and was disrespectful",
            "expected_intents": ["doctor_misbehavior"]
        },
        {
            "query": "hospital asked for payment in emergency",
            "expected_intents": ["emergency_care"]
        },
        {
            "query": "they overcharged me for treatment",
            "expected_intents": ["transparent_pricing"]
        }
    ]
    
    all_passed = True
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: '{test_case['query']}'")
        intents = classifier.classify(test_case["query"])
        matched_intents = [intent for intent, _ in intents]
        
        for expected in test_case["expected_intents"]:
            if expected in matched_intents:
                print(f"  ✓ Correctly identified '{expected}'")
            else:
                print(f"  ✗ Failed to identify '{expected}'")
                print(f"    Found intents: {matched_intents}")
                all_passed = False
        
        print(f"  Confidence scores: {[(i, f'{c:.2f}') for i, c in intents[:2]]}")
    
    return all_passed

def test_confidence_scores():
    """Test that confidence scores are reasonable"""
    classifier = IntentClassifier()
    
    # Strong match query
    strong_query = "hospital denied access to my medical records and refused to give copies"
    strong_intents = classifier.classify(strong_query)
    
    print(f"\nStrong match query: '{strong_query}'")
    for intent, confidence in strong_intents[:3]:
        print(f"  {intent}: {confidence:.2f}")
    
    # Weak match query  
    weak_query = "I need some documents"
    weak_intents = classifier.classify(weak_query)
    
    print(f"\nWeak match query: '{weak_query}'")
    for intent, confidence in weak_intents[:3]:
        print(f"  {intent}: {confidence:.2f}")
    
    # Check that strong match has higher confidence
    if strong_intents and weak_intents:
        strong_conf = strong_intents[0][1]
        weak_conf = weak_intents[0][1] if weak_intents else 0
        if strong_conf > weak_conf:
            print(f"\n✓ Strong match has higher confidence ({strong_conf:.2f} > {weak_conf:.2f})")
            return True
        else:
            print(f"\n✗ Confidence scores not as expected")
            return False
    return True

def test_multiple_intents():
    """Test queries that match multiple intents"""
    classifier = IntentClassifier()
    
    test_cases = [
        {
            "query": "doctor refused reports and shouted at me",
            "expected_intents": ["access_medical_records", "doctor_misbehavior"]
        },
        {
            "query": "surgery without consent and overcharged",
            "expected_intents": ["informed_consent", "transparent_pricing"]
        }
    ]
    
    all_passed = True
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: '{test_case['query']}'")
        intents = classifier.classify(test_case["query"])
        matched_intents = [intent for intent, _ in intents]
        
        matched_count = 0
        for expected in test_case["expected_intents"]:
            if expected in matched_intents:
                matched_count += 1
                print(f"  ✓ Found '{expected}'")
            else:
                print(f"  ✗ Missing '{expected}'")
        
        if matched_count >= 2:
            print(f"  ✓ Found {matched_count} expected intents")
        else:
            print(f"  ✗ Only found {matched_count} expected intents")
            all_passed = False
        
        print(f"  All matched: {matched_intents}")
    
    return all_passed

def test_intent_details():
    """Test getting details about intents"""
    classifier = IntentClassifier()
    
    test_intents = ["access_medical_records", "informed_consent", "emergency_care"]
    
    print("\nTesting intent details:")
    for intent in test_intents:
        details = classifier.get_intent_details(intent)
        if details:
            print(f"\n{intent}:")
            print(f"  Description: {details.get('description', 'N/A')}")
            print(f"  Category: {details.get('category', 'N/A')}")
            print(f"  Keywords: {details.get('keywords', [])[:5]}...")
        else:
            print(f"\n✗ Intent '{intent}' not found")
            return False
    
    return True

def test_intent_categories():
    """Test getting intents by category"""
    classifier = IntentClassifier()
    
    categories = ["access_information", "consent_autonomy", "quality_safety"]
    
    print("\nTesting intents by category:")
    for category in categories:
        intents = classifier.get_intents_by_category(category)
        print(f"\n{category.replace('_', ' ').title()}:")
        for intent in intents[:3]:  # Show first 3
            details = classifier.get_intent_details(intent)
            print(f"  • {intent} - {details.get('description', '')[:60]}...")
        print(f"  Total: {len(intents)} intents")
    
    return True

def run_all_tests():
    """Run all intent classifier tests"""
    print("Running Intent Classifier Tests")
    print("=" * 70)
    
    tests = [
        test_basic_classification,
        test_confidence_scores,
        test_multiple_intents,
        test_intent_details,
        test_intent_categories
    ]
    
    results = []
    for test in tests:
        print(f"\n{'='*70}")
        print(f"Running: {test.__name__}")
        print(f"{'='*70}")
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    print("Test Summary:")
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test.__name__}: {status}")
    
    print("\n" + "=" * 70)
    if all(results):
        print("✅ All intent classifier tests passed!")
        return True
    else:
        print(f"❌ {sum(1 for r in results if not r)} tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)