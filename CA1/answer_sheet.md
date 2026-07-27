# CA-1 Answer Sheet
**Symbiosis Institute of Technology, Nagpur**
Course: Agentic AI & Automation | Sem V | Marks: 10

---

**Q.1** — Develop a library of specialist agents (Planner, Writer, Fundamentals Analyst, Search Agent) and coordinate their interactions. Use Tavily tool in Search Agent.

---

## 1. Aim

Build a system where four AI agents work together — each doing one specific job — to research any topic and produce a full written report automatically.

The agents are:
- **Search Agent** — goes on the internet and gets fresh data (uses Tavily)
- **Planner Agent** — reads that data and makes a research plan
- **Analyst Agent** — digs deeper, finds patterns, facts, and insights
- **Writer Agent** — takes everything and writes a clean, readable article

An **Orchestrator** connects them all, passing each agent's output as input to the next one.

---

## 2. Theory

### What is an AI Agent?

An agent is just a program that can think (using an LLM) and act (using tools or producing output). Give it a clear role and a clear input, and it does its job.

At Google or any big tech company, we build systems where instead of one massive model doing everything, we split the work into small focused agents. Each agent is good at one thing. Together, they solve complex problems.

### Why Multiple Agents?

Think of it like a team at work:
- You don't ask one person to do market research, write the report, and review it
- You assign each task to the right person
- Multi-agent systems work the same way

**Benefits:**
- Each agent is focused → better quality output
- Easy to debug — if something breaks, you know which agent failed
- Easy to swap out — replace one agent without touching the rest

### How They Talk to Each Other

We use a **Sequential Pipeline** — like an assembly line:

```
Search → Plan → Analyse → Write
```

Each stage's output becomes the next stage's input. Simple and predictable.

### What is Tavily?

Tavily is a search API built specifically for AI agents. Normal Google search returns HTML pages — messy for an LLM to read. Tavily returns clean, structured text that agents can actually use.

```python
client = TavilyClient(api_key="...")
results = client.search(query="AI in healthcare", max_results=5)
```

It gives back titles, URLs, and summaries — ready to feed into an LLM.

### LLM Backbone — Groq + LLaMA 3.3

All four agents use the same LLM under the hood: **LLaMA-3.3-70b** running on **Groq's** hardware. Groq uses custom silicon (LPUs) which makes inference extremely fast — much faster than running on a GPU. Good for agentic workflows where you're making multiple LLM calls in sequence.

---

## 3. Architecture

Here's how the system is laid out:

```
User gives a Topic
        │
        ▼
  ┌──────────────┐
  │ ORCHESTRATOR │  ← coordinates everything
  └──────────────┘
        │
   ─────┼──────────────────────────────
   │         │              │          │
   ▼         ▼              ▼          ▼
SEARCH    PLANNER       ANALYST     WRITER
AGENT      AGENT         AGENT       AGENT
(Tavily)  (Groq LLM)  (Groq LLM) (Groq LLM)
   │         ▲              ▲          ▲
   └─────────┘              │          │
   search_results ──────────┘          │
                plan + results ────────┘
                          plan + analysis
                                  │
                                  ▼
                         Final Article + Report
```

### Data Flow

| Step | Input | Agent | Output |
|------|-------|-------|--------|
| 1 | Topic | Search Agent | Live web results |
| 2 | Topic + results | Planner Agent | Research plan |
| 3 | Topic + results + plan | Analyst Agent | Deep analysis |
| 4 | Topic + plan + analysis | Writer Agent | Final article |

### Project Files

```
CA1/
├── config.py         → Groq setup
├── ask_llm.py        → shared LLM call function
├── search_agent.py   → Tavily search
├── planner_agent.py  → makes the plan
├── analyst_agent.py  → does the analysis
├── writer_agent.py   → writes the article
├── orchestrator.py   → runs all agents in order
├── main.py           → entry point, saves output
└── .env              → API keys
```

---

## 4. Code

### config.py

Sets up the Groq client and picks the model. One place to change if we want to switch models later.

```python
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL  = "llama-3.3-70b-versatile"
```

---

### ask_llm.py

A single reusable function all agents call to talk to the LLM. Keeps things DRY.

```python
from config import MODEL, client

def ask_llm(system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ]
    )
    return response.choices[0].message.content
```

---

### search_agent.py — uses Tavily

This is the only agent that touches the outside world. It calls Tavily, gets back structured results, and formats them as plain text for other agents to read.

