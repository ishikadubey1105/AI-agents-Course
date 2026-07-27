import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from config import MODEL, client

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

def ask_llm(system: str, user: str) -> str:
    """Send a prompt to the LLM and return the response text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ]
    )
    return response.choices[0].message.content
