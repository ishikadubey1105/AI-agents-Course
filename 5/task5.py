Parag Naik <paragspnaik@gmail.com>
Attachments
12:09 PM (0 minutes ago)
to me

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq as an OpenAI compatible API
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "true"

from agents import Agent, Runner
from agents.memory import SQLiteSession

# Create an agent that acts as a conversational assistant
memory_agent = Agent(
    name="Memory Assistant",
    instructions="You are a helpful assistant with persistent memory. Keep track of details the user tells you. Be conversational and concise.",
    model="llama-3.1-8b-instant" # Using Groq's LLaMA model
)

async def main():
    # Initialize SQLite session
    # session_id uniquely identifies the conversation thread
    # db_path is the location of the SQLite database file
    db_file = os.path.join(os.path.dirname(__file__), "agent_memory.db")
    session = SQLiteSession(
        session_id="user_session_1",
        db_path=db_file
    )

    print(f"Using SQLite Database at: {db_file}\n")

    print("--- First Interaction ---")
    print("User: Hi, my name is Parag Naik, I am 36 years old.")
    response1 = await Runner.run(
        starting_agent=memory_agent,
        input="Hi, my name is Parag Naik, I am 36 years old.",
        session=session
    )
    print(f"Agent: {response1.final_output}\n")

    print("--- Second Interaction ---")
    print("User: Can you remind me what my name is and what my age is?")
    response2 = await Runner.run(
        starting_agent=memory_agent,
        input="Can you remind me what my name is and what my age is?",
        session=session
    )
    print(f"Agent: {response2.final_output}\n")
   
    # Close the session connection when done
    session.close()

if __name__ == "__main__":
    asyncio.run(main())