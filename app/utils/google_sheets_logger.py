"""
Google Sheets Logger Utility
"""
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

class GoogleSheetsLogger:
    def __init__(self):
        self.spreadsheet = None
        self.worksheet = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets using credentials from environment variable"""
        try:
            # Get credentials from environment variable
            creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
            
            if not creds_json:
                print("⚠️  GOOGLE_CREDENTIALS_JSON not found in environment")
                return
            
            # Parse the JSON string
            credentials_dict = json.loads(creds_json)
            
            # Authenticate
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=scopes
            )
            
            # Connect to Google Sheets
            client = gspread.authorize(credentials)
            
            # Open spreadsheet
            spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
            if not spreadsheet_id:
                print("⚠️  GOOGLE_SHEETS_ID not found in environment")
                return
            
            self.spreadsheet = client.open_by_key(spreadsheet_id)
            
            # Try to get existing worksheet or create new
            try:
                self.worksheet = self.spreadsheet.worksheet('Query Logs')
            except gspread.exceptions.WorksheetNotFound:
                self.worksheet = self.spreadsheet.add_worksheet(
                    title='Query Logs', 
                    rows=1000, 
                    cols=10
                )
                # Add headers
                headers = [
                    'Timestamp', 'Session ID', 'Query', 
                    'Intent', 'Response Time (ms)', 'Status'
                ]
                self.worksheet.append_row(headers)
            
            print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {type(e).__name__}: {e}")
            self.spreadsheet = None
            self.worksheet = None
    
    def is_connected(self):
        """Check if connected to Google Sheets"""
        return self.worksheet is not None
    
    def log_query(self, session_id, query, intent, response_time, status='success'):
        """Log a query to Google Sheets"""
        if not self.is_connected():
            print("⚠️  Not connected to Google Sheets, skipping log")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Prepare row data
            row = [
                timestamp,
                session_id,
                query,
                intent,
                response_time,
                status
            ]
            
            # Append to worksheet
            self.worksheet.append_row(row)
            print(f"✅ Logged query: {query[:50]}...")
            
        except Exception as e:
            print(f"❌ Error logging to Google Sheets: {type(e).__name__}: {e}")

# Singleton instance
_logger_instance = None

def get_logger():
    """Get or create logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = GoogleSheetsLogger()
    return _logger_instance

if __name__ == '__main__':
    # Test the logger
    logger = get_logger()
    if logger.is_connected():
        print("✅ Logger working!")
        logger.log_query(
            session_id="test_001",
            query="Test query from utility",
            intent="test",
            response_time=100
        )
