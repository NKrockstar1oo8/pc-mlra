#!/usr/bin/env python3
"""Verify Google Sheet sharing status"""

import json

print("🔍 VERIFY GOOGLE SHEET SHARING STATUS")
print("=" * 60)

# Load service account email
with open('config/google_sheets_credentials.json', 'r') as f:
    data = json.load(f)

service_email = data['client_email']

print(f"📧 Your Service Account Email:")
print(f"   {service_email}")
print()

print("📋 STEP-BY-STEP VERIFICATION:")
print("1. ✅ Service Account created: pc-mlra-logs@pc-mlra-logs.iam.gserviceaccount.com")
print("2. ✅ Google Sheet created: PC-MLRA_Usage_Logs")
print("3. ✅ Sheet ID: 1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
print()
print("4. ❓ IS THE SHEET SHARED?")
print()
print("🔗 OPEN THIS LINK RIGHT NOW:")
print(f"   https://docs.google.com/spreadsheets/d/1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
print()
print("👀 WHAT TO DO:")
print("a. Open the link above")
print("b. Click the GREEN 'Share' button (top-right)")
print("c. Look for this email in the sharing list:")
print(f"   → {service_email}")
print("d. If NOT there, ADD IT:")
print("   1. Click 'Add people and groups'")
print(f"   2. Type: {service_email}")
print("   3. Click dropdown → Select 'Editor'")
print("   4. Click 'Send'")
print()
print("e. If it IS there, check permission:")
print("   1. Click the dropdown next to the email")
print("   2. Make sure it says 'Editor'")
print("   3. If it says 'Viewer', change to 'Editor'")
print()

print("📱 QUICK CHECK:")
print("Can YOU access this link?")
print("https://docs.google.com/spreadsheets/d/1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0")
print()
print("If YES → The sheet exists")
print("If NO → Sheet doesn't exist or you don't have access")
print()

print("🎯 FINAL TEST - RUN THIS AFTER SHARING:")
print("python direct_connection_test.py")
