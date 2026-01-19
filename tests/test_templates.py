"""
Test suite for Template Engine
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.template_engine import TemplateEngine

def test_template_loading():
    """Test that templates load correctly"""
    engine = TemplateEngine()
    
    # Check metadata
    templates = engine.templates
    assert "metadata" in templates
    assert "templates" in templates
    
    metadata = templates["metadata"]
    assert metadata.get("system") == "PC-MLRA Template Library"
    assert metadata.get("total_templates") >= 10
    
    print("✅ Template loading test passed")
    return True

def test_template_retrieval():
    """Test retrieving specific templates"""
    engine = TemplateEngine()
    
    test_templates = [
        "TEMPLATE_SINGLE_CLAUSE",
        "TEMPLATE_RIGHT_TO_RECORDS",
        "TEMPLATE_DISCLAIMER"
    ]
    
    for template_id in test_templates:
        template = engine.get_template(template_id)
        if template:
            print(f"✅ Found template: {template_id}")
            assert "description" in template
            assert "components" in template
        else:
            print(f"❌ Template not found: {template_id}")
            return False
    
    return True

def test_template_filling():
    """Test filling templates with data"""
    engine = TemplateEngine()
    
    context = {
        "title": "Right to Access Medical Records",
        "citation_format": "NHRC Charter, Right 2",
        "paraphrase": "Patients can get copies of their medical documents.",
        "rights_bulleted": ["access_medical_records", "obtain_documents"],
        "obligations_bulleted": ["hospital_provide_records", "doctor_maintain_records"],
        "exceptions_bulleted": ["ongoing_legal_cases"],
        "legal_references_bulleted": ["MCI Code of Ethics", "Consumer Protection Act"],
        "show_exact_text": False
    }
    
    result = engine.fill_template("TEMPLATE_SINGLE_CLAUSE", context)
    
    # Check that variables were replaced
    assert "Right to Access Medical Records" in result
    assert "NHRC Charter, Right 2" in result
    assert "Patients can get copies" in result
    
    print("✅ Template filling test passed")
    print(f"Result preview:\n{result[:200]}...")
    return True

def test_formatting_functions():
    """Test formatting functions"""
    engine = TemplateEngine()
    
    # Test bulleted list formatting
    items = ["First item", "Second item", "Third item"]
    bulleted = engine.format_bulleted_list(items)
    assert "• First item" in bulleted
    assert "• Second item" in bulleted
    assert "• Third item" in bulleted
    
    # Test legal references formatting
    references = ["MCI Code of Ethics", "Consumer Protection Act, 1986"]
    formatted_refs = engine.format_legal_references(references)
    assert "MCI Code of Ethics" in formatted_refs
    
    # Test empty lists
    empty_bulleted = engine.format_bulleted_list([])
    assert empty_bulleted == "None specified"
    
    print("✅ Formatting functions test passed")
    return True

def test_condition_processing():
    """Test condition processing in templates"""
    engine = TemplateEngine()
    
    context_with_data = {
        "rights": ["right1", "right2"],
        "obligations": ["obligation1"],
        "exceptions": [],
        "show_exact_text": True
    }
    
    context_empty = {
        "rights": [],
        "obligations": [],
        "exceptions": [],
        "show_exact_text": False
    }
    
    # Test conditions
    assert engine.process_condition("has_rights", context_with_data) == True
    assert engine.process_condition("has_rights", context_empty) == False
    assert engine.process_condition("has_obligations", context_with_data) == True
    assert engine.process_condition("has_exceptions", context_empty) == False
    assert engine.process_condition("show_exact_text", context_with_data) == True
    assert engine.process_condition("show_exact_text", context_empty) == False
    
    print("✅ Condition processing test passed")
    return True

def test_clause_summary():
    """Test generating clause summaries"""
    engine = TemplateEngine()
    
    sample_clause = {
        "title": "Right to Information",
        "document_abbr": "NHRC",
        "section": "1",
        "paraphrase": "Patients have right to information about diagnosis and treatment."
    }
    
    summary = engine.generate_clause_summary(sample_clause)
    
    assert "Right to Information" in summary
    assert "NHRC" in summary
    assert "Section 1" in summary
    assert "diagnosis and treatment" in summary
    
    print("✅ Clause summary test passed")
    print(f"Summary:\n{summary}")
    return True

def test_multiple_clauses_list():
    """Test generating list of multiple clauses"""
    engine = TemplateEngine()
    
    clauses = [
        {
            "title": "Right to Information",
            "document_abbr": "NHRC",
            "section": "1",
            "paraphrase": "Right to information about treatment."
        },
        {
            "title": "Right to Records",
            "document_abbr": "NHRC",
            "section": "2",
            "paraphrase": "Right to access medical records."
        }
    ]
    
    result = engine.generate_multiple_clauses_list(clauses)
    
    assert "Right to Information" in result
    assert "Right to Records" in result
    assert "---" in result  # Separator
    
    print("✅ Multiple clauses list test passed")
    print(f"Result preview:\n{result[:200]}...")
    return True

def run_all_tests():
    """Run all template engine tests"""
    print("Running Template Engine Tests")
    print("=" * 70)
    
    tests = [
        test_template_loading,
        test_template_retrieval,
        test_template_filling,
        test_formatting_functions,
        test_condition_processing,
        test_clause_summary,
        test_multiple_clauses_list
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
        print("✅ All template engine tests passed!")
        return True
    else:
        print(f"❌ {sum(1 for r in results if not r)} tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)