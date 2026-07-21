# Walkthrough - CrewAI Multi-Agent System with AI Planning (Task 6)

This document covers Task 6, which builds a full multi-agent crew using CrewAI with two specialized agents, task delegation, AI planning, and blog post generation — all running on Groq's free LLaMA model.

## Project Structure

```
6/
├── TASK6.PY           # Main crew script — multi-agent blog writer
├── .env               # API keys — not committed (create locally)
├── blog-posts/
│   └── new_post.md    # Auto-generated blog post output
└── walkthrough.md     # This documentation
```

> **Note:** API keys are loaded from `6/.env`. Never commit `.env` files.

---

## What This Task Does

Orchestrates **two AI agents** working together to research and write a blog post:

| Agent | Role | Tools |
|---|---|---|
| **Market Research Analyst** | Searches the web for latest AI trends | `WebsiteSearchTool` |
| **Content Writer** | Writes a 4-paragraph markdown blog post based on research | None |

With **AI Planning enabled** (`planning=True`), CrewAI generates an execution plan before running the tasks, resulting in better-coordinated output.

---

## Key Concepts

| Concept | Description |
|---|---|
| `Agent` | A specialized AI with a role, goal, backstory, and optional tools |
| `Task` | A unit of work assigned to an agent with a description and expected output |
| `Crew` | Orchestrator that runs agents and tasks in sequence |
| `planning=True` | Enables a pre-run AI planning step that improves task coordination |
| `output_file` | The writer task saves its output to `blog-posts/new_post.md` |
| Groq via litellm | CrewAI uses `groq/llama-3.3-70b-versatile` through litellm routing |

---

## Issues Fixed

1. **Windows Emoji Encoding Error** (`charmap` codec):
   - CrewAI's verbose output uses emoji characters that Windows terminals can't display.
   - **Fix**: Added UTF-8 stdout/stderr wrappers at the top of the script.

2. **`cache_breakpoint` Groq Incompatibility**:
   - CrewAI adds Anthropic-style fields that Groq rejects.
   - **Fix**: Monkey-patch on `litellm.completion` strips those fields before every API call.

---

## Setup & Implementation

1. **Install Dependencies**:
   ```powershell
   pip install crewai crewai-tools litellm python-dotenv
   ```

2. **Set API Key** — Create `6/.env`:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   CREWAI_TRACING_ENABLED=false
   ```

3. **Run the crew**:
   ```powershell
   $env:PYTHONUTF8=1; & .venv313\Scripts\python 6/TASK6.PY
   ```

---

## Running the Task

```powershell
$env:PYTHONUTF8=1; & .venv313\Scripts\python 6/TASK6.PY
```

**Output**: A 4-paragraph blog post saved to `6/blog-posts/new_post.md` covering top AI trends such as Explainable AI, Edge AI, and Transfer Learning.
