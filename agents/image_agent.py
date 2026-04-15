from utils.ollama_client import ask_ollama


def detect_visual_need(content, question):
    prompt = f"""
    Check if this answer needs a visual aid or image reference.
    Return YES or NO.

    Document:\n{content[:3000]}

    Question: {question}
    """

    return ask_ollama(prompt)