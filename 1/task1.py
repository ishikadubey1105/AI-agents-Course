import os
import asyncio
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load the API key from the local .env file in this script's directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get the OpenAI API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Let's configure the OpenAI Client using our key
if openai_api_key:
    openai_client = OpenAI(api_key=openai_api_key)
    print("OpenAI client successfully configured.")
    # Let's view the first few characters in the key
    print(f"API Key prefix: {openai_api_key[:5]}...")
else:
    print("WARNING: OPENAI_API_KEY is not set in the environment or .env file.")

def print_markdown(text):
    """Displays text as Markdown in Jupyter or prints to standard console."""
    try:
        from IPython.display import display, Markdown
        display(Markdown(text))
    except (ImportError, NameError):
        print(text)

# Import the Agent and Runner classes to create and manage AI agents
from agents import Agent, Runner

# Define the instructions for the fact-checker AI Agent
fact_checker_instructions = """
Context:
You are a fact-checker who verifies the accuracy of statements.

Instructions:
When given a statement, carefully analyze its factual accuracy using your knowledge.

Input:
You will receive a statement that requires fact-checking.

Output:
Respond with:
1. A verdict prefix: either "✅ TRUE:" or "❌ FALSE:"
2. A brief, one-sentence explanation justifying your conclusion
"""

# Create a new agent called "Fact Checker"
fact_checker_agent = Agent(
    name="Fact Checker",                     # Name of the agent
    instructions=fact_checker_instructions,   # The rules and behavior for the agent
    model="gpt-4o-mini"                      # Using gpt-4o-mini as gpt-4.1 is not a valid OpenAI model
)

# Print a confirmation message that the agent was created
print(f"Agent '{fact_checker_agent.name}' created successfully!")

# A statement we want the Fact Checker agent to verify
statement = "The Great Wall of China is visible from space with the naked eye."

async def main():
    # Display the statement we're going to check (in markdown format for nicer formatting)
    print_markdown(f"Asking the Fact Checker to verify: '{statement}'")

    # Run the Fact Checker agent on the input statement
    # 'await' is used because running the agent is an asynchronous operation (it might take time)
    response = await Runner.run(
        starting_agent=fact_checker_agent,  # The agent we created earlier
        input=statement                     # The statement we want it to fact-check
    )

    # Display the agent's response
    print_markdown("\n🤖 Agent's Response:\n")
    print_markdown(response.final_output)    # Shows the final verdict and explanation

if __name__ == "__main__":
    asyncio.run(main())
