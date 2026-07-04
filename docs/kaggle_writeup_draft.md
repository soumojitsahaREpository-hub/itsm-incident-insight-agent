# ITSM Incident Insight Agent: Kaggle Writeup Draft

## 1. Project Overview
The ITSM Incident Insight Agent is a local, AI-driven analytics assistant designed to answer business questions about IT incidents. By bridging the gap between natural language requests and structured data queries, this project empowers business leaders to extract operational insights without writing SQL or depending on complex BI dashboards.

## 2. Problem Statement
IT Service Management (ITSM) platforms like ServiceNow and Jira generate massive volumes of incident data. Analyzing this data to identify SLA bottlenecks, overburdened assignment groups, or recurring categories is difficult for non-technical users. Conversely, allowing an AI agent to freely write SQL against enterprise databases introduces significant security risks, including prompt injection and destructive commands. This project solves that by enforcing strict, tool-based guardrails and a predefined query catalog.

## 3. Dataset and Preprocessing
The agent operates on an anonymized ITSM incident dataset provided as a local CSV file (`incidents_level_df.csv`). This dataset includes historical records detailing incident priority, SLA compliance status, assignment group, category, and timestamps. Prior to building the agent, the data was thoroughly cleaned and standardized in a series of Jupyter notebooks, ensuring the agent interacts with highly structured, reliable data.

## 4. Agent Architecture
The system employs a strict "Observe -> Decide -> Act -> Respond" loop orchestrated by a custom Python controller:
- **Intent Parser:** Maps natural language to a secure `query_id`.
- **Guardrails Layer:** Validates SQL logic and blocks destructive intents.
- **SQL Tool:** Executes read-only queries against a local DuckDB engine.
- **Chart Tool:** Generates deterministic data visualizations via Matplotlib.
- **Explainer Layer:** Translates raw database rows into plain-English business guidance.
- **Local Web UI:** A local Streamlit interface that lets users type business questions, view explanations, inspect mapped query IDs, and see generated charts. This is not deployed to production and does not accept arbitrary SQL or require an LLM.

## 5. Course/Capstone Concepts Demonstrated
- **Antigravity-Assisted Workflow:** The entire architecture was developed iteratively using Google Antigravity as an AI-assisted development environment, adhering strictly to best practices and safety-first design.
- **Local Tool-Based Agent/Controller:** The architecture demonstrates how specialized Python functions act as independent "tools" called by a central controller logic.
- **Agent Skill (`SKILL.md`):** Features a custom instruction file that dictates the agent's behavior, tool usage, and tone.
- **Structured Query Catalog:** Proves how confining an AI to a predefined menu of queries reduces hallucinated metrics by forcing the agent to use approved SQL only.
- **Deterministic Chart Generation:** Showcases that Charts are generated deterministically from SQL results, keeping visualizations grounded in the actual data.

## 6. Safety and Guardrails
Security is the cornerstone of this project. The system does not allow raw user SQL execution. Instead, the `guardrails.py` layer actively scans both the user's plain text and the underlying SQL template for malicious keywords (`DROP`, `DELETE`, `password`, `api key`). If an unauthorized table is accessed or a destructive command is detected, the agent instantly refuses the request before establishing a database connection.

## 7. Demo Examples
The MVP successfully processes various complex intents:
- **"Show SLA distribution."** -> Calculates met/breach percentages based on exact row counts.
- **"Create a pie chart of SLA distribution."** -> Successfully generates and saves a local PNG chart.
- **"Which categories have the most reopened incidents?"** -> Identifies high-risk categories requiring better initial triage.
- **"Delete all incident records."** -> Securely blocked with a status of REFUSED.

## 8. Results and Business Insights
The agent successfully acts as an interactive reporting layer. By analyzing the data, the agent can immediately provide *investigation guidance*—for example, pointing out that "Priority 1" incidents or a specific "Assignment Group" have the highest correlation with SLA breaches. While this doesn't definitively prove root cause, it provides IT managers with immediate, actionable areas to investigate.

## 9. Limitations
- **Local Data Only:** The agent currently analyzes a static, local CSV/DuckDB file, not a live production database.
- **Investigation Guidance vs. True RCA:** The system identifies operational patterns but cannot mathematically prove causal root cause.
- **Template Explanations:** To guarantee safety and eliminate API costs during the MVP phase, explanations are currently template-based rather than fully LLM-generated.

## 10. Future Improvements
- **LLM Explanation Integration:** Expanding the `explainer.py` layer to call Gemini for more nuanced, conversational responses (a toggle for this is already prepped in `.env`).
- **Model Context Protocol (MCP):** Exposing the SQL and Chart tools as an MCP server so they can be consumed by external, cross-platform agents.
- **Live API Integration:** Transitioning from DuckDB CSV reads to secure, live API fetching against a real ITSM instance.
