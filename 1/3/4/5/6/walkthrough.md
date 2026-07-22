# Walkthrough - CrewAI Multi-Agent System with AI Planning (Task 6)

This document covers Task 6, which builds a full multi-agent crew using CrewAI with two specialized agents, task delegation, AI planning, and blog post generation — all running on Groq's free LLaMA model.

## Project Structure under Folder `1/3/4/5/6`

```
1/3/4/5/6/
├── TASK6.PY           # Main crew script — multi-agent blog writer
├── blog-posts/
│   └── new_post.md    # Auto-generated blog post output
└── walkthrough.md     # This documentation
```

> **Note:** API keys are loaded from the parent `.env` at `1/3/4/.env`. Never commit `.env` files.

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
| `output_file` | The writer task saves its output directly to `blog-posts/new_post.md` |
| Groq via litellm | CrewAI uses `groq/llama-3.3-70b-versatile` through litellm routing |

---

## Issues Fixed

1. **Windows Emoji Encoding Error** (`charmap` codec):
   - CrewAI's verbose output uses emoji characters (🚀📋) that Windows terminals can't display.
   - **Fix**: Added `sys.stdout`/`sys.stderr` wrappers with `encoding='utf-8'` at the top of the script.

2. **`cache_breakpoint` Groq Incompatibility**:
   - CrewAI adds Anthropic-style `cache_breakpoint` fields to messages; Groq rejects them.
   - **Fix**: Applied a monkey-patch on `litellm.completion` to strip those fields before every API call.

3. **`WebsiteSearchTool` 429 Error**:
   - The tool uses OpenAI embeddings internally; hitting quota limits causes a 429.
   - **Impact**: Non-fatal — the writer agent uses its own knowledge as a fallback.

---

## Setup & Implementation

1. **Install Dependencies**:
   ```powershell
   pip install crewai crewai-tools litellm python-dotenv
   ```

2. **Set API Key** in `1/3/4/.env`:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   CREWAI_TRACING_ENABLED=false
   ```
   > `CREWAI_TRACING_ENABLED=false` silences the `ConnectionResetError` telemetry warnings.

3. **Run the crew**:
   ```powershell
   $env:PYTHONUTF8=1; & .venv313\Scripts\python 1/3/4/5/6/TASK6.PY
   ```

---

## Running the Task

```powershell
$env:PYTHONUTF8=1; & .venv313\Scripts\python 1/3/4/5/6/TASK6.PY
```

**What happens**:
1. CrewAI plans the execution using the LLM
2. The **Researcher** agent searches for the latest AI trends
3. The **Writer** agent composes a 4-paragraph blog post
4. Output is saved to `blog-posts/new_post.md` and printed to console

**Sample generated blog post topics**: Explainable AI (XAI), Edge AI, Transfer Learning, AI-powered Cybersecurity.
