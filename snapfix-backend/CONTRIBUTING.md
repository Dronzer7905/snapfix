# Contributing to the Snapfix Engine

<p align="left">
  <strong>Help us build the most intelligent error analyzer in the world.</strong>
</p>

Thank you for wanting to improve the **Snapfix AI Analysis Engine**! This specific guide has everything you need to get started modifying the Python backend's core logic, expanding LLM integrations, or improving the internal caching. 

---

## 🛠️ Step-by-Step Development Setup

Our engine requires **Python 3.10+**. Follow these precise steps to get a fully working, editable environment locally.

### 1. Clone & Navigate
If you haven't already, ensure you have the full `snapfix` repository cloned, then focus on the backend folder:

```bash
# Navigate into the backend application space
cd snapfix-backend
```

### 2. Create the Virtual Environment
We strongly recommend an isolated virtual environment to avoid dependency conflicts.

```bash
# Generate the virtual environment (.venv)
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Editable Packages
Install the core application in "editable" mode alongside development dependencies like `pytest`, `black`, or `mypy`.

```bash
# The [dev] flag ensures testing frameworks are installed
python -m pip install -e ".[dev]"
```

---

## 🧪 Running Tests (Critically Important)

Before opening any Pull Request altering the Engine's behavior, you **MUST** ensure all tests reliably pass. The Engine leverages `pytest` for all functional testing.

```bash
# Ensure you are inside snapfix-backend/ and your venv is active
pytest tests/
```

> [!WARNING]
> Do not force tests to pass by commenting them out. If you modify a core routing handler in `snapfix/llm/` that breaks a test, update the test to reflect the new desired behavior.

---

## 🧱 Local Code Architecture

Understanding the folder structure saves hours of debugging:

- **`snapfix/`**: The core Python package housing the application domain logic.
  - `llm/`: The integration layer interacting with `LiteLLM`, parsing outputs, and formatting AI responses for VS Code.
  - `db/`: The local SQLite asynchronous caching layer. This prevents repeated API calls for identical tracebacks.
  - `server.py`: The FastAPI implementation, including our REST endpoints (`/health`, `/analyze`, etc.).
- **`tests/`**: Pytest mocks, fixtures, and unit definitions specifically for the engine.

---

## 📜 Pull Request Etiquette

We love reviewing clean code! Please adhere to the following when preparing a PR for the Engine:
1. Limit PRs to one specific feature/bug fix.
2. If introducing a new API provider or complex LLM parameter, document it inside the `README.md`.
3. Provide an example or screenshot if your change returns radically different markdown to the frontend.

Thank you again for your time and contribution to the Snapfix ecosystem! 🚀
