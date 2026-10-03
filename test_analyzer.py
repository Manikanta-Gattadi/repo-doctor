from github_analyzer import build_repository_context


repo_url = "https://github.com/Manikanta-Gattadi/repo-doctor"


try:

    context = build_repository_context(repo_url)

    print("\nRepository successfully analyzed!\n")

    print(context[:10000])

except Exception as e:

    print("ERROR:", e)
