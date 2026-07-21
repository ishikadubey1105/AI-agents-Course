"""
Task 6: CrewAI Multi-Agent System (using Groq - free)
- Market Research Analyst Agent (uses WebsiteSearchTool)
- Content Writer Agent (no tools, writes based on research)
- Crew orchestrates both agents with AI planning enabled
"""

# Fix Windows emoji/Unicode encoding issue with CrewAI verbose output
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Step 1: Install dependencies (run in terminal)
# py -3.13 -m pip install crewai crewai-tools langchain langchain-community langchain-openai python-dotenv

# Step 2: Imports & Setup
import os
from dotenv import load_dotenv
from crewai import LLM
import litellm

# Monkey-patch: crewai adds Anthropic-style 'cache_breakpoint' to messages,
# but Groq doesn't support it. Strip it before every API call.
_orig_completion = litellm.completion
def _groq_safe_completion(*args, **kwargs):
    if "messages" in kwargs:
        for msg in kwargs["messages"]:
            if isinstance(msg, dict):
                msg.pop("cache_breakpoint", None)
                msg.pop("cache_control", None)
    return _orig_completion(*args, **kwargs)
litellm.completion = _groq_safe_completion

# Load API key from .env file in this folder (6/.env)
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# Groq has an OpenAI-compatible API — use crewai's native openai provider
# pointed at Groq's endpoint. No litellm needed!
groq_api_key = os.environ.get("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",   # Requires litellm (pip install litellm)
    api_key=groq_api_key,
    temperature=0
)

# Step 3: Websearch Tool
from crewai_tools import WebsiteSearchTool

# Instantiate web search tool
web_search_tool = WebsiteSearchTool()

# Step 4: Create Agents
from crewai import Agent

researcher = Agent(
    role='Market Research Analyst',
    goal='Provide up-to-date market analysis of the AI industry',
    backstory='An expert analyst with a keen eye for market trends.',
    tools=[web_search_tool],  # Only uses web search tool
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Content Writer',
    goal='Craft engaging blog posts about the AI Industry',
    backstory='A skilled writer with a passion for technology.',
    tools=[],   # No tools needed, writes based on research summary
    llm=llm,
    verbose=True
)

# Step 5: Define Tasks
from crewai import Task, Crew

research = Task(
    description='Search the web for the latest AI trends and provide a summarized report.',
    expected_output='A summary of the top 3 trending developments in AI with insights on their impact.',
    agent=researcher
)

write = Task(
    description="Write an engaging blog post about the AI industry based on the research analyst's summary.",
    expected_output='A well-structured, 4-paragraph blog post in markdown format with simple, engaging content.',
    agent=writer,
    output_file='blog-posts/new_post.md'
)

# Step 6: Assemble the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    verbose=True,
    planning=True,       # Enabling AI planning feature
    planning_llm=llm     # Required in crewai>=1.0 when planning=True
)


# Create output directory if it doesn't exist
os.makedirs('blog-posts', exist_ok=True)
# Step 7: Execute the Tasks
result = crew.kickoff()
print(result)
