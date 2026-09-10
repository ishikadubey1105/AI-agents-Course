# Agentic AI — Course Work

Seven progressively harder LLM-agent builds, plus a graded assignment, from a flexi-credit course on Agentic AI taught by a visiting industry practitioner at Symbiosis Institute of Technology, Nagpur.

Each task folder has its own `walkthrough.md` explaining what was built and why. The two substantial pieces are **task 7** and **CA1** — if you're only going to look at one thing, look at task 7.

---

## Task 7 — Multi-Agent Campaign System

The largest build here. An orchestrator decomposes a product brief and routes each sub-task to a specialist agent, then a reviewer critiques the assembled output before it's finalised.

```
                    product brief
                          |
                          v
                   orchestrator.py          plans + dispatches
                          |
     +---------------+----+----+----------------+
     v               v         v                v
market_research  product_  creative_       copywriter
                 analyst   director
     +---------------+----+----+----------------+
                          |
                          v
                     reviewer.py   <-- critique / revise loop
                          |
                          v
              campaign_<timestamp>.md
```

| Module | Responsibility |
| --- | --- |
| `orchestrator.py` | Decomposes the brief, sequences agents, assembles output |
| `market_research.py` | Audience, competitive landscape, positioning |
| `product_analyst.py` | Feature-to-benefit translation |
| `creative_director.py` | Campaign concept and tone |
| `copywriter.py` | Headlines, body copy, calls to action |
| `social_media.py` | Channel-specific adaptations |
| `image_prompt.py` | Prompts for accompanying visuals |
| `reviewer.py` | Critiques the campaign, triggers revisions |
| `ask_llm.py` | Provider wrapper — one place to swap models |

Sample outputs are committed as `campaign_<timestamp>.md`.

**Known weakness:** there is no evaluation harness. Whether the multi-agent decomposition actually beats a single well-prompted call is currently an assumption, not a measured result, and the revision loop has no cap or stopping criterion beyond the reviewer's judgement. Both are the first things I'd fix.

## CA1 — Research assistant

A four-agent research pipeline: a planner decomposes the question, a search agent gathers sources, an analyst synthesises, and a writer produces the final answer sheet.

```
main.py -> orchestrator.py -> planner_agent.py
                           -> search_agent.py
                           -> analyst_agent.py
                           -> writer_agent.py
                           -> answer_sheet.md / .html
```

## Tasks 1-6

| Task | Build |
| --- | --- |
| 1 | Fact-checker agent — takes a claim, returns a verdict with reasoning |
| 2 | Agent running against a different provider backend (Groq) |
| 3 | Prompt and control-flow refinements |
| 4 | Tool-using agent (`tools.py`) — the agent calls functions, not just text |
| 5 | Extended agent behaviour |
| 6 | Blog-post generation agent, with outputs in `blog-posts/` |

Each folder's `walkthrough.md` has the detail.

## Running

```bash
git clone https://github.com/ishikadubey1105/AI-agents-Course
cd AI-agents-Course
pip install -r requirements.txt

cp 1/.env.example 1/.env    # add your API key
python 7/app.py             # the multi-agent campaign system
```

| Variable | Used by |
| --- | --- |
| `OPENAI_API_KEY` | task 1 |
| `GROQ_API_KEY` | task 2 onward |

Model choice and generation parameters live in `config.py`.

---

**Stack:** Python, OpenAI and Groq APIs, multi-agent orchestration

*Built by [Ishika Dubey](https://github.com/ishikadubey1105) — B.Tech CSE (AI & ML), SIT Nagpur*

