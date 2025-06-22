import os
from dotenv import load_dotenv

load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_BASE = "https://api.groq.com/openai/v1"

# Model Configuration - Different models for different tasks
MODELS = {
    "researcher": "deepseek-r1-distill-llama-70b",    # Best for research and analysis
    "writer": "llama-3.3-70b-versatile",             # Good for creative writing
    "validator": "meta-llama/llama-4-scout-17b-16e-instruct",        # Fast for validation
    "editor": "qwen/qwen3-32b"                    # Good for editing/refinement
}

# Content Configuration
CONTENT_CONFIG = {
    "min_word_count": 800,
    "max_word_count": 1500,
    "required_citations": 3,
    "topics": [
        "LLM Security Fundamentals",
        "Prompt Injection Prevention",
        "AI Model Governance",
        "Zero Trust for AI Systems",
        "ISO 42001 Implementation",
        "OWASP LLM Top 10",
        "AI Bias Detection",
        "Secure AI Deployment"
    ]
}

# File Paths
OUTPUT_DIR = "output/generated"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"