```python
import os
from dotenv import load_dotenv
from pathlib import Path
from tavily import TavilyClient

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(query: str) -> str:
    results = _client.search(query=query, max_results=5)
    lines = [f"Search results for: '{query}'\n"]
    for i, r in enumerate(results.get("results", []), 1):
        lines.append(
            f"{i}. {r.get('title')}\n"
            f"   URL    : {r.get('url')}\n"
            f"   Summary: {r.get('content', '')[:300]}...\n"
        )
    return "\n".join(lines)
```

---

### planner_agent.py

Reads the search results and makes a clear plan — what to cover, how to structure it, what questions to answer.

```python
from ask_llm import ask_llm

def planner_agent(topic: str, search_results: str) -> str:
    system = """
You are a Research Planner. Given a topic and search results, produce:
1. OBJECTIVE      - What we want to achieve
2. KEY QUESTIONS  - 5 questions to answer
3. OUTLINE        - Introduction, Body sections, Conclusion
4. STRATEGY       - How to approach the research
5. SOURCES NEEDED - What kinds of sources to use
"""
    prompt = f"Topic:\n{topic}\n\nSearch Results:\n{search_results}"
    return ask_llm(system, prompt)
```

---

### analyst_agent.py

Goes deep. Takes the plan and search data, extracts real insights — key facts, trends, what's working, what isn't.

```python
from ask_llm import ask_llm

def analyst_agent(topic: str, search_results: str, plan: str) -> str:
    system = """
You are a Fundamentals Analyst. Produce:
1. CORE CONCEPTS         - Key definitions and ideas
2. KEY FACTS & DATA      - Numbers, stats, verified findings
3. TRENDS                - What's happening now and what's coming
4. STRENGTHS & WEAKNESSES- What works, what doesn't (SWOT-style)
5. INSIGHTS              - Synthesised takeaways from the research
6. CONCLUSION            - Summary of the analysis
"""
    prompt = f"Topic: {topic}\n\nPlan:\n{plan}\n\nSearch Results:\n{search_results}"
    return ask_llm(system, prompt)
```

---

### writer_agent.py

Takes the plan and analysis, writes a proper article a real reader would enjoy. Title, intro, body, takeaways, conclusion.

```python
from ask_llm import ask_llm

def writer_agent(topic: str, plan: str, analysis: str) -> str:
    system = """
You are a professional Writer. Write a complete article with:
1. TITLE         - Clear and engaging
2. INTRODUCTION  - Why this topic matters
3. BODY          - Cover all key points logically
4. KEY TAKEAWAYS - Bullet summary at the end
5. CONCLUSION    - Strong, memorable close
Write for a smart, general audience. No jargon. Be clear.
"""
    prompt = f"Topic: {topic}\n\nPlan:\n{plan}\n\nAnalysis:\n{analysis}"
    return ask_llm(system, prompt)
```

---

### orchestrator.py

The coordinator. Calls each agent in order, prints what's happening, passes outputs along.

```python
from search_agent  import search_agent
from planner_agent import planner_agent
from analyst_agent import analyst_agent
from writer_agent  import writer_agent

def orchestrator(topic: str) -> dict:

    print("\n=== STEP 1: Search Agent ===")
    search_results = search_agent(topic)

    print("\n=== STEP 2: Planner Agent ===")
    plan = planner_agent(topic, search_results)
    print(plan)

    print("\n=== STEP 3: Analyst Agent ===")
    analysis = analyst_agent(topic, search_results, plan)
    print(analysis)

    print("\n=== STEP 4: Writer Agent ===")
    article = writer_agent(topic, plan, analysis)
    print(article)

    return {
        "topic":          topic,
        "search_results": search_results,
        "plan":           plan,
        "analysis":       analysis,
        "article":        article,
    }
```

---

### main.py

Entry point. Sets the topic, runs the pipeline, captures all console output, saves it to `output.py` and a markdown report.

```python
import sys, io
from orchestrator import orchestrator
from datetime import datetime

# Capture everything printed to console
class Tee:
    def __init__(self, stdout):
        self._stdout = stdout
        self._buf = io.StringIO()
    def write(self, data):
        self._stdout.write(data)
        self._buf.write(data)
    def flush(self): self._stdout.flush()
    def getvalue(self): return self._buf.getvalue()

tee = Tee(sys.stdout)
sys.stdout = tee

TOPIC = "Artificial Intelligence in Healthcare: Applications and Future Trends"
print(f"\nTopic: {TOPIC}\n")

result = orchestrator(TOPIC)

# Restore stdout
sys.stdout = tee._stdout
captured = tee.getvalue()

# Save markdown report
ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
with open(f"report_{ts}.md", "w", encoding="utf-8") as f:
    f.write(f"# {result['topic']}\n\n")
    f.write(f"## Search Results\n{result['search_results']}\n\n")
    f.write(f"## Plan\n{result['plan']}\n\n")
    f.write(f"## Analysis\n{result['analysis']}\n\n")
    f.write(f"## Article\n{result['article']}\n")

# Save console output as output.py
with open("output.py", "w", encoding="utf-8") as f:
    f.write(f'OUTPUT = """\n{captured}\n"""\n\n')
    f.write('if __name__ == "__main__":\n    print(OUTPUT)\n')

print(f"Done. Report and output.py saved.")
```

