from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

# Import your logger
from utils.google_sheets_logger import get_logger

app = Flask(__name__)
CORS(app)

# Initialize logger
logger = get_logger()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'PC-MLRA'
    })

@app.route('/api/logs/status', methods=['GET'])
def logs_status():
    """Check logging status"""
    try:
        connected = logger.is_connected()
        return jsonify({
            'connected': connected,
            'spreadsheet_id': os.environ.get('GOOGLE_SHEETS_ID'),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'connected': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Main query endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        
        # Start timer
        start_time = datetime.now()
        
        # Your ML logic here
        response = {
            'response': f"Processed query: {query}",
            'intent': 'medical_inquiry',
            'confidence': 0.95,
            'suggestions': ['medical_reports', 'appointment_scheduling']
        }
        
        # End timer
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000  # ms
        
        # Log the query
        logger.log_query(
            session_id=f"session_{datetime.now().timestamp()}",
            query=query,
            intent=response.get('intent', 'unknown'),
            response_time=response_time
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
