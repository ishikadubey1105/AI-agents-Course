#LANGCHAIN : BUILDING CHATBOT,CALLING TOOLS,CREATING RAG APPLICATIONS,SIMPLE AGENTS.abs
#LANGGRAPH: BUILDING PRODUCTION AI AGENTS , COORDINATING MULTIPLE AGENTS ,NEEDING LONG RUNNING WORKFLOWS,SUPPORTING HUMAN APPROVAL,HANDLING RETRICS AND INTERRUPTIONS

import os
import uuid
from dotenv import load_dotenv

from tavily import TavilyClient

from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

load_dotenv()


# 1. Brain (Groq LLM)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)




# 2. Tools (Tavily search)
tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_web(query: str):
    result = tavily_client.search(
        query=query,
        max_results=3
    )
    return result

search_tool = Tool(
    name="tavily_search",
    func=search_web,
    description="Search the internet for latest information."
)

from tools import calculator, word_counter, get_current_time, fetch_webpage_content, get_weather

tools = [
    search_tool,
    calculator,
    word_counter,
    get_current_time,
    fetch_webpage_content,
    get_weather
]


# 3. Memory
memory = MemorySaver()


# 4. Create Agent
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,
    prompt="You are a helpful AI assistant. Use tools when required. Remember previous conversation."
)


# 5. Chat Loop
print("="*50)
print("      GROQ AI AGENT WITH MEMORY STARTED")
print("="*50)

print("Type 'exit' to quit.\n")

# Use a thread_id to track conversation memory
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

while True:
    try:
        question = input("You : ")
        
        if question.lower() == "exit":
            break
            
        response = agent_executor.invoke(
            {"messages": [HumanMessage(content=question)]},
            config=config
        )
        
        print("\nAgent :", response["messages"][-1].content)
        print()
    except EOFError:
        break
    except KeyboardInterrupt:
        break