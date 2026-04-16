from utils.ollama_client import ask_ollama


def needs_graph(content):
    prompt = f"""
You are an intelligent survey insight and visualization recommendation agent.

Analyze the uploaded file content thoroughly and provide a COMPLETE insight response.

Your tasks:
1. Determine whether graph-based insights are possible
2. Identify the most suitable survey questions / columns for visualization
3. Recommend the best chart type
4. Briefly explain why the chart is suitable
5. Mention any trends or patterns observed

Guidelines:
- Use PIE chart for few categorical responses
- Use BAR chart for multiple unique categorical values
- Use LINE chart for time-based trends or dates
- Use HISTOGRAM for numeric distribution if applicable

IMPORTANT:
- do not copy exact text from the uploaded file
- generate smart analytical topics
- complete all sections fully
- do not stop mid-sentence
- end with a final recommendation

Return exactly in this format:

GRAPH_REQUIRED: YES / NO

RECOMMENDED_TOPICS:
- topic 1
- topic 2
- topic 3

SUGGESTED_CHART:
- chart type

REASON:
- clear explanation

PATTERN_OBSERVED:
- key trend / observation

FINAL_RECOMMENDATION:
- best topic to visualize first

Content:
{content[:5000]}
"""
    return ask_ollama(prompt)