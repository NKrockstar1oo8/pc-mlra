#!/usr/bin/env python3
"""Test with correct OAuth scopes"""

import gspread
from google.oauth2.service_account import Credentials

creds_file = 'config/google_sheets_credentials.json'
sheet_id = '1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0'

print("🔧 Testing Google Sheets connection with scopes...")

try:
    # Define the correct scopes
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    print(f"✅ Using scopes: {SCOPES}")
    
    # Create credentials with scopes
    creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    
    print("✅ Credentials created")
    
    # Authorize client
    client = gspread.authorize(creds)
    print("✅ Client authorized")
    
    # Open spreadsheet
    sheet = client.open_by_key(sheet_id)
    print(f'✅ SUCCESS! Connected to: {sheet.title}')
    
    # Try to write something to the first sheet
    ws = sheet.sheet1
    ws.update('A1', 'PC-MLRA Test Connection - ' + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('✅ Successfully wrote to cell A1')
    
    # Read it back
    value = ws.acell('A1').value
    print(f'✅ Read back from A1: "{value}"')
    
    print(f"\n🎉 All tests passed!")
    print(f"📊 Spreadsheet: {sheet.title}")
    print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
    
except Exception as e:
    print(f'❌ ERROR: {type(e).__name__}: {e}')
    
    if hasattr(e, 'response'):
        import json
        print(f"Response: {json.dumps(e.response.json(), indent=2)}")