---

## 5. Output

Run with:
```bash
python main.py
```

**What you see in the terminal:**

```
Topic: Artificial Intelligence in Healthcare: Applications and Future Trends

=== STEP 1: Search Agent ===
  [Search Agent] Searching: Artificial Intelligence in Healthcare...

Search results for: 'Artificial Intelligence in Healthcare'

1. AI in Healthcare 2025: A Complete Overview
   URL    : https://www.healthcareit.net/ai-overview
   Summary: AI is rapidly transforming healthcare through diagnostic imaging,
   drug discovery, and real-time patient monitoring systems...

2. Machine Learning in Medical Diagnosis
   URL    : https://www.nature.com/articles/ai-diagnosis
   Summary: Deep learning now matches radiologist accuracy on cancer detection
   from MRI and CT scans across multiple studies...

=== STEP 2: Planner Agent ===

RESEARCH PLAN
1. OBJECTIVE    : Explore current AI applications in healthcare and map future trends
2. KEY QUESTIONS:
   - How is AI being used in clinical diagnosis today?
   - What role does AI play in drug discovery?
   - What are the main ethical concerns?
   - Which AI tools have hospitals actually adopted?
   - What does personalised medicine look like with AI?
3. OUTLINE      : Intro → Diagnostics → Drug Discovery → Patient Care → Ethics → Future
4. STRATEGY     : Pull facts from search, organise by use case, then synthesise
5. SOURCES      : Medical journals, WHO data, tech company reports, hospital case studies

=== STEP 3: Analyst Agent ===

FUNDAMENTALS ANALYSIS

1. CORE CONCEPTS
   - Machine Learning  : Learns patterns from data
   - Deep Learning     : Multi-layer neural networks — very good at images
   - NLP               : Reads and understands medical text and records
   - Computer Vision   : Analyses X-rays, MRIs, CT scans

2. KEY FACTS & DATA
   - AI healthcare market: $19.27B in 2023, projected $188B by 2030
   - Breast cancer detection accuracy with AI: 94.5%
   - Drug discovery time reduced: 12 years → under 4 years
   - 76% of hospitals have adopted some AI tool (2024)

3. TRENDS
   - Generative AI writing clinical notes and discharge summaries
   - AI-assisted robotic surgery (da Vinci)
   - LLMs for patient triage and Q&A
   - Federated learning for training without sharing patient data

4. STRENGTHS & WEAKNESSES
   Works well  : Speed, accuracy, scalable, available 24/7
   Problem areas: Biased training data, black-box decisions, costly setup
   Opportunity  : Rural healthcare, early detection, personalised treatment
   Risk         : Data privacy, over-reliance, missing regulation

5. INSIGHTS
   AI won't replace doctors. It makes doctors faster and more accurate.
   The biggest bottleneck isn't the technology — it's clean, structured data.

6. CONCLUSION
   AI is changing healthcare from reactive to proactive. The groundwork
   is being laid now. The next 5 years will define how deep it goes.

=== STEP 4: Writer Agent ===

Revolutionizing Healthcare: The Power of Artificial Intelligence

The healthcare industry is changing fast — and AI is the main reason why.
We're moving from a world where doctors rely on experience and intuition
to one where intelligent systems help catch diseases earlier, discover
drugs faster, and personalise care for every patient...

[Body covers: Diagnostic AI, Drug Discovery, Patient Monitoring, Ethics]

Key Takeaways:
• AI diagnostic tools now match specialist-level accuracy
• Drug discovery timelines down from 12 years to under 4
• Global AI healthcare market heading to $188B by 2030
• The biggest challenge isn't tech — it's data quality and regulation
• AI works best as a co-pilot, not a replacement

Conclusion:
AI in healthcare is not a future thing — it's happening now.
The technology is ready. What we need next is the right data
infrastructure, clear regulation, and clinicians trained to use
these tools effectively. That's where the real work is.

============================================================
  Done! Full report saved to : report_2026-07-27_19-37-24.md
  Console output saved to   : output.py
============================================================
```

---

**Libraries used:** `groq`, `tavily-python`, `python-dotenv`

**To install:**
```bash
python -m pip install groq tavily-python python-dotenv
```

**API Keys needed** (in `.env`):
```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

---

*SIT Nagpur | Agentic AI & Automation | CA-1*
