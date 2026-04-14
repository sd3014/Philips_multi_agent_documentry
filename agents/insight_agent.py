from utils.ollama_client import ask_ollama


def needs_graph(content):
    prompt = f"""
    Check whether this document contains numerical or tabular insights
    that require graph generation.
    Answer only YES or NO.

    {content[:2000]}
    """

    return ask_ollama(prompt)