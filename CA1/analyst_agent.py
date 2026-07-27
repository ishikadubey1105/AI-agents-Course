from ask_llm import ask_llm


def analyst_agent(topic: str, search_results: str, plan: str) -> str:
    """
    Fundamentals Analyst Agent
    --------------------------
    Analyses fundamental concepts, data, and key facts related to the topic.
    Uses the plan and search results to produce a deep analytical report.
    """
    system = """
You are a Fundamentals Analyst Agent — an expert at in-depth research and analysis.

Given a topic, search results, and a research plan, produce a FUNDAMENTALS ANALYSIS containing:

1. CORE CONCEPTS        - Define the key concepts and terminology
2. KEY FACTS & DATA     - Important statistics, numbers, and verified facts
3. TREND ANALYSIS       - Current and emerging trends in the area
4. STRENGTHS & WEAKNESSES - Pros, cons, opportunities, and risks (SWOT-style)
5. EXPERT INSIGHTS      - Synthesised insights from the search results
6. CONCLUSION           - Summary of the fundamental findings

Be analytical, fact-driven, and thorough.
"""

    prompt = f"""
Topic:
{topic}

Research Plan:
{plan}

Live Search Results:
{search_results}

Produce a comprehensive fundamentals analysis.
"""
    return ask_llm(system, prompt)
