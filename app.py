from github_analyzer import get_repository_files
from llm import analyze_repository
import requests


def get_file_content(owner, repo, path):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    if len(response.content) > 50000:
        return None

    try:
        return response.text
    except UnicodeDecodeError:
        return None


def build_context(repo_url, files):
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    context = []

    context.append(f"Repository: {owner}/{repo}")

    context.append("\nRepository structure:\n")

    for file in files:
        context.append(file)

    context.append("\n\nImportant file contents:\n")

    # Start simple: analyze first 15 files
    for file in files[:15]:

        content = get_file_content(owner, repo, file)

        if content:
            context.append(f"\n===== {file} =====\n")
            context.append(content)

    return "\n".join(context)


if __name__ == "__main__":

    repo_url = input("Enter GitHub repository URL: ").strip()

    print("\nScanning repository...\n")

    files = get_repository_files(repo_url)

    print(f"Found {len(files)} files.")

    print("\nBuilding repository context...\n")

    context = build_context(repo_url, files)

    print("Sending repository to RepoDoctor AI...\n")

    result = analyze_repository(context)

    print("\n")
    print("=" * 70)
    print("              REPO DOCTOR ANALYSIS")
    print("=" * 70)
    print()

    print(result)

    print()
    print("=" * 70)