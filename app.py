#!/usr/bin/env python3
"""
PC-MLRA Flask Web Application
Proof-Carrying Medical Legal Rights Advisor
"""

import os
import sys
import json
import uuid
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime

# Add current directory to path to import PC-MLRA modules
sys.path.insert(0, os.path.dirname(__file__))

print("🚀 Starting PC-MLRA Web Application...")
print("=" * 60)

# Import PC-MLRA components
try:
    from src.main import PCMLRAConsole
    print("✓ PC-MLRA Console imported successfully")
    
    # Initialize PC-MLRA system
    print("Initializing PC-MLRA system...")
    pc_mlra = PCMLRAConsole()
    
    # Quick test
    test_response = pc_mlra.process_query("Can I get my medical reports?")
    if test_response:
        print(f"✓ System test passed: Generated {len(test_response)} character response")
    else:
        print("✓ System initialized (command mode)")
        
    print("✓ PC-MLRA system ready!")
    
except Exception as e:
    print(f"✗ Error initializing PC-MLRA: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pc-mlra-secret-key-2024')
CORS(app)

# In-memory storage for chat history (for demo purposes)
# In production, use a database
chat_histories = {}

def format_response_for_html(response_text):
    """Format the response text for HTML display"""
    if not response_text:
        return ""
    
    # Convert markdown-style headers
    formatted = response_text
    formatted = formatted.replace('## ', '<h3>').replace('\n\n', '</h3>\n')
    
    # Convert bold text
    formatted = formatted.replace('**', '<strong>').replace('**', '</strong>')
    
    # Convert newlines to <br>
    formatted = formatted.replace('\n', '<br>')
    
    return formatted

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Chat interface"""
    # Generate a session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        chat_histories[session['session_id']] = []
    
    return render_template('chat.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PC-MLRA',
        'version': '1.0.0',
        'system': 'Proof-Carrying Medical Legal Rights Advisor',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/stats', methods=['GET'])
def get_system_stats():
    """Get system statistics"""
    try:
        # Get system metadata
        metadata = pc_mlra.kb.get_metadata()
        
        # Get all clauses
        clauses = pc_mlra.kb.get_all_clauses()
        
        # Count by category
        categories = {}
        for clause in clauses:
            category = clause.get("category", "uncategorized")
            categories[category] = categories.get(category, 0) + 1
        
        # Format categories for display
        formatted_categories = {}
        for cat, count in categories.items():
            readable_name = cat.replace('_', ' ').title()
            formatted_categories[readable_name] = count
        
        stats = {
            'system_name': metadata.get('system_name', 'PC-MLRA'),
            'version': metadata.get('version', '1.0.0'),
            'total_clauses': len(clauses),
            'documents': [
                'NHRC Patient Charter (2019)',
                'IMC Ethics Regulations (2002)'
            ],
            'categories': formatted_categories,
            'system_status': 'operational'
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process a user query"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'error': 'No query provided',
                'status': 'error'
            }), 400
        
        user_query = data['query'].strip()
        if not user_query:
            return jsonify({
                'error': 'Empty query',
                'status': 'error'
            }), 400
        
        # Get session ID
        session_id = session.get('session_id', 'default')
        if session_id not in chat_histories:
            chat_histories[session_id] = []
        
        # Add user message to history
        user_message = {
            'type': 'user',
            'content': user_query,
            'timestamp': datetime.now().isoformat()
        }
        chat_histories[session_id].append(user_message)
        
        # Process query using PC-MLRA
        show_proof = data.get('show_proof', False)
        response_text = pc_mlra.process_query(user_query)
        
        # Handle commands that return None (like 'stats', 'list rights')
        if response_text is None:
            # For commands, we need to capture their output
            # Since we can't easily capture console output, return a generic message
            response_text = "Command executed. For detailed output, please use the console version."
        
        # Get proof trace if available
        proof_trace = None
        if hasattr(pc_mlra.assembler, 'last_proof_trace'):
            proof = pc_mlra.assembler.last_proof_trace
            if hasattr(proof, 'to_dict'):
                proof_trace = proof.to_dict()
        
        # Format response for HTML
        formatted_response = format_response_for_html(response_text)
        
        # Add bot message to history
        bot_message = {
            'type': 'bot',
            'content': response_text,
            'formatted_content': formatted_response,
            'timestamp': datetime.now().isoformat(),
            'proof_trace': proof_trace
        }
        chat_histories[session_id].append(bot_message)
        
        # Keep only last 50 messages per session
        if len(chat_histories[session_id]) > 50:
            chat_histories[session_id] = chat_histories[session_id][-50:]
        
        return jsonify({
            'query': user_query,
            'response': response_text,
            'formatted_response': formatted_response,
            'proof_trace': proof_trace,
            'status': 'success',
            'session_id': session_id,
            'message_count': len(chat_histories[session_id])
        })
        
    except Exception as e:
        app.logger.error(f"Error processing query: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_chat_history():
    """Get chat history for current session"""
    session_id = session.get('session_id', 'default')
    history = chat_histories.get(session_id, [])
    
    return jsonify({
        'session_id': session_id,
        'history': history,
        'count': len(history)
    })

@app.route('/api/history/clear', methods=['POST'])
def clear_chat_history():
    """Clear chat history for current session"""
    session_id = session.get('session_id', 'default')
    if session_id in chat_histories:
        chat_histories[session_id] = []
    
    return jsonify({
        'status': 'success',
        'message': 'Chat history cleared',
        'session_id': session_id
    })

@app.route('/api/knowledge/search', methods=['GET'])
def search_knowledge():
    """Search the knowledge base"""
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'No search term provided'}), 400
    
    try:
        results = pc_mlra.kb.search_clauses_by_keyword(keyword)
        
        # Format results
        formatted_results = []
        for clause in results[:20]:  # Limit to 20 results
            formatted_results.append({
                'id': clause.get('id', ''),
                'title': clause.get('title', ''),
                'document': clause.get('document_abbr', ''),
                'section': clause.get('section', ''),
                'category': clause.get('category', '').replace('_', ' ').title(),
                'summary': clause.get('paraphrase', '')[:200] + '...' if clause.get('paraphrase') else ''
            })
        
        return jsonify({
            'query': keyword,
            'results': formatted_results,
            'total': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_example_queries():
    """Get example queries for users"""
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Production settings
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"\n📡 PC-MLRA Web Application")
    print("=" * 60)
    print(f"🌐 Server starting on port: {port}")
    print(f"🔧 Debug mode: {debug}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
