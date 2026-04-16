from utils.ollama_client import ask_ollama


def extract_questions(data, file_type):
    # ---------- CSV / EXCEL ----------
    if file_type in ["csv", "excel"]:
        df = data
        questions = []

        for col in df.columns:
            col_name = str(col)

            questions.extend([
                f"What is the most common response in '{col_name}'?",
                f"Which category has the highest frequency in '{col_name}'?",
                f"What trends are visible in '{col_name}'?",
                f"Are there any unusual patterns in '{col_name}'?"
            ])

        unique_questions = list(dict.fromkeys(questions))

        return "\n".join(
            f"- {q}" for q in unique_questions[:8]
        )

    # ---------- OTHER FILES ----------
    else:
        content = data

        prompt = f"""
You are an intelligent document question generation agent.

Generate 6–8 NEW analytical user-friendly questions
based on the uploaded document.

IMPORTANT:
- do not copy exact headings
- generate insight-driven questions
- questions should help understand key sections,
  trends, arguments, and important findings
- keep them short and meaningful

Examples:
- What are the key findings in this document?
- Which section contains the most critical information?
- What trends or insights are highlighted?

Document Content:
{content[:2000]}
"""

        return ask_ollama(prompt)