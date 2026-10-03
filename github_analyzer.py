import os
import shutil
import subprocess
import tempfile


def get_repository_files(repo_url):
    temp_dir = tempfile.mkdtemp(prefix="repodoctor_")

    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, temp_dir],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise Exception(
                f"Could not clone repository:\n{result.stderr}"
            )

        files = []

        ignored = {
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv"
        }

        for root, dirs, filenames in os.walk(temp_dir):

            dirs[:] = [
                d for d in dirs
                if d not in ignored
            ]

            for filename in filenames:

                full_path = os.path.join(root, filename)

                relative_path = os.path.relpath(
                    full_path,
                    temp_dir
                )

                files.append(
                    relative_path.replace("\\", "/")
                )

        return files

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )