import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from io import StringIO

from agents.planner_agent import plan_workflow
from agents.summarizer_agent import summarize_text
from agents.question_extractor import extract_questions
from agents.insight_agent import needs_graph


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Intelligent Document Workflow Agent",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>📄 Intelligent Document Workflow Agent</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h4 style='text-align:center;'>Use Case 3: Dynamic Multi-Agent Workflow using Ollama</h4>",
    unsafe_allow_html=True
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload PDF / TXT / CSV / Excel",
    type=["pdf", "txt", "csv", "xlsx"]
)

# ---------------- FILE PROCESSING ----------------
if uploaded_file:
    file_name = uploaded_file.name.lower()
    content = ""
    df = None

    # -------- PDF --------
    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                content += page_text + "\n"

    # -------- TXT --------
    elif file_name.endswith(".txt"):
        content = StringIO(
            uploaded_file.getvalue().decode("utf-8")
        ).read()

    # -------- CSV --------
    elif file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        content = df.to_string()

    # -------- EXCEL --------
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        content = df.to_string()

    # ---------------- LAYOUT ----------------
    col1, col2 = st.columns([1, 2])

    # ---------------- LEFT SIDE PIPELINE ----------------
    with col1:
        st.markdown("## ⚙ Workflow Pipeline")

        steps = [
            "Identify File Type",
            "Extract Content",
            "Detect Form",
            "Summarize",
            "Extract Questions",
            "Generate Response",
            "Generate Graph (if needed)"
        ]

        for step in steps:
            st.success(f"✔ {step}")

    # ---------------- RIGHT SIDE OUTPUT ----------------
    with col2:
        st.markdown("## 📌 Output")

        # -------- PLANNER AGENT --------
        workflow = plan_workflow(content)

        st.markdown("### 🤖 Planned Workflow")
        st.info(workflow)

        # -------- SUMMARY --------
        summary = summarize_text(content)

        st.markdown("### 📄 Summary")
        st.write(summary)

        # -------- QUESTION EXTRACTION --------
        questions = extract_questions(content)

        st.markdown("### ❓ Extracted Questions")
        st.write(questions)

        # -------- GRAPH DECISION --------
        graph_needed = needs_graph(content)

        st.markdown("### 📊 Graph Decision")
        st.write(graph_needed)

        # -------- AUTO GRAPH GENERATION --------
        if df is not None:
            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:
                st.markdown("### 📈 Auto Generated Insight Graph")

                selected_col = numeric_cols[0]

                fig, ax = plt.subplots()
                df[selected_col].plot(kind="hist", ax=ax)
                ax.set_title(f"Distribution of {selected_col}")

                st.pyplot(fig)

        elif "yes" in graph_needed.lower():
            st.markdown("### 📈 Suggested Insight")
            st.write("Graph insights recommended based on document content.")