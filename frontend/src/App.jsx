import { useState } from "react";
import "./App.css";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setAnalyzing(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          repo_url: repoUrl.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();

      console.log("RepoDoctor result:", data);

      setResult(data);
    } catch (error) {
      console.error("Analysis error:", error);

      setError(
        "Could not connect to RepoDoctor backend. Make sure the Python server is running."
      );
    } finally {
      setAnalyzing(false);
    }
  };

  // Format AI response into readable sections
  const formatAIResponse = (analysis) => {
    if (!analysis) {
      return null;
    }

    const lines = analysis.split(/\r?\n/);

    return lines.map((line, index) => {
      const text = line.trim();

      // Empty line
      if (!text) {
        return (
          <div
            key={index}
            className="report-space"
          />
        );
      }

      // Markdown heading
      if (/^#{1,6}\s/.test(text)) {
        return (
          <div
            key={index}
            className="report-heading"
          >
            {text.replace(/^#{1,6}\s*/, "")}
          </div>
        );
      }

      // Numbered heading
      if (/^\d+\.\s+/.test(text)) {
        return (
          <div
            key={index}
            className="report-heading"
          >
            {text}
          </div>
        );
      }

      // Bullet point
      if (/^[-*•]\s+/.test(text)) {
        return (
          <div
            key={index}
            className="report-bullet"
          >
            <span className="bullet-dot">•</span>
            <span>
              {text.replace(/^[-*•]\s+/, "")}
            </span>
          </div>
        );
      }

      // Normal paragraph
      return (
        <div
          key={index}
          className="report-line"
        >
          {text}
        </div>
      );
    });
  };

  return (
    <div className="app">

      {/* ================= NAVBAR ================= */}

      <nav className="navbar">

        <div className="logo">
          <span className="logo-icon">
            🩺
          </span>

          <span>
            RepoDoctor
          </span>
        </div>

        <div className="nav-badge">
          Open-Source AI Developer Sidekick
        </div>

      </nav>


      {/* ================= MAIN ================= */}

      <main>

        {/* ================= HERO ================= */}

        <section className="hero">

          <div className="hero-badge">
            ✦ AI-powered repository intelligence
          </div>

          <h1>
            Understand any
            <span> GitHub repository</span>
            <br />
            in seconds.
          </h1>

          <p className="hero-description">
            RepoDoctor analyzes repository structure and code using
            an open-weight AI model to help developers understand
            unfamiliar projects.
          </p>


          {/* ================= INPUT ================= */}

          <div className="input-card">

            <label>
              GitHub Repository URL
            </label>

            <div className="input-row">

              <input
                type="text"
                placeholder="https://github.com/user/project"
                value={repoUrl}
                onChange={(e) =>
                  setRepoUrl(e.target.value)
                }
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleAnalyze();
                  }
                }}
                disabled={analyzing}
              />

              <button
                onClick={handleAnalyze}
                disabled={analyzing}
              >
                {analyzing
                  ? "Analyzing..."
                  : "Analyze Repository →"}
              </button>

            </div>


            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}

          </div>

        </section>


        {/* ================= FEATURES ================= */}

        <section className="features">

          <div className="feature-card">

            <div className="feature-icon">
              📋
            </div>

            <h3>
              Project Overview
            </h3>

            <p>
              Understand what the repository does and
              how it works.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon">
              🏗️
            </div>

            <h3>
              Architecture
            </h3>

            <p>
              Discover the structure and relationships
              between components.
            </p>

          </div>


          <div className="feature-card">

            <div className="feature-icon">
              ⚠️
            </div>

            <h3>
              Potential Issues
            </h3>

            <p>
              Identify missing functionality and
              possible risks.
            </p>

          </div>


          <div className="feature-card start-card">

            <div className="feature-icon">
              🚀
            </div>

            <h3>
              Where Should I Start?
            </h3>

            <p>
              Get a recommended starting point for
              exploring the codebase.
            </p>

          </div>

        </section>


        {/* ================= AI REPORT ================= */}

        <section className="result-section">

          <div className="result-header">

            <div>

              <span className="result-label">
                REPOSITORY ANALYSIS
              </span>

              <h2>
                AI Developer Report
              </h2>

            </div>


            <span className="ai-status">
              ●{" "}
              {result
                ? "Analysis Complete"
                : "AI Ready"}
            </span>

          </div>


          {/* ================= LOADING ================= */}

          {analyzing && (

            <div className="loading-card">

              <div className="loading-spinner"></div>

              <h3>
                Analyzing repository...
              </h3>

              <p>
                RepoDoctor is scanning the repository
                and asking the AI model to understand
                the codebase.
              </p>

            </div>

          )}


          {/* ================= RESULTS ================= */}

          {result && !analyzing && (

            <div className="results-container">


              {/* ================= REPOSITORY INFO ================= */}

              <div className="repository-info">

                <div>

                  <span className="info-label">
                    REPOSITORY
                  </span>

                  <p>
                    {result.repository}
                  </p>

                </div>


                <div>

                  <span className="info-label">
                    FILES ANALYZED
                  </span>

                  <p>
                    {result.file_count}
                  </p>

                </div>

              </div>


              {/* ================= AI ANALYSIS ================= */}

              <div className="report-card">

                <div className="report-title">

                  <span className="report-icon">
                    🤖
                  </span>

                  <div>

                    <span className="result-label">
                      OPEN-WEIGHT AI ANALYSIS
                    </span>

                    <h3>
                      Repository Intelligence Report
                    </h3>

                  </div>

                </div>


                <div className="ai-report">

                  {formatAIResponse(
                    result.analysis
                  )}

                </div>

              </div>


              {/* ================= IMPORTANT FILES ================= */}

              <div className="result-card">

                <div className="card-heading">

                  <span className="card-icon">
                    📁
                  </span>

                  <div>

                    <span className="result-label">
                      CODEBASE
                    </span>

                    <h3>
                      Important Files
                    </h3>

                  </div>

                </div>


                <p>
                  RepoDoctor analyzed{" "}
                  <strong>
                    {result.file_count}
                  </strong>{" "}
                  files from this repository.
                </p>


                <div className="file-list">

                  {result.files &&
                    result.files
                      .slice(0, 15)
                      .map((file, index) => (

                        <div
                          className="file-item"
                          key={index}
                        >

                          <span>
                            📄
                          </span>

                          <span>
                            {file}
                          </span>

                        </div>

                      ))}

                </div>

              </div>


              {/* ================= STARTING POINT ================= */}

              <div className="start-section">

                <div className="start-icon">
                  🚀
                </div>


                <div>

                  <span className="result-label">
                    RECOMMENDED STARTING POINT
                  </span>

                  <h2>
                    Where should I start?
                  </h2>

                  <p>
                    Start with the AI-generated report above.
                    Identify the main entry point of the project,
                    understand the repository structure, and then
                    explore the important files highlighted by
                    RepoDoctor.
                  </p>

                </div>

              </div>

            </div>

          )}


          {/* ================= EMPTY STATE ================= */}

          {!result && !analyzing && (

            <div className="empty-state">

              <div className="empty-icon">
                🩺
              </div>

              <h3>
                Ready to diagnose a repository
              </h3>

              <p>
                Enter a public GitHub repository above
                and let RepoDoctor explain the codebase
                for you.
              </p>

            </div>

          )}

        </section>

      </main>


      {/* ================= FOOTER ================= */}

      <footer>

        <span>
          RepoDoctor
        </span>

        <span>
          Built with React + Python + Open-Weight AI
        </span>

      </footer>

    </div>
  );
}

export default App;