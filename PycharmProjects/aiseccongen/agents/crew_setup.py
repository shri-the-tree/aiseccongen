from crewai import Agent, Task, Crew, Process
from agents.tools import web_search, get_security_frameworks, save_content
from config import GROQ_API_KEY, MODELS
import os
import time
import random


class AISecurityCrew:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found. Check your .env file.")

        os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    def create_single_agent(self):
        """Create a single comprehensive agent to avoid rate limits."""

        agent = Agent(
            role='AI Security Content Generator',
            goal='Research and write comprehensive AI security content',
            backstory="""You are an expert AI security consultant who can research, 
            analyze, and write authoritative content on AI security topics. You have 
            deep knowledge of OWASP, ISO 42001, NIST AI RMF, and current threats.""",
            tools=[web_search, get_security_frameworks],
            llm=f"groq/{MODELS['writer']}",  # Use writer model for better content generation
            verbose=True,
            max_iter=1,
            allow_delegation=False
        )

        return agent

    def create_single_task(self, topic: str, word_count: int = 1000):
        """Create a comprehensive task that combines research and writing."""

        task = Task(
            description=f"""
            Create a comprehensive {word_count}-word article on: "{topic}"

            Your process:
            1. First, research latest developments using web_search
            2. Get framework details using get_security_frameworks for OWASP, NIST, ISO
            3. Write a complete article covering:
               - Introduction and importance
               - Current landscape and latest developments  
               - Key security frameworks (OWASP LLM Top 10, ISO 42001, NIST AI RMF)
               - Common threats and vulnerabilities
               - Best practices and solutions
               - Implementation guidance with examples
               - Future considerations
               - Conclusion with key takeaways

            Requirements:
            - Include practical examples and code snippets
            - Cite authoritative sources from your research
            - Format in Markdown with proper headers
            - Maintain professional but accessible tone
            """,
            expected_output=f"A complete {word_count}-word article in Markdown format with research citations"
        )

        return task

    def generate_content(self, topic: str, word_count: int = 1000) -> dict:
        """Generate content with simplified single-agent approach."""

        max_retries = 2
        for attempt in range(max_retries):
            try:
                # Create single agent and task
                agent = self.create_single_agent()
                task = self.create_single_task(topic, word_count)
                task.agent = agent

                # Create minimal crew
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True
                )

                # Execute
                result = crew.kickoff()

                # Save content
                filename = topic.lower().replace(" ", "_").replace("/", "_")
                save_content._run(filename, str(result))

                return {
                    "topic": topic,
                    "content": str(result),
                    "word_count": len(str(result).split()),
                    "filename": f"{filename}.md",
                    "status": "completed"
                }

            except Exception as e:
                if ("rate_limit" in str(e).lower() or "no healthy upstream" in str(
                        e).lower()) and attempt < max_retries - 1:
                    wait_time = 60 + random.randint(0, 20)  # 1-1.3 minutes
                    print(f"Service issue. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)
                    continue
                else:
                    raise e
