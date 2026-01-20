#!/usr/bin/env python3
"""Test the fixed Google Sheets logger"""

import sys
import os
sys.path.append('.')

print("🔧 Testing Fixed Google Sheets Logger")
print("=" * 50)

# Import the logger
from utils.google_sheets_logger import get_logger

# Get logger instance
logger = get_logger()

print(f"✅ Logger created")
print(f"📊 Connected: {logger.is_connected()}")

if logger.is_connected():
    print(f"📋 Spreadsheet: {logger.spreadsheet.title if logger.spreadsheet else 'Unknown'}")
    
    # Test logging
    print("\n📝 Testing log functions...")
    
    # Test session start
    logger.log_session_start(
        session_id="test_session_001",
        user_agent="Mozilla/5.0 Test",
        ip_address="192.168.1.100"
    )
    print("✅ Session start logged")
    
    # Test query log
    logger.log_query(
        session_id="test_session_001",
        query="Can I get my medical reports?",
        intent="access_medical_records",
        clauses=["NHRC-2", "IMC-1.3"],
        response_time=1250,
        user_agent="Mozilla/5.0 Test",
        ip_address="192.168.1.100"
    )
    print("✅ Query logged")
    
    # Test error log
    logger.log_error(
        error_type="TestError",
        error_message="This is a test error message",
        session_id="test_session_001",
        query="test query"
    )
    print("✅ Error logged")
    
    # Test session end
    logger.log_session_end("test_session_001", 5)
    print("✅ Session end logged")
    
    print("\n🎉 All tests completed!")
    print(f"📊 Check your Google Sheet for logs:")
    print(f"   https://docs.google.com/spreadsheets/d/1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
    
else:
    print("❌ Logger not connected to Google Sheets")
    print("\n🔧 Troubleshooting:")
    print("1. Check config/google_sheets_credentials.json exists")
    print("2. Verify Sheet ID in config/google_sheets_config.py")
    print("3. Ensure Google Sheet is shared with service account")
    print("4. Service account needs 'Editor' permission")

print("\n" + "=" * 50)
