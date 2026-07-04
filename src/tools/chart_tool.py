import matplotlib.pyplot as plt
import os
from pathlib import Path

# Define paths relative to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"

# Ensure the charts directory exists
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

def create_chart_from_result(query_id: str, sql_result: dict, chart_type: str | None = None) -> dict:
    """
    Generates a chart image from SQL tool results and saves it to disk.
    
    Args:
        query_id: The ID of the query that generated the data.
        sql_result: The structured dictionary returned by query_incidents_database.
        chart_type: Optional requested chart type (unused for now as it's hardcoded per query).
        
    Returns:
        A dictionary containing the chart status and file path.
    """
    # 1. Validate the SQL result
    if sql_result.get("status") != "success":
        return {
            "status": "error",
            "query_id": query_id,
            "chart_type": chart_type,
            "chart_path": "",
            "message": "Cannot generate chart: SQL result was not successful.",
            "error_message": sql_result.get("error_message") or sql_result.get("safety_notes")
        }

    data = sql_result.get("data", [])
    if not data:
        return {
             "status": "error",
             "query_id": query_id,
             "chart_type": chart_type,
             "chart_path": "",
             "message": "Cannot generate chart: No data returned from SQL.",
             "error_message": "Empty data array."
        }
        
    # Helper function to handle None (null) labels from the database
    def clean_label(label):
        return "Unknown / Unassigned" if label is None else str(label)

    chart_filename = f"{query_id}_chart.png"
    chart_path = CHARTS_DIR / chart_filename
    
    # Create a new figure
    plt.figure(figsize=(10, 6))
    
    try:
        # Supported chart 1: pie chart for sla_distribution
        if query_id == "sla_distribution":
            labels = [clean_label(row.get('made_sla')) for row in data]
            sizes = [row.get('incident_count', 0) for row in data]
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title("SLA Distribution (Met vs Breached)")
            final_type = "pie"
            
        # Supported chart 2: bar chart for priority_distribution
        elif query_id == "priority_distribution":
            labels = [clean_label(row.get('priority')) for row in data]
            values = [row.get('incident_count', 0) for row in data]
            plt.bar(labels, values, color='skyblue')
            plt.title("Incident Distribution by Priority")
            plt.xlabel("Priority")
            plt.ylabel("Incident Count")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            final_type = "bar"
            
        # Supported chart 3: bar chart for top_assignment_groups
        elif query_id == "top_assignment_groups":
            labels = [clean_label(row.get('assignment_group')) for row in data]
            values = [row.get('incident_count', 0) for row in data]
            plt.bar(labels, values, color='coral')
            plt.title("Top 10 Assignment Groups by Volume")
            plt.xlabel("Assignment Group")
            plt.ylabel("Incident Count")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            final_type = "bar"
            
        # Supported chart 4: bar chart for breach_rate_by_priority
        elif query_id == "breach_rate_by_priority":
            labels = [clean_label(row.get('priority')) for row in data]
            values = [row.get('breach_rate_percentage', 0) for row in data]
            plt.bar(labels, values, color='salmon')
            plt.title("SLA Breach Rate by Priority (%)")
            plt.xlabel("Priority")
            plt.ylabel("Breach Rate (%)")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            final_type = "bar"
            
        else:
            # If we don't have a hardcoded chart for this query, return unsupported
            plt.close()
            return {
                "status": "unsupported",
                "query_id": query_id,
                "chart_type": chart_type,
                "chart_path": "",
                "message": f"Charting for query ID '{query_id}' is not supported yet.",
                "error_message": None
            }

        # Save the figure to disk
        plt.savefig(chart_path)
        plt.close() # Close to free up memory
        
        return {
            "status": "success",
            "query_id": query_id,
            "chart_type": final_type,
            "chart_path": str(chart_path),
            "message": f"Successfully generated {final_type} chart.",
            "error_message": None
        }

    except Exception as e:
        plt.close()
        return {
            "status": "error",
            "query_id": query_id,
            "chart_type": chart_type,
            "chart_path": "",
            "message": "An error occurred while generating the chart.",
            "error_message": str(e)
        }


if __name__ == "__main__":
    from src.tools.sql_tool import query_incidents_database
    import json
    
    print("--- Testing Chart Tool ---")
    
    # 1. Test pie chart
    print("\n1. Fetching SLA Distribution data...")
    res_sla = query_incidents_database("sla_distribution")
    print("Creating pie chart...")
    chart_res_sla = create_chart_from_result("sla_distribution", res_sla)
    print(json.dumps(chart_res_sla, indent=2))
    
    # 2. Test bar chart
    print("\n2. Fetching Priority Distribution data...")
    res_prio = query_incidents_database("priority_distribution")
    print("Creating bar chart...")
    chart_res_prio = create_chart_from_result("priority_distribution", res_prio)
    print(json.dumps(chart_res_prio, indent=2))
