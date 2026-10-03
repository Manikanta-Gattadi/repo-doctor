import requests
from urllib.parse import urlparse


IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

IMPORTANT_FILES = {
    "README.md",
    "README",
    "requirements.txt",
    "package.json",
    "pyproject.toml",
    "setup.py",
    "Dockerfile",
    "docker-compose.yml",
    "app.py",
    "main.py",
    "index.js",
    "index.ts"
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".php",
    ".html",
    ".css",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".txt"
}


def parse_github_url(repo_url):
    """
    Extract owner and repository name from a GitHub URL.
    """

    parsed = urlparse(repo_url)

    if parsed.netloc.lower() != "github.com":
        raise ValueError("Please provide a valid GitHub repository URL.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def get_repository_tree(repo_url):
    """
    Get the file tree of a public GitHub repository.
    """

    owner, repo = parse_github_url(repo_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"

    response = requests.get(api_url, timeout=20)

    if response.status_code == 404:
        raise ValueError("Repository not found or is not public.")

    response.raise_for_status()

    data = response.json()

    return owner, repo, data.get("tree", [])


def should_include_file(path):
    """
    Decide whether a repository file is useful for AI analysis.
    """

    parts = path.split("/")

    # Ignore unwanted directories
    for part in parts:
        if part in IGNORED_DIRS:
            return False

    filename = parts[-1]

    # Always include important project files
    if filename in IMPORTANT_FILES:
        return True

    # Include common source-code/documentation files
    for extension in ALLOWED_EXTENSIONS:
        if filename.lower().endswith(extension):
            return True

    return False


def select_files(tree, max_files=30):
    """
    Select useful files from the repository.
    """

    files = []

    for item in tree:

        if item.get("type") != "blob":
            continue

        path = item.get("path", "")

        if should_include_file(path):
            files.append(path)

    # Put important files first
    files.sort(
        key=lambda path: (
            0 if path.split("/")[-1] in IMPORTANT_FILES else 1,
            len(path)
        )
    )

    return files[:max_files]


def fetch_file(owner, repo, path):
    """
    Download a single file from GitHub.
    """

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"

    response = requests.get(url, timeout=20)

    if response.status_code != 200:
        return None

    # Avoid accidentally processing huge files
    if len(response.content) > 100_000:
        return None

    try:
        return response.text
    except UnicodeDecodeError:
        return None


def build_repository_context(repo_url):
    """
    Build a compact text representation of the repository
    that can later be sent to the open-weight AI model.
    """

    owner, repo, tree = get_repository_tree(repo_url)

    selected_files = select_files(tree)

    context_parts = []

    context_parts.append(f"Repository: {owner}/{repo}")
    context_parts.append("\nRepository files:\n")

    for path in selected_files:
        context_parts.append(f"- {path}")

    context_parts.append("\n\nSource files:\n")

    for path in selected_files:

        content = fetch_file(owner, repo, path)

        if not content:
            continue

        context_parts.append(
            f"\n===== FILE: {path} =====\n"
        )

        context_parts.append(content)

    return "\n".join(context_parts)
