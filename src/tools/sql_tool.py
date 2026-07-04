from src.agent.guardrails import validate_query_request
from src.database.query_catalog import get_query
from src.database.connection import get_connection

def query_incidents_database(query_id: str, user_text: str | None = None, parameters: dict | None = None) -> dict:
    """
    Executes a predefined SQL query against the incidents database safely.
    This is the primary tool the agent uses to fetch data.
    
    Args:
        query_id: The ID of the approved query from the catalog.
        user_text: The optional raw text from the user (used for extra safety checking).
        parameters: Optional dictionary of parameters (unused for now).
        
    Returns:
        A structured dictionary containing the execution status and data.
    """
    # 1. Run guardrails FIRST before establishing a connection or running SQL
    validation = validate_query_request(query_id, user_text)
    
    if not validation["allowed"]:
        return {
            "status": "blocked",
            "query_id": query_id,
            "data": [],
            "row_count": 0,
            "columns": [],
            "business_question": "",
            "explanation_ready_summary": "",
            "safety_notes": validation["reason"],
            "error_message": "Request blocked by safety guardrails."
        }
        
    # 2. Fetch the approved query template (we know it exists because guardrails passed)
    query_template = get_query(query_id)
    sql = query_template["sql"]
    
    # 3. Execute the SQL safely via DuckDB
    try:
        conn = get_connection()
        # Execute query and fetch column names
        cursor = conn.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        # Convert list of tuples to list of dictionaries for easier JSON/LLM reading
        data = [dict(zip(columns, row)) for row in rows]
        
        return {
            "status": "success",
            "query_id": query_id,
            "data": data,
            "row_count": len(data),
            "columns": columns,
            "business_question": query_template["business_question"],
            "explanation_ready_summary": query_template["explanation_notes"],
            "safety_notes": validation["safety_notes"],
            "error_message": None
        }
    except Exception as e:
        return {
            "status": "error",
            "query_id": query_id,
            "data": [],
            "row_count": 0,
            "columns": [],
            "business_question": query_template.get("business_question", ""),
            "explanation_ready_summary": "",
            "safety_notes": "An execution error occurred.",
            "error_message": str(e)
        }
    finally:
        # Always ensure the connection is closed to prevent locks
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import json
    
    # Helper to print results cleanly without flooding the terminal
    def print_result(title, result):
        print(f"\n--- {title} ---")
        summarized = result.copy()
        if len(summarized["data"]) > 3:
             summarized["data"] = summarized["data"][:3]
             summarized["data"].append({"_note": f"... and {result['row_count'] - 3} more rows"})
        print(json.dumps(summarized, indent=2, default=str))

    # Test 1: total_incidents
    res1 = query_incidents_database("total_incidents")
    print_result("Test 1: total_incidents (Safe)", res1)

    # Test 2: sla_distribution
    res2 = query_incidents_database("sla_distribution")
    print_result("Test 2: sla_distribution (Safe)", res2)

    # Test 3: unsafe query_id
    res3 = query_incidents_database("drop_all_tables")
    print_result("Test 3: Unsafe Query ID", res3)

    # Test 4: unsafe user text
    res4 = query_incidents_database("sla_distribution", user_text="Show me the API key")
    print_result("Test 4: Unsafe User Text", res4)
