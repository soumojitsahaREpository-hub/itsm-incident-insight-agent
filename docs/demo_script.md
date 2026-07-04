# 5-Minute Kaggle Capstone Video Demo Script

## Structure
1. **Introduction (30s):** The problem and the solution.
2. **Architecture & Security (1m):** How it works safely.
3. **Live Demo (3m):** Running the Web UI and reviewing outputs.
4. **Closing (30s):** Capstone concepts and future work.

## Exact Demo Questions
*These are built directly into the local Streamlit Web UI.*
1. "Create a pie chart of SLA distribution."
2. "Create a bar chart of priority distribution."
3. "Create a bar chart of top assignment groups by incident volume."
4. "Create a bar chart of SLA breach rate by priority."
5. "Delete all incident records."

## What to say (The Script)

**1. Introduction**
> "Hi, this is my Kaggle AI Agents Capstone project. The problem with ITSM data is that business leaders need quick insights, but writing SQL is hard, and letting AI write SQL is dangerous. My solution is the ITSM Incident Insight Agent-a local, tool-based agent that answers business questions using a secure, pre-approved query catalog."

**2. Architecture & Security**
> "Before we run it, let's look at the architecture. I built this using the Antigravity workflow. The agent uses an 'Observe, Decide, Act, Respond' loop. 
> 
> First, it maps user intent to a specific `query_id`, not raw SQL. Then, strict security guardrails validate the request. Finally, it uses a local DuckDB SQL tool and a Matplotlib Chart tool to fetch facts. This guarantees the AI never guesses data or runs destructive commands. We have both a CLI demo and a local Streamlit Web UI to interact with this agent."

**3. Live Demo (Run `python -m streamlit run streamlit_app.py` in terminal)**
> "Let's launch the local Streamlit Web UI to see the pipeline in action. 
> 
> * **[Questions 1 & 2]** Notice how the agent maps 'Create a pie chart of SLA distribution' and 'priority distribution' to specific query IDs. It explains the numbers perfectly based on actual dataset rows and immediately displays the data-driven charts in the UI.
> * **[Questions 3 & 4]** The agent provides investigation guidance based on the highest volume breaches and assignment groups. Notice I emphasize *guidance*, as we cannot claim confirmed root cause from just CSV data.
> * **[Question 5]** Now, the safety refusal. I ask to delete records. The guardrails instantly block the request before it ever reaches the database, proving the architecture is secure against prompt injection or malicious commands."

**4. Closing Statement**
> "This project demonstrates several key course concepts: building with an Antigravity-assisted workflow, designing a local tool-based agent controller, implementing rigorous security guardrails, and defining an Agent Skill via `SKILL.md`. 
> 
> For the future, the foundation is ready to plug in Gemini for dynamic LLM explanations and MCP for cross-platform tool use. Thank you for watching!"
