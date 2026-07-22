from orchestrator import orchestrator
from datetime import datetime
import os

product = "Wireless noise-cancelling headphones with 40-hour battery life"

result = orchestrator(product)

# Save result to a markdown file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"campaign_{timestamp}.md"

md_content = f"""# 📢 Marketing Campaign Report

**Product:** {product}  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 🔍 Market Research

{result['market_research']}

---

## 🎨 Creative Strategy

{result['creative_strategy']}

---

## ✍️ Copywriting

{result['copy']}

---

## 📱 Social Media Posts

{result['social_media']}

---

## 🖼️ Image Prompt

{result['image_prompt']}

---

## ⭐ Review & Feedback

{result['review']}
"""

with open(filename, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"\nDone! Campaign saved to: {filename}")
