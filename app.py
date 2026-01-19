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

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Current directory: {current_dir}")

# Add src directory to Python path
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, current_dir)  # Add current directory first
sys.path.insert(0, src_dir)      # Then add src directory

print("🚀 Starting PC-MLRA Web Application...")
print("=" * 60)
print(f"Python path: {sys.path}")

# Import PC-MLRA components with robust error handling
pc_mlra = None

try:
    # Try direct import first
    print("Attempting to import PCMLRAConsole...")
    from src.main import PCMLRAConsole
    print("✓ Import successful: from src.main import PCMLRAConsole")
except ImportError as e1:
    print(f"First import attempt failed: {e1}")
    try:
        # Try alternative import path
        from main import PCMLRAConsole
        print("✓ Import successful: from main import PCMLRAConsole")
    except ImportError as e2:
        print(f"Second import attempt failed: {e2}")
        # List files to debug
        print("\n🔍 Checking directory structure:")
        print(f"Current dir contents: {os.listdir(current_dir)}")
        if os.path.exists(src_dir):
            print(f"src dir contents: {os.listdir(src_dir)}")
        
        # Try one more approach
        try:
            # Manually add the path
            import_path = os.path.join(current_dir, 'src', 'main.py')
            if os.path.exists(import_path):
                print(f"Found main.py at: {import_path}")
                # Use exec to import
                with open(import_path, 'r') as f:
                    code = f.read()
                exec_globals = {}
                exec(code, exec_globals)
                PCMLRAConsole = exec_globals.get('PCMLRAConsole')
                if PCMLRAConsole:
                    print("✓ Import successful via exec")
                else:
                    raise ImportError("PCMLRAConsole not found in main.py")
            else:
                raise ImportError(f"main.py not found at {import_path}")
        except Exception as e3:
            print(f"Final import attempt failed: {e3}")
            traceback.print_exc()
            sys.exit(1)

try:
    # Initialize PC-MLRA system
    print("\n🔧 Initializing PC-MLRA system...")
    pc_mlra = PCMLRAConsole()
    print("✓ PC-MLRA Console initialized")
    
    # Quick test
    test_response = pc_mlra.process_query("Can I get my medical reports?")
    if test_response:
        print(f"✓ System test passed: Generated response")
    else:
        print("✓ System initialized (command mode)")
        
    print("✅ PC-MLRA system ready!")
    
except Exception as e:
    print(f"❌ Error initializing PC-MLRA: {e}")
    traceback.print_exc()
    print("\n⚠️ Continuing without PC-MLRA core (demo mode)...")
    # We'll continue in demo mode instead of exiting

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

def demo_process_query(query):
    """Demo response if PC-MLRA is not available"""
    demo_responses = {
        "Can I get my medical reports?": "Yes, you have the right to access your medical records and reports. This is established in the NHRC Patient Charter 2019.",
        "Doctor was rude to me": "Doctors are expected to maintain professional conduct. The IMC Ethics Regulations 2002 outline obligations regarding respectful behavior.",
        "I need a second opinion": "You have the right to seek a second opinion from another healthcare provider.",
        "Hospital is charging too much": "Hospitals should provide transparent billing. Patients have rights regarding fair and itemized charges.",
        "Can I choose my own pharmacy?": "Yes, you generally have the right to choose your pharmacy or source for medications.",
        "hi": "Hello! I'm PC-MLRA, your Medical Legal Rights Advisor. How can I help you today?",
        "hello": "Hello! I'm PC-MLRA, your Medical Legal Rights Advisor. How can I help you today?",
        "help": "I can help you understand your medical rights and doctor obligations. Try asking about medical records, consent, billing, or doctor behavior.",
    }
    
    query_lower = query.lower()
    for key in demo_responses:
        if key.lower() in query_lower or query_lower in key.lower():
            return demo_responses[key]
    
    return f"I understand you're asking about '{query}'. In the full PC-MLRA system, I would provide specific legal references from the NHRC Patient Charter 2019 and IMC Ethics Regulations 2002."

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
        'pc_mlra_available': pc_mlra is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/system/stats', methods=['GET'])
def get_system_stats():
    """Get system statistics"""
    try:
        if pc_mlra is None:
            return jsonify({
                'system_name': 'PC-MLRA (Demo Mode)',
                'version': '1.0.0',
                'total_clauses': 77,
                'documents': [
                    'NHRC Patient Charter (2019)',
                    'IMC Ethics Regulations (2002)'
                ],
                'categories': {
                    'Access Information': 8,
                    'Consent Autonomy': 12,
                    'Privacy Confidentiality': 9,
                    'Quality Safety': 10,
                    'Redressal Complaint': 7,
                    'Professional Conduct': 8,
                    'Transparency Rates': 6,
                    'Continuity Care': 5,
                    'Emergency Care': 4,
                    'Research Education': 4,
                    'Non Discrimination': 4
                },
                'system_status': 'demo_mode'
            })
        
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
        
        # Process query using PC-MLRA or demo mode
        if pc_mlra is None:
            response_text = demo_process_query(user_query)
            proof_trace = None
        else:
            show_proof = data.get('show_proof', False)
            response_text = pc_mlra.process_query(user_query)
            
            # Handle commands that return None
            if response_text is None:
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
            'proof_trace': proof_trace,
            'mode': 'demo' if pc_mlra is None else 'full'
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
            'message_count': len(chat_histories[session_id]),
            'mode': 'demo' if pc_mlra is None else 'full'
        })
        
    except Exception as e:
        app.logger.error(f"Error processing query: {e}")
        traceback.print_exc()
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
        if pc_mlra is None:
            # Return demo search results
            return jsonify({
                'query': keyword,
                'results': [],
                'total': 0,
                'note': 'PC-MLRA core not loaded. Search unavailable in demo mode.'
            })
        
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
    print(f"🤖 PC-MLRA Core: {'✅ Available' if pc_mlra else '⚠️ Demo Mode'}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)