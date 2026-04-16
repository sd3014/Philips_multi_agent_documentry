from utils.ollama_client import ask_ollama


def explain_visual(context):
    prompt = f"""
You are a visual explanation agent.

Explain any figures, charts, tables, or images
present in the uploaded document.

Provide:
- what the visual represents
- trend / meaning
- business insight

Context:
{context[:3000]}
"""
    return ask_ollama(prompt)