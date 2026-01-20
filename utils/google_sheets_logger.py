#!/usr/bin/env python3
"""
Secure Google Sheets Logger for PC-MLRA - Uses environment variables
"""

import os
import json
import time
import threading
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class SecureSheetsLogger:
    """Secure logger that reads credentials from environment variable"""
    
    def __init__(self):
        self.connected = False
        self.client = None
        self.spreadsheet = None
        self.worksheets = {}
        
        print("🔧 Initializing Secure Google Sheets Logger...")
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets using environment variable"""
        try:
            # Get Sheet ID from config or environment
            sheet_id = self._get_sheet_id()
            if not sheet_id:
                print("❌ Sheet ID not found")
                return
            
            print(f"📋 Using Sheet ID: {sheet_id}")
            
            # Get credentials from environment variable (SECURE!)
            creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
            if not creds_json:
                print("❌ GOOGLE_CREDENTIALS_JSON environment variable not set")
                print("💡 On Render, add this environment variable with your service account JSON")
                return
            
            # Parse JSON from environment variable
            creds_dict = json.loads(creds_json)
            
            # Create credentials
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(sheet_id)
            print(f"✅ Connected to Google Sheets: '{self.spreadsheet.title}'")
            
            # Initialize worksheets
            self._init_worksheets()
            self.connected = True
            
        except Exception as e:
            print(f"❌ Failed to connect: {type(e).__name__}: {e}")
    
    def _get_sheet_id(self):
        """Get Sheet ID from config or environment"""
        # First try environment variable
        sheet_id = os.environ.get('GOOGLE_SHEETS_ID')
        if sheet_id:
            return sheet_id
        
        # Try config file (for local development)
        try:
            with open("config/google_sheets_config.py", "r") as f:
                content = f.read()
                import re
                match = re.search(r'"SHEET_ID"\s*:\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except:
            pass
        
        # Default (your Sheet ID)
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
                        headers = ["timestamp", "session_id", "query", "intent", "response_time", "user_agent"]
                    elif sheet_name == "user_sessions":
                        headers = ["session_id", "start_time", "end_time", "query_count", "user_agent"]
                    elif sheet_name == "error_logs":
                        headers = ["timestamp", "error_type", "message", "session_id", "query"]
                    
                    worksheet.append_row(headers)
                    self.worksheets[sheet_name] = worksheet
                    print(f"✓ Created: {sheet_name}")
                except Exception as e:
                    print(f"⚠️ Could not create {sheet_name}: {e}")
    
    def log_query(self, session_id, query, intent="", response_time=0, user_agent=""):
        """Log a query"""
        if not self.connected or "query_logs" not in self.worksheets:
            return
        
        try:
            row = [
                datetime.now().isoformat(),
                session_id,
                str(query)[:100],  # Truncate long queries
                intent,
                response_time,
                user_agent[:50] if user_agent else ""
            ]
            
            # Log in background thread
            threading.Thread(
                target=self.worksheets["query_logs"].append_row,
                args=(row,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log query: {e}")
    
    def log_session_start(self, session_id, user_agent=""):
        """Log session start"""
        if not self.connected or "user_sessions" not in self.worksheets:
            return
        
        try:
            row = [
                session_id,
                datetime.now().isoformat(),
                "",  # end_time (empty for now)
                0,   # query_count
                user_agent[:50] if user_agent else ""
            ]
            
            threading.Thread(
                target=self.worksheets["user_sessions"].append_row,
                args=(row,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log session start: {e}")
    
    def log_error(self, error_type, error_message, session_id="", query=""):
        """Log an error"""
        if not self.connected or "error_logs" not in self.worksheets:
            return
        
        try:
            row = [
                datetime.now().isoformat(),
                error_type,
                str(error_message)[:150],
                session_id,
                str(query)[:80] if query else ""
            ]
            
            threading.Thread(
                target=self.worksheets["error_logs"].append_row,
                args=(row,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log error: {e}")
    
    def is_connected(self):
        return self.connected

# Global instance
_secure_logger = None

def get_secure_logger():
    """Get secure logger instance"""
    global _secure_logger
    if _secure_logger is None:
        _secure_logger = SecureSheetsLogger()
    return _secure_logger

class DummyLogger:
    """Dummy logger when Google Sheets is not available"""
    def log_query(self, *args, **kwargs):
        pass
    
    def log_session_start(self, *args, **kwargs):
        pass
    
    def log_error(self, *args, **kwargs):
        pass
    
    def is_connected(self):
        return False
