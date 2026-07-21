# Walkthrough - LangGraph ReAct Agent with Memory & Tools (Task 4)

This document covers Task 4, which builds a full ReAct agent using LangGraph with persistent in-memory conversation history and multiple tools.

## Project Structure

```
4/
├── task4.py       # Main agent script — LangGraph ReAct agent
├── tools.py       # Custom tool definitions (calculator, weather, etc.)
├── .env           # API keys — not committed (create locally)
└── walkthrough.md # This documentation
```

> **Note:** All API keys are loaded from `4/.env`. Never commit `.env` files.

---

## What This Task Does

Builds a **conversational AI agent** using:
- **LangGraph's `create_react_agent`** — implements the ReAct (Reason + Act) loop
- **Groq LLM** (`llama-3.3-70b-versatile`) as the brain
- **MemorySaver** for persistent in-session conversation memory
- **Multiple tools** that the agent can choose from:

| Tool | Description |
|---|---|
| `tavily_search` | Live web search via Tavily API |
| `calculator` | Evaluate math expressions safely |
| `word_counter` | Count words, characters, sentences |
| `get_current_time` | Returns current UTC time |
| `fetch_webpage_content` | Fetches and strips HTML from a URL |
| `get_weather` | Current weather via Open-Meteo (no key needed) |

---

## Key Concepts

| Concept | Description |
|---|---|
| **ReAct Pattern** | Agent reasons about what tool to use, uses it, observes result, repeats |
| **LangGraph** | Production-grade framework for stateful, multi-step agent workflows |
| **MemorySaver** | Stores conversation history in-memory using a `thread_id` |
| **`thread_id`** | Unique UUID per session — allows multiple independent conversations |

---

## Setup & Implementation

1. **Install Dependencies**:
   ```powershell
   pip install langchain-groq langgraph tavily-python python-dotenv requests
   ```

2. **Set API Keys** — Create `4/.env`:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   TAVILY_API_KEY=your-tavily-api-key-here
   ```

3. **Run the agent**:
   ```powershell
   & .venv313\Scripts\python 4/task4.py
   ```

---

## Running the Task

```powershell
& .venv313\Scripts\python 4/task4.py
```

Type any question at the `You :` prompt. The agent will decide whether a tool is needed, call it, and remember context from previous messages. Type `exit` to quit.
