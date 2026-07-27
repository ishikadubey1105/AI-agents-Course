"""
convert_to_pdf.py
-----------------
Converts answer_sheet.md → answer_sheet.html (print-ready, full formatting)
Open the HTML in Chrome, then Ctrl+P → Save as PDF
"""

import re
from pathlib import Path

MD_FILE   = Path(__file__).parent / "answer_sheet.md"
HTML_FILE = Path(__file__).parent / "answer_sheet.html"



# ── Read markdown ────────────────────────────────────────────────────────────
md = MD_FILE.read_text(encoding="utf-8")


# ── Simple Markdown → HTML converter ────────────────────────────────────────
def md_to_html(text):
    lines = text.split("\n")
    html  = []
    in_code  = False
    in_table = False
    in_ul    = False
    code_buf = []
    code_lang= ""

    i = 0
    while i < len(lines):
        line = lines[i]

        # ── Fenced code blocks ────────────────────────────────────────────
        if line.startswith("```"):
            if not in_code:
                in_code   = True
                code_lang = line[3:].strip()
                code_buf  = []
            else:
                in_code = False
                code_content = "\n".join(code_buf)
                code_content = code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                label = f'<span class="lang-label">{code_lang}</span>' if code_lang else ""
                html.append(f'<div class="code-block">{label}<pre><code>{code_content}</code></pre></div>')
                code_buf  = []
                code_lang = ""
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # ── Horizontal rule ───────────────────────────────────────────────
        if re.match(r"^-{3,}$", line.strip()):
            if in_ul:
                html.append("</ul>")
                in_ul = False
            if in_table:
                html.append("</tbody></table>")
                in_table = False
            html.append("<hr>")
            i += 1
            continue

        # ── Tables ────────────────────────────────────────────────────────
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                in_table = True
                # header row
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                html.append('<table><thead><tr>')
                for c in cells:
                    html.append(f'<th>{inline(c)}</th>')
                html.append('</tr></thead><tbody>')
                i += 1
                # skip separator row
                if i < len(lines) and re.match(r"[\|\-\s:]+", lines[i]):
                    i += 1
                continue
            else:
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                html.append('<tr>')
                for c in cells:
                    html.append(f'<td>{inline(c)}</td>')
                html.append('</tr>')
                i += 1
                continue
        else:
            if in_table:
                html.append("</tbody></table>")
                in_table = False

        # ── Headings ──────────────────────────────────────────────────────
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            if in_ul: html.append("</ul>"); in_ul = False
            level = len(m.group(1))
            html.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # ── Unordered list ────────────────────────────────────────────────
        m = re.match(r"^[-*]\s+(.*)", line)
        if m:
            if not in_ul:
                in_ul = True
                html.append("<ul>")
            html.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue
        else:
            if in_ul:
                html.append("</ul>")
                in_ul = False

        # ── Blank line ────────────────────────────────────────────────────
        if line.strip() == "":
            html.append("")
            i += 1
            continue

        # ── Normal paragraph ──────────────────────────────────────────────
        html.append(f"<p>{inline(line)}</p>")
        i += 1

    if in_ul:    html.append("</ul>")
    if in_table: html.append("</tbody></table>")
    return "\n".join(html)


