#!/usr/bin/env python3
"""
Test PC-MLRA Web Application
"""

import requests
import time
import sys

def test_web_app():
    """Test the web application endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing PC-MLRA Web Application...")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ Health check passed: {response.json()}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
        return False
    
    # Test 2: System stats
    print("2. Testing system stats...")
    try:
        response = requests.get(f"{base_url}/api/system/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ System stats: {data.get('system_name')}")
            print(f"   ✓ Total clauses: {data.get('total_clauses')}")
        else:
            print(f"   ✗ System stats failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ System stats error: {e}")
    
    # Test 3: Example queries
    print("3. Testing example queries...")
    try:
        response = requests.get(f"{base_url}/api/examples", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Loaded {len(data.get('examples', []))} example questions")
        else:
            print(f"   ✗ Example queries failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Example queries error: {e}")
    
    # Test 4: Process a query
    print("4. Testing query processing...")
    try:
        test_query = "Can I get my medical reports?"
        response = requests.post(
            f"{base_url}/api/query",
            json={"query": test_query, "show_proof": False},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Query processed: '{test_query}'")
            print(f"   ✓ Response length: {len(data.get('response', ''))} chars")
            print(f"   ✓ Status: {data.get('status')}")
        else:
            print(f"   ✗ Query processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ✗ Query processing error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Web application tests completed!")
    print("\nTo use the web interface:")
    print(f"1. Open browser to: http://localhost:5000")
    print(f"2. Click 'Start Chatting with PC-MLRA'")
    print(f"3. Ask questions about medical rights!")
    
    return True

if __name__ == "__main__":
    # Wait a bit for the server to start if needed
    time.sleep(2)
    success = test_web_app()
    sys.exit(0 if success else 1)
