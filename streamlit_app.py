import streamlit as st
import os
import json
from src.agent.controller import run_agent

# Set page config
st.set_page_config(
    page_title="ITSM Incident Insight Agent",
    page_icon="🔍",
    layout="wide"
)

# Title and Description
st.title("ITSM Incident Insight Agent")
st.markdown("Ask safe business questions about incident data. The agent securely maps your request to predefined SQL queries.")

# Sidebar with examples
st.sidebar.header("Try these examples:")
example_questions = [
    "Show SLA distribution.",
    "Create a pie chart of SLA distribution.",
    "Which priority has the highest SLA breach rate?",
    "Show top 10 assignment groups by incident volume.",
    "Which categories have the most reopened incidents?",
    "Delete all incident records.",
    "Create a bar chart of priority distribution.",
    "Create a bar chart of top assignment groups by incident volume.",
    "Create a bar chart of SLA breach rate by priority."
]

# Use session state to manage input box from sidebar buttons
if "user_question" not in st.session_state:
    st.session_state.user_question = ""

def set_question(q):
    st.session_state.user_question = q

for q in example_questions:
    st.sidebar.button(q, on_click=set_question, args=(q,))



# Check database existence
db_path = "data/processed/itsm_agent.duckdb"
if not os.path.exists(db_path):
    st.error(f"Database not found at `{db_path}`. Please run: `python -m src.database.connection`")
    st.stop()

# Input area
user_question = st.text_input("Enter your question:", key="user_question")

if st.button("Run Agent", type="primary") and user_question:
    with st.spinner("Agent is observing, deciding, acting..."):
        result = run_agent(user_question)
        
        status = result.get("status", "unknown")
        final_answer = result.get("final_answer", "")
        intent = result.get("intent", {})
        query_id = intent.get("query_id")
        safety_notes = result.get("safety_notes", "")
        chart_result = result.get("chart_result")
        
        st.divider()
        
        # Display Agent Response
        st.subheader("Agent Response")
        if status == "refused":
            st.error(final_answer)
        elif status == "error":
            st.warning(final_answer)
        else:
            st.success(final_answer)
            
        # Display Chart if generated
        if chart_result and chart_result.get("status") == "success":
            chart_path = chart_result.get("chart_path")
            if os.path.exists(chart_path):
                st.image(chart_path, caption=f"Generated Chart: {query_id}")
            else:
                st.warning(f"Chart generated but file not found at {chart_path}")
                
        # Display Metadata
        st.subheader("Metadata & Safety")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", status.upper())
            st.metric("Mapped Intent (Query ID)", query_id if query_id else "None")
        with col2:
            if safety_notes:
                st.info(f"System Note: {safety_notes}")
            else:
                st.info("System Note: Request passed all guardrails cleanly.")
                
        # Expandable Debug Area
        with st.expander("View Raw Agent JSON Data (Debug)"):
            st.json(result)