def inline(text):
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    # Bold + italic
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*(.*?)\*\*",     r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.*?)\*",         r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`",         r"<code>\1</code>", text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# ── Build HTML ───────────────────────────────────────────────────────────────
body = md_to_html(md)

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CA-1 Answer Sheet — Agentic AI & Automation</title>
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

  /* ── Reset & Base ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a2e;
    background: #fff;
    padding: 0;
  }}

  /* ── Page Layout ── */
  .page {{
    max-width: 210mm;
    margin: 0 auto;
    padding: 18mm 20mm 18mm 20mm;
  }}

  /* ── Header Banner ── */
  .header-banner {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    color: white;
    padding: 18px 24px;
    border-radius: 8px;
    margin-bottom: 24px;
    text-align: center;
  }}
  .header-banner h1 {{
    font-size: 16pt;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: white;
    border: none;
    padding: 0;
    margin: 0 0 4px 0;
  }}
  .header-banner p {{
    font-size: 9.5pt;
    opacity: 0.85;
    margin: 2px 0;
    color: #d0d0e8;
  }}

  /* ── Question Box ── */
  .question-box {{
    border-left: 4px solid #0f3460;
    background: #f0f4ff;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    margin-bottom: 28px;
    font-weight: 600;
    font-size: 10.5pt;
    color: #0f3460;
  }}

  /* ── Headings ── */
  h1 {{ display: none; }}   /* handled by banner */

  h2 {{
    font-size: 13pt;
    font-weight: 700;
    color: #0f3460;
    border-bottom: 2.5px solid #0f3460;
    padding-bottom: 5px;
    margin: 28px 0 14px 0;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 11pt;
    font-weight: 600;
    color: #16213e;
    margin: 18px 0 8px 0;
    page-break-after: avoid;
  }}

  h4 {{
    font-size: 10.5pt;
    font-weight: 600;
    color: #444;
    margin: 14px 0 6px 0;
  }}

  /* ── Paragraphs ── */
  p {{
    margin: 8px 0;
    text-align: justify;
  }}

  /* ── Lists ── */
  ul {{
    margin: 8px 0 8px 24px;
    padding: 0;
  }}
  li {{
    margin: 4px 0;
    padding-left: 4px;
  }}
  li::marker {{
    color: #0f3460;
    font-weight: 600;
  }}

  /* ── Tables ── */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 10pt;
    page-break-inside: avoid;
  }}
  thead {{
    background: #0f3460;
    color: white;
  }}
  th {{
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 9.5pt;
    letter-spacing: 0.3px;
  }}
  td {{
    padding: 8px 12px;
    border-bottom: 1px solid #e0e6f0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background: #f5f8ff;
  }}
  tr:hover td {{
    background: #eef2ff;
  }}

  /* ── Code blocks ── */
  .code-block {{
    position: relative;
    background: #0d1117;
    border-radius: 8px;
    margin: 14px 0;
    page-break-inside: avoid;
    overflow: hidden;
    border: 1px solid #30363d;
  }}
  .lang-label {{
    display: block;
    background: #161b22;
    color: #7d8590;
    font-family: 'Fira Code', monospace;
    font-size: 8pt;
    padding: 4px 14px;
    border-bottom: 1px solid #30363d;
    letter-spacing: 0.5px;
  }}
  pre {{
    margin: 0;
    padding: 14px 16px;
    overflow-x: auto;
  }}
  code {{
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 8.5pt;
    color: #e6edf3;
    line-height: 1.6;
  }}
  p code, li code, td code {{
    background: #f0f0f0;
    color: #c7254e;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 8.5pt;
  }}

  /* ── Horizontal Rule ── */
  hr {{
    border: none;
    border-top: 1.5px solid #e0e6f0;
    margin: 24px 0;
  }}

  /* ── Inline styles ── */
  strong {{ font-weight: 700; color: #111; }}
  em     {{ font-style: italic; color: #333; }}
  a      {{ color: #0f3460; text-decoration: none; }}

  /* ── Section label pills ── */
  h2::before {{
    content: '';
  }}

  /* ── Footer ── */
  .footer {{
    margin-top: 32px;
    text-align: center;
    font-size: 8.5pt;
    color: #888;
    border-top: 1px solid #e0e6f0;
    padding-top: 12px;
  }}

  /* ── Print Settings ── */
  @media print {{
    body {{ background: white; }}
    .page {{ padding: 10mm 14mm; max-width: 100%; }}
    .code-block {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    thead {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .header-banner {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    h2, h3 {{ page-break-after: avoid; }}
    pre, table, .code-block {{ page-break-inside: avoid; }}
    @page {{
      size: A4;
      margin: 15mm 15mm 15mm 15mm;
    }}
  }}
</style>
</head>
<body>
<div class="page">

  <!-- Header -->
  <div class="header-banner">
    <h1>CA-1 Answer Sheet</h1>
    <p>Symbiosis Institute of Technology, Nagpur</p>
    <p>Agentic AI &amp; Automation (0705210501) &nbsp;|&nbsp; B.Tech CSE &nbsp;|&nbsp; Semester V &nbsp;|&nbsp; Marks: 10</p>
    <p>Session: 2026-27 (ODD) &nbsp;|&nbsp; Batch: 2024-28</p>
  </div>

  <!-- Question -->
  <div class="question-box">
    Q.1 &mdash; Develop a library of specialist agents (Planner, Writer, Fundamentals Analyst, Search Agent)
    and coordinate their interactions. Use Tavily tool in Search Agent. &nbsp;<strong>[10 Marks]</strong>
  </div>

  <!-- Body -->
  {body}

  <!-- Footer -->
  <div class="footer">
    SIT Nagpur &nbsp;|&nbsp; Agentic AI &amp; Automation &nbsp;|&nbsp; CA-1 &nbsp;|&nbsp; 2026-27
  </div>

</div>
</body>
</html>"""

HTML_FILE.write_text(html_doc, encoding="utf-8")
print(f"[OK] HTML saved to: {HTML_FILE}")
print()
print("HOW TO GET PDF:")
print("  1. Open the file in Chrome  (double-click it)")
print("  2. Press  Ctrl + P")
print("  3. Destination -> 'Save as PDF'")
print("  4. Layout -> Portrait  |  Margins -> Minimum  |  [x] Background graphics")
print("  5. Click Save")

