from utils.ollama_client import ask_ollama


def needs_graph(content):
    prompt = f"""
You are an intelligent survey insight agent.

Analyze the uploaded file content and determine:

1. Whether survey-style graph insights are possible
2. Which columns / questions seem most suitable for visualization
3. What chart type is recommended

Guidelines:
- use PIE chart if responses are few categories
- use BAR chart for many unique responses
- use LINE chart for trends / dates

Return in this format:

GRAPH_REQUIRED: YES / NO
RECOMMENDED_TOPICS:
- topic 1
- topic 2
SUGGESTED_CHART:
- chart type
REASON:
- why

Content:
{content[:5000]}
"""
    return ask_ollama(prompt)