#!/usr/bin/env python3
"""Test the simple logger"""

import sys
import os
sys.path.append('.')

print("🔧 Testing Simple Google Sheets Logger")
print("=" * 50)

# Import the simple logger
from utils.simple_sheets_logger import get_simple_logger

# Get logger
logger = get_simple_logger()

print(f"✅ Logger created")
print(f"📊 Connected: {logger.is_connected()}")

if logger.is_connected():
    print(f"📋 Spreadsheet: {logger.spreadsheet.title}")
    print(f"📊 Worksheets: {list(logger.worksheets.keys())}")
    
    # Test logging
    print("\n📝 Testing log functions...")
    
    # Test a query log
    logger.log_query(
        session_id="test_session_001",
        query="Can I get my medical reports?",
        intent="access_medical_records",
        response_time=1200
    )
    print("✅ Query logged")
    
    # Test another query
    logger.log_query(
        session_id="test_session_001",
        query="Doctor was rude",
        intent="professional_conduct",
        response_time=800
    )
    print("✅ Second query logged")
    
    print("\n🎉 All tests completed!")
    print(f"📊 Check your Google Sheet:")
    print(f"   https://docs.google.com/spreadsheets/d/1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
    print("\n📋 Look for 'query_logs' worksheet")
    
else:
    print("\n❌ Logger not connected")
    print("\n🔧 Let's debug step by step...")
    
    # Check files
    print("\n1. Checking files...")
    creds_file = "config/google_sheets_credentials.json"
    if os.path.exists(creds_file):
        print(f"   ✅ Credentials file exists: {creds_file}")
        try:
            with open(creds_file, 'r') as f:
                creds = json.load(f)
            print(f"   ✅ Valid JSON, Service Account: {creds.get('client_email')}")
        except Exception as e:
            print(f"   ❌ Invalid JSON: {e}")
    else:
        print(f"   ❌ Missing: {creds_file}")
    
    print("\n2. Checking Sheet ID...")
    # Try to get sheet ID manually
    try:
        with open("config/google_sheets_config.py", 'r') as f:
            content = f.read()
            if '"SHEET_ID"' in content:
                print("   ✅ SHEET_ID found in config")
                # Extract it
                import re
                match = re.search(r'"SHEET_ID"\s*:\s*"([^"]+)"', content)
                if match:
                    sheet_id = match.group(1)
                    print(f"   📋 Sheet ID: {sheet_id}")
                else:
                    print("   ❌ Could not extract Sheet ID")
            else:
                print("   ❌ SHEET_ID not in config")
    except Exception as e:
        print(f"   ❌ Error reading config: {e}")
    
    print("\n📋 ACTION REQUIRED:")
    print("1. Open: https://docs.google.com/spreadsheets/d/1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
    print("2. Click SHARE button (top-right)")
    print("3. Add: pc-mlra-logs@pc-mlra-logs.iam.gserviceaccount.com")
    print("4. Set permission: Editor")
    print("5. Click SEND")

print("\n" + "=" * 50)
