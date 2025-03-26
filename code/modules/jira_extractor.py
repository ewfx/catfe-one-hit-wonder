import re
import csv
import os

# Path to the JIRA CSV file
CSV_FILE = os.path.join("data", "jira_data.csv")

def extract_jira_id(title):
    """
    Extract JIRA ID from the PR title using regex.
    Supports formats like: ABC-123, ID1234, XYZ_456.
    """
    jira_pattern = re.compile(r'\b([A-Z]+[-_]*\d+)\b')  # Improved regex
    match = jira_pattern.search(title)
    return match.group(0) if match else "N/A"

def get_jira_details(jira_id):
    """
    Fetch JIRA details from the CSV file by JIRA ID.
    Returns None if no match is found.
    """
    if not os.path.exists(CSV_FILE):
        return None

    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['JIRA_ID'] == jira_id:
                return {
                    "title": row['Title'],
                    "description": row['Description'],
                    "acceptance_criteria": row['Acceptance_Criteria']
                }
    return None
