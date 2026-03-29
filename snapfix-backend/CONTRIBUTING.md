# Contributing to Snapfix Engine

Thank you for wanting to improve the Snapfix AI analysis engine! This guide has everything you need to get started with the codebase and local development.

## 🛠️ Development Environment

Requires Python 3.10+ and Node.js (for the extension).

### Backend (Python)
```bash
cd snapfix-backend
python -m venv venv
venv/Scripts/activate
python -m pip install -e ".[dev]"
```

### Frontend (VS Code Extension)
```bash
cd snapfix-vscode
npm install
npm run compile
```

## 🧪 Running Tests

We use `pytest` for the backend and standard VS Code test suites for the extension.

### Backend Tests
```bash
cd snapfix-backend
pytest tests/
```

### Extension Tests
Run "Extension Tests" from the VS Code Debug panel (`Ctrl+Shift+D`).

## 🧱 Code Architecture

- **`snapfix/`**: The core Python package.
- **`snapfix-vscode/`**: The VS Code extension source.
- **`snapfix/llm/`**: AI handler and prompt templates.
- **`snapfix/db/`**: Local SQLite caching layer.

---
MIT © Snapfix Contributors
