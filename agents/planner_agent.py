from utils.ollama_client import ask_ollama


def plan_workflow(file_content):
    prompt = f"""
You are a MASTER PLANNER AGENT in a multi-agent document workflow system.

Analyze the uploaded file completely.

Your responsibility is to intelligently analyze the uploaded document
and decide the BEST execution workflow in a NON-HARDCODED manner.

AVAILABLE AGENTS:
1. File Identification Agent
2. Content Extraction Agent
3. Form Detection Agent
4. Summary Agent
5. Question Extraction Agent
6. Answer Generation Agent
7. Insight / Graph Agent
8. Image / Visual Support Agent
9. Final Response Agent

YOUR TASK:
Read the document content carefully and decide:

A. Document Understanding
- Identify probable file/document type
- Detect whether it is a form, questionnaire, report, dataset, invoice, or general text
- Detect whether it contains structured tabular data
- Detect whether images/visual references may be useful

B. Task Routing
Choose which agents should be executed and in what sequence.

C. Special Conditions
- If numerical values, repeated rows, trends, percentages, time-series values,
  or tabular records exist → include Insight / Graph Agent
- If explicit questions, numbered items, form fields, labels, or FAQs exist
  → include Question Extraction Agent
- If the content topic can benefit from supporting visuals
  → include Image / Visual Support Agent
- If the user is likely to ask follow-up questions
  → include Answer Generation Agent

D. Output Format (STRICT)
Return ONLY in the following structured format:

DOCUMENT_TYPE: ...
FORM_DETECTED: YES / NO
SUMMARY_REQUIRED: YES / NO
QUESTION_EXTRACTION_REQUIRED: YES / NO
GRAPH_REQUIRED: YES / NO
IMAGE_SUPPORT_REQUIRED: YES / NO
WORKFLOW_PATH:
- Step 1: ...
- Step 2: ...
- Step 3: ...

Document Content:
{file_content[:4000]}
"""

    return ask_ollama(prompt)