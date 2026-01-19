````md
# PC-MLRA  
## Proof-Carrying Medical Legal Rights Advisor

A **deterministic, zero-hallucination** system for **medical rights awareness**.  
Every response is **proof-carrying**, backed by **exact legal citations** from:

- **NHRC Patient Charter (2019)**
- **IMC Ethics Regulations (2002)**

This system is designed for **academic evaluation, demonstrations, and awareness**, not legal advice.

---

## 🎯 Key Features

- ✅ **Zero Hallucination**  
  Fully template-based responses. No generative AI content.

- ✅ **Proof-Carrying Responses**  
  Every answer includes exact legal clauses and citations.

- ✅ **Deterministic Behavior**  
  Same input → same output, every time.

- ✅ **Bidirectional Coverage**  
  Covers **patient rights** and **doctor obligations**.

- ✅ **Web Interface**  
  Flask-based web application with chat UI.

- ✅ **Console Application**  
  CLI interface for testing and debugging.

---

## 📊 System Statistics

- **Legal Clauses:** 77  
- **Rights & Obligations:** 46  
- **Response Templates:** 28  
- **Medical Rights Intents:** 20+  
- **Source Documents:**  
  - NHRC Patient Charter (2019)  
  - IMC Ethics Regulations (2002)

---

## 🚀 Quick Start

### 🔧 Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/pc-mlra.git
cd pc-mlra

# Install Flask dependencies
pip install -r requirements_flask.txt

# Run the web application
python run.py
````

Open your browser at:

```
http://localhost:5000
```

---

## 🖥️ Console Application

```bash
# Run the console interface
python src/main.py
```

### Example Commands

```text
> Can I get my medical reports?
> stats
> list rights
> search emergency
```

---

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │◄──►│  Flask Server   │◄──►│   PC-MLRA Core   │
│   (HTML / JS)   │    │   (REST API)    │    │   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## ⚙️ Core Components

1. **KnowledgeBase**
   Loads and queries structured legal clauses.

2. **IntentClassifier**
   Rule-based intent detection.

3. **TemplateEngine**
   Deterministic template-based response generation.

4. **ResponseAssembler**
   Generates proof-carrying answers.

5. **ProofTrace**
   Tracks and attaches legal citations to every response.

---

## 🌐 Web Interface

### Available Endpoints

```text
GET  /                     → Home page with system statistics
GET  /chat                 → Interactive chat interface
GET  /api/health            → Health check
GET  /api/system/stats      → System statistics
POST /api/query             → Process medical rights queries
GET  /api/examples          → Example questions
```

---

## ✨ Web Features

* ✅ Session-based chat history
* ✅ Toggleable legal proof display
* ✅ Example questions sidebar
* ✅ Real-time system statistics
* ✅ Responsive UI design

---

## 📁 Project Structure

```
pc-mlra/
├── src/                    # Core system components
├── data/                   # Knowledge base & templates
├── templates/              # HTML templates (Flask)
├── app.py                  # Flask application
├── run.py                  # Server runner
├── requirements.txt        # Core dependencies
├── requirements_flask.txt  # Flask dependencies
└── README.md
```

---

## 🧪 Testing

```bash
# Run complete system tests
python test_system_complete.py

# Test console application
python test_console.py

# Test web API endpoints
python test_endpoints.py
```

---

## 🔧 Deployment (Local)

```bash
# Method 1: Runner script
python run.py

# Method 2: Direct Flask execution
python app.py

# Method 3: Startup shell script
./start_pc_mlra.sh
```

---

## ☁️ Cloud Deployment Options

* Render.com (Free tier)
* Railway.app
* PythonAnywhere
* Heroku (with Procfile)
* AWS / GCP / Azure (Production)

---

## ⚖️ Legal Disclaimer

PC-MLRA provides **informational content only** based on:

* NHRC Patient Charter (2019)
* IMC Ethics Regulations (2002)

This system **does NOT provide legal advice**.
It is intended solely for **education and awareness**.
For legal matters, consult a **qualified legal professional**.

---

## 📝 License

MIT License
See the `LICENSE` file for details.

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests
5. Submit a pull request

---

## 📧 Support

For issues or questions, please open a **GitHub Issue**.

---

Built with ❤️ for **Medical Rights Awareness**
**Zero Hallucination. Fully Deterministic. Proof-Carrying by Design.**

```
