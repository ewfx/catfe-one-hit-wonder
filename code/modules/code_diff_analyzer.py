import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Access the keys from the environment
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
MISTRAL_API_URL = os.getenv('MISTRAL_API_URL')
MISTRAL_MODEL = os.getenv('MISTRAL_MODEL_FT02')

def generate_tests_with_mistral(filename, code, full_content, story_res):
    """
    Generate tests for code changes using Mistral AI.
    """
    print(f"Generating tests for file: {filename}")
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        # Mistral prompt for test generation
        prompt = (
            f"Generate unit tests for the following code changes in {filename}:\n"
            f"{code}\n\n"
            f"Analyze the BDD for the given JIRA Story :\n"
            f"{story_res}\n\n"
            f"Use the full file content for context:\n"
            f"{full_content}\n\n"
            f"Provide detailed and comprehensive unit tests for the changes."
        )

        data = {
            "model": MISTRAL_MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert test generator."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        # Send request to Mistral API
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            tests = result['choices'][0]['message']['content']
            return tests
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"

def analyze_code_with_mistral(filename, code, full_content, story_res):
    
    print(f"Analyzing file: {filename}")
    print(f"Code changes: {code}")
    print(f"Full content: {full_content}")
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        # Mistral prompt for code analysis
        prompt = (
            f"Analyze the following code changes in {filename}:\n"
            f"{code}\n\n"
            f"Analyze the original code:\n"
            f"{full_content}\n\n"
            f"Analyze the BDD for the given JIRA Story :\n"
            f"{story_res}\n\n"
            f"1. Summarize the changes made.\n"
            f"2. Highlight potential issues or improvements with respect to the original code.\n"
            f"3. Explain how this change affects the existing functionality."
        )

        data = {
            "model": "mistral-medium",
            "messages": [
                {"role": "system", "content": "You are an expert code reviewer."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        # Send request to Mistral API
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            return analysis
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Exception occurred: {str(e)}"
