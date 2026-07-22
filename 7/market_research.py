from ask_llm import ask_llm

def market_research(product):

    system = """
You are a market analyst.

Provide

Target audience

Pain points

Current trends

Competitor positioning
"""

    return ask_llm(system, product)
