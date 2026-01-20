"""
Google Sheets Service for logging
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
import traceback

class GoogleSheetsService:
    """Service for Google Sheets integration"""
    
    def __init__(self, app):
        self.app = app
        self.worksheet = None
        self.initialized = False
        self._initialize()
    
    def _initialize(self) -> bool:
        """Initialize Google Sheets connection"""
        try:
            # Get configuration
            sheet_id = self.app.config.get('GOOGLE_SHEET_ID')
            creds_path = self.app.config.get('GOOGLE_CREDENTIALS_PATH')
            
            if not sheet_id or not creds_path:
                self.app.logger.warning('Google Sheets not configured')
                return False
            
            if not os.path.exists(creds_path):
                self.app.logger.warning(f'Credentials file not found: {creds_path}')
                return False
            
            # Import here to avoid dependency issues
            import gspread
            from google.oauth2 import service_account
            
            # Authenticate
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=scopes
            )
            
            gc = gspread.authorize(credentials)
            sheet = gc.open_by_key(sheet_id)
            
            # Use first worksheet
            self.worksheet = sheet.get_worksheet(0)
            
            # Add headers if sheet is empty
            if not self.worksheet.get_all_values():
                headers = ['Timestamp', 'Query', 'Response', 'Intent', 'User IP', 'Session ID']
                self.worksheet.append_row(headers)
            
            self.initialized = True
            self.app.logger.info(f'✅ Google Sheets connected: {sheet.title}')
            return True
            
        except Exception as e:
            self.app.logger.error(f'❌ Google Sheets initialization failed: {e}')
            return False
    
    def log_query(self, query: str, response: str, intent: str, 
                  user_ip: str = '', session_id: str = '') -> Dict[str, Any]:
        """Log a query-response pair to Google Sheets"""
        if not self.initialized or not self.worksheet:
            return {
                'status': 'error',
                'message': 'Google Sheets not configured or initialized'
            }
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Truncate long strings
            query_short = query[:200] + '...' if len(query) > 200 else query
            response_short = response[:200] + '...' if response and len(response) > 200 else (response or '')
            
            row_data = [timestamp, query_short, response_short, intent, user_ip, session_id]
            self.worksheet.append_row(row_data)
            
            return {
                'status': 'success',
                'message': 'Logged to Google Sheets',
                'timestamp': timestamp
            }
            
        except Exception as e:
            self.app.logger.error(f'⚠️ Failed to log to Google Sheets: {e}')
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_connection(self, query: str = 'Test query', 
                       response: str = 'Test response', 
                       intent: str = 'test') -> Dict[str, Any]:
        """Test Google Sheets connection by logging a test entry"""
        result = self.log_query(query, response, intent, '127.0.0.1', 'test_session')
        
        if result['status'] == 'success':
            return {
                'status': 'connected',
                'message': 'Google Sheets is working',
                'test_result': result
            }
        else:
            return {
                'status': 'error',
                'message': 'Google Sheets test failed',
                'test_result': result
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get Google Sheets connection status"""
        if not self.initialized:
            return {
                'status': 'not_initialized',
                'message': 'Google Sheets not initialized'
            }
        
        try:
            # Try to get some data to verify connection
            all_values = self.worksheet.get_all_values()
            
            return {
                'status': 'connected',
                'total_rows': len(all_values),
                'headers': all_values[0] if all_values else [],
                'recent_entries': all_values[-3:] if len(all_values) > 3 else all_values
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
