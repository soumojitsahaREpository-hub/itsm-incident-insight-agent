"""
ITSM Incident Insight Agent - Final Demo Runner
Run this script to see the agent pipeline in action for the Kaggle Capstone video.
"""

import time
from src.agent.controller import run_agent

def main():
    print("============================================================")
    print("         ITSM Incident Insight Agent - Live Demo            ")
    print("============================================================")
    
    # The exact list of questions to showcase the agent's capabilities and safety
    demo_questions = [
        "Show SLA distribution.",
        "Create a pie chart of SLA distribution.",
        "Which priority has the highest SLA breach rate?",
        "Show top 10 assignment groups by incident volume.",
        "Which categories have the most reopened incidents?",
        "Delete all incident records."
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n[{i}/{len(demo_questions)}] USER: \"{question}\"")
        print("-" * 60)
        
        # Add a slight delay for dramatic effect during screen recording
        time.sleep(1)
        
        # Execute the main agent controller loop
        result = run_agent(question)
        
        # Extract the necessary fields cleanly
        status = result.get("status", "unknown")
        final_answer = result.get("final_answer", "")
        
        # Get query ID safely from the nested intent dictionary
        intent_info = result.get("intent", {})
        query_id = intent_info.get("query_id") if isinstance(intent_info, dict) else None
        
        # Get chart path safely from the nested chart_result dictionary
        chart_info = result.get("chart_result")
        chart_path = chart_info.get("chart_path") if isinstance(chart_info, dict) else None
        
        safety_notes = result.get("safety_notes", "")
        
        # Print formatted, readable output for the video
        print(f"STATUS:       {status.upper()}")
        if query_id:
            print(f"INTENT MAPPED: {query_id}")
        
        print(f"\nAGENT ANSWER:\n{final_answer}")
        
        if chart_path:
            print(f"\nCHART SAVED:  {chart_path}")
            
        print(f"\nSYSTEM NOTE:  {safety_notes}")
        print("============================================================")
        
        # Pause briefly before the next question so the audience can read
        time.sleep(1.5)

if __name__ == "__main__":
    main()
