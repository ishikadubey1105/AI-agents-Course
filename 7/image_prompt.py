from ask_llm import ask_llm 
 
def image_prompt(strategy): 
 
  system = """ 
Create a detailed AI image generation prompt. 
 
Include 
 
Lighting 
 
Composition 
 
Style 
 
Background 
 
Objects 
 
Camera Angle 
 
Realistic 
""" 
 
  return ask_llm(system, strategy) 
