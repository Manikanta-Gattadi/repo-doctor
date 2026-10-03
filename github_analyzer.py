import requests


def get_repository_files(repo_url):
    """
    Get the list of files from a public GitHub repository.
    """

    # Example:
    # https://github.com/Manikanta-Gattadi/repo-doctor
    # becomes:
    # Manikanta-Gattadi/repo-doctor

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"

    response = requests.get(api_url, timeout=10)

    if response.status_code != 200:
        raise Exception(
            f"GitHub returned status code {response.status_code}"
        )

    data = response.json()

    files = []

    for item in data.get("tree", []):

        if item["type"] == "blob":
            files.append(item["path"])

    return files


if __name__ == "__main__":

    repository = "https://github.com/Manikanta-Gattadi/repo-doctor"

    print("Analyzing repository...")
    print()

    files = get_repository_files(repository)

    print(f"Found {len(files)} files.")
    print()

    for file in files:
        print(file)
