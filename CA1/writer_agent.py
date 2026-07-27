from ask_llm import ask_llm


def writer_agent(topic: str, plan: str, analysis: str) -> str:
    """
    Writer Agent
    ------------
    Takes the research plan and analysis, then writes a complete,
    well-structured article / report ready for publication.
    """
    system = """
You are a professional Writer Agent — an expert at transforming research into compelling content.

Given a topic, research plan, and analysis, write a COMPLETE ARTICLE containing:

1. TITLE            - A catchy, informative title
2. INTRODUCTION     - Hook the reader; state the purpose (2-3 paragraphs)
3. BODY             - Detailed, logically flowing sections covering all key points
4. KEY TAKEAWAYS    - Bullet-point summary of the most important insights
5. CONCLUSION       - Strong closing that ties everything together
6. REFERENCES STYLE - Mention sources naturally within the text

Use clear, engaging language. Avoid jargon. Write for an educated general audience.
"""

    prompt = f"""
Topic:
{topic}

Research Plan:
{plan}

Fundamentals Analysis:
{analysis}

Write a complete, publication-ready article on the topic.
"""
    return ask_llm(system, prompt)
