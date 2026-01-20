#!/usr/bin/env python3
"""
Create Render environment variable from Google credentials
"""

import json
import os

def main():
    print("🚀 Creating Render Environment Variable")
    print("=" * 60)
    
    # Check file
    creds_file = "config/google_sheets_credentials.json"
    if not os.path.exists(creds_file):
        print(f"❌ File not found: {creds_file}")
        return
    
    # Load and convert
    with open(creds_file, 'r') as f:
        data = json.load(f)
    
    # Convert to single-line JSON
    # Use separators to ensure no extra whitespace
    single_line = json.dumps(data, separators=(',', ':'))
    
    print("✅ Successfully converted to single-line JSON")
    print()
    print("📋 FOR RENDER DASHBOARD:")
    print("=" * 40)
    print("Variable Key: GOOGLE_CREDENTIALS_JSON")
    print("Variable Value (copy EXACTLY):")
    print("-" * 40)
    print(single_line)
    print("-" * 40)
    print()
    print("📊 DETAILS:")
    print(f"• Service Account: {data.get('client_email')}")
    print(f"• Project ID: {data.get('project_id')}")
    print(f"• Character count: {len(single_line)}")
    print(f"• Has newlines: {'Yes' if '\\n' in single_line else 'No'}")
    print()
    print("🎯 ADDITIONAL VARIABLES NEEDED ON RENDER:")
    print("GOOGLE_SHEETS_ID=1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
    print("FLASK_ENV=production")
    print("FLASK_DEBUG=0")
    print("PORT=10000")

if __name__ == "__main__":
    main()
