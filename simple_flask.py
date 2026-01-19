#!/usr/bin/env python3
"""
Simple Flask test for PC-MLRA
"""

from flask import Flask, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def home():
    return "PC-MLRA Flask Test - Server is running!"

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "PC-MLRA Flask server is running"})

if __name__ == '__main__':
    print("Starting simple Flask server...")
    print("Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
