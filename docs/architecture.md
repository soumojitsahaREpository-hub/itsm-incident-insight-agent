# Agent Architecture

The ITSM Incident Insight Agent follows a strict, modular "Observe -> Decide -> Act -> Respond" pipeline to ensure accuracy and safety.

## Text Architecture Diagram

```text
[User]
   |
   v
[Streamlit Web UI or CLI Demo]
   |
   v
[Agent Controller]
   |
   v
[Intent Parser]
   |
   v
[Guardrails]
   |
   v
[SQL Tool] ---> [Query Catalog]
   |
   v
[DuckDB incidents table]
   |
   v
[Chart Tool if requested]
   |
   v
[Explainer]
   |
   v
[Final Answer + Optional Chart]
```

## Component Breakdown
1. **CSV & DuckDB:** `data/processed/incidents_level_df.csv` is loaded into a fast, local embedded DuckDB instance (`src/database/connection.py`).
2. **Query Catalog (`src/database/query_catalog.py`):** The single source of truth for all permitted SQL. The agent cannot hallucinate queries; it must select from this menu.
3. **Guardrails (`src/agent/guardrails.py`):** The security bouncer. Analyzes user intent and SQL strings to block injection attacks or destructive commands before they execute.
4. **Intent Parser (`src/agent/intent_parser.py`):** A rule-based engine that maps conversational requests (e.g., "SLA graph") to structured intents (`query_id: sla_distribution`, `chart_type: pie`).
5. **SQL & Chart Tools (`src/tools/`):** Dedicated Python execution tools that safely retrieve data and draw deterministic visuals.
6. **Controller (`src/agent/controller.py`):** The orchestrator that chains all these components together into the core agent loop.
7. **Explainer (`src/agent/explainer.py`):** The final layer that wraps the data in readable templates (with a built-in hook for future Gemini LLM integration).
8. **Agent Skill (`SKILL.md`):** A configuration file providing Antigravity and ADK-style agents with instructions on how to leverage the above architecture safely.
