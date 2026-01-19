"""
Test suite for Knowledge Base
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.knowledge_loader import KnowledgeBase

def test_knowledge_base_loading():
    """Test that knowledge base loads correctly"""
    kb = KnowledgeBase()
    
    # Check metadata
    metadata = kb.get_metadata()
    assert metadata.get("system_name") == "PC-MLRA Knowledge Base"
    assert metadata.get("version") in ["2.0.0", "2.0.1"]
    assert metadata.get("total_clauses") == 46
    
    # Check documents
    docs = kb.get_documents_info()
    assert "NHRC" in docs
    assert "IMC" in docs
    assert docs["NHRC"]["name"] == "Charter of Patients' Rights by NHRC (2019)"
    
    print("✅ Knowledge base metadata test passed")
    return True

def test_clause_retrieval():
    """Test retrieval of specific clauses"""
    kb = KnowledgeBase()
    
    # Test by ID
    clause = kb.get_clause_by_id("NHRC-1")
    assert clause is not None
    assert clause["title"] == "Right to Information"
    assert "right_to_information" in clause["rights"]
    
    clause = kb.get_clause_by_id("NHRC-2")
    assert clause is not None
    assert clause["title"] == "Right to Records and Reports"
    assert "access_medical_records" in clause["rights"]
    
    clause = kb.get_clause_by_id("NHRC-3")
    assert clause is not None
    assert clause["title"] == "Right to Emergency Medical Care"
    
    print("✅ Clause retrieval test passed")
    return True

def test_intent_matching():
    """Test clause retrieval by intent"""
    kb = KnowledgeBase()
    
    # Test access_medical_records intent
    clauses = kb.get_clauses_by_intent("access_medical_records")
    assert len(clauses) >= 1
    assert any(c["id"] == "NHRC-2" for c in clauses)
    
    # Test informed_consent intent
    clauses = kb.get_clauses_by_intent("informed_consent")
    assert len(clauses) >= 1
    assert any(c["id"] == "NHRC-4" for c in clauses)
    
    # Test emergency_care intent
    clauses = kb.get_clauses_by_intent("emergency_care")
    assert len(clauses) >= 1
    assert any(c["id"] == "NHRC-3" for c in clauses)
    
    print("✅ Intent matching test passed")
    return True

def test_category_search():
    """Test retrieval by category"""
    kb = KnowledgeBase()
    
    # Test access_information category
    clauses = kb.get_clauses_by_category("access_information")
    assert len(clauses) >= 5
    
    category_titles = [c["title"] for c in clauses]
    assert "Right to Information" in category_titles
    assert "Right to Records and Reports" in category_titles
    
    # Test consent_autonomy category
    clauses = kb.get_clauses_by_category("consent_autonomy")
    assert len(clauses) >= 2
    
    print("✅ Category search test passed")
    return True

def test_keyword_search():
    """Test keyword search functionality"""
    kb = KnowledgeBase()
    
    # Test emergency keyword
    results = kb.search_clauses_by_keyword("emergency")
    assert len(results) >= 1
    assert any("emergency" in c["title"].lower() for c in results)
    
    # Test consent keyword
    results = kb.search_clauses_by_keyword("consent")
    assert len(results) >= 2
    
    # Test privacy keyword
    results = kb.search_clauses_by_keyword("privacy")
    assert len(results) >= 1
    
    print("✅ Keyword search test passed")
    return True

def test_actor_rights():
    """Test rights retrieval for actors"""
    kb = KnowledgeBase()
    
    # Test patient rights
    patient_rights = kb.get_rights_for_actor("patient")
    assert len(patient_rights) >= 10
    
    # Test doctor obligations
    doctor_obligations = kb.get_obligations_for_actor("doctor")
    assert len(doctor_obligations) >= 5
    
    # Test hospital obligations
    hospital_obligations = kb.get_obligations_for_actor("hospital")
    assert len(hospital_obligations) >= 5
    
    print("✅ Actor rights test passed")
    return True

def test_relationships():
    """Test relationship extraction"""
    kb = KnowledgeBase()
    
    relationships = kb.get_relationships()
    assert len(relationships) >= 5
    
    # Check that we have right->obligation relationships
    relationship_types = [r["type"] for r in relationships]
    assert "creates_obligation" in relationship_types
    
    # Check specific relationship exists
    relationship_descriptions = [r["description"] for r in relationships]
    assert any("right to information" in desc.lower() for desc in relationship_descriptions)
    
    print("✅ Relationships test passed")
    return True

def test_all_clauses():
    """Test retrieving all clauses"""
    kb = KnowledgeBase()
    
    clauses = kb.get_all_clauses()
    assert len(clauses) >= 17
    
    # Check a few specific clauses exist
    clause_ids = [c["id"] for c in clauses]
    assert "NHRC-1" in clause_ids
    assert "NHRC-2" in clause_ids
    assert "NHRC-3" in clause_ids
    assert "NHRC-17" in clause_ids  # Last NHRC clause
    
    print("✅ All clauses retrieval test passed")
    return True

def run_all_tests():
    """Run all knowledge base tests"""
    print("Running Knowledge Base Tests")
    print("=" * 70)
    
    tests = [
        test_knowledge_base_loading,
        test_clause_retrieval,
        test_intent_matching,
        test_category_search,
        test_keyword_search,
        test_actor_rights,
        test_relationships,
        test_all_clauses
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
        print("✅ All knowledge base tests passed!")
        return True
    else:
        print(f"❌ {sum(1 for r in results if not r)} tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)