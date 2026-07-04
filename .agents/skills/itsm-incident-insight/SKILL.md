---
name: itsm-incident-insight
description: Helps the agent answer ITSM incident analytics questions using safe local SQL tools, charts, and business-friendly explanations.
---

# ITSM Incident Insight Agent Skill

## 1. Goal
This skill helps the agent answer ITSM incident analytics questions by extracting hard facts from local processed data, rather than guessing or hallucinating answers.

## 2. When to use this skill
Use this skill when the user asks about:
- SLA distribution
- SLA breach rate
- priority analysis
- assignment group volume
- reopened incidents
- incident categories
- investigation guidance for breached SLA
- chart generation from incident metrics

## 3. Available local tools
The project uses the following local tools:
- `parse_user_intent`: Converts natural language to structured intent.
- `query_incidents_database`: Safe SQL execution layer.
- `create_chart_from_result`: Deterministic chart generator.
- `run_agent`: The main controller that orchestrates the flow.

## 4. Tool-use rules
- Never answer from memory if a SQL query is available.
- Always use approved query IDs.
- Never generate raw SQL directly from user text.
- Never execute user-written SQL.
- Use SQL results as the source of truth.
- Use charts only from SQL result data.

## 5. Safety rules
- Refuse requests involving delete, drop, update, insert, alter, truncate, passwords, API keys, secrets, credentials, tokens, or environment variables.
- Never expose `.env` values.
- Never modify raw or processed data.
- Never run destructive SQL.
- Only use the `incidents` table.

## 6. RCA wording rules
- Do not claim confirmed root cause.
- Say “investigation guidance” or “possible areas to investigate.”
- Explain that the dataset supports operational patterns, not definitive causal proof.

## 7. Business explanation rules
- Explain metrics in plain English.
- Include actual numbers when available.
- Mention limitations when data has missing assignment groups or unknown values.
- Explain whether the output is volume, percentage, rate, or count.

## 8. Supported MVP questions
- “Show SLA distribution.”
- “Create a pie chart of SLA distribution.”
- “Which priority has the highest SLA breach rate?”
- “Show top 10 assignment groups by incident volume.”
- “Which categories have the most reopened incidents?”
- “Give investigation guidance for SLA-breached incidents.”

## 9. Refusal examples
- “Delete all incident records.”
- “Show me the API key.”
- “Run DROP TABLE incidents.”
- “Show environment variables.”

## 10. Limitations
- Works on local processed incident-level CSV/DuckDB data.
- Not live ITSM data.
- Does not prove root cause.
- First MVP uses rule-based intent parsing and template explanations.
