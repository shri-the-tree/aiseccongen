#!/usr/bin/env python3
"""
CLI runner for AI Security Blog Generator
Run directly without web interface
"""

from agents.crew_setup import AISecurityCrew
from config import CONTENT_CONFIG
import sys
import os


def main():
    print("🛡️ AI Security Blog Generator - CLI Mode")
    print("=" * 50)

    # Show available topics
    print("\nAvailable topics:")
    for i, topic in enumerate(CONTENT_CONFIG['topics'], 1):
        print(f"{i}. {topic}")

    # Get user input
    try:
        choice = input("\nSelect topic number or enter custom topic: ").strip()

        if choice.isdigit():
            topic_index = int(choice) - 1
            if 0 <= topic_index < len(CONTENT_CONFIG['topics']):
                topic = CONTENT_CONFIG['topics'][topic_index]
            else:
                print("Invalid topic number")
                return
        else:
            topic = choice

        if not topic:
            print("No topic provided")
            return

        word_count = input(f"Word count (default 1000): ").strip()
        word_count = int(word_count) if word_count.isdigit() else 1000

        print(f"\n🚀 Generating content for: {topic}")
        print(f"Target word count: {word_count}")
        print("\nThis may take 2-5 minutes...")

        # Generate content
        crew = AISecurityCrew()
        result = crew.generate_content(topic, word_count)

        print(f"\n✅ Generation complete!")
        print(f"📄 File saved: {result['filename']}")
        print(f"📊 Word count: {result['word_count']}")
        print(f"\nContent saved to: output/generated/{result['filename']}")

    except KeyboardInterrupt:
        print("\n\nGeneration cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()