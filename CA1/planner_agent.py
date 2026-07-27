from ask_llm import ask_llm


def planner_agent(topic: str, search_results: str) -> str:
    """
    Planner Agent
    -------------
    Receives a topic and live search results, then produces a structured
    research plan: objectives, key questions, outline, and strategy.
    """
    system = """
You are an expert Research Planner Agent.

Given a topic and live search results, produce a structured PLAN containing:

1. OBJECTIVE       - What we aim to achieve
2. KEY QUESTIONS   - 5 important questions to answer about the topic
3. RESEARCH OUTLINE- A clear section-by-section outline (Introduction, Body, Conclusion)
4. STRATEGY        - How to approach and organise the research
5. SOURCES NEEDED  - Types of sources to consult

Be concise, logical, and structured.
"""

    prompt = f"""
Topic:
{topic}

Live Search Results:
{search_results}

Produce a detailed research plan based on the above.
"""
    return ask_llm(system, prompt)
