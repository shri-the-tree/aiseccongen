from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from agents.tools import web_search, fetch_url_content, get_security_frameworks, save_content
from config import GROQ_API_KEY, OPENAI_API_BASE, MODELS
import os


# Configure Groq LLMs for different agents
def create_groq_llm(model_name: str) -> LLM:
    return LLM(
        model=f"groq/{model_name}",
        api_key=GROQ_API_KEY,
        base_url=OPENAI_API_BASE
    )


class AISecurityCrew:
    def __init__(self):
        self.researcher_llm = create_groq_llm(MODELS["researcher"])
        self.writer_llm = create_groq_llm(MODELS["writer"])
        self.validator_llm = create_groq_llm(MODELS["validator"])

    def create_agents(self):
        """Create specialized agents with different Groq models."""

        # Research Agent - Uses Llama 70B for deep analysis
        researcher = Agent(
            role='AI Security Research Specialist',
            goal='Research latest AI security threats, frameworks, and best practices',
            backstory="""You are an expert AI security researcher with deep knowledge of 
            frameworks like OWASP LLM Top 10, ISO 42001, and NIST AI RMF. You stay current 
            with emerging threats and defense mechanisms.""",
            tools=[web_search, fetch_url_content, get_security_frameworks],
            llm=self.researcher_llm,
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )

        # Writer Agent - Uses Mixtral for creative content generation
        writer = Agent(
            role='Technical Content Writer',
            goal='Create clear, engaging, and technically accurate AI security content',
            backstory="""You are a skilled technical writer specializing in cybersecurity 
            and AI. You can explain complex concepts clearly while maintaining technical depth. 
            Your content is always original and well-structured.""",
            llm=self.writer_llm,
            verbose=True,
            max_iter=2,
            allow_delegation=True
        )

        # Validator Agent - Uses Llama 8B for fast validation
        validator = Agent(
            role='Content Quality Validator',
            goal='Ensure content accuracy, completeness, and quality',
            backstory="""You are a meticulous editor with expertise in AI security. 
            You validate technical accuracy, check for plagiarism, ensure proper citations, 
            and maintain consistent quality standards.""",
            llm=self.validator_llm,
            verbose=True,
            max_iter=2,
            allow_delegation=False
        )

        return researcher, writer, validator

    def create_tasks(self, topic: str, word_count: int = 1000):
        """Create tasks for the crew based on the topic."""

        research_task = Task(
            description=f"""
            Research the topic: "{topic}"

            Your research should include:
            1. Latest developments and current state
            2. Key security frameworks and standards
            3. Common threats and vulnerabilities
            4. Best practices and solutions
            5. Real-world examples and case studies

            Use web search to find recent information and get framework details.
            Focus on authoritative sources like NIST, OWASP, ISO, and academic papers.
            """,
            expected_output="Comprehensive research findings with sources and key insights",
            agent=None  # Will be assigned in generate_content
        )

        writing_task = Task(
            description=f"""
            Write a {word_count}-word article on: "{topic}"

            Structure your article with:
            1. Introduction explaining relevance and importance
            2. Current landscape and challenges
            3. Key frameworks and standards
            4. Best practices and solutions
            5. Implementation guidance with examples
            6. Future considerations
            7. Conclusion with key takeaways

            Requirements:
            - Use research findings as foundation
            - Include practical examples and code snippets where relevant
            - Cite at least 3 authoritative sources
            - Maintain professional but accessible tone
            - Format in Markdown
            """,
            expected_output=f"A complete {word_count}-word article in Markdown format",
            agent=None  # Will be assigned in generate_content
        )

        validation_task = Task(
            description=f"""
            Validate the article on: "{topic}"

            Check for:
            1. Technical accuracy of all claims
            2. Completeness of coverage
            3. Proper citation and attribution
            4. Quality of examples and recommendations
            5. Clarity and readability

            Provide:
            - List of any corrections needed
            - Suggestions for improvement
            - Overall quality assessment
            - Final approval status
            """,
            expected_output="Validation report with corrections and final approved content",
            agent=None  # Will be assigned in generate_content
        )

        return research_task, writing_task, validation_task

    def generate_content(self, topic: str, word_count: int = 1000) -> dict:
        """Generate AI security content for a given topic."""

        # Create agents
        researcher, writer, validator = self.create_agents()

        # Create tasks
        research_task, writing_task, validation_task = self.create_tasks(topic, word_count)

        # Assign agents to tasks
        research_task.agent = researcher
        writing_task.agent = writer
        validation_task.agent = validator

        # Create crew
        crew = Crew(
            agents=[researcher, writer, validator],
            tasks=[research_task, writing_task, validation_task],
            process=Process.sequential,
            verbose=2,
            memory=True
        )

        # Execute the crew
        result = crew.kickoff()

        # Save the content
        filename = topic.lower().replace(" ", "_").replace("/", "_")
        save_content(filename, str(result))

        return {
            "topic": topic,
            "content": str(result),
            "word_count": len(str(result).split()),
            "filename": f"{filename}.md",
            "status": "completed"
        }