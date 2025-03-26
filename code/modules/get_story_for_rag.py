import sqlite3
import json

DB_PATH = "analysis_results.db"

def fetch_analyze_story_result(jira_id, pr_number):
    """
    Fetch the analyze_story result from the database for a given JIRA ID and PR number.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query the database for the analyze_story_result
        cursor.execute("""
            SELECT analyze_story_result FROM analysis_results
            WHERE jira_id = ? AND pr_number = ?
        """, (jira_id, pr_number))
        record = cursor.fetchone()

        if record and record[0]:
            # Deserialize the JSON string back into a Python object
            return json.loads(record[0])
        else:
            return None  # Return None if no result is found

    except Exception as e:
        print(f"Error fetching analyze_story_result: {e}")
        return None
    finally:
        if conn:
            conn.close()