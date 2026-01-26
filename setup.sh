#!/bin/bash
echo "🚀 PC-MLRA Setup"
echo "================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python version: $(python3 --version)"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup environment
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your settings."
fi

# Check Google Sheets credentials
if [ ! -f "config/secrets/google_sheets_credentials.json" ]; then
    echo "⚠️ Google Sheets credentials not found."
    echo "Please copy your credentials to config/secrets/google_sheets_credentials.json"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  python run.py"
echo ""
echo "Test with:"
echo "  curl http://localhost:5000/api/health"
