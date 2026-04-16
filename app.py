import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from io import StringIO

from agents.planner_agent import plan_workflow
from agents.summarizer_agent import summarize_text
from agents.insight_agent import needs_graph
from utils.ollama_client import ask_ollama
from utils.column_matcher import get_best_matching_column


# ---------------- FILE CONTENT EXTRACTION ----------------
def extract_content(uploaded_file):
    import csv
    import pandas as pd
    from PyPDF2 import PdfReader
    from io import StringIO

    file_name = uploaded_file.name.lower()
    df = None
    content = ""
    file_type = "unknown"

    if file_name.endswith(".pdf"):
        file_type = "pdf"
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            txt = page.extract_text()
            if txt:
                content += txt + "\n"

    elif file_name.endswith(".txt"):
        file_type = "txt"
        content = StringIO(
            uploaded_file.getvalue().decode("utf-8")
        ).read()

    elif file_name.endswith(".csv"):
        file_type = "csv"

        uploaded_file.seek(0)
        sample = uploaded_file.read(2048).decode("utf-8")
        uploaded_file.seek(0)

        try:
            delimiter = csv.Sniffer().sniff(sample).delimiter
        except Exception:
            delimiter = ","

        df = pd.read_csv(
            uploaded_file,
            sep=delimiter,
            engine="python",
            on_bad_lines="skip"
        )

        content = df.to_string()

    elif file_name.endswith(".xlsx"):
        file_type = "excel"
        df = pd.read_excel(uploaded_file)
        content = df.to_string()

    # IMPORTANT: always return
    return content, df, file_type

# ---------------- QUESTION GENERATION ----------------
def generate_possible_questions(content):
    prompt = f"""
Generate all meaningful questions a user may ask from this file.
Return as bullet points.

Content:
{content[:4000]}
"""
    return ask_ollama(prompt)


# ---------------- ANSWER GENERATION ----------------
def answer_question(content, question):
    prompt = f"""
Answer the following question strictly from the given file content.

Content:
{content[:5000]}

Question:
{question}

Give a clear detailed answer.
"""
    return ask_ollama(prompt)


# ---------------- STREAMLIT UI ----------------
st.set_page_config(
    page_title="Intelligent Document Workflow Agent",
    layout="wide"
)

st.title("📄 Intelligent Document Workflow Agent")
st.subheader("Use Case 3: Dynamic Multi-Agent Workflow using Ollama")

feature = st.selectbox(
    "Choose an option",
    [
        "Workflow Summary",
        "Generate Possible Questions",
        "Ask Your Own Question",
        "Insights & Graph"
    ]
)

uploaded_file = st.file_uploader(
    "Upload File",
    type=["pdf", "txt", "csv", "xlsx"]
)

# ---------------- MAIN FLOW ----------------
if uploaded_file:
    content, df, file_type = extract_content(uploaded_file)

    # ---------------- SUMMARY ----------------
    if feature == "Workflow Summary":
        st.write("## 🤖 Planned Workflow")
        st.info(plan_workflow(content))

        st.write("## 📄 Detailed Summary")
        st.write(summarize_text(content, file_type))

    # ---------------- POSSIBLE QUESTIONS ----------------
    elif feature == "Generate Possible Questions":
        st.write("## ❓ Suggested Questions")
        questions = generate_possible_questions(content)
        st.write(questions)

        selected_q = st.text_input("Enter one question from above")

        if st.button("➡ Get Answer"):
            if selected_q.strip():
                ans = answer_question(content, selected_q)

                st.write("## 💡 Answer")
                st.success(ans)
            else:
                st.warning("Please enter a question first.")

    # ---------------- CUSTOM QUESTION ----------------
    elif feature == "Ask Your Own Question":
        user_q = st.text_input("Ask anything from the file")

        if st.button("➡ Answer My Question"):
            if user_q.strip():
                ans = answer_question(content, user_q)

                st.write("## 💡 Answer")
                st.success(ans)
            else:
                st.warning("Please enter a question first.")

    # ---------------- GRAPH ----------------
    elif feature == "Insights & Graph":
        st.write("## 📊 Survey Insight & Auto Graph")

        if df is not None:
            user_question = st.text_input(
                "Ask a question from the uploaded survey / dataset"
            )

            if st.button("📈 Generate Insight Graph"):
                if user_question.strip():

                    # match question to column
                    matched_col, score = get_best_matching_column(
                        user_question,
                        df.columns
                    )

                    st.write(f"### 🎯 Matched Topic: {matched_col}")
                    st.write(f"Similarity Score: {round(score, 2)}")

                    responses = df[matched_col].dropna().astype(str).str.strip()
                    value_counts = responses.value_counts()

                    if value_counts.empty:
                        st.warning("No valid responses found.")

                    else:
                        fig, ax = plt.subplots(figsize=(8, 5))

                        if len(value_counts) <= 6:
                            ax.pie(
                                value_counts,
                                labels=value_counts.index,
                                autopct="%1.1f%%"
                            )
                            ax.set_title(f"Response distribution for {matched_col}")
                            chart_used = "Pie Chart"

                        else:
                            value_counts.head(10).plot(
                                kind="bar",
                                ax=ax
                            )
                            ax.set_title(f"Top responses for {matched_col}")
                            chart_used = "Bar Chart"

                        st.pyplot(fig)

                        # ---------------- INSIGHT ANSWER BELOW GRAPH ----------------
                        top_response = value_counts.idxmax()
                        top_count = value_counts.max()
                        total = value_counts.sum()
                        percentage = round((top_count / total) * 100, 2)

                        st.write("## 💡 Insight Explanation")
                        st.success(
                            f"""
            The **{chart_used}** represents responses for **{matched_col}**.

            The most frequent response is **'{top_response}'**
            with **{top_count} responses**, contributing approximately
            **{percentage}%** of total responses.

            This indicates that **{top_response}** is the dominant trend
            observed in the uploaded survey / dataset.

            Total responses analyzed: **{total}**
            """
                        )

                        # optional detailed breakdown
                        st.write("## 📝 Top Response Breakdown")
                        for val, count in value_counts.head(5).items():
                            pct = round((count / total) * 100, 2)
                            st.write(f"- {val}: {count} responses ({pct}%)")

                else:
                    st.warning("Please enter a question first.")