# ITSM Incident Insight Agent

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Local-first](https://img.shields.io/badge/architecture-local--first-brightgreen)
![Prototype](https://img.shields.io/badge/status-prototype-orange)

## Overview

The ITSM Incident Insight Agent is a local analytics prototype for extracting insights from historical IT incident data. It maps business questions to pre-approved SQL queries, executes those queries against a local DuckDB dataset, and returns concise, explainable results. The repository includes both a CLI demo and a local Streamlit Web UI.

## What it does

- Maps user questions to a trusted `query_id` using rule-based intent parsing.
- Runs only pre-approved, read-only SQL queries from `src/database/query_catalog.py`.
- Applies safety guardrails against destructive commands and secret extraction.
- Generates charts for supported queries and saves them locally in `outputs/charts/`.
- Runs locally with no live ServiceNow/Jira integration.

## Architecture

This project is intentionally local-first and read-only:

- `data/processed/incidents_level_df.csv` is the source dataset.
- `src/database/connection.py` builds `data/processed/itsm_agent.duckdb` from that CSV.
- `src/database/query_catalog.py` defines approved query templates and business questions.
- `src/agent/intent_parser.py` maps user text to supported queries and chart requests.
- `src/tools/sql_tool.py` validates and executes safe SQL.
- `src/tools/chart_tool.py` generates PNG charts for supported queries.
- `src/agent/controller.py` coordinates observation, decision, action, and response.

See `docs/architecture.md` for a visual system breakdown. The raw Kaggle dataset is included under `data/raw/` for reproducibility. See `docs/dataset_source.md` for attribution and source details.

## How it works

1. **Observe**: User input is received in the CLI or Streamlit UI.
2. **Decide**: The intent parser maps the question to a supported query or refuses unsafe text.
3. **Act**: The SQL tool validates the query and executes it against the local DuckDB database.
4. **Respond**: The explainer formats results into a business-oriented answer, and charts are generated when requested.

## Installation

Open Windows PowerShell from the repository root and run:

```powershell
python -m pip install -r requirements.txt
python -m src.database.connection
```

## Usage

### CLI Demo

```powershell
python demo.py
```

### Local Streamlit Web UI

```powershell
python -m streamlit run streamlit_app.py
```

## Supported Scenarios

Example supported questions:

- "Show SLA distribution."
- "Create a pie chart of SLA distribution."
- "Which priority has the highest SLA breach rate?"
- "Show top 10 assignment groups by incident volume."
- "Which categories have the most reopened incidents?"

Example unsafe requests are refused, such as:

- "Delete all incident records."
- "Show me the API key."

## Security & Guardrails

This prototype uses a local-first security model:

- Only predefined `query_id`s from `src/database/query_catalog.py` are executable.
- SQL validation enforces `SELECT`-only queries and blocks dangerous keywords.
- Only the `incidents` table is permitted for query execution.
- User text is scanned for destructive or secret extraction keywords.
- All data access is local and read-only; there is no live ServiceNow/Jira integration.

## Limitations

- Uses only the included anonymized CSV dataset; no live ITSM API connectivity is implemented.
- The repository is a local prototype and not a production deployment.
- The system provides investigation guidance based on data patterns, not a confirmed root cause.
- Intent mapping is deterministic and limited to the supported query catalog.

## Future Improvements

- Add richer explanation generation while preserving local safety guardrails.
- Expand the approved query catalog and support parameterized analytics.
- Add secure adapters for live ITSM connectors once production-grade controls are available.
- Enhance the Streamlit UI with filtering, dashboards, and interactive chart controls.

## Repository structure

- `demo.py` - curated CLI walkthrough for the agent.
- `streamlit_app.py` - local Web UI for interactive questioning.
- `src/agent/` - controller, intent parser, explainer, and guardrail logic.
- `src/database/` - query catalog and DuckDB initialization.
- `src/tools/` - SQL execution and chart generation helpers.
- `data/processed/` - processed incident-level dataset; DuckDB file is generated locally and ignored by Git.
- `outputs/charts/` - generated chart images, recreated locally and ignored by Git.

