# Snapfix Engine: AI Error Analysis for Python

Snapfix is a premium, AI-powered error analysis engine that transforms raw Python tracebacks into clean, actionable, and developer-friendly reports. It embeds directly into your VS Code environment to provide instant context, plain-English explanations, and suggested fixes for every exception.

## ✨ Features

- **Instant Analysis**: Automatically detects tracebacks in your terminal and analyzes them in real-time.
- **Deep Context**: Identifies exact failure points, understands the underlying cause, and explains it in plain English.
- **Actionable Fixes**: Provides copy-pasteable Python code snippets with inline `# snapfix:` comments.
- **Prevention Insights**: Offers proactive tips and code patterns to prevent similar bugs in the future.
- **Framework Aware**: Specialized analysis for Django, FastAPI, and Flask.
- **Privacy First**: Ships with local Ollama (`llama3.2`) as the default engine. No API keys required.

## 🚀 Quick Start

### 1. Install the Backend
Requires Python 3.10+.

```bash
cd snapfix-backend
python -m pip install -e .
```

### 2. Start the Engine
```bash
python -m snapfix server
```

### 3. Install the VS Code Extension
Open the `snapfix-vscode` folder in VS Code and press `F5` to launch or run the "Snapfix: Show Analysis Panel" command.

## ⚙️ Configuration

Snapfix auto-creates a configuration file at `~/.snapfix/config.toml` on first run.

```toml
[llm]
model = "ollama/llama3.2"  # or "openai/gpt-4"
api_base = "http://localhost:11434"

[server]
port = 7842
host = "127.0.0.1"
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, LiteLLM, Typer
- **Database**: SQLite (Async) for local analysis caching
- **Frontend**: VS Code (TypeScript), Tailwind CSS

---
MIT © Snapfix Contributors
