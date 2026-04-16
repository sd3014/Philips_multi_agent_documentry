from utils.ollama_client import ask_ollama


def answer_from_document(content, question):
    prompt = f"""
    Answer the user question completely.
    Answer the question strictly from the document.
    If relevant, mention if graph or image support is useful.

    Document:\n{content[:3000]}

    Question: {question}
    """

    return ask_ollama(prompt)