from ask_llm import ask_llm

def copywriter(strategy):

    system = """
You are a professional advertising copywriter.

Write

Headline

Body

Instagram Caption

Call To Action

Facebook Ad

Google Ad
"""

    return ask_llm(system, strategy)
