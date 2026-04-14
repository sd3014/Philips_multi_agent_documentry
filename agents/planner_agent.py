from utils.ollama_client import ask_ollama


def plan_workflow(file_content):
    prompt = f"""
    You are an intelligent planner agent.

    Analyze the uploaded document carefully.

    Based on the actual content decide dynamically:
    - file type
    - whether it is a questionnaire/form
    - whether summary is needed
    - whether questions should be extracted
    - whether graph insights are required

    IMPORTANT:
    If the document contains numbers, tables, trends, percentages, or repeated structured rows,
    graph generation should be YES.

    If the document contains questions, labels, numbered items, or form fields,
    question extraction should be YES.

    Document content:
    {file_content[:3000]}

    Give output in bullet points.
    """

    return ask_ollama(prompt)