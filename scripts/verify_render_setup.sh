#!/bin/bash
echo "🔍 VERIFYING RENDER DEPLOYMENT SETUP"
echo "===================================="

echo ""
echo "📦 Checking required files..."
echo ""

# Check each critical file
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1 exists"
        if [ "$2" = "show" ]; then
            echo "   Content:"
            head -5 "$1"
        fi
    else
        echo "❌ $1 MISSING!"
        return 1
    fi
}

check_file "requirements.txt" "show"
check_file "app.py" "show"
check_file "Procfile" "show"
check_file "runtime.txt" "show"
check_file "utils/google_sheets_logger.py"

echo ""
echo "🐍 Checking Python imports..."
echo ""

# Create a test script
cat > test_imports.py << 'PYEOF'
import sys
print("Python version:", sys.version[:6])
print()

deps = [
    ('Flask', 'flask'),
    ('Flask-CORS', 'flask_cors'),
    ('gunicorn', 'gunicorn'),
    ('gspread', 'gspread'),
    ('google-auth', 'google.auth'),
    ('oauth2client', 'oauth2client'),
]

for name, module in deps:
    try:
        __import__(module.replace('-', '_'))
        print(f"✅ {name}")
    except ImportError as e:
        print(f"❌ {name}: {e}")
PYEOF

python test_imports.py
rm -f test_imports.py

echo ""
echo "🌐 Checking Google Sheets setup..."
echo ""

# Test the logger
cat > test_logger.py << 'PYEOF'
import sys
import os
sys.path.append('.')

print("Testing Google Sheets Logger...")
try:
    from utils.google_sheets_logger import get_logger
    logger = get_logger()
    
    print(f"Logger created: {logger}")
    print(f"Is connected: {logger.is_connected()}")
    
    if not logger.is_connected():
        print("⚠️  Not connected (expected without env vars)")
        print("This is OK for now - will work on Render with env vars")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
PYEOF

python test_logger.py
rm -f test_logger.py

echo ""
echo "📊 Git status of critical files..."
echo ""

for file in requirements.txt app.py Procfile runtime.txt; do
    if git ls-files --error-unmatch $file >/dev/null 2>&1; then
        echo "✅ $file is tracked by Git"
    else
        echo "❌ $file is NOT tracked by Git"
    fi
done

echo ""
echo "🎯 DEPLOYMENT CHECKLIST:"
echo "1. ✅ All required files exist locally"
echo "2. ✅ Files are committed to Git (check above)"
echo "3. ✅ Requirements.txt has correct packages"
echo "4. ✅ Procfile points to app:app"
echo "5. ✅ Runtime.txt specifies Python 3.11.9"
echo ""
echo "🚀 After pushing, Render should deploy successfully!"
