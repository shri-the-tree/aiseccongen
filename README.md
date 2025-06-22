# 🛡️ AI Security Blog Generator

**Multi-Agent Content Generation System for AI Security Topics**

Generate comprehensive, original AI security articles using CrewAI with specialized agents and multiple Groq models.

## 🚀 Features

- **Multi-Agent System**: Research, Writer, and Validator agents working together
- **Multiple Models**: Uses different Groq models optimized for each task
- **Web Search**: Real-time research with DuckDuckGo integration
- **Web Interface**: Flask-based UI for easy content generation
- **CLI Mode**: Command-line interface for batch processing
- **Security Focus**: Covers OWASP LLM Top 10, ISO 42001, NIST AI RMF, and more

## 📋 Prerequisites

- Python 3.9+
- Groq API key (free tier available)
- 2GB+ RAM recommended

## ⚡ Quick Setup

### 1. Clone/Download Project
```bash
git clone <your-repo> # or download files
cd ai_security_blog
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_BASE=https://api.groq.com/openai/v1
```

Get your free Groq API key: https://console.groq.com/

### 4. Test Setup
```bash
python test_setup.py
```

### 5. Run Generator
**Web Interface:**
```bash
python app.py
# Open http://localhost:5000
```

**CLI Mode:**
```bash
python main.py
```

## 🏗️ Project Structure

```
ai_security_blog/
├── .env                    # API keys
├── config.py              # Model & topic configuration
├── app.py                 # Flask web interface
├── main.py                # CLI runner
├── test_setup.py          # Setup verification
├── agents/
│   ├── crew_setup.py      # CrewAI agents
│   └── tools.py           # Web search & utilities
├── templates/             # HTML templates
├── static/               # CSS styling
└── output/generated/     # Generated articles
```

## 🤖 Agent System

| Agent | Model | Purpose |
|-------|-------|---------|
| **Researcher** | `llama-3.1-70b-versatile` | Web search & analysis |
| **Writer** | `mixtral-8x7b-32768` | Content creation |
| **Validator** | `llama-3.1-8b-instant` | Quality assurance |

## 📝 Available Topics

- LLM Security Fundamentals
- Prompt Injection Prevention
- AI Model Governance
- Zero Trust for AI Systems
- ISO 42001 Implementation
- OWASP LLM Top 10
- AI Bias Detection
- Secure AI Deployment

## 🔧 Configuration

**Models** (in `config.py`):
```python
MODELS = {
    "researcher": "llama-3.1-70b-versatile",
    "writer": "mixtral-8x7b-32768", 
    "validator": "llama-3.1-8b-instant"
}
```

**Content Settings**:
```python
CONTENT_CONFIG = {
    "min_word_count": 800,
    "max_word_count": 1500,
    "required_citations": 3
}
```

## 🌐 Web Interface Usage

1. **Select Topic**: Choose from predefined topics or enter custom
2. **Set Word Count**: 500-2000 words
3. **Generate**: AI agents collaborate to create content
4. **View Results**: Read, copy, or download generated articles

## 💻 CLI Usage

```bash
python main.py
# Follow prompts to select topic and word count
```

## 📊 Output

Generated articles include:
- Executive summary
- Technical analysis
- Best practices
- Implementation guidance
- Framework references (ISO 42001, NIST, OWASP)
- Authoritative citations

## 🔍 Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"API key not found":**
- Check `.env` file exists
- Verify GROQ_API_KEY is set correctly

**"Web search failed":**
- Check internet connection
- DuckDuckGo may be rate-limiting

**Generation takes too long:**
- Normal for first run (model loading)
- 2-5 minutes typical generation time

## 🛠️ Development

**Add New Topics:**
Edit `CONTENT_CONFIG['topics']` in `config.py`

**Change Models:**
Update `MODELS` dictionary in `config.py`

**Custom Tools:**
Add new functions to `agents/tools.py`

## 📄 License

Educational and research use. See LICENSE file for details.

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Test changes with `test_setup.py`
4. Submit pull request

## 🆘 Support

- Issues: Create GitHub issue
- Documentation: Check inline comments
- API Limits: Monitor Groq usage dashboard
