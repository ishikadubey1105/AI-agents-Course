import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the local .env file relative to the script path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get the Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client using the loaded API key
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment or .env file.")

client = Groq(api_key=groq_api_key)

sys_msg = """You are a travel agent AI.
             Your job is to:    
            -answer travel questions.
            -suggest itineraries.
            -recommend hotels and transport.
            """

while True:
    query = input("User: ")
    if not query.strip():
        continue
        
    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": query}
            ]
        )
        print("Agent:", response.choices[0].message.content)
        print("\n")
    except Exception as e:
        print(f"Error: {e}")
        print("\n")
