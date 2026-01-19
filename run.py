#!/usr/bin/env python3
"""
Run PC-MLRA Flask Application
"""

import os
import sys

# Install Flask if not already installed
try:
    import flask
except ImportError:
    print("Installing Flask...")
    os.system(f"{sys.executable} -m pip install -r requirements_flask.txt")

# Run the Flask app
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"""
╔═════════════════════════════════════════════════════════╗
║      PC-MLRA WEB APPLICATION v1.0.0                     ║
║                                                         ║
║  System Status: ✓ READY                                 ║
║  Web Interface: http://localhost:{port}                 ║
║  API Health:    http://localhost:{port}/api/health      ║
║  Chat Interface: http://localhost:{port}/chat           ║
║                                                         ║
║  Press Ctrl+C to stop the server                        ║
╚═════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
