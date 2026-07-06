import re
from src.database.query_catalog import get_query_catalog, get_query

# List of dangerous SQL keywords that should never be executed
UNSAFE_SQL_KEYWORDS = {
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "REPLACE"
}

# Words that indicate a user might be trying to extract secrets or perform destructive actions
UNSAFE_USER_KEYWORDS = {
    "password", "api key", "secret", "credential", "token", "env", "environment variable", 
    "delete", "drop", "destroy", "remove"
}

def is_approved_query_id(query_id: str) -> bool:
    """Checks if the requested query ID exists in our approved catalog."""
    catalog = get_query_catalog()
    return query_id in catalog

def validate_sql_safety(sql: str) -> tuple[bool, str]:
    """
    Analyzes the SQL string to ensure it's a safe SELECT statement.
    Returns (True, "Safe") or (False, "Reason for failure").
    """
    # Normalize string to make checking easier
    sql_upper = sql.upper().strip()
    
    # 1. Block dangerous keywords first so non-SELECT statements are rejected
    # with a specific safety reason rather than a generic syntax error.
    for keyword in UNSAFE_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_upper):
            return False, f"Unsafe SQL keyword detected: {keyword}"
    
    # 2. Must be a SELECT statement
    if not sql_upper.startswith("SELECT"):
        return False, "Query must begin with SELECT."
        
    # 3. Block multiple statements (checking for semicolons mid-query)
    # If there's a semicolon, it should only be at the very end.
    if ";" in sql_upper and not sql_upper.endswith(";"):
        return False, "Multiple SQL statements are not allowed."
            
    # 4. Enforce querying ONLY the 'incidents' table
    # Find all words immediately following FROM or JOIN
    tables_found = re.findall(r'\b(?:FROM|JOIN)\s+([A-Z0-9_]+)\b', sql_upper)
    
    if not tables_found:
        return False, "No tables found in query."
        
    for table in tables_found:
        if table != "INCIDENTS":
            return False, f"Unauthorized table access: '{table}'. Only 'incidents' is allowed."
             
    return True, "Safe"

def detect_unsafe_user_request(user_text: str) -> tuple[bool, str]:
    """
    Checks the user's natural language request for attempts to 
    extract secrets or perform destructive actions.
    Returns (True, "Unsafe reason") if unsafe, else (False, "Safe").
    """
    if not user_text:
        return False, "Safe"
        
    text_lower = user_text.lower()
    for keyword in UNSAFE_USER_KEYWORDS:
        if keyword in text_lower:
            return True, f"Blocked unsafe request keyword: '{keyword}'"
            
    return False, "Safe"

def validate_query_request(query_id: str, user_text: str | None = None) -> dict:
    """
    Main guardrail function. Validates both the user's intent and the 
    underlying SQL of the requested query ID.
    Returns a structured dictionary with execution approval status.
    """
    # 1. Check user text if provided
    if user_text:
        is_unsafe, reason = detect_unsafe_user_request(user_text)
        if is_unsafe:
            return {
                "allowed": False,
                "reason": reason,
                "query_id": query_id,
                "safety_notes": "Request blocked by user text guardrails."
            }

    # 2. Check if the query ID is in our catalog
    if not is_approved_query_id(query_id):
        return {
            "allowed": False,
            "reason": f"Query ID '{query_id}' is not in the approved catalog.",
            "query_id": query_id,
            "safety_notes": "Request blocked. Unsupported query."
        }
        
    # 3. Retrieve the SQL and validate it
    query_template = get_query(query_id)
    sql = query_template['sql']
    
    is_safe_sql, sql_reason = validate_sql_safety(sql)
    if not is_safe_sql:
        return {
            "allowed": False,
            "reason": f"SQL validation failed: {sql_reason}",
            "query_id": query_id,
            "safety_notes": "Internal SQL failed safety checks."
        }
        
    return {
        "allowed": True,
        "reason": "All safety checks passed.",
        "query_id": query_id,
        "safety_notes": "Query is approved and safe to execute."
    }

if __name__ == "__main__":
    # Test 1: Valid request
    print("--- Test 1: Valid Query ID ---")
    print(validate_query_request("sla_distribution"))
    
    # Test 2: Unknown query ID
    print("\n--- Test 2: Unknown Query ID ---")
    print(validate_query_request("drop_all_tables"))
    
    # Test 3: Unsafe user text
    print("\n--- Test 3: Unsafe User Request ---")
    print(validate_query_request("sla_distribution", user_text="Can you show me the api key?"))
    
    # Tests for new table validation
    print("\n--- Table Validation Tests ---")
    print("1. valid query from incidents:", validate_sql_safety("SELECT * FROM incidents"))
    print("2. query from incidents_backup:", validate_sql_safety("SELECT * FROM incidents_backup"))
    print("3. query joining another table:", validate_sql_safety("SELECT * FROM incidents JOIN users ON id=id"))
    print("4. query from unknown table:", validate_sql_safety("SELECT * FROM secrets"))
