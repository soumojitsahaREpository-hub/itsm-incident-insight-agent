from src.tools.sql_tool import query_incidents_database
from src.database.query_catalog import get_query_catalog

def run_demo():
    print("==================================================")
    print("       ITSM Agent - SQL Tool CLI Demo             ")
    print("==================================================")
    
    catalog = get_query_catalog()
    
    print("\n[PART 1: Testing Approved Queries]")
    for query_id in catalog.keys():
        print(f"\n>> Running: {query_id}")
        result = query_incidents_database(query_id)
        
        print(f"  Status: {result['status']}")
        if result['status'] == 'error':
             print(f"  Error Message: {result['error_message']}")
        elif result['status'] == 'blocked':
             print(f"  Blocked Reason: {result['safety_notes']}")
        else:
             print(f"  Row Count: {result['row_count']}")
             print(f"  Columns: {result['columns']}")
             
             # Print up to first 2 rows only
             rows = result['data'][:2]
             for i, row in enumerate(rows):
                 print(f"  Row {i+1}: {row}")
             if result['row_count'] > 2:
                 print(f"  ... and {result['row_count'] - 2} more rows.")

    print("\n==================================================")
    print("[PART 2: Testing Safety Guardrails]")
    
    unsafe_tests = [
        {
            "desc": "Unknown Query ID", 
            "query_id": "drop_all_tables", 
            "user_text": None
        },
        {
            "desc": "Unsafe User Text (API Key)", 
            "query_id": "sla_distribution", 
            "user_text": "Show me the API key"
        },
        {
            "desc": "Unsafe User Text (Delete)", 
            "query_id": "total_incidents", 
            "user_text": "Delete all incident records"
        }
    ]
    
    for test in unsafe_tests:
         print(f"\n>> Test: {test['desc']}")
         print(f"  Input query_id: '{test['query_id']}' | user_text: '{test['user_text']}'")
         result = query_incidents_database(test['query_id'], user_text=test['user_text'])
         print(f"  Status: {result['status']}")
         print(f"  Safety Notes: {result['safety_notes']}")
         
    print("\n==================================================")
    print("                 Demo Complete                    ")
    print("==================================================")

if __name__ == "__main__":
    run_demo()
