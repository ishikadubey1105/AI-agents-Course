# Walkthrough - Web Search Tool with Tavily & LangChain (Task 3)

This document covers Task 3, which introduces web search as an agent tool using the Tavily API wrapped with a LangChain `Tool`.

## Project Structure under Folder `1/3`

```
1/3/
├── task3.py       # Main script — Tavily web search tool demo
└── walkthrough.md # This documentation
```

> **Note:** The Tavily API key is loaded from `1/3/4/.env` (shared with Task 4). Never hardcode keys in source files.

---

## What This Task Does

- Connects to the **Tavily Search API** — a search engine built for AI agents that returns structured, clean web results.
- Wraps the Tavily client in a **LangChain `Tool`** so it can be plugged into any LangChain/LangGraph agent.
- Runs a sample search query: `"Who is Virat Kohli?"` and prints the structured results.

---

## Key Concepts

| Concept | Description |
|---|---|
| `TavilyClient` | Tavily's Python SDK for real-time web search |
| `langchain_core.tools.Tool` | LangChain wrapper that makes a Python function usable as an agent tool |
| `.invoke()` | Calls the tool with a string input and returns the search results |

---

## Setup & Implementation

1. **Install Dependencies**:
   ```powershell
   pip install tavily-python langchain-core langchain-community python-dotenv
   ```

2. **Set API Key** — Add to `1/3/4/.env`:
   ```env
   TAVILY_API_KEY=your-tavily-api-key-here
   ```
   Get a free key at [app.tavily.com](https://app.tavily.com).

3. **Run the script**:
   ```powershell
   & .venv313\Scripts\python 1/3/task3.py
   ```

---

## Running the Task

```powershell
& .venv313\Scripts\python 1/3/task3.py
```

**Expected output**: A list of up to 3 structured web search results about Virat Kohli, including titles, URLs, and content snippets.
