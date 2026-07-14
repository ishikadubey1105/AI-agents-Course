#pip show langchain
#pip show langchain-core
#pip show langchain-community
#pip show langchain-tavily

#pip show tavily-python

from tavily import TavilyClient
# pyrefly: ignore [missing-import]
from langchain_core.tools import Tool

client = TavilyClient(api_key="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")

def search_web(query: str):
    return client.search(query=query, max_results=3)

tavily_tool = Tool(
    name="Tavily Search",
    func=search_web,
    description="Search the web for current information."
)

print(tavily_tool.invoke("Who is Virat Kohli?"))