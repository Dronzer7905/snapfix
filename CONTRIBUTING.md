# Contributing to Snapfix: You Are Welcome Here! 🌟

Thank you for your interest in contributing to **Snapfix**! We are building the premium, AI-powered error analysis engine that developers deserve, and we rely on an active, passionate community to help us succeed.

Whether you are fixing a typo, expanding our LLM integrations, or overhauling the VS Code UI, **your contributions matter.** We want to make sure your onboarding process is as simple and professional as possible.

---

## 🚀 Getting Started

Follow these steps to set up a complete development environment on your machine. Snapfix is a modern, full-stack ecosystem requiring both Python and Node.js.

### 1. Fork and Clone
We recommend maintaining a single Git repository for both the Snapfix Engine (backend) and the VS Code Extension (frontend).

1. **Fork** this repository.
2. **Clone** it down to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/snapfix.git
   ```
3. Open the cloned `snapfix/` folder in your preferred code editor.

---

### 2. Set Up the Engine (Backend)

The Snapfix Engine is a high-performance Python FastAPI server handling the core AI logic, caching, and model interactions.

> [!NOTE]
> Prerequisites: Ensure you have **Python 3.10+** installed.

```bash
# 1. Navigate into the backend directory
cd snapfix-backend

# 2. Create an isolated virtual environment (best practice)
python -m venv venv

# 3. Activate the virtual environment
# On macOS / Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install Snapfix Engine in "editable" mode for development, including dev tools
python -m pip install -e ".[dev]"
```

> [!TIP]
> With the `.[dev]` flag, you installed tools like `pytest`. You can now run `pytest tests/` in the `snapfix-backend` folder to ensure the engine tests pass locally before committing code.

---

### 3. Set Up the VS Code Extension (Frontend)

The VS Code extension contains the beautifully designed webview panels, terminal watchers, and state managers built on TypeScript and React.

> [!NOTE]
> Prerequisites: Ensure you have **Node.js** (v18+) and **npm** installed.

```bash
# 1. Navigate into the extension directory
cd snapfix-vscode

# 2. Install all node dependencies
npm install

# 3. Compile the TypeScript code
npm run compile
```

> [!TIP]
> To test your changes to the extension natively: Open `snapfix-vscode` inside VS Code and press `F5`. This will launch a new "Extension Development Host" window with your custom extension running locally!

---

## 🧠 Project Architecture Overview

Knowing where to look is half the battle. Here is a simplified map of the Snapfix ecosystem:

- **`snapfix-backend/`**: The core AI analysis engine.
  - `snapfix/llm/`: Handlers for various models (Ollama, LiteLLM, prompt engineering logic).
  - `snapfix/server.py`: The core FastAPI REST endpoints.
  - `snapfix/db/`: The SQLite asynchronous caching layer for instant lookups.
- **`snapfix-vscode/`**: The VS Code extension logic.
  - `src/extension.ts`: Main activation point and process management (spawning the backend automatically).
  - `webview/`: The React/Tailwind frontend code that formats and displays the analysis panel.

---

## 📜 Standard Pull Request Workflow

We strive to keep the main branch stable. Please adhere to the following workflow for all PRs:

1. **Create a branch** off `main` for your feature or bugfix (e.g., `git checkout -b feature/gemini-support` or `fix/terminal-parsing-bug`).
2. **Write clean code** and add tests if you're introducing new backend logic.
3. **Ensure tests pass** across the codebase.
4. **Commit your changes** clearly. Use a descriptive PR title.
5. **Open a Pull Request (PR)** against the upstream `main` branch. A project maintainer will review your code, request changes if necessary, and ultimately merge your contribution.

---

## 🛟 Need Help?

If you hit a roadblock during setup or have architectural questions, please don't hesitate to:
- Open an **Issue** tagged with the `question` label.
- Tag `@Dronzer7905` explicitly if you need immediate guidance on a PR blocking issue.

> [!IMPORTANT]
> **We strongly enforce our Code of Conduct.** Please read the [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) file before contributing to ensure a safe, welcoming, and inclusive professional environment for everyone.

Happy coding, and thank you again for helping us build Snapfix! 🚀
