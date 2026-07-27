import sys
import io
from orchestrator import orchestrator
from datetime import datetime

# ── Tee: write to both console AND a buffer simultaneously ───────────────────
class Tee:
    """Mirrors every write to stdout AND to an internal buffer."""
    def __init__(self, original_stdout):
        self._stdout = original_stdout
        self._buf    = io.StringIO()

    def write(self, data):
        self._stdout.write(data)
        self._buf.write(data)

    def flush(self):
        self._stdout.flush()

    def getvalue(self):
        return self._buf.getvalue()

tee = Tee(sys.stdout)
sys.stdout = tee          # redirect stdout → tee

# ── Topic to research ────────────────────────────────────────────────────────
TOPIC = "Artificial Intelligence in Healthcare: Applications and Future Trends"

print("\n" + "=" * 60)
print("  MULTI-AGENT RESEARCH SYSTEM")
print("  Symbiosis Institute of Technology, Nagpur")
print("  Course: Agentic AI & Automation  |  CA-1")
print("=" * 60)
print(f"\n  Topic : {TOPIC}\n")

# ── Run all agents ───────────────────────────────────────────────────────────
result = orchestrator(TOPIC)

# ── Save full markdown report ────────────────────────────────────────────────
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
md_file   = f"report_{timestamp}.md"

md_content = f"""# 📋 Multi-Agent Research Report

**Topic:** {result['topic']}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Course:** Agentic AI & Automation — CA-1

---

## 🔍 Step 1 — Search Agent (Tavily Results)

{result['search_results']}

---

## 📝 Step 2 — Planner Agent Output

{result['plan']}

---

## 📊 Step 3 — Fundamentals Analyst Agent Output

{result['analysis']}

---

## ✍️ Step 4 — Writer Agent Output (Final Article)

{result['article']}
"""

with open(md_file, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"\n{'=' * 60}")
print(f"  Done! Full report saved to : {md_file}")
print(f"  Console output saved to   : output.py")
print("=" * 60)

# ── Restore stdout and capture everything that was printed ───────────────────
sys.stdout = tee._stdout
captured_output = tee.getvalue()

# ── Save captured console output to output.py ────────────────────────────────
output_py_content = f'''\
"""
output.py
---------
Exact console output produced by running main.py
Topic   : {TOPIC}
Run at  : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

OUTPUT = """
{captured_output}
"""

if __name__ == "__main__":
    print(OUTPUT)
'''

with open("output.py", "w", encoding="utf-8") as f:
    f.write(output_py_content)

print("All files saved successfully.")

