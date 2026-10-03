from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from github_analyzer import get_repository_files
from llm import analyze_repository
import requests


app = FastAPI(title="RepoDoctor API")


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepositoryRequest(BaseModel):
    repo_url: str


def get_file_content(owner, repo, path):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        if len(response.content) > 50000:
            return None

        return response.text

    except Exception:
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

    # Analyze first 15 files
    for file in files[:15]:

        content = get_file_content(
            owner,
            repo,
            file
        )

        if content:

            context.append(
                f"\n===== {file} =====\n"
            )

            context.append(content)

    return "\n".join(context)


@app.get("/")
def home():

    return {
        "message": "RepoDoctor API is running"
    }


@app.post("/analyze")
def analyze(request: RepositoryRequest):

    print("Received repository:", request.repo_url)

    # Get repository files
    files = get_repository_files(
        request.repo_url
    )

    print(
        "Files found:",
        len(files)
    )

    # Build AI context
    context = build_context(
        request.repo_url,
        files
    )

    print("Sending repository to AI...")

    # AI analysis
    result = analyze_repository(
        context
    )

    print("AI analysis completed.")

    return {
        "repository": request.repo_url,
        "file_count": len(files),
        "files": files,
        "analysis": result
    }