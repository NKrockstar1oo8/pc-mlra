#!/usr/bin/env python3
"""Test Google Sheets connection"""

import os
import sys
sys.path.append('.')

from utils.google_sheets_logger import get_logger

print("Testing Google Sheets connection...")
print("=" * 50)

# Check if credentials file exists
creds_file = "config/google_sheets_credentials.json"
if os.path.exists(creds_file):
    print(f"✅ Credentials file found: {creds_file}")
    print(f"   File size: {os.path.getsize(creds_file)} bytes")
else:
    print(f"❌ Credentials file NOT found: {creds_file}")
    print("   Please download service account JSON and save as above")
    exit(1)

# Check config file
config_file = "config/google_sheets_config.py"
if os.path.exists(config_file):
    print(f"✅ Config file found: {config_file}")
    
    # Check if Sheet ID is updated
    with open(config_file, 'r') as f:
        content = f.read()
        if '1aBcDeFgHiJkLmNoPqRsTuVwXyZ' in content:
            print("⚠️  Warning: Using default Sheet ID")
            print("   Please update config/google_sheets_config.py with your actual Sheet ID")
        else:
            print("✅ Sheet ID appears to be updated")
else:
    print(f"❌ Config file NOT found: {config_file}")
    exit(1)

# Try to create logger
try:
    logger = get_logger()
    print("✅ Logger created successfully")
    
    # Get stats
    stats = logger.get_stats()
    print(f"📊 Logger stats: {stats}")
    
    # Test a simple log
    class MockRequest:
        remote_addr = "192.168.1.100"
        headers = {'User-Agent': 'Test/1.0'}
    
    logger.log_session_start(MockRequest(), "test_session_001")
    print("✅ Test log sent")
    
    # Flush logs
    logger.flush()
    print("✅ Logs flushed to Google Sheets")
    
    print("\n🎉 SUCCESS! Check your Google Sheet for test data:")
    print("   https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Verify credentials.json is in config/ folder")
    print("2. Check Sheet ID in config file")
    print("3. Ensure sheet is shared with service account")
    print("4. Check service account has Editor permission")

print("\n" + "=" * 50)
