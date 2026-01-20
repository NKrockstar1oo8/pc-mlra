#!/usr/bin/env python3
"""Direct connection test - bypassing all logger code"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials

print("🔌 DIRECT Google Sheets Connection Test")
print("=" * 60)

# Your details
SHEET_ID = "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
CREDS_FILE = "config/google_sheets_credentials.json"

print(f"Sheet ID: {SHEET_ID}")
print(f"Creds file: {CREDS_FILE}")

# Step 1: Check if files exist
if not os.path.exists(CREDS_FILE):
    print(f"❌ ERROR: Credentials file not found: {CREDS_FILE}")
    exit(1)

print("✅ Step 1: Credentials file exists")

# Step 2: Load credentials
try:
    with open(CREDS_FILE, 'r') as f:
        creds_data = json.load(f)
    service_email = creds_data.get('client_email', 'Unknown')
    print(f"✅ Step 2: Loaded credentials")
    print(f"   Service Account: {service_email}")
except Exception as e:
    print(f"❌ Step 2: Failed to load credentials: {e}")
    exit(1)

# Step 3: Try to connect
try:
    print("\n🔄 Attempting to connect to Google Sheets...")
    
    # Create credentials
    creds = Credentials.from_service_account_file(
        CREDS_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    print("✅ Step 3a: Credentials created")
    
    # Authorize
    gc = gspread.authorize(creds)
    print("✅ Step 3b: Client authorized")
    
    # Open spreadsheet
    sh = gc.open_by_key(SHEET_ID)
    print(f"✅ Step 3c: Spreadsheet opened: '{sh.title}'")
    
    print("\n🎉 SUCCESS! Direct connection works!")
    print(f"📊 View sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    
    # List worksheets
    print(f"\n📋 Worksheets in '{sh.title}':")
    for i, ws in enumerate(sh.worksheets()):
        print(f"   {i+1}. {ws.title} ({ws.row_count} rows × {ws.col_count} cols)")
    
    # Try to write something
    print("\n📝 Testing write operation...")
    ws = sh.sheet1
    test_text = f"PC-MLRA Direct Test at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}"
    ws.update('A1', [[test_text]])
    print(f"✅ Wrote to A1: '{test_text}'")
    
    # Read it back
    value = ws.acell('A1').value
    print(f"✅ Read from A1: '{value}'")
    
    print("\n✅ ALL TESTS PASSED! Your setup is correct.")
    
except gspread.exceptions.SpreadsheetNotFound:
    print("\n❌ ERROR: Spreadsheet not found!")
    print("\n🔧 This means:")
    print("   1. Wrong Sheet ID, OR")
    print("   2. Sheet not shared with service account")
    print(f"\n📋 Service account email: {service_email}")
    print(f"📋 Expected Sheet ID: {SHEET_ID}")
    print(f"\n🔗 Please share this sheet with the service account:")
    print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    
except gspread.exceptions.APIError as e:
    print(f"\n❌ API ERROR: {e}")
    print("\n🔧 This usually means permission issues")
    print(f"📋 Service account: {service_email}")
    print(f"\n✅ Please verify:")
    print("   1. Sheet is shared with service account")
    print("   2. Permission is 'Editor' (not 'Viewer')")
    print("   3. No typo in the email address")
    
except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
