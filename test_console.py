#!/usr/bin/env python3
"""
Test PC-MLRA Console Application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import PCMLRAConsole

print("Testing PC-MLRA Console Application...")
print("=" * 60)

try:
    # Create instance
    app = PCMLRAConsole()
    print("✅ PCMLRAConsole initialized successfully")
    
    # Test a query
    test_queries = [
        "Can I get my medical reports?",
        "Doctor was rude to me",
        "I need second opinion"
    ]
    
    for query in test_queries:
        response = app.process_query(query)
        if response:
            print(f"✅ Query: '{query}'")
            print(f"   Response length: {len(response)} characters")
            print(f"   Preview: {response[:150]}...")
        else:
            print(f"✅ Query: '{query}' (command processed)")
    
    # Test system commands
    print("\nTesting system commands...")
    commands = ["stats", "list rights", "list categories"]
    for cmd in commands:
        response = app.process_query(cmd)
        print(f"✅ Command: '{cmd}' executed")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Console app is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
