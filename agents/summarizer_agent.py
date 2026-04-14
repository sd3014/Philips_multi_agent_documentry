from utils.ollama_client import ask_ollama


def summarize_text(content):
    prompt = f"Summarize this document:\n{content[:3000]}"
    return ask_ollama(prompt)