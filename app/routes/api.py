"""
API Routes (REST endpoints)
"""
from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime
import uuid
import traceback

api_bp = Blueprint('api', __name__)

# Import services
from app.services.pc_mlra_service import PCMLRAService
from app.services.google_sheets_service import GoogleSheetsService
from app.services.demo_service import DemoService

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PC-MLRA',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'pc_mlra_available': current_app.pc_mlra_service is not None
    })

@api_bp.route('/system/stats', methods=['GET'])
def get_system_stats():
    """Get system statistics"""
    try:
        if current_app.pc_mlra_service is None:
            return DemoService.get_system_stats()
        
        stats = current_app.pc_mlra_service.get_system_stats()
        return jsonify(stats)
        
    except Exception as e:
        current_app.logger.error(f"Error getting system stats: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/query', methods=['POST'])
def process_query():
    """Process a user query"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'error': 'No query provided',
                'status': 'error'
            }), 400
        
        query_text = data['query'].strip()
        if not query_text:
            return jsonify({
                'error': 'Query cannot be empty',
                'status': 'error'
            }), 400
        
        # Generate or get session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Process the query
        if current_app.pc_mlra_service is None:
            # Use demo mode
            response_data = DemoService.process_query(query_text)
        else:
            # Use real PC-MLRA system
            response_data = current_app.pc_mlra_service.process_query(query_text)
        
        # Log to Google Sheets
        try:
            google_sheets = GoogleSheetsService(current_app)
            log_result = google_sheets.log_query(
                query=query_text,
                response=response_data.get('response', ''),
                intent=response_data.get('intent', 'unknown'),
                user_ip=request.remote_addr,
                session_id=session_id
            )
            
            if log_result['status'] == 'success':
                current_app.logger.info('✅ Query logged to Google Sheets')
            else:
                current_app.logger.warning(f'⚠️ Failed to log to Google Sheets: {log_result["message"]}')
                
        except Exception as e:
            current_app.logger.error(f'⚠️ Error in Google Sheets logging: {e}')
        
        # Return response
        return jsonify({
            'status': 'success',
            'query': query_text,
            'response': response_data.get('response', ''),
            'intent': response_data.get('intent', 'unknown'),
            'confidence': response_data.get('confidence', 0.0),
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in /api/query: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500

@api_bp.route('/examples', methods=['GET'])
def get_example_queries():
    """Get example queries"""
    examples = [
        "Can I get my medical reports?",
        "Doctor was rude to me",
        "I need a second opinion",
        "Hospital is charging too much",
        "Can I choose my own pharmacy?",
        "Doctor didn't take my consent",
        "My medical information was shared without permission",
        "What are my rights in emergency care?",
        "Can I get an itemized bill?",
        "What if I want to leave against medical advice?"
    ]
    
    return jsonify({
        'examples': examples,
        'count': len(examples)
    })

@api_bp.route('/knowledge/search', methods=['GET'])
def search_knowledge():
    """Search the knowledge base"""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'No search term provided'}), 400
    
    try:
        if current_app.pc_mlra_service is None:
            return DemoService.search_knowledge(keyword)
        
        results = current_app.pc_mlra_service.search_knowledge(keyword)
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error searching knowledge: {e}")
        return jsonify({'error': str(e)}), 500

# Debug endpoints
@api_bp.route('/debug/sheets-test', methods=['POST'])
def debug_sheets_test():
    """Test Google Sheets connection"""
    try:
        data = request.get_json() or {}
        google_sheets = GoogleSheetsService(current_app)
        
        result = google_sheets.test_connection(
            query=data.get('query', 'Test query'),
            response=data.get('response', 'Test response'),
            intent=data.get('intent', 'debug')
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/debug/sheets-status', methods=['GET'])
def debug_sheets_status():
    """Check Google Sheets status"""
    try:
        google_sheets = GoogleSheetsService(current_app)
        status = google_sheets.get_status()
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
