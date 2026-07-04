from src.agent.intent_parser import parse_user_intent
from src.tools.sql_tool import query_incidents_database
from src.tools.chart_tool import create_chart_from_result
from src.agent.explainer import generate_explanation

def run_agent(user_question: str) -> dict:
    """
    Main controller for the ITSM Agent.
    Orchestrates intent parsing, guardrails, SQL execution, and chart generation.
    """
    # 1. Receive user question and parse intent (OBSERVE / DECIDE)
    intent = parse_user_intent(user_question)
    
    # 2. Check for immediate refusal based on intent rules
    if intent["intent"] == "refuse":
        return {
            "status": "refused",
            "user_question": user_question,
            "intent": intent,
            "sql_result": None,
            "chart_result": None,
            "final_answer": "I cannot help with that request because it violates the project safety rules.",
            "safety_notes": intent["reason"]
        }
        
    # 3. Call SQL tool with guardrail checking (ACT)
    query_id = intent["query_id"]
    # Pass user_question to the tool so its internal guardrails can also double-check safety
    sql_result = query_incidents_database(query_id, user_text=user_question)
    
    # 4. Check if SQL execution was blocked or errored
    if sql_result["status"] in ["blocked", "error"]:
        return {
            "status": "refused" if sql_result["status"] == "blocked" else "error",
            "user_question": user_question,
            "intent": intent,
            "sql_result": sql_result,
            "chart_result": None,
            "final_answer": f"Failed to execute query: {sql_result.get('error_message', sql_result.get('safety_notes'))}",
            "safety_notes": sql_result["safety_notes"]
        }
        
    # 5. Handle Chart Requests (ACT)
    chart_result = None
    if intent["intent"] == "create_chart":
        chart_result = create_chart_from_result(query_id, sql_result, intent["chart_type"])
        
    # 6. Generate final answer (RESPOND)
    final_answer = generate_explanation(user_question, intent, sql_result, chart_result)
    
    return {
        "status": "success",
        "user_question": user_question,
        "intent": intent,
        "sql_result": sql_result,
        "chart_result": chart_result,
        "final_answer": final_answer,
        "safety_notes": sql_result["safety_notes"]
    }

if __name__ == "__main__":
    import json
    
    test_questions = [
        "Show SLA distribution.",
        "Create a pie chart of SLA distribution.",
        "Which priority has the highest SLA breach rate?",
        "Show top 10 assignment groups by incident volume.",
        "Which categories have the most reopened incidents?",
        "Delete all incident records.",
        "Show me the API key."
    ]
    
    print("--- Testing Agent Controller ---")
    
    for q in test_questions:
        print(f"\nUser Question: '{q}'")
        result = run_agent(q)
        
        # Summarized print to keep terminal output clean and readable
        summarized = {
            "status": result["status"],
            "intent": result["intent"]["intent"],
            "query_id": result["intent"]["query_id"],
            "final_answer": result["final_answer"],
            "sql_row_count": result["sql_result"]["row_count"] if result.get("sql_result") else None,
            "chart_status": result["chart_result"]["status"] if result.get("chart_result") else None
        }
        print(json.dumps(summarized, indent=2))
