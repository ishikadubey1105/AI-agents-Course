from ask_llm import ask_llm 
 
def product_analyst(product): 
  system = """ 
Analyze product features. 
 
Explain 
 
USP 
 
Benefits 
 
Competitors 
 
Ideal Customer 
""" 
 
  return ask_llm(system, product) 
