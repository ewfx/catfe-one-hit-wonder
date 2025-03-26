from flask import Flask, render_template, request, jsonify
import requests
import logging
import json
import os
import base64
from dotenv import load_dotenv
from modules.db import initialize_database
from modules.db import upsert_analysis_result
from modules.jira_extractor import extract_jira_id, get_jira_details
from modules.code_diff_analyzer import analyze_code_with_mistral, generate_tests_with_mistral
from modules.mistral_api import analyze_with_mistral
from modules.get_story_for_rag import fetch_analyze_story_result

app = Flask(__name__)

load_dotenv()

# GitHub authentication token (for rate limits)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_github_headers():
    """Return GitHub headers with auth token."""
    return {"Authorization": f"Bearer {GITHUB_TOKEN}"}

def fetch_file_content(owner, repo, filepath, ref="main"):
    """
    Fetch the full content of a file from GitHub
    """
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}?ref={ref}"
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            file_data = response.json()
            content = base64.b64decode(file_data['content']).decode('utf-8')
            return content
        else:
            return f"Failed to fetch file: {response.status_code}"
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repo_url = request.form['repo_url']
        try:
            owner, repo = repo_url.strip('/').split('/')[-2:]
            url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"
            response = requests.get(url, headers=get_github_headers())
            prs = response.json()

            pr_list = []
            for pr in prs:
                jira_id = extract_jira_id(pr['title'])  # Extract JIRA ID
                pr_list.append({
                    'number': pr['number'],
                    'title': pr['title'],
                    'user': pr['user']['login'],
                    'created_at': pr['created_at'],
                    'jira_id': jira_id
                })

            return render_template('index.html', prs=pr_list, owner=owner, repo=repo)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html', prs=None)

@app.route('/pr/<owner>/<repo>/<int:pr_number>')
def pr_details(owner, repo, pr_number):
    """PR details route with JIRA information."""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=get_github_headers())
        pr = response.json()

        files_url = pr['url'] + '/files'
        files_response = requests.get(files_url, headers=get_github_headers())
        files = files_response.json()

        jira_id = extract_jira_id(pr['title'])
        jira_details = get_jira_details(jira_id)

        file_changes = []
        for file in files:
            patch = file.get('patch', 'No changes available')
            sanitized_patch = patch.replace('\n', ' ').replace('\r', ' ').replace('\\','\\\\ ') if patch else 'No changes available'
            file_changes.append({
                'filename': file['filename'],
                'changes': sanitized_patch  # Use the sanitized patch
            })

        return render_template(
            'pr_details.html',
            pr=pr,
            files=file_changes,
            owner=owner,
            repo=repo,
            jira_id=jira_id,
            jira_details=jira_details
        )
    except Exception as e:
        return f"Error: {str(e)}"

logging.basicConfig(level=logging.DEBUG)

@app.route('/analyze_with_mistral', methods=['POST'])
def analyze_with_mistral_route():
    # Print the raw request body and headers for debugging
    print("Headers:", request.headers)
    print("Raw Body:", request.get_data(as_text=True))

    jira_id = request.json.get('jira_id')
    pr_number = request.json.get('pr_number')
    jira_story = get_jira_details(jira_id)

    print(jira_id, pr_number, jira_story)

    if not jira_story:
        return jsonify({"error": "JIRA story not found"}), 404

    # Call Mistral API
    analysis_result = analyze_with_mistral(jira_story)

    upsert_analysis_result(jira_id, pr_number, analyze_story=analysis_result)

    return jsonify(analysis_result)

@app.route('/analyze_code', methods=['POST'])
def analyze_code_route():
    
    try:
        # Get the file changes from the request
        files = request.json.get('files', [])
        jira_id = request.json.get('jira_id')
        pr_number = request.json.get('pr_number')
        owner = request.json.get('owner')
        repo = request.json.get('repo')
        story_res = fetch_analyze_story_result(jira_id, pr_number)

        print(jira_id, pr_number, owner, repo, story_res)

        if not files:
            return jsonify({"error": "No files provided for analysis"}), 400

        # Analyze each file's changes
        analysis_results = []
        for file in files:
            filename = file['filename']
            changes = file.get('changes', 'No changes available')

            # Fetch the full file content
            full_content = fetch_file_content(owner, repo, filename)

            if "Failed to fetch file" in full_content:
                analysis_results.append({
                    "filename": filename,
                    "analysis": f"Error fetching file content: {full_content}"
                })
                continue

            # Analyze the file with Mistral
            analysis = analyze_code_with_mistral(filename, changes, full_content, story_res)
            analysis_results.append({
                "filename": filename,
                "analysis": analysis
            })
            upsert_analysis_result(jira_id,pr_number,analyze_code=analysis)

        return jsonify({"results": analysis_results})
    except Exception as e:
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500

@app.route('/generate_tests', methods=['POST'])
def generate_tests_route():
    """
    Generate tests for the code changes in the PR by fetching the full file content.
    """
    try:
        # Get the file changes from the request
        files = request.json.get('files', [])
        owner = request.json.get('owner')
        repo = request.json.get('repo')
        jira_id = request.json.get('jira_id')
        pr_number = request.json.get('pr_number')
        story_res = fetch_analyze_story_result(jira_id, pr_number)

        if not files or not owner or not repo:
            return jsonify({"error": "Missing required parameters"}), 400

        # Generate tests for each file's changes
        test_results = []
        for file in files:
            filename = file['filename']
            changes = file.get('changes', 'No changes available')

            # Fetch the full file content
            full_content = fetch_file_content(owner, repo, filename)

            if "Failed to fetch file" in full_content:
                test_results.append({
                    "filename": filename,
                    "tests": f"Error fetching file content: {full_content}"
                })
                continue

            # Generate tests using Mistral
            tests = generate_tests_with_mistral(filename, changes, full_content, story_res)
            test_results.append({
                "filename": filename,
                "tests": tests
            })

            upsert_analysis_result(jira_id, pr_number, generate_tests=tests)

        return jsonify({"results": test_results})
    except Exception as e:
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)