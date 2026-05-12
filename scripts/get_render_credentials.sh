#!/bin/bash
echo "🔧 Generating Render Environment Variable"
echo "========================================"

if [ ! -f "config/google_sheets_credentials.json" ]; then
    echo "❌ Credentials file not found!"
    exit 1
fi

# Method 1: Python (most reliable)
echo ""
echo "🎯 METHOD 1: Python (Recommended)"
echo "--------------------------------"
python3 -c "
import json
import sys

with open('config/google_sheets_credentials.json', 'r') as f:
    data = json.load(f)

# Convert to single line
single_line = json.dumps(data)

# Check if it's truly single line
if '\\n' in single_line:
    print('⚠️  Warning: Contains newlines!')
    single_line = single_line.replace('\\n', '\\\\n')

print('Copy this ENTIRE line for Render:')
print('=' * 60)
print(single_line)
print('=' * 60)
print(f'Length: {len(single_line)} characters')
"

# Method 2: Alternative format
echo ""
echo "📋 METHOD 2: Alternative Format"
echo "-----------------------------"
python3 -c "
import json

with open('config/google_sheets_credentials.json', 'r') as f:
    content = f.read().strip()

# Remove all whitespace (including newlines)
compact = ''.join(content.split())
print('Compact version:')
print('=' * 40)
print(compact[:100] + '...' + compact[-100:])
print('=' * 40)
print(f'Length: {len(compact)} characters')
"

echo ""
echo "🎯 HOW TO USE ON RENDER:"
echo "1. Go to: https://dashboard.render.com/"
echo "2. Select 'pc-mlra' service"
echo "3. Click 'Environment'"
echo "4. Add new variable:"
echo "   Key: GOOGLE_CREDENTIALS_JSON"
echo "   Value: [PASTE THE SINGLE LINE FROM ABOVE]"
echo "5. Also add:"
echo "   Key: GOOGLE_SHEETS_ID"
echo "   Value: 1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
echo "6. Save and redeploy"
