# PC-MLRA: Proof-Carrying Medical Legal Rights Advisor

A deterministic, zero-hallucination system for medical rights awareness. Every response carries legal proof and exact citations from NHRC Patient Charter (2019) and IMC Ethics Regulations (2002).

## 🎯 Features

- **✅ Zero Hallucination:** Template-based system, no AI-generated content
- **✅ Proof-Carrying:** Every response includes exact legal citations
- **✅ Deterministic:** Same query → same response every time
- **✅ Bidirectional:** Covers both patient rights AND doctor obligations
- **✅ Web Interface:** Full Flask web application with chat interface
- **✅ Console App:** Command-line interface for testing

## 📊 System Statistics

- **Knowledge Base:** 77 legal clauses, 46 rights/obligations
- **Source Documents:** NHRC Patient Charter 2019 + IMC Ethics Regulations 2002
- **Response Templates:** 28 templates for different query types
- **Intent Classification:** 20+ medical rights intents

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/pc-mlra.git
cd pc-mlra

# Install dependencies
pip install -r requirements_flask.txt

# Run the web application
python run.py

# Open browser to: http://localhost:5000

===================================================================

--------------------
Console Application
--------------------
# Run the console interface
python src/main.py

# Try these commands:
# > Can I get my medical reports?
# > stats
# > list rights
# > search emergency

----------------
🏗️ Architecture
----------------
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│   Flask Server  │◄──►│   PC-MLRA Core  │
│   (HTML/JS)     │    │   (REST API)    │    │   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘

----------------
Core Components
----------------
1. KnowledgeBase - Loads and queries structured legal clauses

2. IntentClassifier - Rule-based intent classification

3. TemplateEngine - Template-based natural language generation

4. esponseAssembler - Generates proof-carrying responses

5. ProofTrace - Tracks legal citations for every response

-----------------
🌐 Web Interface
-----------------
Endpoints

GET / - Home page with system statistics

GET /chat - Interactive chat interface

GET /api/health - Health check

GET /api/system/stats - System statistics

POST /api/query - Process medical rights queries

GET /api/examples - Get example questions

---------
Features
---------
✅ Session-based chat history

✅ Legal proof display toggle

✅ Example questions sidebar

✅ Real-time statistics

✅ Responsive design

---------------------
📁 Project Structure
---------------------
pc-mlra/
├── src/                    # Core system components
├── data/                   # Knowledge base and templates
├── templates/              # HTML templates for web interface
├── app.py                  # Flask web application
├── run.py                  # Server runner
├── requirements.txt        # Core dependencies
└── requirements_flask.txt  # Flask dependencies

-----------
🧪 Testing
-----------
# Run comprehensive tests
python test_system_complete.py

# Test console application
python test_console.py

# Test web endpoints
python test_endpoints.py

---------------------------------
🔧 Deployment : Local Deployment
---------------------------------
# Method 1: Using runner script
python run.py

# Method 2: Direct Flask app
python app.py

# Method 3: Startup script
./start_pc_mlra.sh

-------------------------
Cloud Deployment Options
-------------------------
1. Render.com (Free tier available)

2. Railway.app (Easy deployment)

3. PythonAnywhere (Free Python hosting)

4. Heroku (With proper Procfile)

5. AWS/GCP/Azure (For production)

====================
📄 Legal Disclaimer
====================
PC-MLRA provides information about medical rights and obligations based on NHRC Patient Charter (2019) and IMC Ethics Regulations (2002). This system does not provide legal advice. The information provided is for educational and awareness purposes only. Always consult with qualified legal professionals for specific legal matters.

===========
📝 License
===========
MIT License - See LICENSE file for details.

----------------
👥 Contributing
----------------
1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Add tests

5. Submit a pull request

==========
📧 Contact
==========
For questions or support, please open an issue on GitHub.

Built with ❤️ for medical rights awareness | Zero Hallucination Guaranteed