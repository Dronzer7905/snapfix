# Snapfix: Premium AI-Powered Python Error Analysis Engine

Snapfix is an advanced, AI-driven error analysis ecosystem designed to transform raw Python tracebacks into clean, actionable, and developer-friendly reports. It consists of two main components: a high-performance backend **(Snapfix Engine)** and a seamless **VS Code Extension**.

---

## ⚡ Components

### [Snapfix Engine (Backend)](./snapfix-backend)
A FastAPI-powered server that handles traceback parsing, AI analysis (via LiteLLM), and result caching. It provides the core intelligence for the Snapfix ecosystem.

### [Snapfix VS Code Extension](./snapfix-vscode)
A premium VS Code interface that captures terminal errors in real-time and displays deep analytical insights directly within your editor.

---

## ✨ Features

- **🚀 Instant Analysis**: Captures tracebacks from your terminal and analyzes them automatically.
- **🧠 Deep Context**: Identifies failure points and explains root causes in plain English.
- **🛠️ Actionable Fixes**: Generates copy-pasteable Python fixes with `# snapfix:` comments.
- **🛡️ Prevention Insights**: Proactive tips to improve code quality and prevent future bugs.
- **🔒 Privacy First**: Designed for local LLMs (Ollama) by default. Your code stays local.

---

## 🚀 Quick Start

Ensure you have **Python 3.10+** and **Node.js** installed.

### 1. Install the Engine
```bash
cd snapfix-backend
python -m pip install -e .
python -m snapfix server
```

### 2. Install the Extension
- Open the `snapfix-vscode` folder in VS Code.
- Run `npm install` and `npm run package`.
- Install the generated `.vsix` file.

---

## ⚙️ Configuration

Snapfix creates a configuration at `~/.snapfix/config.toml` on first launch. You can configure LLM providers (Ollama, OpenAI, Gemini, etc.) and server settings.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./CONTRIBUTING.md) and [Code of Conduct](./CODE_OF_CONDUCT.md) to get started.

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

---

MIT © [Dronzer7905](https://github.com/Dronzer7905)
