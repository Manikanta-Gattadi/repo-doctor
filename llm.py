import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing from .env")

MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"

client = InferenceClient(
    model=MODEL,
    token=HF_TOKEN
)

def analyze_repository(context):

    prompt = f"""
You are RepoDoctor, an AI developer sidekick.

Analyze this GitHub repository and help a developer understand it.

Provide:

1. Project overview
2. Technology stack
3. Architecture explanation
4. Important files and what they do
5. Potential issues or risks
6. Where the developer should start
7. Recommended learning path

Only make claims supported by the repository context.

Repository context:

{context}
"""

    response = client.chat_completion(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.2
    )

    return response.choices[0].message.content