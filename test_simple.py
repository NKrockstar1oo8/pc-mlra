#!/usr/bin/env python3
"""Simple Google Sheets Connection Test"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials

print("🔧 Testing Google Sheets Connection")
print("=" * 50)

# Check credentials file
creds_file = "config/google_sheets_credentials.json"
if not os.path.exists(creds_file):
    print(f"❌ Credentials file not found: {creds_file}")
    exit(1)

print(f"✅ Credentials file: {creds_file}")

# Load credentials
try:
    with open(creds_file, 'r') as f:
        creds_data = json.load(f)
    service_email = creds_data['client_email']
    print(f"✅ Service Account: {service_email}")
except Exception as e:
    print(f"❌ Error loading credentials: {e}")
    exit(1)

# Get Sheet ID from config
sheet_id = None
try:
    # Simple way to extract sheet ID
    with open("config/google_sheets_config.py", 'r') as f:
        for line in f:
            if '"SHEET_ID"' in line:
                # Extract the value between quotes
                start = line.find('"') + 1
                end = line.find('"', start)
                sheet_id = line[start:end]
                break
    
    if sheet_id:
        print(f"✅ Sheet ID found: {sheet_id}")
    else:
        print("❌ Could not find SHEET_ID in config")
        # Try to get it manually
        sheet_id = "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
        print(f"   Using provided Sheet ID: {sheet_id}")
except:
    # Use the sheet ID you provided
    sheet_id = "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
    print(f"⚠️  Using hardcoded Sheet ID: {sheet_id}")

print("\n📡 Connecting to Google Sheets...")
try:
    # Define scope
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    
    # Create credentials
    creds = Credentials.from_service_account_file(creds_file, scopes=scope)
    
    # Authorize client
    client = gspread.authorize(creds)
    print("✅ Client authorized")
    
    # Open spreadsheet
    spreadsheet = client.open_by_key(sheet_id)
    print(f"✅ Spreadsheet opened: '{spreadsheet.title}'")
    
    # List worksheets
    worksheets = spreadsheet.worksheets()
    print(f"✅ Worksheets found: {len(worksheets)}")
    
    for ws in worksheets:
        print(f"   - {ws.title}: {ws.row_count} rows x {ws.col_count} cols")
    
    print("\n🎉 SUCCESS! Google Sheets connection is working!")
    
    # Create test worksheets if they don't exist
    required_sheets = ["query_logs", "user_sessions", "error_logs"]
    existing_sheets = [ws.title for ws in worksheets]
    
    print("\n📝 Creating required worksheets if missing...")
    for sheet_name in required_sheets:
        if sheet_name not in existing_sheets:
            try:
                new_ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=15)
                print(f"✅ Created: {sheet_name}")
                
                # Add headers
                if sheet_name == "query_logs":
                    headers = ["timestamp", "session_id", "user_query", "intent", "clauses", "response_time"]
                elif sheet_name == "user_sessions":
                    headers = ["session_id", "start_time", "end_time", "query_count", "user_agent"]
                elif sheet_name == "error_logs":
                    headers = ["timestamp", "error_type", "error_message", "session_id", "query"]
                else:
                    headers = ["timestamp", "data"]
                
                new_ws.append_row(headers)
                print(f"✅ Added headers to: {sheet_name}")
                
            except Exception as e:
                print(f"⚠️  Could not create {sheet_name}: {e}")
        else:
            print(f"✓ Already exists: {sheet_name}")
    
    print("\n🔗 Your Google Sheet:")
    print(f"   https://docs.google.com/spreadsheets/d/{sheet_id}")
    
except Exception as e:
    print(f"❌ Connection error: {e}")
    
    print("\n🔧 TROUBLESHOOTING STEPS:")
    print("1. SHARE the Google Sheet with the service account email:")
    print(f"   {service_email}")
    print("2. Make sure sharing permission is 'Editor'")
    print("3. Check Sheet ID is correct")
    print("4. Verify service account is active in Google Cloud Console")
    
    print("\n📋 To share the sheet:")
    print(f"   a. Open: https://docs.google.com/spreadsheets/d/{sheet_id}")
    print(f"   b. Click SHARE button (top-right)")
    print(f"   c. Paste: {service_email}")
    print(f"   d. Set permission to 'Editor'")
    print(f"   e. Click SEND")

print("\n" + "=" * 50)
