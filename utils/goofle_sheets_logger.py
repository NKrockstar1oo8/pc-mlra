# Create the logger file
cat > utils/google_sheets_logger.py << 'EOF'
#!/usr/bin/env python3
"""
Google Sheets Logger for PC-MLRA
Simplified version for initial testing
"""

import os
import json
import time
import uuid
import re
import threading
from datetime import datetime
from typing import Dict, Any
import gspread
from google.oauth2.service_account import Credentials

class GoogleSheetsLogger:
    """Simplified logger for PC-MLRA"""
    
    def __init__(self, credentials_file: str = None, sheet_id: str = None):
        self.credentials_file = credentials_file or "config/google_sheets_credentials.json"
        self.sheet_id = sheet_id
        
        # Default config
        self.config = {
            "SHEET_NAMES": {
                "queries": "query_logs",
                "sessions": "user_sessions",
                "errors": "error_logs"
            },
            "async_logging": True
        }
        
        self.client = None
        self.spreadsheet = None
        self.worksheets = {}
        
        # Try to initialize
        self._try_initialize()
    
    def _try_initialize(self):
        """Try to initialize Google Sheets connection"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"⚠️ Credentials file not found: {self.credentials_file}")
                return False
            
            if not self.sheet_id:
                print("⚠️ Sheet ID not provided")
                return False
            
            # Load credentials
            scope = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scope
            )
            
            # Create client
            self.client = gspread.authorize(creds)
            
            # Open spreadsheet
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            
            # Initialize worksheets
            self._initialize_worksheets()
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize Google Sheets: {e}")
            return False
    
    def _initialize_worksheets(self):
        """Initialize worksheets"""
        for key, sheet_name in self.config["SHEET_NAMES"].items():
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
                self.worksheets[key] = worksheet
                print(f"✓ Loaded worksheet: {sheet_name}")
            except Exception:
                try:
                    # Try to create worksheet
                    worksheet = self.spreadsheet.add_worksheet(
                        title=sheet_name, 
                        rows=1000, 
                        cols=15
                    )
                    
                    # Add headers based on sheet type
                    if sheet_name == "query_logs":
                        headers = [
                            "timestamp", "session_id", "user_query", 
                            "detected_intent", "matched_clauses", "response_time_ms"
                        ]
                    elif sheet_name == "user_sessions":
                        headers = [
                            "session_id", "start_time", "end_time", 
                            "total_queries", "user_agent"
                        ]
                    elif sheet_name == "error_logs":
                        headers = [
                            "timestamp", "error_type", "error_message", 
                            "session_id", "query_context"
                        ]
                    else:
                        headers = ["timestamp", "data"]
                    
                    worksheet.append_row(headers)
                    self.worksheets[key] = worksheet
                    print(f"✓ Created worksheet: {sheet_name}")
                except Exception as e:
                    print(f"⚠️ Could not create worksheet {sheet_name}: {e}")
    
    def _anonymize_query(self, query: str) -> str:
        """Simple anonymization"""
        if not query:
            return ""
        
        # Remove phone numbers
        query = re.sub(r'\b\d{10}\b', '[PHONE]', query)
        
        # Truncate if too long
        if len(query) > 200:
            query = query[:197] + "..."
        
        return query
    
    def log_query(self, session_id: str, query: str, intent: str, 
                  clauses: list, response_time: int):
        """Log a user query"""
        if not self.worksheets.get("queries"):
            return
        
        log_entry = [
            datetime.now().isoformat(),
            session_id,
            self._anonymize_query(query),
            intent,
            ",".join(clauses) if clauses else "",
            response_time
        ]
        
        # Log asynchronously if enabled
        if self.config.get("async_logging", True):
            threading.Thread(
                target=self._append_row,
                args=("queries", log_entry)
            ).start()
        else:
            self._append_row("queries", log_entry)
    
    def log_session_start(self, session_id: str, user_agent: str = ""):
        """Log session start"""
        if not self.worksheets.get("sessions"):
            return
        
        log_entry = [
            session_id,
            datetime.now().isoformat(),
            "",  # end_time (empty for now)
            0,   # total_queries
            user_agent[:100] if user_agent else ""
        ]
        
        self._append_row("sessions", log_entry)
    
    def log_error(self, error_type: str, error_message: str, 
                  session_id: str = "", query: str = ""):
        """Log an error"""
        if not self.worksheets.get("errors"):
            return
        
        log_entry = [
            datetime.now().isoformat(),
            error_type,
            str(error_message)[:200],
            session_id,
            self._anonymize_query(query)[:100]
        ]
        
        self._append_row("errors", log_entry)
    
    def _append_row(self, sheet_key: str, row_data: list):
        """Append a row to worksheet"""
        try:
            worksheet = self.worksheets.get(sheet_key)
            if worksheet:
                worksheet.append_row(row_data)
        except Exception as e:
            print(f"⚠️ Failed to log to {sheet_key}: {e}")
    
    def is_connected(self):
        """Check if connected to Google Sheets"""
        return self.client is not None and self.spreadsheet is not None

# Global logger instance
_logger_instance = None

def get_logger(credentials_file: str = None, sheet_id: str = None):
    """Get or create logger instance"""
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = GoogleSheetsLogger(credentials_file, sheet_id)
    
    return _logger_instance

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
EOF