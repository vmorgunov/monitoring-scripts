import requests
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
CONFIG_FILE = "accounts.json"
LAST_COMMIT_JSON = "last_commits.json"
COMMITS_FOLDER = "commits_info"
CHECK_INTERVAL = 60  # Interval in seconds
START_DATE = datetime.strptime("2025-05-15", "%Y-%m-%d")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            accounts = config.get("accounts", [])
            repos = config.get("repos", [])
            if not isinstance(accounts, list) or not isinstance(repos, list):
                raise ValueError("Invalid config format. Must be lists.")
            return accounts, repos
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading config: {e}")
        return [], []


def load_last_commits():
    try:
        with open(LAST_COMMIT_JSON, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_last_commits(last_commits):
    with open(LAST_COMMIT_JSON, "w") as file:
        json.dump(last_commits, file, indent=4)


def get_all_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos = response.json()
    return [repo["full_name"] for repo in repos]


def get_latest_commit(repo):
    url = f"https://api.github.com/repos/{repo}/commits"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    commits = response.json()
    return commits[0] if commits else None


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")


def save_commit_to_file(repo_path, folder_name, message):
    repo_folder = os.path.join(COMMITS_FOLDER, repo_path)
    if folder_name != "root":
        repo_folder = os.path.join(repo_folder, folder_name)
        
    os.makedirs(repo_folder, exist_ok=True)

    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    file_path = os.path.join(repo_folder, file_name)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(message)


def extract_changed_files(files):
    changed_files = [file['filename'] for file in files]
    return '\n'.join(changed_files), changed_files


def main():
    os.makedirs(COMMITS_FOLDER, exist_ok=True)
    last_commits = load_last_commits()

    while True:
        GITHUB_ACCOUNTS, GITHUB_REPOS = load_config()
        all_repos = set(GITHUB_REPOS)

        # Add repositories from GitHub accounts
        for account in GITHUB_ACCOUNTS:
            try:
                repos_from_account = get_all_repositories(account)
                all_repos.update(repos_from_account)
            except Exception as e:
                print(f"Error loading repositories for account {account}: {e}")

        for repo in all_repos:
            try:
                latest_commit = get_latest_commit(repo)
                if not latest_commit:
                    continue

                commit_sha = latest_commit['sha']
                commit_message = latest_commit['commit']['message']
                commit_url = latest_commit['html_url']
                commit_author = latest_commit['commit']['author']['name']
                commit_date = latest_commit['commit']['author']['date']

                commit_datetime = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = commit_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                if commit_datetime < START_DATE:
                    continue

                if repo in last_commits and last_commits[repo] == commit_sha:
                    continue

                commit_details_url = f"https://api.github.com/repos/{repo}/commits/{commit_sha}"
                headers = {"Authorization": f"token {GITHUB_TOKEN}"}
                response = requests.get(commit_details_url, headers=headers)
                response.raise_for_status()
                commit_details = response.json()
                
                changed_files_text, changed_files = extract_changed_files(commit_details['files'])

                # Save commit details by folder
                folders = {}
                for file in changed_files:
                    folder = file.split('/')[0] if '/' in file else "root"
                    if folder not in folders:
                        folders[folder] = []
                    folders[folder].append(file)

                for folder, files in folders.items():
                    message_for_file = (
                        f"Repository: {repo}\n"
                        f"Folder: {folder}\n"
                        f"Author: {commit_author}\n"
                        f"Message: {commit_message}\n"
                        f"Date: {formatted_date}\n"
                        f"Changed Files:\n"
                        + '\n'.join(files) + "\n"
                        + f"Link: {commit_url}\n"
                    )
                    save_commit_to_file(repo, folder, message_for_file)

                message = (
                    f"📌 New Commit in <b>{repo}</b>\n"
                    f"👤 Author: <b>{commit_author}</b>\n"
                    f"📝 Message: <b>{commit_message}</b>\n"
                    f"📅 Date: <b>{formatted_date}</b>\n"
                    f"📂 Changed Files: \n<pre>{changed_files_text}</pre>\n\n"
                    f"🔗 <a href='{commit_url}'>View Commit</a>"
                )
                send_telegram_message(message)

                last_commits[repo] = commit_sha
                save_last_commits(last_commits)

            except Exception as e:
                print(f"Error processing repository {repo}: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()