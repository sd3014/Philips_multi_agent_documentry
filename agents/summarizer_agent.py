from utils.ollama_client import ask_ollama


def summarize_text(content, file_type="document"):
    prompt = f"""
You are an ADVANCED UNIVERSAL DOCUMENT INTELLIGENCE AGENT.

Provide a COMPLETE structured summary.

Your task is to generate a DETAILED, PROFESSIONAL, LONG-FORM
SUMMARY for ANY uploaded file type.

SUPPORTED TYPES:
- text document
- spreadsheet
- tabular data
- research article
- report
- business file
- survey / form
- invoice
- presentation content
- any general uploaded file

IMPORTANT REQUIREMENTS:
1. Understand the file type and purpose
2. Explain every major section / field clearly
3. Preserve numerical values and factual details
4. Mention trends, tables, percentages, metrics, dates
5. Mention whether visual insights / graphs are possible
6. Mention extracted images / diagrams if available
7. Keep it long, structured, and presentation-ready

STRICT OUTPUT FORMAT:

1. FILE OVERVIEW
2. SECTION-WISE EXPLANATION
3. NUMERICAL / FACTUAL INSIGHTS
4. VISUAL / GRAPHICAL INSIGHTS
5. KEY TAKEAWAYS
6. DETAILED FINAL EXPLANATION

File Type: {file_type}

Content:
{content[:8000]}
"""

    return ask_ollama(prompt)