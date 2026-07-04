"""
Query Catalog for ITSM Agent
Contains all approved, pre-defined SQL queries.
"""

QUERY_CATALOG = {
    "total_incidents": {
        "query_id": "total_incidents",
        "business_question": "How many total incidents are in the dataset?",
        "sql": "SELECT COUNT(*) AS total_incidents FROM incidents",
        "output_type": "single_value",
        "chart_recommendation": "none",
        "explanation_notes": "State the total volume of incidents."
    },
    "sla_distribution": {
        "query_id": "sla_distribution",
        "business_question": "What is the distribution of SLA compliance (met vs breached)?",
        "sql": "SELECT made_sla, COUNT(*) AS incident_count FROM incidents GROUP BY made_sla ORDER BY incident_count DESC",
        "output_type": "tabular",
        "chart_recommendation": "pie",
        "explanation_notes": "Compare how many incidents met their SLA versus how many breached."
    },
    "sla_breach_rate": {
        "query_id": "sla_breach_rate",
        "business_question": "What is the overall SLA breach rate percentage?",
        # We use a string match 'False' or boolean False depending on how DuckDB read the CSV. 
        # COALESCE and standard CAST ensure safety.
        "sql": "SELECT ROUND(SUM(CASE WHEN LOWER(CAST(made_sla AS VARCHAR)) = 'false' OR CAST(made_sla AS VARCHAR) = '0' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS breach_rate_percentage FROM incidents",
        "output_type": "single_value",
        "chart_recommendation": "none",
        "explanation_notes": "Explain the overall percentage of incidents that failed to meet their SLA."
    },
    "priority_distribution": {
        "query_id": "priority_distribution",
        "business_question": "How are incidents distributed across different priorities?",
        "sql": "SELECT priority, COUNT(*) AS incident_count FROM incidents GROUP BY priority ORDER BY incident_count DESC",
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "Summarize which priorities have the highest volume."
    },
    "top_assignment_groups": {
        "query_id": "top_assignment_groups",
        "business_question": "Which assignment groups handle the most incidents?",
        "sql": "SELECT assignment_group, COUNT(*) AS incident_count FROM incidents GROUP BY assignment_group ORDER BY incident_count DESC LIMIT 10",
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "List the busiest groups by volume."
    },
    "top_categories": {
        "query_id": "top_categories",
        "business_question": "What are the most common incident categories?",
        "sql": "SELECT category, COUNT(*) AS incident_count FROM incidents GROUP BY category ORDER BY incident_count DESC LIMIT 10",
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "Highlight the most frequent types of issues."
    },
    "breach_rate_by_priority": {
        "query_id": "breach_rate_by_priority",
        "business_question": "Which priority has the highest SLA breach rate?",
        "sql": """
            SELECT 
                priority, 
                COUNT(*) AS total_incidents, 
                SUM(CASE WHEN LOWER(CAST(made_sla AS VARCHAR)) = 'false' OR CAST(made_sla AS VARCHAR) = '0' THEN 1 ELSE 0 END) AS breached_incidents, 
                ROUND(SUM(CASE WHEN LOWER(CAST(made_sla AS VARCHAR)) = 'false' OR CAST(made_sla AS VARCHAR) = '0' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) AS breach_rate_percentage 
            FROM incidents 
            GROUP BY priority 
            ORDER BY breach_rate_percentage DESC
        """,
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "Identify which priority levels struggle the most to meet SLA."
    },
    "reopened_incidents_by_category": {
        "query_id": "reopened_incidents_by_category",
        "business_question": "Which categories have the most reopened incidents?",
        # Cast to INT in case it was read as string
        "sql": "SELECT category, COUNT(*) AS reopened_count FROM incidents WHERE CAST(reopen_count AS INTEGER) > 0 GROUP BY category ORDER BY reopened_count DESC LIMIT 10",
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "Discuss which categories might need better initial resolution based on high reopen rates."
    },
    "avg_resolution_hours_by_priority": {
        "query_id": "avg_resolution_hours_by_priority",
        "business_question": "What is the average resolution time by priority?",
        "sql": "SELECT priority, ROUND(AVG(CAST(resolution_hours AS FLOAT)), 2) AS avg_resolution_hours FROM incidents GROUP BY priority ORDER BY avg_resolution_hours DESC",
        "output_type": "tabular",
        "chart_recommendation": "bar",
        "explanation_notes": "Explain the average number of hours it takes to resolve incidents across different priority levels."
    },
    "investigation_summary_for_breached_sla": {
        "query_id": "investigation_summary_for_breached_sla",
        "business_question": "Give investigation guidance for SLA-breached incidents.",
        "sql": """
            SELECT 
                priority, 
                category, 
                assignment_group, 
                COUNT(*) AS breached_count 
            FROM incidents 
            WHERE LOWER(CAST(made_sla AS VARCHAR)) = 'false' OR CAST(made_sla AS VARCHAR) = '0' 
            GROUP BY priority, category, assignment_group 
            ORDER BY breached_count DESC 
            LIMIT 5
        """,
        "output_type": "tabular",
        "chart_recommendation": "none",
        "explanation_notes": "Do not claim to know the definitive RCA. Suggest these high-volume breach combinations as the best places to start investigating."
    }
}

def get_query_catalog():
    """Returns the full dictionary of approved queries."""
    return QUERY_CATALOG

def get_query(query_id: str):
    """Returns a specific query template by ID, or None if not found."""
    return QUERY_CATALOG.get(query_id)

if __name__ == "__main__":
    # Simple test to verify the catalog loads
    catalog = get_query_catalog()
    print(f"Loaded {len(catalog)} approved queries.")
    print("Example Query ID: 'sla_distribution'")
    print(f"SQL: {get_query('sla_distribution')['sql']}")
