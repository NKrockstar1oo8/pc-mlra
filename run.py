#!/usr/bin/env python3
"""
PC-MLRA Runner Script
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"\n📡 PC-MLRA Web Application")
    print("=" * 60)
    print(f"🌐 Server starting on port: {port}")
    print(f"🔧 Debug mode: {debug}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
