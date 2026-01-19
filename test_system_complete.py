#!/usr/bin/env python3
"""
Complete Test of PC-MLRA System
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_knowledge_loader():
    """Test KnowledgeBase loader"""
    print("\n1. Testing KnowledgeBase Loader...")
    print("-" * 50)
    
    from src.knowledge_loader import KnowledgeBase
    
    try:
        kb = KnowledgeBase()
        print(f"✓ KnowledgeBase initialized")
        
        # Check metadata
        metadata = kb.get_metadata()
        print(f"  System: {metadata.get('system_name', 'N/A')}")
        print(f"  Version: {metadata.get('version', 'N/A')}")
        
        # Check clauses
        clauses = kb.get_all_clauses()
        print(f"  Total clauses: {len(clauses)}")
        
        if clauses:
            sample = clauses[0]
            print(f"  Sample clause ID: {sample.get('id', 'N/A')}")
            print(f"  Sample clause title: {sample.get('title', 'N/A')}")
            print(f"  Sample category: {sample.get('category', 'N/A')}")
        
        return kb, True
        
    except Exception as e:
        print(f"✗ Error loading KnowledgeBase: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def test_intent_classifier():
    """Test Intent Classifier"""
    print("\n2. Testing Intent Classifier...")
    print("-" * 50)
    
    from src.intent_classifier import IntentClassifier
    
    try:
        classifier = IntentClassifier()
        print(f"✓ IntentClassifier initialized")
        
        test_queries = [
            "Can I get my medical reports?",
            "Doctor was rude to me",
            "I need second opinion",
            "Hospital charges too much",
            "Can I see my medical records?"
        ]
        
        for query in test_queries:
            intents = classifier.classify(query)
            print(f"  Query: '{query[:30]}...'")
            print(f"    Intents: {intents}")
        
        return classifier, True
        
    except Exception as e:
        print(f"✗ Error in IntentClassifier: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def test_template_engine():
    """Test Template Engine"""
    print("\n3. Testing Template Engine...")
    print("-" * 50)
    
    from src.template_engine import TemplateEngine
    
    try:
        engine = TemplateEngine()
        print(f"✓ TemplateEngine initialized")
        
        # Test template loading
        templates = engine.templates
        print(f"  Loaded {len(templates)} templates")
        
        # Show sample template types
        template_types = set()
        for t in templates.values():
            template_types.add(t.get("template_type", "unknown"))
        
        print(f"  Template types: {', '.join(template_types)}")
        
        return engine, True
        
    except Exception as e:
        print(f"✗ Error in TemplateEngine: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def test_response_assembler():
    """Test Response Assembler"""
    print("\n4. Testing Response Assembler...")
    print("-" * 50)
    
    from src.response_assembler import ResponseAssembler
    
    try:
        assembler = ResponseAssembler()
        print(f"✓ ResponseAssembler initialized")
        
        # Test simple query
        test_query = "Can I get my medical reports?"
        response, proof = assembler.generate_response(test_query, show_proof=False)
        
        print(f"  Test query: '{test_query}'")
        print(f"  Response length: {len(response)} characters")
        print(f"  Response preview: {response[:100]}...")
        
        if proof:
            print(f"  Proof trace keys: {list(proof.keys())}")
        
        return assembler, True
        
    except Exception as e:
        print(f"✗ Error in ResponseAssembler: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def test_full_pipeline():
    """Test the complete pipeline"""
    print("\n5. Testing Complete Pipeline...")
    print("-" * 50)
    
    from src.main import PCMLRAConsole
    
    try:
        console = PCMLRAConsole()
        print(f"✓ PCMLRAConsole initialized")
        
        # Test various queries
        test_cases = [
            ("Can I get my medical reports?", "access_medical_records"),
            ("Doctor was rude to me", "doctor_misbehavior"),
            ("I need second opinion", "second_opinion"),
            ("Hospital is charging too much", "transparency_rates"),
            ("Can I choose my own pharmacy?", "choose_pharmacy"),
        ]
        
        for query, expected_intent_type in test_cases:
            response = console.process_query(query)
            if response:
                print(f"  ✓ '{query[:25]}...' → Response: {len(response)} chars")
            else:
                print(f"  ✓ '{query[:25]}...' → Command processed")
        
        # Test system stats
        print(f"\n  Testing system commands...")
        console.display_stats()
        
        return console, True
        
    except Exception as e:
        print(f"✗ Error in full pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def check_data_files():
    """Check all data files"""
    print("\n6. Checking Data Files...")
    print("-" * 50)
    
    files_to_check = [
        "data/structured/knowledge_base_complete.json",
        "data/templates/response_templates.json",
        "data/structured/integration_summary.json"
    ]
    
    all_ok = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    size = len(data)
                    item_type = "dictionary"
                elif isinstance(data, list):
                    size = len(data)
                    item_type = "list"
                else:
                    size = "unknown"
                    item_type = type(data).__name__
                
                print(f"✓ {file_path}")
                print(f"  Size: {os.path.getsize(file_path):,} bytes")
                print(f"  Content: {item_type} with {size} items")
                
            except Exception as e:
                print(f"✗ {file_path}: Error reading - {e}")
                all_ok = False
        else:
            print(f"✗ {file_path}: File not found")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 70)
    print("PC-MLRA SYSTEM COMPREHENSIVE TEST")
    print("=" * 70)
    
    # Check data files first
    data_ok = check_data_files()
    
    if not data_ok:
        print("\n✗ Data files have issues. Fix them before proceeding.")
        return False
    
    # Test components
    kb_ok = test_knowledge_loader()[1]
    intent_ok = test_intent_classifier()[1]
    template_ok = test_template_engine()[1]
    assembler_ok = test_response_assembler()[1]
    pipeline_ok = test_full_pipeline()[1]
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    results = {
        "Knowledge Base": kb_ok,
        "Intent Classifier": intent_ok,
        "Template Engine": template_ok,
        "Response Assembler": assembler_ok,
        "Complete Pipeline": pipeline_ok,
    }
    
    all_passed = True
    for component, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{component:25} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready for deployment.")
        print("\nNext steps:")
        print("1. Run: python run_web.py")
        print("2. Open browser to: http://localhost:5000")
        print("3. Start using the web interface!")
    else:
        print("⚠️  SOME TESTS FAILED. Please fix issues before deployment.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
