# Contributing to Snapfix

Thank you for your interest in contributing to Snapfix! This guide will help you set up your development environment and understand our contribution process.

---

## 🛠️ Development Environment

Snapfix is a multi-language project requiring **Python 3.10+** and **Node.js**.

### 1. Root Setup
We recommend using a single Git repository for both the engine and the extension.

### 2. Backend (Snapfix Engine)
The engine is a Python-based FastAPI server.
```bash
cd snapfix-backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
python -m pip install -e ".[dev]"
```

### 3. Frontend (VS Code Extension)
The extension is built with TypeScript and Webpack.
```bash
cd snapfix-vscode
npm install
npm run compile
```

---

## 🧪 Testing

### Backend Tests
We use `pytest` for the engine logic.
```bash
cd snapfix-backend
pytest tests/
```

### Extension Tests
Run "Launch Extension" from the VS Code Debug panel (`F5`) to test the integration manually, or run specialized extension tests via the VS Code test runner.

---

## 🏗️ Architecture

- **`snapfix-backend/`**: The core AI analysis engine.
    - `snapfix/llm/`: LiteLLM handlers and prompt engineering.
    - `snapfix/server.py`: FastAPI implementation.
    - `snapfix/db/`: Asynchronous SQLite caching.
- **`snapfix-vscode/`**: The VS Code extension logic.
    - `src/extension.ts`: Main activation point and process manager.
    - `webview/`: The React/Tailwind frontend for the analysis panel.

---

## 📜 Pull Request Process

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Ensure all tests pass.
4. Submit a Pull Request with a clear description of the changes.

---

MIT © [Snapfix Contributors](https://github.com/Dronzer7905/snapfix)
