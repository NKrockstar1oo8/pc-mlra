"""
Google Sheets utility functions
"""
import os
from flask import current_app

def init_google_sheets():
    """Initialize Google Sheets connection for the app"""
    # This is a simplified version - the real implementation is in GoogleSheetsService
    # We return a placeholder for app context
    return {'status': 'initialized_in_service_layer'}

def log_to_sheets(app, query, response, intent, user_ip='', session_id=''):
    """Utility function to log to Google Sheets (legacy support)"""
    try:
        from app.services.google_sheets_service import GoogleSheetsService
        service = GoogleSheetsService(app)
        return service.log_query(query, response, intent, user_ip, session_id)
    except Exception as e:
        app.logger.error(f"Error in legacy sheets logging: {e}")
        return {'status': 'error', 'message': str(e)}
