"""
Google Sheets Configuration Template for PC-MLRA
Copy this to google_sheets_config.py and fill in your details
"""

# Google Sheets Configuration
GOOGLE_SHEETS_CONFIG = {
    # Your Google Sheet ID
    "SHEET_ID": "YOUR_SHEET_ID_HERE",
    
    # Sheet names
    "SHEET_NAMES": {
        "sessions": "user_sessions",
        "queries": "query_logs", 
        "errors": "error_logs"
    },
    
    # For production, use environment variables:
    # GOOGLE_CREDENTIALS_JSON environment variable should contain service account JSON
    # GOOGLE_SHEETS_ID environment variable should contain your Sheet ID
}

# DO NOT COMMIT ACTUAL CREDENTIALS!
# On Render, set these environment variables:
# GOOGLE_CREDENTIALS_JSON = {"type": "service_account", ...}
# GOOGLE_SHEETS_ID = "your-sheet-id-here"
