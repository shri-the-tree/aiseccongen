#!/usr/bin/env python3
"""
Test setup for AI Security Blog Generator
Verifies all dependencies and configuration
"""

import os
import sys
from dotenv import load_dotenv


def test_environment():
    """Test Python environment and dependencies"""
    print("🔧 Testing Python Environment...")

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Test imports
    try:
        import crewai
        print("✅ CrewAI imported")
    except ImportError:
        print("❌ CrewAI not installed")
        return False

    try:
        import flask
        print("✅ Flask imported")
    except ImportError:
        print("❌ Flask not installed")
        return False

    try:
        from duckduckgo_search import DDGS
        print("✅ DuckDuckGo Search imported")
    except ImportError:
        print("❌ DuckDuckGo Search not installed")
        return False

    return True


def test_configuration():
    """Test configuration and API keys"""
    print("\n🔑 Testing Configuration...")

    load_dotenv()

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return False

    if len(groq_key) < 20:
        print("❌ GROQ_API_KEY appears invalid (too short)")
        return False

    print("✅ GROQ_API_KEY found")
    return True


def test_directories():
    """Test directory structure"""
    print("\n📁 Testing Directory Structure...")

    required_dirs = [
        "agents",
        "static",
        "templates",
        "output",
        "output/generated"
    ]

    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ missing")
            return False

    required_files = [
        "config.py",
        "app.py",
        "main.py",
        "agents/tools.py",
        "agents/crew_setup.py",
        "templates/index.html",
        "static/style.css"
    ]

    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} missing")
            return False

    return True


def test_web_search():
    """Test web search functionality"""
    print("\n🔍 Testing Web Search...")

    try:
        from agents.tools import web_search
        result = web_search("AI security test")
        if "Title:" in result:
            print("✅ Web search working")
            return True
        else:
            print("❌ Web search returned unexpected format")
            return False
    except Exception as e:
        print(f"❌ Web search failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🛡️ AI Security Blog Generator - Setup Test")
    print("=" * 50)

    tests = [
        test_environment,
        test_configuration,
        test_directories,
        test_web_search
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Ready to generate content.")
        print("\nTo start:")
        print("1. Web interface: python app.py")
        print("2. CLI mode: python main.py")
    else:
        print("❌ Some tests failed. Check errors above.")

    return all_passed


if __name__ == "__main__":
    main()