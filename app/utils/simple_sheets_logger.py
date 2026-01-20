#!/usr/bin/env python3
"""
Simple Google Sheets Logger for PC-MLRA
"""

import os
import json
import time
import threading
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class SimpleSheetsLogger:
    """Simple logger that connects to Google Sheets"""
    
    def __init__(self):
        self.connected = False
        self.client = None
        self.spreadsheet = None
        self.worksheets = {}
        
        print("🔧 Initializing Simple Google Sheets Logger...")
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets"""
        try:
            # Check for credentials file
            creds_file = "config/google_sheets_credentials.json"
            if not os.path.exists(creds_file):
                print(f"❌ Credentials file not found: {creds_file}")
                return
            
            # Get Sheet ID from config
            sheet_id = self._get_sheet_id()
            if not sheet_id:
                print("❌ Sheet ID not found in config")
                return
            
            print(f"📋 Using Sheet ID: {sheet_id}")
            
            # Create credentials with correct scope
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(sheet_id)
            print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            
            # Initialize worksheets
            self._init_worksheets()
            self.connected = True
            
        except Exception as e:
            print(f"❌ Failed to connect: {type(e).__name__}: {e}")
    
    def _get_sheet_id(self):
        """Extract Sheet ID from config file"""
        try:
            # Try to import config
            import sys
            sys.path.append('.')
            from config.google_sheets_config import GOOGLE_SHEETS_CONFIG
            return GOOGLE_SHEETS_CONFIG["SHEET_ID"]
        except:
            # Try to read config file directly
            try:
                with open("config/google_sheets_config.py", "r") as f:
                    content = f.read()
                    # Look for SHEET_ID
                    import re
                    match = re.search(r'"SHEET_ID"\s*:\s*"([^"]+)"', content)
                    if match:
                        return match.group(1)
            except:
                pass
            
            # Return hardcoded ID as last resort
            return "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
    
    def _init_worksheets(self):
        """Initialize worksheets"""
        sheet_names = ["query_logs", "user_sessions", "error_logs"]
        
        for sheet_name in sheet_names:
            try:
                # Try to get existing worksheet
                worksheet = self.spreadsheet.worksheet(sheet_name)
                self.worksheets[sheet_name] = worksheet
                print(f"✓ Loaded: {sheet_name}")
            except:
                try:
                    # Create new worksheet
                    worksheet = self.spreadsheet.add_worksheet(
                        title=sheet_name, 
                        rows=1000, 
                        cols=10
                    )
                    
                    # Add headers
                    if sheet_name == "query_logs":
                        headers = ["timestamp", "session_id", "query", "intent", "response_time"]
                    elif sheet_name == "user_sessions":
                        headers = ["session_id", "start_time", "query_count", "user_agent"]
                    elif sheet_name == "error_logs":
                        headers = ["timestamp", "error_type", "message", "session_id"]
                    
                    worksheet.append_row(headers)
                    self.worksheets[sheet_name] = worksheet
                    print(f"✓ Created: {sheet_name}")
                except Exception as e:
                    print(f"⚠️ Could not create {sheet_name}: {e}")
    
    def log_query(self, session_id, query, intent="", response_time=0):
        """Log a query"""
        if not self.connected or "query_logs" not in self.worksheets:
            return
        
        try:
            row = [
                datetime.now().isoformat(),
                session_id,
                str(query)[:100],  # Truncate long queries
                intent,
                response_time
            ]
            
            # Log in background thread
            threading.Thread(
                target=self.worksheets["query_logs"].append_row,
                args=(row,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log query: {e}")
    
    def is_connected(self):
        return self.connected

# Global instance
_simple_logger = None

def get_simple_logger():
    """Get simple logger instance"""
    global _simple_logger
    if _simple_logger is None:
        _simple_logger = SimpleSheetsLogger()
    return _simple_logger
