# Walkthrough - OpenAI Agents SDK with Persistent SQLite Memory (Task 5)

This document covers Task 5, which demonstrates persistent memory across conversations using the OpenAI Agents SDK with a SQLite backend — running on Groq's free LLaMA model.

## Project Structure

```
5/
├── task5.py          # Main agent script — persistent memory demo
├── agent_memory.db   # SQLite database (auto-created, not committed)
├── .env              # API keys — not committed (create locally)
└── walkthrough.md    # This documentation
```

> **Note:** `agent_memory.db` is excluded from Git via `.gitignore` as it may contain personal conversation data.

---

## What This Task Does

Demonstrates **persistent cross-turn memory** using `SQLiteSession` from the OpenAI Agents SDK:

1. **First interaction**: User tells the agent their name and age
2. **Second interaction**: User asks the agent to recall the name and age
3. The agent correctly remembers — using the SQLite session as a conversation store

---

## Key Concepts

| Concept | Description |
|---|---|
| `SQLiteSession` | Stores conversation history in a local `.db` file |
| `session_id` | Unique string key identifying a specific conversation thread |
| `Runner.run(..., session=session)` | Passes the session so history is read and written automatically |
| Groq as OpenAI-compatible backend | Uses `OPENAI_BASE_URL` env var to redirect calls to Groq's API |

---

## Setup & Implementation

1. **Install Dependencies**:
   ```powershell
   pip install openai-agents python-dotenv
   ```

2. **Set API Keys** — Create `5/.env`:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   OPENAI_API_KEY=your-groq-api-key-here
   ```
   > The Agents SDK reads `OPENAI_API_KEY`. Groq is configured as an OpenAI-compatible endpoint via `OPENAI_BASE_URL`.

3. **Run the script**:
   ```powershell
   & .venv313\Scripts\python 5/task5.py
   ```

---

## Running the Task

```powershell
& .venv313\Scripts\python 5/task5.py
```

**Expected output**:
```
--- First Interaction ---
User: Hi, my name is Parag Naik, I am 36 years old.
Agent: Nice to meet you, Parag! ...

--- Second Interaction ---
User: Can you remind me what my name is and what my age is?
Agent: Your name is Parag Naik, and you are 36 years old.
```
