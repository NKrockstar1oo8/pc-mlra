#!/bin/bash
# Start PC-MLRA Server

echo "Starting PC-MLRA Web Application..."
echo "=========================================="

# Check if port 5000 is already in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 5000 is already in use. Trying to stop existing process..."
    fuser -k 5000/tcp 2>/dev/null
    sleep 2
fi

# Kill any existing Python Flask processes
pkill -f "python.*run" 2>/dev/null || true
pkill -f "python.*app" 2>/dev/null || true
sleep 2

# Run the server in the background
echo "Starting server on port 5000..."
python run.py > pc-mlra.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Check if server started successfully
if curl -s http://localhost:5000/api/health >/dev/null; then
    echo ""
    echo "✅ Server started successfully!"
    echo "🌐 Web Interface: http://localhost:5000"
    echo "💬 Chat: http://localhost:5000/chat"
    echo "📊 API Health: http://localhost:5000/api/health"
    echo ""
    echo "Server logs are being written to: pc-mlra.log"
    echo "Press Ctrl+C to stop viewing logs (server will continue running)"
    echo ""
    echo "To stop the server later, run: pkill -f 'python.*run'"
    echo "=========================================="
    
    # Show logs in real-time
    tail -f pc-mlra.log
else
    echo "❌ Server failed to start. Check pc-mlra.log for details."
    kill $SERVER_PID 2>/dev/null
    exit 1
fi
