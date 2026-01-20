#!/usr/bin/env python3
"""Test Google Sheets Connection"""

import os
import sys
import json

# Add current directory to path
sys.path.append('.')

print("🔧 Testing Google Sheets Setup")
print("=" * 50)

# Check 1: Config file
config_file = "config/google_sheets_config.py"
if os.path.exists(config_file):
    print(f"✅ Config file found: {config_file}")
    
    # Read config to get sheet ID
    with open(config_file, 'r') as f:
        content = f.read()
        if 'SHEET_ID = "' in content:
            # Extract sheet ID
            start = content.find('SHEET_ID = "') + len('SHEET_ID = "')
            end = content.find('"', start)
            sheet_id = content[start:end]
            print(f"📋 Sheet ID: {sheet_id}")
        else:
            print("❌ SHEET_ID not found in config")
            sheet_id = None
else:
    print(f"❌ Config file not found: {config_file}")
    sheet_id = None

# Check 2: Credentials file
creds_file = "config/google_sheets_credentials.json"
if os.path.exists(creds_file):
    print(f"✅ Credentials file found: {creds_file}")
    
    # Check if it's valid JSON
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
        print(f"✅ Valid JSON credentials")
        print(f"   Service account: {creds_data.get('client_email', 'Unknown')}")
    except json.JSONDecodeError:
        print("❌ Invalid JSON in credentials file")
else:
    print(f"❌ Credentials file not found: {creds_file}")

print("\n" + "=" * 50)
print("🔌 Testing Connection...")

if sheet_id and os.path.exists(creds_file):
    try:
        # Import and test
        from utils.google_sheets_logger import get_logger
        
        # Create logger with explicit parameters
        logger = get_logger(creds_file, sheet_id)
        
        if logger.is_connected():
            print("🎉 SUCCESS! Connected to Google Sheets")
            print(f"📊 Spreadsheet: {logger.spreadsheet.title if logger.spreadsheet else 'Unknown'}")
            
            # Test logging
            print("\n📝 Testing log entry...")
            logger.log_query(
                session_id="test_session_001",
                query="Can I get my medical reports?",
                intent="access_medical_records",
                clauses=["NHRC-2", "IMC-1.3"],
                response_time=1500
            )
            
            logger.log_session_start(
                session_id="test_session_001",
                user_agent="Test/1.0"
            )
            
            print("✅ Test logs sent to Google Sheets")
            print("\n📋 Check your sheet: https://docs.google.com/spreadsheets/d/" + sheet_id)
        else:
            print("❌ Failed to connect to Google Sheets")
            print("   Common issues:")
            print("   1. Sheet not shared with service account")
            print("   2. Invalid Sheet ID")
            print("   3. Service account doesn't have editor permission")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
else:
    print("⚠️  Cannot test - missing sheet ID or credentials")

print("\n" + "=" * 50)
print("Next steps:")
print("1. Ensure Google Sheet is shared with service account")
print("2. Check service account email in credentials.json")
print("3. Make sure service account has Editor permission")
