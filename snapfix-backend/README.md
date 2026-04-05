# Snapfix Engine: AI Error Analysis Backend

<p align="left">
  <strong>The intelligent heart of the Snapfix ecosystem.</strong> 🧠
</p>

The **Snapfix Engine** is a high-performance, FastAPI-powered backend server designed to ingest raw Python tracebacks, communicate gracefully with Advanced Large Language Models (LLMs), and cache deep analytical insights securely and locally. 

When your VS Code terminal crashes, this backend springs to life, delivering plain English explanations and `# snapfix:` commented code solutions instantly to the extension panel.

---

## ✨ Core Features

- **⚡ Blazing Fast Analysis**: Powered by an asynchronous SQLite database (`snapfix/db/`), ensuring previously analyzed tracebacks are loaded in milliseconds.
- **🌍 Multi-Model Support**: Integrated seamlessly with `LiteLLM`. Connect to local models via **Ollama** (Privacy-first!) or cloud providers like **OpenAI** and **Gemini**.
- **🚦 Contextual Awareness**: Not just a generic wrapper. Snapfix is specifically optimized for deep Python context, gracefully handling complex frameworks like Django, FastAPI, and Flask.
- **🛡️ Actionable Output**: Returns structured markdown specifically formatted to provide "Actionable Fixes" with precise code snippets you can copy-paste directly.

---

## 🚀 Setup & Installation (Engine)

Setting up the backend independently is perfect for developers wishing to contribute or integrate the Snapfix Engine into custom pipelines.

> [!NOTE]
> Prerequisites: The Engine requires **Python 3.10+**.

### Step 1: Install Locally

1. Navigate to the backend directory.
2. We highly recommend using a virtual environment (`venv`, `conda`, or `poetry`).
3. Install the package using `pip` in editable mode (`-e`) so your changes apply instantly.

```bash
cd snapfix-backend

# Optional but recommended: Create a virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install the engine
python -m pip install -e .
```

### Step 2: Start the Engine

To boot the FastAPI server locally:

```bash
python -m snapfix server
```

> [!TIP]
> The server will bind to `127.0.0.1:7842` by default. You can test if it's running by sending a simple GET request to `http://127.0.0.1:7842/health` or hitting it in your browser.

---

## ⚙️ Configuration Management

Upon its first execution, the Engine automatically scaffolds a configuration file for you at `~/.snapfix/config.toml` (in your user home directory).

Here is an example structure to customize your AI backend:

```toml
[llm]
# Default is a local model. 
# Requires Ollama running in the background.
model = "ollama/llama3.2"  

# You can also switch to cloud models:
# model = "openai/gpt-4"
# model = "gemini/gemini-pro"

# Override API endpoint if not running Ollama locally
api_base = "http://localhost:11434"

[server]
port = 7842
host = "127.0.0.1"
```

> [!WARNING]
> If you configure a cloud model (OpenAI, Anthropic, Gemini), you must ensure the corresponding API keys (e.g., `OPENAI_API_KEY`) are properly set in your environment variables.

---

## 🛠️ Technology Stack

- **Framework**: `FastAPI` (for lightning-fast REST endpoints).
- **AI Routing**: `LiteLLM` (abstracts API calls across 100+ LLMs).
- **CLI Management**: `Typer` (provides beautiful, robust command-line tools).
- **Database**: `SQLite` via `aiosqlite` (for asynchronous local caching).

---

## 🤝 Contribution Guidelines

Looking to help improve the Engine's parsing logic or add a new LLM provider integration? Please refer to the specific **[Backend Contributing Guide](./CONTRIBUTING.md)** for more details on running our `pytest` suite.

<br/>
<p align="center">MIT © Snapfix Contributors</p>
