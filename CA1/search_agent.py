import os
from dotenv import load_dotenv
from pathlib import Path
from tavily import TavilyClient

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

# ── Tavily client setup ──────────────────────────────────────────────────────
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found. Add it to CA1/.env")

_tavily_client = TavilyClient(api_key=tavily_api_key)


def search_agent(query: str) -> str:
    """
    Search Agent
    ------------
    Calls Tavily directly to fetch live web results for a given query.
    Returns a formatted string of the top-5 search results.
    (LangChain Tool wrapper removed — uses TavilyClient directly.)
    """
    print(f"  [Search Agent] Searching: {query}")
    results = _tavily_client.search(query=query, max_results=5)
    output_lines = [f"Search results for: '{query}'\n"]
    for i, r in enumerate(results.get("results", []), 1):
        output_lines.append(
            f"{i}. {r.get('title', 'No title')}\n"
            f"   URL    : {r.get('url', '')}\n"
            f"   Summary: {r.get('content', '')[:300]}...\n"
        )
    return "\n".join(output_lines)


if __name__ == "__main__":
    print(search_agent("Latest trends in AI autonomous agents 2025"))

