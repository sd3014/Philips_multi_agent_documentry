from utils.ollama_client import ask_ollama


def extract_questions(content):
    prompt = f"""
    Extract all questions from this document.
    Return as bullet points.

    {content[:3000]}
    """

    return ask_ollama(prompt)