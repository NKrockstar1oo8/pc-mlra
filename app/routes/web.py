"""
Web routes (HTML pages)
"""
from flask import Blueprint, render_template, session, jsonify
import uuid

web_bp = Blueprint('web', __name__)

# In-memory storage for chat history (in production, use database)
chat_histories = {}

@web_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@web_bp.route('/chat')
def chat():
    """Chat interface"""
    # Generate a session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        chat_histories[session['session_id']] = []
    
    return render_template('chat.html')

@web_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', 
                         system_name="PC-MLRA",
                         version="1.0.0",
                         description="Proof-Carrying Medical Legal Rights Advisor")

@web_bp.route('/documentation')
def documentation():
    """Documentation page"""
    return render_template('documentation.html')

@web_bp.route('/api-docs')
def api_docs():
    """API Documentation"""
    return render_template('api_docs.html')
