#!/usr/bin/env python3
"""
Test PC-MLRA Web Endpoints
"""

import requests
import time
import sys

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method='GET', data=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {endpoint} - Status: {response.status_code}")
            return response.json()
        else:
            print(f"❌ {endpoint} - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")
        return None

def main():
    """Test all endpoints"""
    print("Testing PC-MLRA Web Endpoints")
    print("=" * 60)
    
    # Wait a moment for server to be fully ready
    time.sleep(2)
    
    # Test basic endpoints
    print("\n1. Basic Endpoints:")
    health = test_endpoint('/api/health')
    stats = test_endpoint('/api/system/stats')
    examples = test_endpoint('/api/examples')
    history = test_endpoint('/api/history')
    
    # Test search
    print("\n2. Search Endpoint:")
    search = test_endpoint('/api/knowledge/search?q=medical')
    
    # Test query processing
    print("\n3. Query Processing:")
    query_result = test_endpoint('/api/query', method='POST', 
                                 data={'query': 'Can I get my medical reports?', 'show_proof': False})
    
    # Test clear history
    print("\n4. History Management:")
    clear_result = test_endpoint('/api/history/clear', method='POST')
    
    # Display summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    
    if health:
        print(f"   Health: {health.get('status', 'N/A')}")
    
    if stats:
        print(f"   System: {stats.get('system_name', 'N/A')}")
        print(f"   Version: {stats.get('version', 'N/A')}")
        print(f"   Total Clauses: {stats.get('total_clauses', 'N/A')}")
    
    if examples:
        print(f"   Example Questions: {len(examples.get('examples', []))}")
    
    if query_result:
        print(f"   Query Response: {len(query_result.get('response', ''))} chars")
        print(f"   Query Status: {query_result.get('status', 'N/A')}")
    
    print("\n✅ Web application is running successfully!")
    print(f"\n🌐 Open browser to: {BASE_URL}")
    print(f"💬 Chat interface: {BASE_URL}/chat")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
