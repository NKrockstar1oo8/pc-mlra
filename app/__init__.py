#!/usr/bin/env python3
"""
PC-MLRA Flask Web Application
Proof-Carrying Medical Legal Rights Advisor
"""

import os
import sys
import json
import uuid
import traceback
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime

# Google Sheets Integration
import gspread
from google.oauth2 import service_account

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'pc-mlra-secret-key-2026')
    CORS(app)
    
    # Get the absolute path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add src directory to Python path
    src_dir = os.path.join(current_dir, '..', 'src')
    sys.path.insert(0, os.path.join(current_dir, '..'))
    sys.path.insert(0, src_dir)
    
    # Initialize PC-MLRA system
    pc_mlra = None
    try:
        from src.main import PCMLRAConsole
        pc_mlra = PCMLRAConsole()
        app.logger.info('✅ PC-MLRA system initialized')
    except Exception as e:
        app.logger.warning(f'⚠️ PC-MLRA core not available: {e}')
        pc_mlra = None
    
    # Initialize Google Sheets
    google_sheets_initialized = False
    try:
        creds_path = os.environ.get('GOOGLE_CREDENTIALS_PATH', './config/secrets/google_sheets_credentials.json')
        sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        
        if sheet_id and os.path.exists(creds_path):
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
            gc = gspread.authorize(credentials)
            sheet = gc.open_by_key(sheet_id)
            worksheet = sheet.get_worksheet(0)
            
            # Add headers if empty
            if not worksheet.get_all_values():
                headers = ['Timestamp', 'Query', 'Response', 'Intent', 'User IP', 'Session ID']
                worksheet.append_row(headers)
            
            app.google_sheets = worksheet
            google_sheets_initialized = True
            app.logger.info(f'✅ Google Sheets connected: {sheet.title}')
        else:
            app.logger.warning('⚠️ Google Sheets not configured')
            app.google_sheets = None
    except Exception as e:
        app.logger.error(f'❌ Google Sheets initialization failed: {e}')
        app.google_sheets = None
    
    # In-memory chat storage
    chat_histories = {}
    
    # Helper functions
    def format_response_for_html(response_text):
        """Format response text for HTML display"""
        if not response_text:
            return ""
        formatted = response_text
        formatted = formatted.replace('## ', '<h3>').replace('\n\n', '</h3>\n')
        formatted = formatted.replace('**', '<strong>').replace('**', '</strong>')
        formatted = formatted.replace('\n', '<br>')
        return formatted
    
    def demo_process_query(query):
        """Demo response if PC-MLRA is not available"""
        demo_responses = {
            "Can I get my medical reports?": "Yes, you have the right to access your medical records and reports.",
            "Doctor was rude to me": "Doctors must maintain professional conduct per IMC Ethics Regulations.",
            "I need a second opinion": "You have the right to seek a second opinion.",
            "Hospital is charging too much": "Patients have rights regarding fair and transparent billing.",
        }
        query_lower = query.lower()
        for key in demo_responses:
            if key.lower() in query_lower or query_lower in key.lower():
                return demo_responses[key]
        return f"I understand you're asking about '{query}'."
    
    def log_to_google_sheets(app, query, response, intent, user_ip='', session_id=''):
        """Log query to Google Sheets"""
        if not hasattr(app, 'google_sheets') or not app.google_sheets:
            return {'status': 'error', 'message': 'Google Sheets not configured'}
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query_short = query[:200] + '...' if len(query) > 200 else query
            response_short = response[:200] + '...' if response and len(response) > 200 else (response or '')
            
            row_data = [timestamp, query_short, response_short, intent, user_ip, session_id]
            app.google_sheets.append_row(row_data)
            
            return {'status': 'success', 'message': 'Logged to Google Sheets'}
            
        except Exception as e:
            app.logger.error(f'⚠️ Failed to log to Google Sheets: {e}')
            return {'status': 'error', 'message': str(e)}
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/chat')
    def chat():
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            chat_histories[session['session_id']] = []
        return render_template('chat.html')
    
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'PC-MLRA',
            'pc_mlra_available': pc_mlra is not None,
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/system/stats')
    def get_system_stats():
        try:
            if pc_mlra is None:
                return jsonify({
                    'system_name': 'PC-MLRA (Demo Mode)',
                    'version': '1.0.0',
                    'total_clauses': 46,
                    'system_status': 'demo_mode'
                })
            
            metadata = pc_mlra.kb.get_metadata()
            clauses = pc_mlra.kb.get_all_clauses()
            
            return jsonify({
                'system_name': metadata.get('system_name', 'PC-MLRA'),
                'version': metadata.get('version', '1.0.0'),
                'total_clauses': len(clauses),
                'system_status': 'operational'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/query', methods=['POST'])
    def process_query():
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({'error': 'No query provided'}), 400
            
            query_text = data['query'].strip()
            if not query_text:
                return jsonify({'error': 'Query cannot be empty'}), 400
            
            # Get or create session
            if 'session_id' not in session:
                session['session_id'] = str(uuid.uuid4())
                chat_histories[session['session_id']] = []
            
            session_id = session['session_id']
            
            # Process query
            response_data = {}
            intent = "unknown"
            
            if pc_mlra is not None:
                try:
                    result = pc_mlra.process_query(query_text)
                    if result:
                        if isinstance(result, dict):
                            response_data = result
                        else:
                            response_data = {'response': str(result), 'intent': 'general_query'}
                        intent = response_data.get('intent', 'unknown')
                    else:
                        response_data = {'response': "I couldn't process your query. Please try rephrasing.", 'intent': 'unknown'}
                except Exception as e:
                    response_data = {'response': f'System error: {str(e)}', 'intent': 'error'}
            else:
                demo_response = demo_process_query(query_text)
                response_data = {'response': demo_response, 'intent': 'demo_mode'}
                intent = 'demo_mode'
            
            # Log to Google Sheets
            try:
                log_result = log_to_google_sheets(app, 
                    query=query_text,
                    response=response_data.get('response', ''),
                    intent=intent,
                    user_ip=request.remote_addr,
                    session_id=session_id
                )
                if log_result['status'] == 'success':
                    app.logger.info('✅ Query logged to Google Sheets')
            except Exception as e:
                app.logger.error(f'⚠️ Google Sheets logging error: {e}')
            
            # Store in chat history
            timestamp = datetime.now().isoformat()
            chat_entry = {
                'timestamp': timestamp,
                'query': query_text,
                'response': response_data.get('response', ''),
                'intent': intent
            }
            
            if session_id in chat_histories:
                chat_histories[session_id].append(chat_entry)
                if len(chat_histories[session_id]) > 50:
                    chat_histories[session_id] = chat_histories[session_id][-50:]
            
            # Return response
            return jsonify({
                'status': 'success',
                'query': query_text,
                'response': response_data.get('response', ''),
                'response_html': format_response_for_html(response_data.get('response', '')),
                'intent': intent,
                'timestamp': timestamp,
                'session_id': session_id
            })
            
        except Exception as e:
            app.logger.error(f'Error in /api/query: {e}')
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/examples')
    def get_example_queries():
        examples = [
            "Can I get my medical reports?",
            "Doctor was rude to me",
            "I need a second opinion",
            "Hospital is charging too much"
        ]
        return jsonify({'examples': examples})
    
    @app.route('/api/knowledge/search')
    def search_knowledge():
        keyword = request.args.get('q', '')
        if not keyword:
            return jsonify({'error': 'No search term'}), 400
        
        try:
            if pc_mlra is None:
                return jsonify({'query': keyword, 'results': [], 'note': 'Demo mode'})
            
            results = pc_mlra.kb.search_clauses_by_keyword(keyword)
            return jsonify({'query': keyword, 'results': results[:10], 'total': len(results)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Debug endpoints
    @app.route('/api/debug/sheets-status')
    def debug_sheets_status():
        if not app.google_sheets:
            return jsonify({'status': 'not_configured'})
        
        try:
            all_values = app.google_sheets.get_all_values()
            return jsonify({
                'status': 'connected',
                'total_rows': len(all_values),
                'recent': all_values[-3:] if len(all_values) > 3 else all_values
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    return app

# For direct execution
if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
