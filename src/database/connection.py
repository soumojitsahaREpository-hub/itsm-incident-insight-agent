import duckdb
import os
from pathlib import Path

# Define paths relative to the project root
# __file__ is connection.py, so parent.parent.parent is the root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "processed" / "itsm_agent.duckdb"
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "incidents_level_df.csv"

def get_connection():
    """
    Establish a connection to the local DuckDB database.
    """
    # Ensure the database directory exists just in case
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # duckdb.connect will open the file if it exists, or create it if it doesn't
    return duckdb.connect(str(DB_PATH))

def initialize_database():
    """
    Initializes the database by creating or replacing the 'incidents' table
    from the processed CSV file. Returns validation statistics.
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Processed CSV not found at {CSV_PATH}")

    conn = get_connection()
    try:
        # Create or replace the table directly from the CSV
        # read_csv_auto intelligently guesses types and headers
        conn.execute(f"""
            CREATE OR REPLACE TABLE incidents AS 
            SELECT * FROM read_csv_auto('{str(CSV_PATH)}')
        """)
        
        # Validate table exists and get row count
        result = conn.execute("SELECT count(*) FROM incidents").fetchone()
        row_count = result[0] if result else 0
        
        return {
            "status": "success",
            "table": "incidents",
            "row_count": row_count,
            "database_file": str(DB_PATH)
        }
    finally:
        conn.close()

if __name__ == "__main__":
    # Simple test block to verify the logic runs standalone
    print("Initializing ITSM Database...")
    stats = initialize_database()
    print(f"Success! Loaded {stats['row_count']} rows into the '{stats['table']}' table.")
    print(f"Database saved to: {stats['database_file']}")
