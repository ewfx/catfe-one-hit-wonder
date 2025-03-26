import sqlite3
from datetime import datetime
import json

DB_PATH = "analysis_results.db"

def initialize_database():
    """
    Initialize the database and create the table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jira_id TEXT NOT NULL,
            pr_number INTEGER NOT NULL,
            analyze_story_result TEXT DEFAULT NULL,
            analyze_code_result TEXT DEFAULT NULL,
            generate_tests_result TEXT DEFAULT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def upsert_analysis_result(jira_id, pr_number, analyze_story=None, analyze_code=None, generate_tests=None):
    """
    Insert or update the analysis results for a given JIRA ID and PR number.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Serialize the data to JSON strings if they are not None
        analyze_story = json.dumps(analyze_story) if analyze_story else None
        analyze_code = json.dumps(analyze_code) if analyze_code else None
        generate_tests = json.dumps(generate_tests) if generate_tests else None

        # Check if a record already exists for the given JIRA ID and PR number
        cursor.execute("""
            SELECT id FROM analysis_results WHERE jira_id = ? AND pr_number = ?
        """, (jira_id, pr_number))
        record = cursor.fetchone()

        if record:
            # Update the existing record
            cursor.execute("""
                UPDATE analysis_results
                SET analyze_story_result = COALESCE(?, analyze_story_result),
                    analyze_code_result = COALESCE(?, analyze_code_result),
                    generate_tests_result = COALESCE(?, generate_tests_result),
                    updated_at = ?
                WHERE jira_id = ? AND pr_number = ?
            """, (analyze_story, analyze_code, generate_tests, datetime.now(), jira_id, pr_number))
        else:
            # Insert a new record
            cursor.execute("""
                INSERT INTO analysis_results (jira_id, pr_number, analyze_story_result, analyze_code_result, generate_tests_result)
                VALUES (?, ?, ?, ?, ?)
            """, (jira_id, pr_number, analyze_story, analyze_code, generate_tests))

        conn.commit()
    except Exception as e:
        print(f"Error in upsert_analysis_result: {e}")
    finally:
        if conn:
            conn.close()