#!/bin/bash
echo "🚀 Starting repository cleanup..."

# Backup important files just in case
echo "📦 Creating backup..."
mkdir -p /tmp/pc-mlra-backup
cp -r src data templates app.py requirements.txt README.md LICENSE .gitignore /tmp/pc-mlra-backup/

# Check what we're removing
echo "🗑️ Files to be removed:"
ls -d config docs tests 2>/dev/null || true
ls -1 *.py | grep -E "(apply_test_fixes|complete_fix|integrate_complete_imc|simple_flask|test_web)\.py" 2>/dev/null || true
ls -1 requirements_flask.txt start_pc_mlra.sh test_system.py 2>/dev/null || true

# Remove unnecessary directories
echo "Removing unnecessary directories..."
rm -rf config docs tests 2>/dev/null || true

# Remove unnecessary Python files
echo "Removing unnecessary Python files..."
rm -f apply_test_fixes.py complete_fix.py integrate_complete_imc.py simple_flask.py test_web.py 2>/dev/null || true

# Remove duplicate requirements file
echo "Removing duplicate requirements file..."
rm -f requirements_flask.txt 2>/dev/null || true

# Optional: Remove test files (keep test_console.py and test_system_complete.py)
echo "Cleaning test files..."
# Keep test_console.py and test_system_complete.py, remove others
rm -f test_system.py 2>/dev/null || true

# Clean up compiled files
echo "Cleaning compiled files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.log" -delete 2>/dev/null || true

# Update requirements.txt to include Flask
echo "Updating requirements.txt..."
cat > requirements.txt << 'REQEOF'
Flask==2.3.3
Flask-CORS==4.0.0
REQEOF

# Update .gitignore
echo "Updating .gitignore..."
cat > .gitignore << 'GITIGNORE
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Temporary files
temp/
tmp/

# Flask
instance/
.webassets-cache

# Jupyter Notebook
.ipynb_checkpoints
GITIGNORE

echo "✅ Cleanup complete!"
echo ""
echo "📁 Final structure:"
ls -la
echo ""
echo "📁 Subdirectories:"
ls -d */ 2>/dev/null || echo "No subdirectories"
