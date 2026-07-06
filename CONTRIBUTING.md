# Contributing

Thank you for helping improve the ITSM Incident Insight Agent. This project is an open-source prototype for exploring incident data safely and locally, with a deterministic workflow that maps business questions to approved read-only queries.

## Project purpose

This repository demonstrates a local-first analytics workflow for historical IT incident data. It is intended to:

- help users ask safe business questions about incident trends,
- map those questions to pre-approved SQL queries,
- execute them locally against a DuckDB database,
- and return explainable results without requiring live ITSM integrations.

The project is a prototype and should be treated as a learning and demonstration tool rather than a production-grade incident management platform.

## Local setup

1. Clone the repository.
2. Create and activate a Python environment (Python 3.11+ is recommended).
3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Initialize the local database:

   ```powershell
   python -m src.database.connection
   ```

## Initialize the DuckDB database

The database is created locally from the processed CSV file at data/processed/incidents_level_df.csv. To build or refresh the DuckDB file:

```powershell
python -m src.database.connection
```

This creates or replaces the incidents table in data/processed/itsm_agent.duckdb.

## Run the CLI demo

To run the CLI demonstration:

```powershell
python demo.py
```

## Run the Streamlit UI

To launch the local web interface:

```powershell
python -m streamlit run streamlit_app.py
```

## Coding rules

- Keep changes focused, minimal, and easy to review.
- Favor clear, readable Python code and consistent naming.
- Preserve the local-first, read-only design of the project.
- Avoid introducing new dependencies unless they are clearly justified.
- Do not modify notebooks, data files, or README.md unless the change is explicitly requested and necessary.

## Safety rules

Contributors must preserve the safety model of this project:

- Do not add arbitrary SQL generation.
- Do not expose secrets or sensitive values.
- Do not claim confirmed root cause analysis (RCA) from the data.
- Keep all execution within the approved query catalog and read-only guardrails.
- Do not add any path that bypasses the existing safety checks.

## Pull request checklist

Before opening a pull request, please confirm:

- [ ] The change is aligned with the project purpose and local-first architecture.
- [ ] The relevant commands still work locally.
- [ ] The DuckDB initialization workflow still works.
- [ ] The CLI demo and Streamlit UI still run as expected.
- [ ] No secrets, credentials, or sensitive data are introduced.
- [ ] No unsupported SQL generation or unsafe behavior was added.
- [ ] Any claims about analysis results are framed as exploratory insights rather than confirmed RCA.

## Questions

If you are unsure whether a change fits the project’s safety model or architecture, open an issue for discussion before submitting a pull request.
