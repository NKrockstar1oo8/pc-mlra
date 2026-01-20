#!/usr/bin/env python3
"""
Google Sheets Logger for PC-MLRA - WORKING VERSION
"""

import os
import json
import time
import threading
import uuid
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsLogger:
    """Logger for PC-MLRA"""
    
    def __init__(self, credentials_file: str = None, sheet_id: str = None):
        self.credentials_file = credentials_file or "config/google_sheets_credentials.json"
        self.sheet_id = sheet_id or "1qzzqiK1rrMqiUPX3JGSTSGFP3JKUCLDrp9i4XLAMPq0"
        
        print("🔧 Initializing Google Sheets Logger...")
        print(f"📋 Sheet ID: {self.sheet_id}")
        
        self.client = None
        self.spreadsheet = None
        self.worksheets = {}
        self.connected = False
        
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets"""
        try:
            # Check credentials file
            if not os.path.exists(self.credentials_file):
                print(f"❌ Credentials file not found: {self.credentials_file}")
                return
            
            # Create credentials
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=SCOPES)
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            print(f"✅ Connected to Google Sheets: '{self.spreadsheet.title}'")
            
            # Initialize worksheets
            self._init_worksheets()
            self.connected = True
            
        except Exception as e:
            print(f"❌ Failed to connect: {type(e).__name__}: {e}")
    
    def _init_worksheets(self):
        """Initialize or create worksheets"""
        required_sheets = {
            "query_logs": ["timestamp", "session_id", "query", "intent", "clauses", "response_time", "user_agent"],
            "user_sessions": ["session_id", "start_time", "end_time", "query_count", "user_agent", "ip_address"],
            "error_logs": ["timestamp", "error_type", "message", "session_id", "query_context"]
        }
        
        existing_sheets = {ws.title: ws for ws in self.spreadsheet.worksheets()}
        
        for sheet_name, headers in required_sheets.items():
            if sheet_name in existing_sheets:
                self.worksheets[sheet_name] = existing_sheets[sheet_name]
                print(f"✓ Loaded: {sheet_name}")
            else:
                try:
                    worksheet = self.spreadsheet.add_worksheet(
                        title=sheet_name, 
                        rows=1000, 
                        cols=len(headers)
                    )
                    worksheet.append_row(headers)
                    self.worksheets[sheet_name] = worksheet
                    print(f"✓ Created: {sheet_name}")
                except Exception as e:
                    print(f"⚠️ Could not create {sheet_name}: {e}")
    
    def log_query(self, session_id: str, query: str, intent: str = "", 
                  clauses: list = None, response_time: int = 0, 
                  user_agent: str = ""):
        """Log a user query"""
        if not self.connected or "query_logs" not in self.worksheets:
            return
        
        try:
            # Truncate long queries
            if len(query) > 200:
                query = query[:197] + "..."
            
            row = [
                datetime.now().isoformat(),
                session_id,
                query,
                intent,
                ",".join(clauses) if clauses else "",
                response_time,
                user_agent[:100] if user_agent else ""
            ]
            
            # Log in background thread
            threading.Thread(
                target=self._append_row,
                args=("query_logs", row),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log query: {e}")
    
    def log_session_start(self, session_id: str, user_agent: str = "", ip_address: str = ""):
        """Log session start"""
        if not self.connected or "user_sessions" not in self.worksheets:
            return
        
        try:
            row = [
                session_id,
                datetime.now().isoformat(),
                "",  # end_time (empty for now)
                0,   # query_count
                user_agent[:100] if user_agent else "",
                ip_address
            ]
            
            threading.Thread(
                target=self._append_row,
                args=("user_sessions", row),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log session start: {e}")
    
    def log_error(self, error_type: str, error_message: str, 
                  session_id: str = "", query: str = ""):
        """Log an error"""
        if not self.connected or "error_logs" not in self.worksheets:
            return
        
        try:
            row = [
                datetime.now().isoformat(),
                error_type,
                str(error_message)[:200],
                session_id,
                str(query)[:100] if query else ""
            ]
            
            threading.Thread(
                target=self._append_row,
                args=("error_logs", row),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"⚠️ Failed to log error: {e}")
    
    def _append_row(self, sheet_name: str, row: list):
        """Append a row to worksheet"""
        try:
            if sheet_name in self.worksheets:
                self.worksheets[sheet_name].append_row(row)
        except Exception as e:
            print(f"⚠️ Failed to append to {sheet_name}: {e}")
    
    def is_connected(self):
        return self.connected

# Global instance
_logger_instance = None

def get_logger():
    """Get logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = GoogleSheetsLogger()
        if not _logger_instance.is_connected():
            print("⚠️ Google Sheets logger not connected - using dummy logger")
            _logger_instance = DummyLogger()
    return _logger_instance

class DummyLogger:
    """Dummy logger for when Google Sheets is not available"""
    def log_query(self, *args, **kwargs):
        pass
    
    def log_session_start(self, *args, **kwargs):
        pass
    
    def log_error(self, *args, **kwargs):
        pass
    
    def is_connected(self):
        return False
