import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Access the keys from the environment
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')
MISTRAL_MODEL = os.getenv('MISTRAL_MODEL_FT01')


def analyze_with_mistral(jira_story):
    """
    Send JIRA story details to Mistral API and generate:
    - Story Explanation
    - BDD Acceptance Criteria
    """

    prompt = f"""
    You are a software tester.
    1. Explain the following JIRA story in simple terms in 1-2 lines:
    - Title: {jira_story['title']}
    - Description: {jira_story['description']}
    - Acceptance Criteria: {jira_story['acceptance_criteria']}

    2. Generate BDD acceptance criteria in Gherkin format.

    3. Generate a mermaid script for the user story.
    """

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "*/*",                          # Add Accept header
        "User-Agent": "PostmanRuntime/7.30.0"      # Mimic Postman user agent
    }

    # ✅ Payload
    data = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role":"system","content":"You are a product owner of a small business software application"},
            {"role": "user", "content": prompt}
            ],
        "temperature": 0.7,
        "max_tokens": 1000
    }   

    try:
        # ✅ Use json=payload to serialize correctly
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            explanation = result['choices'][0]['message']['content']
            return {
                "bdd_criteria": explanation
            }
        else:
            print(f"Error {response.status_code}: {response.text}")
            return {
                "error": f"Failed to connect. Status: {response.status_code}. Response: {response.text}"
            }

    except Exception as e:
        return {
            "error": f"Exception occurred: {str(e)}"
        }
