# 🩺 RepoDoctor

### AI Developer Sidekick for Understanding GitHub Repositories

RepoDoctor is an open-source AI developer sidekick that analyzes a GitHub repository and turns its codebase into an understandable roadmap for developers.

Instead of manually exploring an unfamiliar repository, a developer can simply enter the GitHub repository URL. RepoDoctor scans the repository, extracts its structure and relevant code context, and uses an open-weight coding model to generate a developer-focused analysis.

> **"Turn any GitHub repository into a roadmap you can understand."**

---

## 🚀 Why RepoDoctor?

Understanding an unfamiliar codebase can be difficult, especially for students, beginners, new contributors, and developers joining an existing project.

A developer normally has to:

- Browse through dozens of files
- Identify the technologies being used
- Understand how the project is structured
- Find important entry-point files
- Understand how components interact
- Look for potential issues
- Decide where to start

RepoDoctor automates this initial exploration process using AI.

---

## ✨ Features

### 🔍 Repository Analysis
Enter a public GitHub repository URL and RepoDoctor automatically scans its file structure.

### 🤖 AI-Powered Understanding
Repository context is analyzed using:

**Qwen/Qwen2.5-Coder-32B-Instruct**

through Hugging Face.

### 🏗️ Architecture Explanation
The AI explains the structure and organization of the project.

### 📁 Important Files
RepoDoctor identifies important files and explains their purpose.

### ⚠️ Potential Issues
The AI highlights potential issues or risks found from the available repository context.

### 🧭 "Where Should I Start?"
One of RepoDoctor's key features is helping developers identify where they should begin when approaching an unfamiliar codebase.

### 📚 Recommended Learning Path
The generated report can provide a suggested sequence for understanding the repository.

---

# 🧠 How It Works

```text
                GitHub Repository
                       │
                       ▼
              ┌─────────────────┐
              │   React Frontend │
              │   Vite Dashboard │
              └────────┬────────┘
                       │
                 Repository URL
                       │
                       ▼
              ┌─────────────────┐
              │  FastAPI Backend │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Git Repository   │
              │     Scanner      │
              └────────┬────────┘
                       │
                Repository Files
                       │
                       ▼
              ┌─────────────────┐
              │ Context Builder  │
              │ Structure + Code │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Qwen Coder Model │
              │ Hugging Face     │
              └────────┬────────┘
                       │
                  AI Analysis
                       │
                       ▼
              ┌─────────────────┐
              │ RepoDoctor Report│
              │                  │
              │ • Overview       │
              │ • Tech Stack     │
              │ • Architecture   │
              │ • Important Files│
              │ • Issues         │
              │ • Starting Point │
              │ • Learning Path  │
              └─────────────────┘
