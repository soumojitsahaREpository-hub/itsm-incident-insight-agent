def parse_user_intent(user_text: str) -> dict:
    """
    Parses a user's natural language question into a structured intent dictionary.
    This version uses rule-based keyword matching to ensure safety and predictability.
    
    Args:
        user_text: The raw question string from the user.
        
    Returns:
        A dictionary containing the parsed intent, query_id, chart_type, and reason.
    """
    if not user_text:
        return {
            "intent": "refuse",
            "query_id": None,
            "chart_type": None,
            "reason": "Empty request.",
            "original_text": ""
        }
        
    text_lower = user_text.lower()
    
    # 1. Check for unsafe words first (Safety first approach)
    unsafe_keywords = ["delete", "drop", "password", "api key", "secret", "token", "credential"]
    for keyword in unsafe_keywords:
        if keyword in text_lower:
            return {
                "intent": "refuse",
                "query_id": None,
                "chart_type": None,
                "reason": f"Request blocked due to unsafe keyword: '{keyword}'.",
                "original_text": user_text
            }
            
    # 2. Check if a chart is requested
    chart_requested = False
    chart_type = None
    if "chart" in text_lower or "graph" in text_lower or "plot" in text_lower:
        chart_requested = True
        if "pie" in text_lower:
            chart_type = "pie"
        elif "bar" in text_lower:
            chart_type = "bar"
            
    # 3. Map to query IDs based on keywords
    query_id = None
    
    if "sla distribution" in text_lower or ("sla" in text_lower and "distribution" in text_lower):
        query_id = "sla_distribution"
        # If chart requested but type not specified, suggest pie
        if chart_requested and not chart_type:
             chart_type = "pie"
             
    elif "priority" in text_lower and "breach rate" in text_lower:
        query_id = "breach_rate_by_priority"
        if chart_requested and not chart_type:
             chart_type = "bar"
             
    elif "priority" in text_lower and "distribution" in text_lower:
        query_id = "priority_distribution"
        if chart_requested and not chart_type:
             chart_type = "bar"
             
    elif "top assignment group" in text_lower or "assignment groups" in text_lower:
        query_id = "top_assignment_groups"
        if chart_requested and not chart_type:
             chart_type = "bar"
             
    elif ("reopen" in text_lower or "reopened" in text_lower) and ("category" in text_lower or "categories" in text_lower):
        query_id = "reopened_incidents_by_category"
        if chart_requested and not chart_type:
             chart_type = "bar"
             
    elif "total incidents" in text_lower:
        query_id = "total_incidents"
        # Total incidents is a single value, charting doesn't make sense here
        chart_type = None
        chart_requested = False
        
    # 4. Finalize intent
    if not query_id:
        return {
            "intent": "refuse",
            "query_id": None,
            "chart_type": None,
            "reason": "Could not understand the question or map it to a supported query.",
            "original_text": user_text
        }
        
    intent = "create_chart" if chart_requested else "answer_question"
    
    return {
        "intent": intent,
        "query_id": query_id,
        "chart_type": chart_type,
        "reason": f"Successfully mapped to {query_id}.",
        "original_text": user_text
    }

if __name__ == "__main__":
    import json
    
    test_questions = [
        "Show SLA distribution.",
        "Create a pie chart of SLA distribution.",
        "Which priority has the highest SLA breach rate?",
        "Show top 10 assignment groups by incident volume.",
        "Which categories have the most reopened incidents?",
        "How many total incidents are there?",
        "Delete all incident records.",
        "Show me the API key."
    ]
    
    print("--- Testing Intent Parser ---")
    for q in test_questions:
        print(f"\nUser Question: '{q}'")
        intent_result = parse_user_intent(q)
        print(json.dumps(intent_result, indent=2))
