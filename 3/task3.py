#pip show langchain
#pip show langchain-core
#pip show langchain-community
#pip show langchain-tavily

#pip show tavily-python

import os
from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient
# pyrefly: ignore [missing-import]
from langchain_core.tools import Tool

# Load API key from .env file in this folder (3/.env)
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not set. Add it to your .env file.")

client = TavilyClient(api_key=tavily_api_key)

def search_web(query: str):
    return client.search(query=query, max_results=3)

tavily_tool = Tool(
    name="Tavily Search",
    func=search_web,
    description="Search the web for current information."
)

print(tavily_tool.invoke("Who is Virat Kohli?"))