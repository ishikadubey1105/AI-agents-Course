from search_agent  import search_agent
from planner_agent import planner_agent
from analyst_agent import analyst_agent
from writer_agent  import writer_agent


def orchestrator(topic: str) -> dict:
    """
    Orchestrator
    ------------
    Coordinates all specialist agents in sequence:
      Step 1 → Search Agent      : Gather live web information
      Step 2 → Planner Agent     : Build a structured research plan
      Step 3 → Analyst Agent     : Perform in-depth fundamentals analysis
      Step 4 → Writer Agent      : Produce the final article

    Returns a dict with each agent's output.
    """

    separator = "=" * 60

    # ── STEP 1: Search Agent ─────────────────────────────────────────────────
    print(f"\n{separator}")
    print("  STEP 1 : Search Agent  (Tavily Web Search)")
    print(separator)
    search_results = search_agent(topic)
    print(search_results[:500], "...\n")   # preview first 500 chars

    # ── STEP 2: Planner Agent ────────────────────────────────────────────────
    print(f"\n{separator}")
    print("  STEP 2 : Planner Agent")
    print(separator)
    plan = planner_agent(topic, search_results)
    print(plan)

    # ── STEP 3: Fundamentals Analyst Agent ───────────────────────────────────
    print(f"\n{separator}")
    print("  STEP 3 : Fundamentals Analyst Agent")
    print(separator)
    analysis = analyst_agent(topic, search_results, plan)
    print(analysis)

    # ── STEP 4: Writer Agent ─────────────────────────────────────────────────
    print(f"\n{separator}")
    print("  STEP 4 : Writer Agent")
    print(separator)
    article = writer_agent(topic, plan, analysis)
    print(article)

    return {
        "topic":          topic,
        "search_results": search_results,
        "plan":           plan,
        "analysis":       analysis,
        "article":        article,
    }
