from crewai_tools import tool
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
from datetime import datetime


@tool("web_search")
def web_search(query: str) -> str:
    """Search the web for current information on AI security topics."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        formatted_results = []
        for result in results:
            formatted_results.append(f"Title: {result['title']}\nURL: {result['href']}\nSnippet: {result['body']}\n")

        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool("fetch_url_content")
def fetch_url_content(url: str) -> str:
    """Fetch and extract text content from a URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text[:2000]  # Limit to 2000 chars
    except Exception as e:
        return f"Failed to fetch content: {str(e)}"


@tool("get_security_frameworks")
def get_security_frameworks(framework_name: str) -> str:
    """Get information about AI security frameworks."""
    frameworks = {
        "owasp": {
            "name": "OWASP Top 10 for LLM Applications",
            "version": "1.1",
            "key_points": [
                "LLM01: Prompt Injection",
                "LLM02: Insecure Output Handling",
                "LLM03: Training Data Poisoning",
                "LLM04: Model Denial of Service",
                "LLM05: Supply Chain Vulnerabilities",
                "LLM06: Sensitive Information Disclosure",
                "LLM07: Insecure Plugin Design",
                "LLM08: Excessive Agency",
                "LLM09: Overreliance",
                "LLM10: Model Theft"
            ],
            "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
        },
        "iso42001": {
            "name": "ISO/IEC 42001:2023",
            "version": "2023",
            "key_points": [
                "AI management system requirements",
                "Risk management for AI systems",
                "AI governance framework",
                "Performance evaluation metrics",
                "Continuous improvement processes"
            ],
            "url": "https://www.iso.org/standard/81230.html"
        },
        "nist": {
            "name": "NIST AI Risk Management Framework",
            "version": "1.0",
            "key_points": [
                "GOVERN: Governance and oversight",
                "MAP: Context and risks mapped",
                "MEASURE: Risks measured and assessed",
                "MANAGE: Risks managed and monitored"
            ],
            "url": "https://www.nist.gov/itl/ai-risk-management-framework"
        }
    }

    framework = frameworks.get(framework_name.lower(), {})
    if framework:
        return json.dumps(framework, indent=2)
    else:
        return f"Framework '{framework_name}' not found. Available: {list(frameworks.keys())}"


@tool("save_content")
def save_content(filename: str, content: str) -> str:
    """Save generated content to a file."""
    try:
        import os
        from config import OUTPUT_DIR

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.md")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return f"Content saved to {filepath}"
    except Exception as e:
        return f"Failed to save content: {str(e)}"