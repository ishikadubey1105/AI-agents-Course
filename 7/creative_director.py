from ask_llm import ask_llm

def creative_director(product, market):

    system = """
You are an award-winning Creative Director.

Responsibilities

Create:

Campaign Theme

Brand Emotion

Story

Tagline

Color Mood

Target Audience

Marketing Angle
"""

    prompt = f"""
Product

{product}

Market Research

{market}
"""

    return ask_llm(system, prompt)
