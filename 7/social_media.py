from ask_llm import ask_llm

def social_media(copy):

    system = """
Convert advertisement into

Instagram

Facebook

LinkedIn

Twitter

YouTube Shorts
"""

    return ask_llm(system, copy)
