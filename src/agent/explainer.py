import os

def generate_explanation(user_question: str, intent: dict, sql_result: dict, chart_result: dict | None = None) -> str:
    """
    Generates a plain-English explanation of the SQL results.
    Currently uses smart templates based on actual data to save tokens and ensure safety.
    
    Future capability: connect to an LLM like Gemini if USE_LLM_EXPLANATION is true.
    """
    # Check if we should use an LLM (not implemented yet, fallback to templates)
    use_llm = os.environ.get("USE_LLM_EXPLANATION", "false").lower() == "true"
    if use_llm:
        # TODO: Implement Gemini API call here in the future
        # e.g., prompt = build_prompt(user_question, sql_result['data'])
        # return call_gemini(prompt)
        pass

    # 1. Handle refused/blocked requests
    if intent.get("intent") == "refuse" or (sql_result and sql_result.get("status") != "success"):
        return "I cannot help with that request because it violates the project safety rules."

    data = sql_result.get("data", [])
    query_id = intent.get("query_id")
    
    # Base explanation text
    explanation = ""

    # 2. Build smart template explanations based on query_id
    if not data:
        explanation = "I executed the query successfully, but no data was returned."
    
    elif query_id == "total_incidents":
        count = data[0].get("total_incidents", 0)
        explanation = f"The dataset contains {count:,} unique incidents."
        
    elif query_id == "sla_distribution":
        # Calculate met vs breached safely
        met = 0
        breached = 0
        for row in data:
            val = str(row.get("made_sla", "")).lower()
            if val == "true" or val == "1":
                met += int(row.get("incident_count", 0))
            elif val == "false" or val == "0":
                breached += int(row.get("incident_count", 0))
                
        total = met + breached
        if total > 0:
            breach_pct = round((breached / total) * 100, 2)
            explanation = f"Out of {total:,} incidents, {met:,} met the SLA and {breached:,} breached the SLA. The overall breach rate is {breach_pct}%."
        else:
            explanation = "SLA distribution calculated, but no valid counts found."
            
    elif query_id == "breach_rate_by_priority":
        top_prio = data[0].get("priority", "Unknown")
        top_rate = data[0].get("breach_rate_percentage", 0)
        explanation = f"Priority '{top_prio}' has the highest SLA breach rate at {top_rate}%. Please review high-priority incident workflows."
        
    elif query_id == "top_assignment_groups":
        top_group = data[0].get("assignment_group")
        top_count = data[0].get("incident_count", 0)
        
        # Check for unassigned tickets based on common Null/empty representations
        if top_group is None or str(top_group).lower() in ["none", "nan", ""]:
            explanation = f"A large volume of incidents ({top_count:,}) are 'Unknown / Unassigned'. We should improve initial ticket routing."
        else:
            explanation = f"The busiest assignment group is '{top_group}' with {top_count:,} incidents."
            
    elif query_id == "reopened_incidents_by_category":
        top_cat = data[0].get("category", "Unknown")
        top_count = data[0].get("reopened_count", 0)
        explanation = f"The category '{top_cat}' has the highest number of reopened incidents ({top_count:,})."
        
    elif query_id == "investigation_summary_for_breached_sla":
        explanation = "This is investigation guidance based on the highest volume SLA breaches. This does not represent a confirmed root cause."
        
    else:
        # Fallback to the hardcoded explanation note from the catalog
        explanation = sql_result.get("explanation_ready_summary", "Here is the data for your request.")

    # 3. Append chart info if a chart was generated
    if chart_result and chart_result.get("status") == "success":
        chart_path = chart_result.get("chart_path")
        explanation += f"\n\nI also generated the requested chart and saved it locally at:\n{chart_path}"

    return explanation
