from ask_llm import ask_llm 
 
def reviewer(ad): 
 
  system = """ 
Review advertisement. 
 
Check 
 
Grammar 
 
Persuasiveness 
 
Consistency 
 
Marketing Impact 
 
Return improved version. 
""" 
 
  return ask_llm(system, ad) 
