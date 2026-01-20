#!/usr/bin/env python3
"""Test Google Sheets Connection"""

import os
import json
import sys
sys.path.append('.')

print("🔧 Testing Google Sheets Connection")
print("=" * 60)

# Check files
creds_file = "config/google_sheets_credentials.json"
config_file = "config/google_sheets_config.py"

print("1. Checking files...")
if os.path.exists(creds_file):
    print(f"   ✅ Credentials file: {creds_file}")
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
        print(f"   ✅ Valid JSON, Service Account: {creds_data['client_email']}")
    except Exception as e:
        print(f"   ❌ Invalid JSON: {e}")
else:
    print(f"   ❌ Missing: {creds_file}")

if os.path.exists(config_file):
    print(f"   ✅ Config file: {config_file}")
else:
    print(f"   ❌ Missing: {config_file}")

print("\n2. Testing Google Sheets API...")
try:
    import gspread
    from google.oauth2.service_account import Credentials
    print("   ✅ gspread imported successfully")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    print("   Run: pip install gspread==5.11.2 google-auth==2.23.3")

print("\n3. Connecting to Google Sheets...")
try:
    # Read config to get sheet ID
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_file)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    
    sheet_id = config_module.GOOGLE_SHEETS_CONFIG["SHEET_ID"]
    print(f"   📋 Sheet ID: {sheet_id}")
    
    # Connect
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(creds_file, scopes=scope)
    client = gspread.authorize(creds)
    
    # Open sheet
    sheet = client.open_by_key(sheet_id)
    print(f"   ✅ Connected! Sheet title: '{sheet.title}'")
    
    # List worksheets
    print(f"   📊 Worksheets: {[ws.title for ws in sheet.worksheets()]}")
    
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    print("\n🔧 Common solutions:")
    print("   A. Share Google Sheet with service account email")
    print("   B. Check Sheet ID is correct")
    print("   C. Ensure service account has Editor permission")

print("\n" + "=" * 60)
